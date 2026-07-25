"""
decision_transformer.py  [SUP]  -- raw L297-312.

A compact, SELF-CONTAINED, GPT-2-style Decision Transformer in pure PyTorch.

WHY NOT HuggingFace's DecisionTransformerModel (raw L299)
---------------------------------------------------------
The raw step suggests adapting HF's `DecisionTransformerModel`, but `transformers` is not a
dependency of this repo and the agent cannot smoke-test its version-specific quirks. So we
write our own -- the same "write it yourself so it runs unchanged" choice Step 11 made for PPO.
We deliberately MIRROR the field names of HF's `DecisionTransformerConfig`
(`state_dim`, `act_dim`, `hidden_size`, `n_layer`, `n_head`, `max_ep_len`) so the code reads
like the reference and could be swapped later with minimal churn.

DISCRETE ACTIONS
----------------
Poker actions are discrete (Kuhn PASS/BET; Leduc FOLD/CALL/RAISE), so unlike the continuous
DT we (a) embed input actions with an `nn.Embedding` and (b) predict actions as a categorical
distribution (linear -> logits -> cross-entropy). This is the standard discrete-DT setup.

TOKEN LAYOUT (Chen et al. 2021)
-------------------------------
Per timestep t we emit three tokens in order: (R_hat_t, s_t, a_t). We add a per-timestep
positional embedding to all three, run a causal transformer, and read the action prediction
from the STATE token position (so a_t is predicted from everything up to and including s_t,
but NOT a_t itself -- the causal mask guarantees no leakage from the dummy action token).

Guarded by deps.require_torch(): importing this module requires torch on purpose. Torch-free
callers (CFR, LLM-with-stub, exploitability) must import it lazily behind torch_available().

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from deps import require_torch

torch = require_torch()
nn = torch.nn
F = torch.nn.functional


@dataclass
class DecisionTransformerConfig:
    """Mirrors the relevant fields of HF's DecisionTransformerConfig."""

    state_dim: int
    act_dim: int              # number of discrete actions
    hidden_size: int = 64
    n_layer: int = 3
    n_head: int = 4
    max_ep_len: int = 16      # max timesteps in an episode (Kuhn hands are tiny)
    dropout: float = 0.1
    max_length: int = 8       # context length in TIMESTEPS (sequence is 3x this in tokens)


class CausalSelfAttention(nn.Module):
    def __init__(self, cfg: DecisionTransformerConfig):
        super().__init__()
        assert cfg.hidden_size % cfg.n_head == 0, "hidden_size must be divisible by n_head"
        self.n_head = cfg.n_head
        self.head_dim = cfg.hidden_size // cfg.n_head
        self.qkv = nn.Linear(cfg.hidden_size, 3 * cfg.hidden_size)
        self.proj = nn.Linear(cfg.hidden_size, cfg.hidden_size)
        self.attn_drop = nn.Dropout(cfg.dropout)
        self.resid_drop = nn.Dropout(cfg.dropout)

    def forward(self, x, attn_mask):
        # x: (B, L, H); attn_mask: (B, 1, L, L) additive (0 keep, -inf block)
        B, L, H = x.shape
        qkv = self.qkv(x).view(B, L, 3, self.n_head, self.head_dim).permute(2, 0, 3, 1, 4)
        q, k, v = qkv[0], qkv[1], qkv[2]  # (B, n_head, L, head_dim)
        att = (q @ k.transpose(-2, -1)) / math.sqrt(self.head_dim)
        att = att + attn_mask
        att = F.softmax(att, dim=-1)
        att = self.attn_drop(att)
        y = att @ v                                  # (B, n_head, L, head_dim)
        y = y.transpose(1, 2).contiguous().view(B, L, H)
        return self.resid_drop(self.proj(y))


class Block(nn.Module):
    def __init__(self, cfg: DecisionTransformerConfig):
        super().__init__()
        self.ln1 = nn.LayerNorm(cfg.hidden_size)
        self.attn = CausalSelfAttention(cfg)
        self.ln2 = nn.LayerNorm(cfg.hidden_size)
        self.mlp = nn.Sequential(
            nn.Linear(cfg.hidden_size, 4 * cfg.hidden_size),
            nn.GELU(),
            nn.Linear(4 * cfg.hidden_size, cfg.hidden_size),
            nn.Dropout(cfg.dropout),
        )

    def forward(self, x, attn_mask):
        x = x + self.attn(self.ln1(x), attn_mask)
        x = x + self.mlp(self.ln2(x))
        return x


class DecisionTransformer(nn.Module):
    """Return-conditioned action predictor for discrete-action poker."""

    def __init__(self, cfg: DecisionTransformerConfig):
        super().__init__()
        self.cfg = cfg
        H = cfg.hidden_size
        self.embed_return = nn.Linear(1, H)
        self.embed_state = nn.Linear(cfg.state_dim, H)
        self.embed_action = nn.Embedding(cfg.act_dim, H)
        self.embed_timestep = nn.Embedding(cfg.max_ep_len, H)
        self.embed_ln = nn.LayerNorm(H)
        self.blocks = nn.ModuleList([Block(cfg) for _ in range(cfg.n_layer)])
        self.ln_f = nn.LayerNorm(H)
        self.predict_action = nn.Linear(H, cfg.act_dim)
        self.apply(self._init_weights)

    @staticmethod
    def _init_weights(m):
        if isinstance(m, (nn.Linear,)):
            nn.init.normal_(m.weight, mean=0.0, std=0.02)
            if m.bias is not None:
                nn.init.zeros_(m.bias)
        elif isinstance(m, nn.Embedding):
            nn.init.normal_(m.weight, mean=0.0, std=0.02)
        elif isinstance(m, nn.LayerNorm):
            nn.init.zeros_(m.bias)
            nn.init.ones_(m.weight)

    def forward(self, states, actions, returns_to_go, timesteps, attention_mask=None):
        """
        states         : (B, T, state_dim) float
        actions        : (B, T) long
        returns_to_go  : (B, T, 1) float
        timesteps      : (B, T) long
        attention_mask : (B, T) float {0,1} (1 = real step). None -> all ones.
        Returns action logits: (B, T, act_dim), aligned so [:, t] predicts action a_t.
        """
        B, T = states.shape[0], states.shape[1]
        if attention_mask is None:
            attention_mask = torch.ones((B, T), dtype=torch.float32, device=states.device)

        time_emb = self.embed_timestep(timesteps)                    # (B, T, H)
        r_emb = self.embed_return(returns_to_go) + time_emb          # (B, T, H)
        s_emb = self.embed_state(states) + time_emb
        a_emb = self.embed_action(actions) + time_emb

        # Interleave to (R_0,s_0,a_0, R_1,s_1,a_1, ...) -> (B, 3T, H)
        tokens = torch.stack((r_emb, s_emb, a_emb), dim=2).reshape(B, 3 * T, self.cfg.hidden_size)
        tokens = self.embed_ln(tokens)

        attn_mask = self._build_attn_mask(attention_mask)            # (B, 1, 3T, 3T)
        x = tokens
        for blk in self.blocks:
            x = blk(x, attn_mask)
        x = self.ln_f(x)

        # State tokens sit at positions 1, 4, 7, ... = 3*t + 1. Predict a_t from those.
        x = x.reshape(B, T, 3, self.cfg.hidden_size)
        state_tokens = x[:, :, 1, :]                                 # (B, T, H)
        return self.predict_action(state_tokens)                    # (B, T, act_dim)

    def _build_attn_mask(self, attention_mask):
        """Combine a causal (lower-triangular) mask with per-timestep padding.

        Returns an additive mask (B, 1, 3T, 3T) with 0 where attention is allowed and a large
        negative where it is blocked (future tokens or padded timesteps).
        """
        B, T = attention_mask.shape
        L = 3 * T
        device = attention_mask.device
        causal = torch.tril(torch.ones((L, L), device=device)).view(1, 1, L, L)
        # Expand per-timestep padding to per-token (each timestep -> 3 tokens).
        pad_tok = attention_mask.repeat_interleave(3, dim=1)         # (B, 3T)
        key_ok = pad_tok.view(B, 1, 1, L)                           # can a query attend key j?
        allowed = causal * key_ok
        neg = torch.finfo(torch.float32).min
        return torch.where(allowed > 0, torch.zeros_like(allowed), torch.full_like(allowed, neg))

    # ---- inference helper ----
    @torch.no_grad()
    def action_probs(self, states, actions, returns_to_go, timesteps, attention_mask=None):
        """Softmax action distribution at the LAST real timestep of each sequence."""
        logits = self.forward(states, actions, returns_to_go, timesteps, attention_mask)
        if attention_mask is None:
            last = torch.full((states.shape[0],), states.shape[1] - 1, device=states.device)
        else:
            last = attention_mask.sum(dim=1).long() - 1              # index of last real step
        idx = last.view(-1, 1, 1).expand(-1, 1, logits.shape[-1])
        last_logits = torch.gather(logits, 1, idx).squeeze(1)        # (B, act_dim)
        return F.softmax(last_logits, dim=-1)


def _selftest():
    torch.manual_seed(0)
    cfg = DecisionTransformerConfig(state_dim=10, act_dim=2, hidden_size=32, n_layer=2, n_head=4)
    model = DecisionTransformer(cfg)
    B, T = 4, 3
    states = torch.randn(B, T, cfg.state_dim)
    actions = torch.randint(0, cfg.act_dim, (B, T))
    rtg = torch.randn(B, T, 1)
    timesteps = torch.arange(T).unsqueeze(0).expand(B, T)
    mask = torch.ones(B, T)
    logits = model(states, actions, rtg, timesteps, mask)
    probs = model.action_probs(states, actions, rtg, timesteps, mask)
    n_params = sum(p.numel() for p in model.parameters())
    print("decision_transformer self-test")
    print("-" * 50)
    print(f"logits shape = {tuple(logits.shape)} (expect ({B},{T},{cfg.act_dim}))")
    print(f"probs shape  = {tuple(probs.shape)}, row sums ~1: "
          f"{torch.allclose(probs.sum(-1), torch.ones(B), atol=1e-5)}")
    print(f"param count  = {n_params}")


if __name__ == "__main__":
    _selftest()
