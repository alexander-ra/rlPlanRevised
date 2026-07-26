"""
llm_agent.py  [CORE + INF]  -- raw L381-446.

An LLM plays Kuhn Poker from a natural-language description of the rules. This module supplies:

  1. A MODEL-AGNOSTIC client interface (`LLMClient`) with three backends:
       - ScriptedReasonerClient : an OFFLINE, deterministic "reasoner" stub (DEFAULT). Zero
         dependencies, no GPU, no keys -- so the evaluation harness and comparison table run
         end-to-end without a real model. It plays a sensible (not optimal) Kuhn strategy and
         emits a short reasoning trace, so parsing / illegal-move handling is exercised offline.
       - OpenAICompatClient    : talks to ANY OpenAI-chat-compatible HTTP endpoint via stdlib
         urllib (no `requests` dep): LM Studio / Ollama / vLLM / OpenRouter, selected purely by
         (base_url, model, api_key). This is how a local model on the RTX 5090 is wired in.
       - HFLocalClient         : optional in-process transformers generation (documented
         secondary; lazy import, guarded).

  2. `KuhnPokerLLMAgent` : builds the prompt (three styles -- plain / CoT / game-theory),
     calls the client, PARSES the action, and HANDLES ILLEGAL / unparseable replies (retry then
     safe fallback), while tracking the illegal-move rate (a headline LLM-agent metric).

  3. `llm_policy(...)` : wrap an agent as a Game-interface policy (info_set -> {action: prob})
     by sampling, so the LLM can be scored with the exact Step 02 exploitability metric.

The model roster (which model to point the client at) lives in config.py.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here. The scripted stub makes
the whole file exercisable offline; the HTTP/HF paths are verified in the run session.
"""

from __future__ import annotations

import json
import re
import time
import urllib.request
import urllib.error
from dataclasses import dataclass, field

import deps  # noqa: F401  (bootstraps step07 onto sys.path)

# Kuhn action ids / names.
_PASS, _BET = 0, 1
_CARD_NAME = {1: "Jack", 2: "Queen", 3: "King"}

# Lenient poker-verb -> Kuhn-action map. "raise/allin" fold into BET (aggressive), "check/fold"
# into PASS (passive). Anything that maps to NEITHER is an illegal/unparseable move.
_VERB_TO_ACTION = {
    "bet": _BET, "call": _BET, "raise": _BET, "allin": _BET, "all-in": _BET,
    "pass": _PASS, "check": _PASS, "fold": _PASS,
}


# --- client interface ----------------------------------------------------------------
class LLMClient:
    name: str = "abstract"

    def chat(self, system: str, user: str, temperature: float = 0.7,
             max_tokens: int = 256) -> str:
        raise NotImplementedError


class ScriptedReasonerClient(LLMClient):
    """Deterministic offline stand-in for an LLM. Parses card + betting context from the prompt
    and returns a short reasoning trace ending in an explicit action line.

    Strategy (intentionally reasonable, NOT Nash -- so its exploitability is honestly > 0):
      - King  : always bet / call (value).
      - Queen : check; call a bet only sometimes; bluff-raise never.
      - Jack  : check; fold to a bet; occasional stubborn bluff to exercise the bluff metric.
    The tiny amount of card-history-driven variation is deterministic (hash of the info set),
    so results are reproducible without an RNG.
    """

    name = "scripted-reasoner(offline-stub)"

    def chat(self, system: str, user: str, temperature: float = 0.7,
             max_tokens: int = 256) -> str:
        card = self._extract_card(user)
        facing_bet = "opponent bet" in user.lower() or "facing a bet" in user.lower()
        det = (hash((card, facing_bet)) % 100) / 100.0  # deterministic pseudo-mix in [0,1)

        if card == 3:  # King
            action, why = "BET", "the King is the best hand; bet for value / always call."
        elif card == 2:  # Queen
            if facing_bet:
                action = "BET" if det < 0.35 else "PASS"
                why = "the Queen is medium; call only sometimes, fold otherwise."
            else:
                action = "PASS"
                why = "the Queen prefers to check and keep the pot small."
        else:  # Jack
            if facing_bet:
                action = "PASS"
                why = "the Jack is the worst hand; fold to a bet."
            else:
                action = "BET" if det < 0.30 else "PASS"
                why = "the Jack can occasionally bluff, but usually checks."
        return f"Reasoning: With the {_CARD_NAME.get(card, '?')}, {why}\nAction: {action}"

    @staticmethod
    def _extract_card(text: str) -> int:
        """Read the stub's own hole card out of the prompt.

        RUN-SESSION FIX (2026-07-25). This used to scan the WHOLE prompt for the first card
        name, which silently broke the `gametheory` prompt style: its instruction text itself
        names every card ("with the King bet/call for value; with the Jack you must sometimes
        BLUFF ..."), so the scan always matched "Jack" first and the stub played EVERY hand as
        a Jack. That produced a fake result in the comparison table (LLM-gametheory 1.667 vs
        0.833 chips) that looked like a finding about game-theory prompting but was pure prompt
        contamination. Anchor on the explicit "Your private card: X." line first.
        """
        low = text.lower()
        m = re.search(r"your private card\s*[:=]\s*([a-z0-9]+)", low)
        if m:
            tok = m.group(1)
            for cid, name in _CARD_NAME.items():
                if tok.startswith(name.lower()[0]):
                    return cid
            if tok[:1] in {"1", "2", "3"}:
                return int(tok[0])
        # Fall back to the old whole-text scan only if the anchored line is absent.
        for cid, name in _CARD_NAME.items():
            if name.lower() in low:
                return cid
        m = re.search(r"card\s*(?:is|=|:)?\s*([jqk123])", low)
        if m:
            ch = m.group(1)
            return {"j": 1, "q": 2, "k": 3, "1": 1, "2": 2, "3": 3}[ch]
        return 2  # default to Queen if unknown


class OpenAICompatClient(LLMClient):
    """OpenAI-chat-compatible HTTP client (LM Studio / Ollama / vLLM / OpenRouter / OpenAI).

    Uses only the standard library. `base_url` should include the version path, e.g.
    "http://localhost:1234/v1" (LM Studio) or "http://localhost:11434/v1" (Ollama). Verified in
    the run session -- not executed here.
    """

    def __init__(self, base_url: str, model: str, api_key: str | None = None,
                 timeout: float = 120.0, max_tokens: int = 256, retries: int = 3,
                 backoff: float = 2.0):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.api_key = api_key
        self.timeout = timeout
        self.max_tokens = max_tokens          # per-preset default (see config.py)
        self.retries = retries
        self.backoff = backoff
        self.name = f"openai-compat:{model}"
        self.truncated = 0                    # replies cut off by max_tokens (diagnostic)
        self.transient_errors = 0             # retried HTTP/transport blips (diagnostic)

    def list_models(self) -> list:
        """Model ids the server actually serves (`GET /v1/models`)."""
        req = urllib.request.Request(f"{self.base_url}/models", method="GET")
        if self.api_key:
            req.add_header("Authorization", f"Bearer {self.api_key}")
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        return [m["id"] for m in body.get("data", [])]

    def chat(self, system: str, user: str, temperature: float = 0.7,
             max_tokens: int | None = None) -> str:
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": self.model,
            "messages": [{"role": "system", "content": system},
                         {"role": "user", "content": user}],
            "temperature": temperature,
            "max_tokens": max_tokens or self.max_tokens,
        }
        data = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        # RETRY (run-session addition). A comparison-table pass is 150+ sequential requests, and a
        # local server WILL hiccup: LM Studio JIT-unloads an idle model and a request arriving
        # mid-reload comes back 400. That killed a full gpt-oss run at ~90 calls in; the identical
        # request succeeded moments later. One transient blip must not throw away minutes of work.
        body = None
        last_err = None
        for attempt in range(self.retries + 1):
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    body = json.loads(resp.read().decode("utf-8"))
                break
            except urllib.error.HTTPError as e:
                detail = ""
                try:
                    detail = e.read().decode("utf-8", "replace")[:300]
                except Exception:
                    pass
                if e.code == 404:
                    try:
                        served = self.list_models()
                    except Exception:
                        served = ["<could not query /v1/models>"]
                    raise RuntimeError(
                        f"Model {self.model!r} is not served by {self.base_url}. "
                        f"Available: {served}. Update the preset in config.py."
                    ) from e
                last_err = RuntimeError(f"HTTP {e.code} from {url}: {detail}")
            except (urllib.error.URLError, TimeoutError, OSError) as e:
                last_err = RuntimeError(f"transport error to {url}: {e!r}")
            if attempt < self.retries:
                self.transient_errors += 1
                time.sleep(self.backoff * (2 ** attempt))
        if body is None:
            raise last_err or RuntimeError("chat() failed with no diagnostic")

        choice = body["choices"][0]
        msg = choice.get("message", {})
        content = msg.get("content") or ""
        # Reasoning models split the trace off into `reasoning` (gpt-oss via LM Studio does this,
        # measured 2026-07-25) or leave it INLINE in <think>...</think>. If the split-off variant
        # returns an empty content -- e.g. the answer got cut before it left the reasoning channel
        # -- fall back to the trace so parse_action still has something to work with.
        if not content.strip():
            # Field name varies by server/model: gpt-oss via LM Studio uses `reasoning`,
            # OpenThinker3 reports `reasoning_content` (and puts its real trace INLINE in
            # `content` as <think>...</think>). Check both before giving up.
            content = msg.get("reasoning") or msg.get("reasoning_content") or ""
        if choice.get("finish_reason") == "length":
            self.truncated += 1
        return content


class HFLocalClient(LLMClient):
    """Optional in-process HuggingFace transformers backend (secondary; lazy import)."""

    def __init__(self, model_id: str, device: str = "cuda", max_new_tokens: int = 256,
                 dtype: str = "bfloat16"):
        self.model_id = model_id
        self.device = device
        self.max_new_tokens = max_new_tokens
        self.dtype = dtype
        self.name = f"hf-local:{model_id}"
        self._tok = None
        self._model = None

    def _ensure_loaded(self):
        if self._model is not None:
            return
        import torch  # noqa: F401
        from transformers import AutoModelForCausalLM, AutoTokenizer  # lazy

        self._tok = AutoTokenizer.from_pretrained(self.model_id)
        self._model = AutoModelForCausalLM.from_pretrained(
            self.model_id, torch_dtype=self.dtype, device_map=self.device)

    def chat(self, system: str, user: str, temperature: float = 0.7,
             max_tokens: int = 256) -> str:
        self._ensure_loaded()
        messages = [{"role": "system", "content": system},
                    {"role": "user", "content": user}]
        prompt = self._tok.apply_chat_template(messages, tokenize=False,
                                               add_generation_prompt=True)
        inputs = self._tok(prompt, return_tensors="pt").to(self.device)
        out = self._model.generate(**inputs, max_new_tokens=max_tokens or self.max_new_tokens,
                                   temperature=temperature, do_sample=temperature > 0)
        text = self._tok.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
        return text


def make_client(spec: dict | None) -> LLMClient:
    """Factory. `spec` is an LLM preset dict (see config.py):
        {"backend": "stub"}
        {"backend": "openai", "base_url": ..., "model": ..., "api_key": ...}
        {"backend": "hf", "model": ...}
    None or backend 'stub' -> the offline scripted reasoner.
    """
    if spec is None or spec.get("backend", "stub") == "stub":
        return ScriptedReasonerClient()
    backend = spec["backend"]
    if backend == "openai":
        return OpenAICompatClient(spec["base_url"], spec["model"], spec.get("api_key"),
                                  spec.get("timeout", 120.0), spec.get("max_tokens", 256))
    if backend == "hf":
        return HFLocalClient(spec["model"], spec.get("device", "cuda"),
                             spec.get("max_new_tokens", 256), spec.get("dtype", "bfloat16"))
    raise ValueError(f"Unknown LLM backend {backend!r}")


# --- the agent -----------------------------------------------------------------------
_RULES = (
    "You are playing Kuhn Poker, a simplified poker game.\n"
    "Deck: three cards -- Jack (weakest), Queen, King (strongest). You are dealt ONE private "
    "card; your opponent has one of the other two. Both players ante 1 chip.\n"
    "On your turn you may take one of two actions:\n"
    "  - PASS: if no bet is facing you this is a CHECK; if a bet is facing you this is a FOLD "
    "(you give up the pot).\n"
    "  - BET: if no bet is facing you this puts in 1 more chip; if a bet is facing you this is a "
    "CALL.\n"
    "Higher card wins at showdown. Your goal is to maximize chips won over many hands."
)

_STYLE_INSTRUCTIONS = {
    "plain": "Reply with ONLY your action on a single line: 'Action: BET' or 'Action: PASS'.",
    "cot": ("Think step by step about your hand strength, the pot, and what your opponent's "
            "actions imply, THEN end your reply with a final line exactly: 'Action: BET' or "
            "'Action: PASS'."),
    "gametheory": ("Approximate game-theory-optimal (Nash) play: with the King bet/call for "
                   "value; with the Jack you must sometimes BLUFF and otherwise fold to bets; "
                   "with the Queen mostly check and call at the right frequency. Balance your "
                   "range so you are not exploitable. End with a final line exactly: "
                   "'Action: BET' or 'Action: PASS'."),
}


@dataclass
class LLMStats:
    calls: int = 0
    illegal: int = 0
    retries: int = 0

    def illegal_rate(self) -> float:
        return self.illegal / self.calls if self.calls else 0.0


@dataclass
class KuhnPokerLLMAgent:
    client: LLMClient
    prompt_style: str = "cot"
    temperature: float = 0.7
    stats: LLMStats = field(default_factory=LLMStats)

    def build_prompt(self, card: int, history: str, opponent_profile: str | None = None):
        facing_bet = self._facing_bet(history)
        situation = self._describe_history(history)
        lines = [
            f"Your private card: {_CARD_NAME[card]}.",
            situation,
            "You are facing a bet." if facing_bet else "No bet is facing you.",
        ]
        if opponent_profile:
            lines.append(f"Note on your opponent: {opponent_profile}")
        lines.append(_STYLE_INSTRUCTIONS.get(self.prompt_style, _STYLE_INSTRUCTIONS["plain"]))
        return _RULES, "\n".join(lines)

    def act(self, card: int, history: str, legal_actions=(_PASS, _BET),
            opponent_profile: str | None = None):
        """Return (action_id, raw_response, parsed_ok). Retries once on illegal, then falls
        back to a safe legal action (PASS = check/fold)."""
        system, user = self.build_prompt(card, history, opponent_profile)
        self.stats.calls += 1
        raw = self.client.chat(system, user, temperature=self.temperature)
        action = self.parse_action(raw, legal_actions)
        if action is None:
            self.stats.illegal += 1
            self.stats.retries += 1
            strict = user + "\n\nIMPORTANT: reply with EXACTLY 'Action: BET' or 'Action: PASS'."
            raw2 = self.client.chat(system, strict, temperature=0.0)
            action = self.parse_action(raw2, legal_actions)
            raw = raw + "\n---retry---\n" + raw2
            if action is None:
                action = _PASS if _PASS in legal_actions else legal_actions[0]
                return action, raw, False
        return action, raw, True

    @staticmethod
    def parse_action(text: str, legal_actions=(_PASS, _BET)):
        """Robustly extract a Kuhn action id from an LLM reply, or None if unmappable."""
        low = text.lower()
        # RUN-SESSION FIX: strip an INLINE chain-of-thought before parsing. Reasoning-tuned
        # models (OpenThinker3) wrap their trace in <think>...</think> inside `content`, and the
        # trace routinely rehearses BOTH actions ("if I bet ... but folding is safer"). Since we
        # take the LAST match, a trailing thought would override the model's actual answer. Keep
        # the post-</think> answer; if the trace never closed (truncated), fall back to the whole
        # string so a cut-off reply still yields an action rather than a false "illegal move".
        if "<think>" in low:
            if "</think>" not in low:
                # The reasoning block never closed => the model was still thinking when it hit
                # the token cap and NEVER COMMITTED to an action. Scraping a poker verb out of
                # that unfinished monologue (the first version of this fix did) manufactures an
                # answer the model did not give, and reports illegal=0% for a model that in fact
                # failed to reply. Measured on OpenThinker3-7B: 18k chars of open <think>, no
                # </think>, yet a confident-looking "BET". Return None -> counted as unparseable.
                return None
            low = low.split("</think>")[-1]
            if not low.strip():
                return None
        # Prefer an explicit 'action:' directive (use the LAST one).
        # Separator class includes "/" and "=": OpenThinker3 emits "Action/PASS" rather than the
        # requested "Action: PASS". That is the same explicit directive with different
        # punctuation, so counting it illegal would overstate the illegal-move rate.
        matches = re.findall(r"action\s*[:\-/=]\s*([a-z\-]+)", low)
        candidates = list(matches)
        if not candidates:
            # else fall back to the last poker verb mentioned anywhere
            verbs = re.findall(r"\b(bet|call|raise|all-?in|pass|check|fold)\b", low)
            candidates = verbs[-1:] if verbs else []
        for tok in reversed(candidates):
            tok = tok.replace("all-in", "allin")
            if tok in _VERB_TO_ACTION:
                a = _VERB_TO_ACTION[tok]
                if a in legal_actions:
                    return a
        return None

    @staticmethod
    def _facing_bet(history: str) -> bool:
        # A bet is facing you iff the last action was a BET ('b') that you have not answered.
        return len(history) > 0 and history[-1] == "b"

    @staticmethod
    def _describe_history(history: str) -> str:
        """Narrate the betting so far from the ACTING player's point of view.

        RUN-SESSION FIX (2026-07-25). This used to label index 0 as "You" unconditionally,
        i.e. it assumed the agent always sits in seat 0. But the agent is queried at ALL 12 Kuhn
        info sets, six of which belong to seat 1, so every second-player prompt was mis-narrated.
        The worst case was history "b", which rendered as "Betting so far: You bet." together
        with "You are facing a bet." -- self-contradictory. Measured effect on gpt-oss-20b at
        temperature 0: it FOLDED THE KING to a bet (a strictly dominated play). After the fix it
        calls. Any second-player LLM number taken before this fix is invalid.

        The player to act is `len(history) % 2`; the action at index i was taken by `i % 2`.
        """
        if history == "":
            return "You act first, before any bets."
        actor = len(history) % 2
        parts = []
        for i, ch in enumerate(history):
            who = "You" if i % 2 == actor else "Opponent"
            parts.append(f"{who} {'bet' if ch == 'b' else 'checked/passed'}")
        return "Betting so far: " + "; ".join(parts) + "."


# --- LLM as a Game-interface policy --------------------------------------------------
def llm_policy(agent: KuhnPokerLLMAgent, samples: int = 8, opponent_profile: str | None = None):
    """Wrap an LLM agent as policy(game, state) -> {action: prob} by sampling `samples` calls
    per info set (cached). With the deterministic stub, one sample suffices; for a real model
    use temperature>0 and more samples to estimate its mixed strategy."""
    cache: dict = {}

    def policy(game, state):
        legal = game.legal_actions(state)
        player = game.current_player(state)
        card = int(state.cards[player])
        history = state.history
        key = (card, history)
        if key not in cache:
            counts = {a: 0 for a in legal}
            for _ in range(samples):
                a, _raw, _ok = agent.act(card, history, tuple(legal), opponent_profile)
                counts[a] = counts.get(a, 0) + 1
            total = sum(counts.values()) or 1
            cache[key] = {a: counts[a] / total for a in legal}
        return dict(cache[key])

    return policy


def _selftest():
    print("llm_agent self-test (offline scripted-reasoner stub)")
    print("-" * 60)
    agent = KuhnPokerLLMAgent(ScriptedReasonerClient(), prompt_style="cot")
    for card in (1, 2, 3):
        for hist in ("", "b"):
            a, raw, ok = agent.act(card, hist)
            name = "BET" if a == _BET else "PASS"
            print(f"card={_CARD_NAME[card]:5s} hist={hist!r:4} -> {name:4s} "
                  f"(parsed_ok={ok}) :: {raw.splitlines()[-1]}")
    print(f"illegal rate = {agent.stats.illegal_rate():.2%} over {agent.stats.calls} calls "
          "(expect 0% for the stub)")

    # Parsing robustness on adversarial strings.
    tests = [("I will Action: raise here", _BET), ("let me fold", _PASS),
             ("Action: PASS", _PASS), ("blah blah nonsense", None)]
    ok = all(KuhnPokerLLMAgent.parse_action(t) == want for t, want in tests)
    print(f"parse_action robustness checks pass: {ok}")


if __name__ == "__main__":
    _selftest()
