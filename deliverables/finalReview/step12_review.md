# Step 12 — final review

**Summary:** The chapter's argument is sound and its numbers trace to the committed JSON, but three things matter most. (1) The Bulgarian text mistranslates the chapter's two core terms, and both come from the settled glossary: *return conditioning* is "условно връщане" (a conditional refund) and *return-to-go* is "очаквана възвръщаемост до края" (the *expected* return). The second makes § 12.2 contradict itself. The BG one-pager also has a string of meaning errors: "ангажирани JSON", "добре овластен модел", "невъзможна разлика е намалена с +1.59", "3 ПАС / 2 НЕУСПЕХ". (2) All six figures print entirely in English, because no BG render exists for step 12. Four of them print at 4.6–7.6 pt. (3) Several headline claims go beyond their evidence. The one-pager's "LLM 0.833" is the scripted offline stub, not a language model. The Kuhn "collapse" is a *spike* in exploitability. "The entire gain comes from passive and random opponents" is contradicted by the chapter's own figure. "In-context adaptation did not emerge" rests on one 7B model with a 20-hand window, and the same models do adapt when told the opponent type. The ARDT "evidence-backed fix" has not been run, and ARDT's target is exact only for deterministic transitions, which poker's chance nodes are not. Centrally decided, counted only: " - " as a dash 27× (summary) + 10× (one-pager); decimal points ≈ 53; "5,000"/"50,000" plus a stray "1,576" (decimal comma in a line of points); 7 pipeline-added bold spans (36 vs 29 in the EN).
**Counts:** S1 21 · S2 40 · S3 6   (by category: G 8 · B 30 · T 11 · C 10 · S 6 · X 2)

Conventions in this file are those of the pilot. Quotes are **raw markdown** from `summaryBg.md` / `onePagerBg.md`. "EN" quotes come from `summaryEn.md` / `onePager.md`, whose lines are wrapped at about 100 characters, so EN changes are given by line number where a quote would cross a line break. Proposals keep " - " and decimal points; those are fixed centrally (F07-B41, F07-B42). Page numbers are PDF pages as in `renders/` (the printed folio is one lower). Printed sizes use scale = 17.6 cm print width ÷ saved width, and every step-12 figure is saved at dpi 130. Step 12 has no box diagrams, so the corpus-wide box-overflow and "\н" defects do not apply here, and none of its 33 mapping entries contains a literal escape. The candidate's August proofreading comments contain none for chapter 12. The only one that applies is the TOC comment on "step" naming, which is not applied here (F12-C09). The report (`report_en.md` / `report_bg.md`) agrees with the summary and one-pager on every number checked. Report BG vs EN: the numbers match.

## G — Figures

### F12-G01 · S1 · Bulgarian captions for all six figures
- **Where:** summaryBg.md, image alt text of figs. 72–77 (pp. 220–225). All six print in English; two are half-translated ("…target return on Ледюк Холдем, with standard errors").
- **Now → Proposed:**
  - "![ARDT exploitability against the expectile tau, with the mean relabel target on the second axis.]" → "![Експлоатируемост на ARDT в зависимост от параметъра τ на експектилната регресия; по втората ос - средната целева стойност при преетикетирането. Средни стойности от три начални числа (за сравнение: стандартен DT - 0.731, равновесие - 0.017 жетона).]"
  - "![Decision Transformer performance against the conditioned target return on Ледюк Холдем, with standard errors.]" → "![Резултат на DT в Ледюк Холдем (жетони на раздаване срещу почти равновесен противник) в зависимост от целевата възвръщаемост, по която е обусловен, със стандартни грешки. Прекъснатата линия отбелязва най-честата възвръщаемост (-1), а точковата - недостижимата цел (+15).]"
  - "![Each information set's share of total exploitability, beside its deviation from equilibrium.]" → "![Дял на всяко информационно множество в общата експлоатируемост на Qwen2.5-7B-Instruct в Кун покер (0.357 жетона) и отклонението му от равновесието на Наш (1/2/3 - вале/дама/поп; p - пас, b - залог в историята). Двете подредби почти не си съответстват.]"
  - "![Stated versus executed betting frequencies for two models, with the exploitability of each strategy.]" → "![Заявени (при запитване) и реално изиграни честоти на залагане на gpt-oss-20b и Qwen2.5-7B-Instruct по информационни множества, с равновесието за сравнение (горе), и експлоатируемост на изиграната стратегия и на стратегия, построена от заявените честоти (долу).]"
  - "![Exploitation against exploitability, with the per-opponent breakdown.]" → "![Печалба срещу всеки противник от набора: Qwen2.5-7B-Instruct печели средно 0.177 жетона на раздаване (равновесието - 0.110) при експлоатируемост 0.357 жетона (равновесието - 0.006).]" (the wording assumes F12-G07 drops the scatter panel)
  - "![Illegal-action intent by category and by situation on Ледюк Холдем.]" → "![Склонност към недопустими действия в Ледюк Холдем (Qwen2.5-7B-Instruct) по категории и по ситуации: почти цялата вероятностна маса е отказ от ръката, когато чекът е безплатен, във втория рунд на залагане.]"
- **Fix:** replace the alt text in `summaryBg.md` and keep the `](file.png)` part (for the `_bg` file names, see F12-G02). The EN captions should also name the model (F12-C10).

### F12-G02 · S1 · No Bulgarian render exists for any step-12 figure
- **Where:** all six figures, pp. 220–225. `summaryBg.md` links the EN files (`impl_tau_sweep.png` …), and `implementation/step12/implementation/results/` contains no `*_bg.png`.
- **Problem:** Every title, axis label, legend, tick label, opponent name and category code prints in English, with decimal points. `plotting.py` is listed by `plotting_scripts()` and has 33 mapping entries, but it has never produced a BG file. A likely cause: `main()` calls `ap.parse_args()`. Under `render_bg_figures.py --only step12` it sees the renderer's own `--only` flag and exits with code 2, and the renderer counts this as "ok … exited" with 0 figures. The mapping also cannot reach six strings that are built with f-strings or taken from the JSON (per-figure lists below).
- **Fix:** In `plotting.py` `main()`, change `args = ap.parse_args()` to `args, _ = ap.parse_known_args()`. Apply the figure changes in F12-G03…G08, then run `python scripts/figures/render_bg_figures.py --only step12`. Copy the six `results/*_bg.png` files to `deliverables/reports/step12/summary/impl_<name>_bg.png` (the copy loop in `deliverables/reports/step12/figures/README.md`, with a `_bg` suffix) and change the six links in `summaryBg.md` to `impl_<name>_bg.png`. For bar labels drawn with `ax.text(f"{v:.3f}")`, use `locale.format_string("%.3f", v)` so that the BG render (LC_NUMERIC = bg) prints a decimal comma and the EN render a point.

### F12-G03 · S2 · Fig. 72 τ sweep: legend 7.9 pt, soft, legend values differ from the one-pager
- **Where:** `renders/ch12/p220_f1.png`. Saved 910 px (7.0 in), so the scale is 0.99. `effective_ppi` 131.
- **Problem:**
  1. Most text prints at 9.9 pt, but the legend (fs 8) prints at 7.9 pt, and the image is soft (131 ppi).
  2. The legend shows "vanilla DT (0.731)" and "Nash (0.017)", which are 3-seed means from `tau_sweep_SMOKE.json`. The one-pager quotes 0.799 and 0.0162 from a single run. A reader sees two DT numbers without explanation.
  3. These labels are f-strings, so the mapping cannot translate them.
  4. The current mapping leaves English: 'exploitability (chips)' → 'експлоатируемост (chips)', 'ARDT: exploitability vs expectile tau' → '…спрямо expectile tau'.
- **Fix:** `plot_tau_sweep`: `label=f"vanilla DT ({…:.3f})"` → `label="vanilla DT"`, `label=f"Nash ({…:.3f})"` → `label="Nash"`, with the values in the caption (F12-G01); `ax.legend(…, fontsize=8, …)` → `fontsize=10`; `fig.savefig(path, dpi=130)` → `dpi=300`. Mapping: 'exploitability (chips)' → 'експлоатируемост (жетони)'; 'ARDT: exploitability vs expectile tau' → 'ARDT: експлоатируемост спрямо τ на експектила'; 'expectile tau  (low = pessimistic / minimax side, per ARDT Eq. 7)' → 'τ на експектила (ниско = песимистична, минимаксна страна; ур. 7 в ARDT)'; 'ARDT exploitability' → 'експлоатируемост на ARDT'; 'mean relabel target' → 'средна целева стойност при преетикетирането'; 'mean relabel target (chips)' → 'средна целева стойност при преетикетирането (жетони)'. New keys: 'vanilla DT' → 'стандартен DT'. For 'Nash', see F12-G06.

### F12-G04 · S2 · Fig. 73 Leduc return conditioning: legend 6.9 pt, title and legend unmappable
- **Where:** `renders/ch12/p221_f1.png`. Saved 1040 px (8.0 in), scale 0.866. `effective_ppi` 150 (borderline).
- **Problem:**
  1. The legend (fs 8) prints at 6.9 pt; ticks and axis labels at 8.7 pt.
  2. The title (`f"Leduc: no steering (Pearson r = …)"`) and the legend entries `f"modal return ({modal:+.0f}, {…:.0%} of steps)"` / `f"impossible ({o:+.0f})"` are f-strings.
  3. The figure shows two deep dips at 0 and −5 next to a text that says "the collapse disappears" (see F12-C07).
- **Fix:** `plot_leduc_return_conditioning`: drop `ax.set_title(...)` (the caption carries r); labels → `"modal return"` and `"impossible target"`; `ax.legend(fontsize=8)` → `fontsize=10`; dpi 130 → 300. Mapping: 'DT vs near-Nash' → 'DT срещу почти равновесен противник'; 'chips/hand vs near-Nash' → 'жетони на раздаване срещу почти равновесен противник' (the current entry starts with a capital "Жетони/ръка"); 'target return-to-go (chips)' → 'целева остатъчна възвръщаемост (жетони)' (T02). New keys: 'modal return' → 'най-честа възвръщаемост'; 'impossible target' → 'недостижима цел'.

### F12-G05 · S1 · Fig. 74 leak decomposition prints at 6.3–7.6 pt
- **Where:** `renders/ch12/p222_f1.png`. Saved from figsize (11, 5): 1430 px, scale 0.630.
- **Problem:**
  1. Ticks and axis labels 10 → 6.3 pt; panel titles 12 → 7.6 pt; suptitle 11 → 6.9 pt. All text is English.
  2. The suptitle (`f"{model} — deviation size does not predict cost"`) and the left title (`f"Where the loss is  (total {base:.3f} chips)"`) are f-strings.
  3. The info-set codes (1, 2p, 3pb …) are explained nowhere in the chapter.
- **Fix:** `plot_leak_decomposition`: figsize (11, 5) → (8, 4.4); remove `fig.suptitle(...)` (the caption names the model and the total); `ax.set_title("Where the loss is")`; dpi 130 → 300. At the default fs 10, text prints at 8.7 pt. Mapping: 'How far from Nash' → 'Отклонение от равновесието'; '|P(bet) - Nash|' → '|P(залог) - равновесие|'. New key: 'Where the loss is' → 'Къде е загубата'. The caption in F12-G01 explains the codes.

### F12-G06 · S1 · Fig. 75 stated vs executed: 6.0 pt labels, truncated model name
- **Where:** `renders/ch12/p223_f1.png`. Saved from figsize (11, 8) with `bbox_inches="tight"`: 1211 px (9.3 in), scale 0.744.
- **Problem:**
  1. x tick labels, both upper legends and the bar values (fs 8) print at 6.0 pt; panel titles (9) at 6.7 pt; y ticks and labels at 7.4 pt.
  2. The lower tick label reads "qwen2.5-7b-ins", cut by `d["model"].split("/")[-1][:14]`.
  3. The panel titles are f-strings.
  4. The mapping entries are poor Bulgarian: 'as played' → 'както се играе'; 'if it played what it says' → 'ако е изиграло това, което казва' (neuter subject); 'stated (asked)' → 'деклариран (поискан)' ("поискан" = requested); 'Playing what they SAY would be far worse than what they DO' → 'Да играеш това, което казват, би било…' (person mismatch); 'Nash' → 'Наш равновесие' (ungrammatical, used in figs. 72 and 75).
- **Fix:** `plot_stated_vs_executed`: figsize (11, 8) → (8, 7); `set_xticklabels(…, fontsize=8)` → `fontsize=10`; `ax.legend(fontsize=8)` → `10`; panel title → display name only, fontsize 9 → 10.5 (MAE values go to the caption); bottom `ax.legend(fontsize=9)` → `10`, bottom title fontsize 10 → 11; bar values fontsize 8 → 10 via `locale.format_string` (F12-G02); names from `NAMES = {"openai/gpt-oss-20b": "gpt-oss-20b", "qwen2.5-7b-instruct": "Qwen2.5-7B-Instruct"}`; dpi 130 → 300. Mapping: 'executed (played)' → 'изиграна'; 'stated (asked)' → 'заявена (при запитване)'; 'as played' → 'изиграна стратегия'; 'if it played what it says' → 'ако играеше заявеното'; 'Playing what they SAY would be far worse than what they DO' → 'Заявеното би било много по-лошо от изиграното'; 'Nash' → 'равновесие на Наш'.

### F12-G07 · S1 · Fig. 76 exploitation frontier: 4.6 pt labels, a title its own bars contradict
- **Where:** `renders/ch12/p224_f1.png`. Saved from figsize (12, 4.6): 1560 px, scale 0.577.
- **Problem:**
  1. Bot names, legend and point labels (fs 8) print at 4.6 pt; ticks and axis labels at 5.8 pt; titles at 6.9 pt.
  2. The right-hand title "Per-opponent: the gain is only vs passive/random" is false by its own bars: the LLM also beats Nash against AlwaysBet (0.191 vs 0.129) and LooseAggressive (0.198 vs 0.162) (F12-C05).
  3. "LLM-plain" does not say which model it is (Qwen2.5-7B-Instruct).
  4. The left panel holds two points whose values fit in one caption line.
  5. The bot names come from the JSON, so they are not in the mapping.
- **Fix:** `plot_exploitation_frontier`: drop the scatter panel (`fig, ax2 = plt.subplots(figsize=(8, 4.2))`); `set_xticklabels(opps, rotation=25, ha="right", fontsize=8)` → `fontsize=10`; `ax2.legend(fontsize=8)` → `10`; title → `"Winnings per opponent"`; series labels via `{"Nash-CFR": "Nash (CFR)", "LLM-plain": "Qwen2.5-7B-Instruct"}`; dpi 130 → 300. Mapping: 'chips/hand won' → 'спечелени жетони на раздаване'. New keys: 'Winnings per opponent' → 'Печалба срещу всеки противник'; 'Nash (CFR)' → 'равновесие (CFR)'; 'AlwaysPass' → 'Винаги пас'; 'AlwaysBet' → 'Винаги залог'; 'TightPassive' → 'Стегнат-пасивен'; 'LooseAggressive' → 'Разпуснат-агресивен'; 'Thresholdish' → 'Прагов'; 'Random' → 'Случаен'. The bot names pass through `set_xticklabels`, which the renderer wraps.

### F12-G08 · S1 · Fig. 77 Leduc illegal-action taxonomy prints at 4.8–6.0 pt
- **Where:** `renders/ch12/p225_f1.png`. Saved from figsize (11.5, 4.4): 1495 px, scale 0.603.
- **Problem:**
  1. Category ticks and "n=" labels (fs 8) print at 4.8 pt; titles (9) at 5.4 pt; y ticks and axis labels at 6.0 pt.
  2. Category and situation names are code identifiers ("FOLD_WHEN_FREE", "round2/nothing due"). They are passed as `bar`/`barh` data, which the renderer does not translate.
  3. The left title is an f-string.
  4. The mapping 'Localised: only round 2 with nothing due' → 'Локализирано: само кръг 2 без нищо друго' is wrong: *nothing due* = nothing to call.
- **Fix:** `plot_leduc_illegal_taxonomy`: figsize (11.5, 4.4) → (8, 4.2); `ax.bar(range(len(cnames)), …)` + `ax.set_xticks(range(len(cnames)))` + `ax.set_xticklabels([CAT[c] for c in cnames], fontsize=10)`; `ax2.barh(range(len(sits)), …)` + `ax2.set_yticks(range(len(sits)))` + `ax2.set_yticklabels([SIT[s] for s in sits], fontsize=10)`; left title → `"Illegal-action intent by category"` (totals to the caption); title fs 9 → 10.5; `tick_params(labelsize=8)` → `10`; "n=" text fs 8 → 10; dpi 130 → 300. Here `CAT = {"FOLD_WHEN_FREE": "fold when check is free", "RAISE_AT_CAP": "raise above the cap", "NON_ACTION": "non-action reply"}` and `SIT` = "round 1, nothing to call" / "round 1, facing a bet" / "round 2, nothing to call" / "round 2, facing a bet". Mapping: those seven strings → 'отказ при безплатен чек', 'повишаване над лимита', 'отговор, който не е действие', '1. рунд, без залог за плащане', '1. рунд, срещу залог', '2. рунд, без залог за плащане', '2. рунд, срещу залог'; 'Illegal-action intent by category' → 'Склонност към недопустими действия по категории'; 'Localised: only round 2 with nothing due' → 'Само във 2. рунд, когато няма залог за плащане'; 'mean illegal mass' → 'средна маса на недопустимите действия' (not 'незаконна').

## B — Bulgarian language

### F12-B01 · S1 · meaning — "При извод просто **условие**"
- **Where:** summaryBg.md § "Защо да се разглежда обучението с подкрепление като прогнозиране на последователност" — "При извод просто **условие**: задайте желана висока очаквана възвръщаемост до края и моделът генерира действията, които исторически са я предшествали."
- **EN:** "At inference you simply **condition**: ask for a high return-to-go and the model produces the actions that historically preceded such returns."
- **Now → Proposed:** "При извод просто **условие**: задайте желана висока очаквана възвръщаемост до края и моделът генерира действията, които исторически са я предшествали." → "При използването на модела той просто се **обуславя**: задава се желана висока остатъчна възвръщаемост и моделът генерира действията, които в данните са предшествали такива възвръщаемости."
- **Why:** "условие" is the noun "a condition", so the sentence has no verb. "При извод" reads as "in a conclusion". Return-to-go: T02.

### F12-B02 · S1 · meaning — "Привлекателността на тази теза … тя работи", with "Step 13" in English
- **Where:** summaryBg.md § 12.1 — "Привлекателността на тази теза е, че тя работи изцяло **извън линия**, върху фиксиран набор от данни - в режима, в който се намират логовете на Playtech на Step 13, където самообучението не е възможно.[^chen2021]"
- **EN:** "The appeal for this thesis is that it works entirely **offline**, on a fixed dataset — the regime Chapter 13's Playtech logs live in, where self-play is unavailable."
- **Now → Proposed:** "Привлекателността на тази теза е, че тя работи изцяло **извън линия**, върху фиксиран набор от данни - в режима, в който се намират логовете на Playtech на Step 13, където самообучението не е възможно.[^chen2021]" → "За дисертацията подходът е привлекателен, защото работи изцяло **офлайн** - върху фиксиран набор от записани данни, какъвто е случаят с историите на реални игри, при които самоигра не е възможна.[^chen2021]"
- **Why:** "тази теза … тя работи" makes the *thesis statement* the thing that works offline; *for this thesis* means "for the dissertation". "Step 13" is English and points to a chapter that was never written (F12-C09). The Playtech logs belong to that chapter too. "извън линия": T06; "самообучение": T03.

### F12-B03 · S1 · English left — "gPT-style", "(measured)"
- **Where:** summaryBg.md § 12.1 and § "Капанът между късмета и умението"
- **Now → Proposed:**
  - "На gPT-style модел се подава траектория от тройки" → "На модел от типа GPT се подава траектория от тройки"
  - "$$P(a = B \mid \hat{R} = 1.0) = 1.00 \quad \text{(measured)}$$" → "$$P(a = B \mid \hat{R} = 1.0) = 1.00 \quad \text{(измерено)}$$"
- **Why:** Both are English in the BG text and both print (pp. 218, 218). "gPT" also has a lower-case g, a pipeline case error. For Cyrillic inside `\text{}`, check the first rebuild (as noted in F07-B08).

### F12-B04 · S1 · terminology — *return conditioning* as "условно връщане" / "условност" (T01)
- **Where:** summaryBg.md §§ 12.2, 12.3, 12.4 headings; onePagerBg.md
- **EN:** "conditioning on an outcome" / "ARDT — conditioning on what you can guarantee" / "What return conditioning actually does in poker" / "Return conditioning never steers, on either game."
- **Now → Proposed:**
  - "Обучаващият се, обусловен от възвръщаемостта, уверено избира действието с по-ниска **очаквана стойност**. Това не е грешка в модела; това е смисълът на **условност върху изход**, когато самият изход съдържа елемент на случайност." → "Обучаваният модел, обусловен по възвръщаемостта, уверено избира действието с по-ниска очаквана стойност. Това не е грешка в модела, а самата същност на обуславянето по изхода, когато изходът отчасти зависи от случайността."
  - "## ARDT - условност върху гарантираното" → "## ARDT - обуславяне по гарантираната възвръщаемост"
  - "## Какво всъщност представлява условното връщане в покера" → "## Какво всъщност прави обуславянето по възвръщаемостта в покера"
  - onePagerBg: "- *Условното връщане никога не насочва в нито една от игрите.*" → "- *Обуславянето по възвръщаемостта не насочва стратегията в нито една от двете игри.*"
  - The remaining occurrences are rewritten in F12-B12 (§ 12.4 ¶ 2), F12-C02 (§ 12.4 ¶ 1), F12-C09 (§ 12.4 last ¶), F12-C08 (takeaway 1) and F12-C01 (one-pager bullet 1).
- **Why:** "условно връщане" reads as "conditional return (of goods)", and "условност върху изход" is a word-for-word calque. The operation is conditioning *on* the return: "обуславяне по възвръщаемостта". The heading also says "what it is" ("представлява") where the EN says "what it does". "Обучаващият се" (the one who is learning) is an awkward substantivised participle.

### F12-B05 · S1 · terminology — *return-to-go* as "очаквана възвръщаемост до края" (T02)
- **Where:** summaryBg.md §§ 12.1, 12.2, 12.3; onePagerBg.md "**Проблем.**"
- **EN:** "where $\hat{R}_t = \sum_{t'\ge t} r_{t'}$ is the *return-to-go*" / "The reframing hides an assumption: that the return-to-go is something the agent *earned*." / "the minimax return-to-go"
- **Now → Proposed:**
  - "е *очакваната възвръщаемост до края*, моделът се обучава" → "е *остатъчната възвръщаемост* (return-to-go), а моделът се обучава"
  - "Преформулирането прикрива едно предположение: че очакваната възвръщаемост до края е нещо, което агентът *е заслужил*." → "Преформулирането прикрива едно предположение: че остатъчната възвръщаемост е нещо, което агентът *е заслужил*."
  - "- минимакс очакваната възвръщаемост до края." → "- минимаксната остатъчна възвръщаемост."
  - onePagerBg: "тройки `(очаквана възвръщаемост до края, състояние, действие)`" → "тройки `(остатъчна възвръщаемост, състояние, действие)`"
- **Why:** $\hat{R}_t$ is the *realised* sum of the remaining rewards, and "очаквана" means *expected*. § 12.2 argues exactly that the realised return is not the expected one, so the BG sentence contradicts the paragraph it opens. The first item also mends a comma splice. B01 carries a fifth occurrence.

### F12-B06 · S1 · meaning — "компетентни" inserted
- **Where:** summaryBg.md § "Експлоатация, адаптация и ограниченията на опростената игра" — "Измерено спрямо набор от умишлено експлоатируеми компетентни архетипи,"
- **EN:** "Measured against a zoo of deliberately exploitable archetypes,"
- **Now → Proposed:** "Измерено спрямо набор от умишлено експлоатируеми компетентни архетипи," → "Измерено спрямо набор от умишлено експлоатируеми архетипи,"
- **Why:** The EN has no "competent", and "deliberately exploitable competent" contradicts itself. The glossary entry "competent archetypes" was pulled in from the next sentence.

### F12-B07 · S2 · calque/terminology — § 12.1 opening (back up, supervised, DT name)
- **Where:** summaryBg.md § 12.1 — "Класическото обучение с подкрепление оптимизира чрез оценка на функция на стойността, връщане на наградите и подобряване на стратегията. Трансформърът за вземане на решения (Chen и др., 2021) предлага различен подход - разглежда целия проблем като **супервизирано моделиране на последователности**."
- **EN:** "Classical RL optimises: estimate a value function, back up rewards, improve the policy. The Decision Transformer (Chen et al., 2021) proposes something different — treat the whole problem as **supervised sequence modelling**."
- **Now → Proposed:** (the quote above) → "Класическото обучение с подкрепление оптимизира, като оценява функцията на стойността, разпространява наградите назад (белманово обновяване) и подобрява стратегията. Decision Transformer (DT, „трансформър за вземане на решения“; Chen и др., 2021) предлага друг подход: разглежда целия проблем като **моделиране на последователности чрез обучение с учител**."
- **Why:** "връщане на наградите" means handing rewards back; *back up* is propagating values backwards. "супервизирано" is a calque (T10). The chapter names the model three ways ("Трансформърът за вземане на решения", "трансфърмъра", "Decision Transformer"), so fix the name at first use (T08).

### F12-B08 · S2 · meaning — "еднорък бандит" for a two-action bandit; Cyrillic "А"
- **Where:** summaryBg.md § 12.2 — "Разгледайте едностъпков еднорък бандит. Действие А изплаща"; "Действие А е оптимално по очаквана стойност."
- **EN:** "Consider a one-step bandit. Action A pays $0.5$ deterministically."
- **Now → Proposed:**
  - "Разгледайте едностъпков еднорък бандит. Действие А изплаща" → "Разгледайте едностъпкова задача с два възможни избора (двурък бандит). Действие A изплаща"
  - "Действие А е оптимално по очаквана стойност." → "Действие A е оптимално по очаквана стойност."
- **Why:** "еднорък бандит" is a one-armed slot machine, and the example has two actions. "А" is Cyrillic (U+0410) while "B" and the formula's $B$ are Latin, which breaks search and the visual pairing in some fonts.

### F12-B09 · S2 · calque — *protagonist* as "главният герой" (cf. F07-T14)
- **Where:** summaryBg.md §§ 12.3, 12.4
- **EN:** "the return the protagonist can **guarantee against a worst-case opponent**" / "which the protagonist does not control"
- **Now → Proposed:**
  - "а върху възвръщаемостта, която главният герой може **да гарантира срещу противник в най-лошия случай**" → "а върху възвръщаемостта, която агентът може **да си гарантира срещу противник в най-лошия случай**"
  - "които главният герой не контролира" → "които агентът не контролира"
- **Why:** ARDT's "protagonist" is the agent being trained. "главният герой" reads as the hero of a novel, the same problem as *hero* → "герой" (F07-T14).

### F12-B10 · S2 · terminology — *relabel* in two words, *return* as "доходност" (T11)
- **Where:** summaryBg.md § 12.3
- **EN:** "The trajectories are relabelled with the estimated minimax return" / "Second — the important one — the relabel target is"
- **Now → Proposed:**
  - "Траекториите се преетикетират с оценената минимакс доходност и върху тях се обучава стандартен DT." → "Траекториите се преетикетират с оценената минимаксна възвръщаемост и върху тях се обучава стандартен DT."
  - "Второ - по-важното - целта за преозначаване е" → "Второ - и по-важно - целевата стойност при преетикетирането е"
  - § 12.3's last paragraph is rewritten in F12-C08.
- **Why:** "доходност" is financial yield; the chapter uses "възвръщаемост" everywhere else. *Relabel* appears as both "преетикетиране" and "преозначаване" within one section.

### F12-B11 · S2 · calque/internal reference — § 12.3 "Два детайла…"
- **Where:** summaryBg.md § "ARDT - условност върху гарантираното"
- **EN:** "Two details of the published method matter, and both were confirmed by reading the source rather than the summary. First, the pessimistic side is **low** $\alpha$ (the raw step's claim that $\tau = 0.9$ is pessimistic is inverted); the paper itself runs $\alpha = 0.01$." / "a state-**action** value produced by two *coupled* estimators alternately fitted" / "which is exactly the discrimination the method relies on."
- **Now → Proposed:**
  - "Два детайла от публикувания метод имат значение и двата бяха потвърдени чрез прочитане на източника, а не само резюмето." → "Два детайла от публикувания метод са съществени; и двата са проверени в самата статия, а не само в резюмето ѝ."
  - "Първо, песимистичната страна е **ниска** $\alpha$ (твърдението в суровия текст, че $\tau = 0.9$ е песимистичен, е обърнато); самата статия изпълнява $\alpha = 0.01$." → "Първо, песимистичната страна съответства на **ниско** $\alpha$ (в първоначалния план на главата $\tau = 0.9$ погрешно е описано като песимистично); самата статия използва $\alpha = 0.01$."
  - "стойност на **състояние-действие**, получена от два *свързани* оценителя, които се напасват последователно със загуби $\alpha$ и $1-\alpha$." → "стойност на двойката **състояние-действие**, получена от два *свързани* оценителя, които се напасват редуващо се със загуби $\alpha$ и $1-\alpha$."
  - "което е точно дискриминацията, върху която методът се основава." → "а точно на това разграничение се основава методът."
- **Why:** A comma is missing between two independent clauses. "суровия текст" (the *raw step*) is internal planning jargon that a bundle reader cannot resolve (F12-C09). "изпълнява α" is a calque of *runs*. "последователно" means one after the other, while the estimators *alternate*. In Bulgarian "дискриминация" is mostly social discrimination.

### F12-B12 · S2 · calque — "четири печалби", "кой залог", "формата на ръката"
- **Where:** summaryBg.md § 12.4 — "Естественото обяснение е, че в игра с четири печалби *големината* на връщането кодира кой **залог** е бил изигран, а неговият *знак* - кой държи по-добрата карта. Следователно условното връщане определя формата на ръката, а не качеството на играта."
- **EN:** "in a four-payoff game the *magnitude* of the return encodes which betting line was played, while its *sign* encodes who held the better card. Conditioning therefore selects the shape of the hand rather than the quality of the play."
- **Now → Proposed:** (the quote above) → "Естественото обяснение е, че в игра само с четири възможни стойности на печалбата *големината* на възвръщаемостта кодира коя последователност от залози е изиграна, а *знакът* ѝ - кой е държал по-добрата карта. Следователно обуславянето избира хода на раздаването, а не качеството на играта."
- **Why:** "игра с четири печалби" means a game with four wins. "кой залог" (which bet) loses *betting line*, the whole sequence of actions. "формата на ръката" is a calque of *shape of the hand*. "връщане": T01.

### F12-B13 · S2 · calque — "алфабета на изплащанията", "количество гранулираност"
- **Where:** summaryBg.md § 12.4
- **EN:** "So the payoff-alphabet account explains the collapse but not the failure." / "No amount of payoff granularity makes an uncontrollable signal steerable."
- **Now → Proposed:**
  - "Следователно обяснението с алфабета на изплащанията обяснява срива, но не и провала." → "Следователно обяснението чрез малкия брой възможни печалби обяснява срива, но не и провала."
  - "Никакво количество гранулираност на печалбата не прави един неконтролируем сигнал управляем." → "Колкото и да са възможните стойности на печалбата, сигнал, който агентът не контролира, не става управляем."
- **Why:** "алфабет" is a literal calque of a metaphor. "изплащания" deviates from the glossary (payoff → печалба; the glossary also has "payoff alphabet → набор печалби"). "количество гранулираност" is a noun pile.

### F12-B14 · S2 · calque — "ЕМ са **честно експлоатируеми**"
- **Where:** summaryBg.md § "Езикови модели като стратегически агенти" — "Измерени по същия точен критерий, ЕМ са **честно експлоатируеми** - но интересният резултат е *къде* те се провалят."
- **EN:** "Measured against the same exact ruler, LLMs are **honestly exploitable** — but the interesting result is *where* they fail."
- **Now → Proposed:** (the quote above) → "Измерени със същия точен критерий, големите езикови модели се оказват **действително експлоатируеми**, но по-интересно е *къде* грешат."
- **Why:** "ЕМ" is an undefined Cyrillic abbreviation. The curated glossary uses "голям езиков модел" in prose, and rule 2 keeps abbreviations in Latin script. "честно експлоатируеми" means "exploitable in an honest way"; *honestly* here means "genuinely".

### F12-B15 · S2 · terminology/calque — King as "краля", "докладване", "Глава 14"
- **Where:** summaryBg.md § 12.5 — "„Провалът“ с краля - най-голямото видимо отклонение от равновесие - представлява **0.1%** от общата загуба, тъй като свръхзалагането на ръка, която никога не е по-слаба, е почти безплатно. Едно единствено решение с дама струва **41.4%**. Величината на отклонението и цената са почти некорелирани, което е конкретният аргумент за докладване на диагностика по решения, вместо да се представя само едно число за експлоатируемост в рамката за оценяване от Глава 14."
- **EN:** "…the concrete argument for reporting per-decision diagnostics rather than a single exploitability number in the Chapter 14 evaluation framework."
- **Now → Proposed:** (the quote above) → "„Провалът“ с поп - най-голямото видимо отклонение от равновесието - носи само **0.1%** от общата загуба, защото прекомерното залагане с ръка, която никога не е по-слаба, почти не струва нищо. Едно-единствено решение с дама струва **41.4%**. Големината на отклонението и цената му почти не са корелирани - конкретен аргумент при оценяването да се отчита диагностика по отделни решения, а не само едно число за експлоатируемост."
- **Why:** The curated card names are Вале/Дама/Поп, and the BG one-pager already says „Поп“. "Едно единствено" needs the hyphen. "докладване" is a calque of *reporting*. "Глава 14" was never written (F12-C09).

### F12-B16 · S2 · meaning — the trade-off *is* the second contribution
- **Where:** summaryBg.md § 12.6 — "Това е компромисът безопасност–експлоатация, който представлява вторият принос на дисертацията, наблюдаван, а не предположен."
- **EN:** "That is the safe-exploitation trade-off of the thesis's second contribution, observed rather than assumed."
- **Now → Proposed:** (the quote above) → "Това е компромисът между безопасност и експлоатация, с който се занимава вторият принос на дисертацията - тук наблюдаван, а не предположен."
- **Why:** The BG says the trade-off *constitutes* the contribution, which is not the claim. The trailing participles have no clear referent.

### F12-B17 · S1 · meaning/terminology — § 12.6 last paragraph (street, check, board, spelling)
- **Where:** summaryBg.md § 12.6 — "Една улица и една обща карта по-късно големият езиков модел е статистически неразличим от трансфърмъра за вземане на решения, изобщо не може да победи слаби противници и има склонност към недопустимо действие с приблизително една четвърт от своята вероятностна маса. Този провал се дължи на *едно* погрешно схващане, а не на разпръсната обърканост - моделът иска да **пасува, когато проверката е безплатна**, почти изключително със слаби несдвоени раздавания срещу висока маса, докато никога не прави опит за повишаване над лимита за залагане."
- **EN:** "One street and one board card later, the LLM is statistically indistinguishable from the Decision Transformer, cannot beat weak opponents at all, and wants to take an illegal action with roughly a quarter of its probability mass. … it wants to **fold when checking is free**, almost exclusively on weak unpaired hands against a high board, while never once attempting to raise past the betting cap."
- **Now → Proposed:** (the quote above) → "С един рунд на залагане и една обща карта повече големият езиков модел вече е статистически неразличим от DT, губи средно срещу набора от слаби противници (печели само срещу двата пасивни типа) и насочва приблизително една четвърт от вероятностната си маса към недопустими действия. Този провал се дължи на *едно* погрешно схващане, а не на обща обърканост: моделът иска **да се откаже от ръката, когато може безплатно да направи чек**, почти изключително със слаби ръце без чифт при висока обща карта, и нито веднъж не се опитва да повиши над лимита за залагане."
- **Why:**
  - The key finding is garbled: "пасува, когато проверката е безплатна" reads "passes when the verification is free" (T07). In Leduc, *fold* and *check* are different actions.
  - "улица" (street), "висока маса" (a high *table*) and "раздавания" for the cards one holds (cf. F07-B20) are calques.
  - "трансфърмъра" is misspelt.
  - The content correction on weak opponents is in F12-C07.

### F12-B18 · S2 · terminology — greedy decoding (T09); "хванат"
- **Where:** summaryBg.md § "Основни изводи за синтеза на дисертацията", last bullet
- **EN:** "At greedy decoding a language model plays a pure strategy … each caught by a cheap check"
- **Now → Proposed:**
  - "При алчен избор на последователност езиковият модел играе чиста стратегия" → "При алчно декодиране (температура 0) езиковият модел играе чиста стратегия"
  - "всеки от които беше хванат чрез евтина проверка" → "всеки от които беше открит чрез евтина проверка"
- **Why:** Greedy decoding chooses the most probable *token* at each step, not a sequence. "хванат" is colloquial.

### F12-B19 · S2 · terminology — chapter title: "Последователни модели", "ситуации" vs "среди"
- **Where:** summaryBg.md heading and front matter; onePagerBg.md title and heading (it prints in the bundle TOC and on p. 218)
- **EN:** "Sequence Models and LLM Agents in Strategic Settings"
- **Now → Proposed:**
  - "# Глава 12 - Последователни модели и агенти с голям езиков модел в стратегически ситуации" → "# Глава 12 - Модели на последователности и агенти с голям езиков модел в стратегически среди"
  - front matter "Глава 12 Обобщение - Последователни модели и агенти с голям езиков модел в стратегически среди" → "Глава 12 Обобщение - Модели на последователности и агенти с голям езиков модел в стратегически среди"
  - onePagerBg (title and heading, 2×): "Глава 12 Резюме - Последователни модели и агенти с голям езиков модел в стратегически среди" → "Глава 12 Резюме - Модели на последователности и агенти с голям езиков модел в стратегически среди"
- **Why:** "последователни модели" reads as "consistent/successive models" (T04). The printed heading says "ситуации", while the front matter and the one-pager say "среди".

### F12-B20 · S3 · punctuation — full stop before a formula that continues the sentence
- **Where:** summaryBg.md § 12.3 — "която минимизира асиметричната квадратична загуба."
- **Now → Proposed:** "която минимизира асиметричната квадратична загуба." → "която минимизира асиметричната квадратична загуба"
- **Why:** The sentence continues after the display formula ("чиито граници дават…"), as it does in the EN. With the full stop, the next paragraph starts in lower case.

### F12-B21 · S1 · meaning — one-pager: "точна експлоатируемост на Наш и точна експлоатируемост"
- **Where:** onePagerBg.md "**Подход.**" — "Кун покер, където глава 2 предоставя точна експлоатируемост на Наш и точна експлоатируемост, с тесен порт към Ледюк Холдем като проверка за сложност."
- **EN:** "Kuhn Poker, where Chapter 2 supplies exact Nash and exact exploitability, with a narrow port to Leduc Hold'em as a complexity check."
- **Now → Proposed:** (the quote above) → "Кун покер, за който глава 2 дава точно равновесие на Наш и точна експлоатируемост, и ограничено пренасяне към Ледюк Холдем като проверка при по-сложна игра."
- **Why:** The BG repeats "exact exploitability" and loses "exact Nash". "тесен порт" (a narrow harbour) is a calque of *narrow port*.

### F12-B22 · S1 · meaning — one-pager: "опорни системи", "извън линия заглушка", case errors
- **Where:** onePagerBg.md "**Подход.**" — "Сравнени са: nash-CFR, поведенческо клониране, Decision Transformer, ARDT и четири опорни системи за големи езикови модели (извън линия заглушка, gpt-oss-20b, Qwen2.5-7B, openThinker3-7B), както и последващи въпроси *защо* се получава тази класация."
- **EN:** "Compared: Nash-CFR, behavioural cloning, a Decision Transformer, ARDT, and four LLM backends (offline stub, gpt-oss-20b, Qwen2.5-7B, OpenThinker3-7B), plus follow-ons asking *why* that ranking falls out."
- **Now → Proposed:** (the quote above) → "Сравнени са: CFR (равновесие на Наш), поведенческо клониране, Decision Transformer, ARDT и четири варианта на агент с голям езиков модел (офлайн заглушка без езиков модел, gpt-oss-20b, Qwen2.5-7B, OpenThinker3-7B), както и допълнителни експерименти, които изясняват *защо* се получава тази класация."
- **Why:**
  - "опорни системи" (support systems) does not mean *backends*.
  - "извън линия заглушка" cannot be parsed.
  - "nash-CFR" and "openThinker3-7B" are pipeline case errors.
  - "въпроси" loses *follow-on experiments*.
  - The stub is not a language model (F12-C01), so the text should say so.

### F12-B23 · S1 · meaning — one-pager: "ангажирани JSON", "невъзможна разлика е намалена с +1.59"
- **Where:** onePagerBg.md "**Подход.**" — "**Всички числа по-долу са измерени** от ангажирани JSON файлове, с две уговорки: два резултата бяха **оттеглени** по средата на сесията (невъзможна разлика е намалена с `+1.59` и Ледюк `-0.83` от декодер, който изхвърля 70% от вероятностната маса), а референтният Наш е `0.0162` жетона при 5,000 итерации на CFR, но `0.0061` при 50,000 - и двете ~0."
- **EN:** "**All numbers below are measured** from committed JSON, with two caveats: two results were **retracted** mid-session (an impossible `+1.59` gap closed, and a Leduc `-0.83` from a decoder discarding 70% of the probability mass), and the Nash reference is `0.0162` chips at 5,000 CFR iterations but `0.0061` at 50,000 — both ~0."
- **Now → Proposed:** (the quote above) → "**Всички числа по-долу са измерени** и взети от JSON файлове, записани в хранилището, с две уговорки: два резултата бяха **оттеглени** по време на работата (невъзможна стойност `+1.59` на затворената част от разликата и резултат `-0.83` в Ледюк, получен от декодер, който отхвърля 70% от вероятностната маса), а експлоатируемостта на референтното равновесие е `0.0162` жетона при 5,000 итерации на CFR, но `0.0061` при 50,000 - и двете са ~0."
- **Why:**
  - "ангажирани" means "committed" in the sense of *obligated*; here *committed* is the git sense.
  - "невъзможна разлика е намалена с +1.59" says an impossible gap was *reduced by* 1.59 (T05). The number is a gap-closed *fraction* above 1.
  - "Ледюк -0.83 от декодер" has no noun.
  - The Nash reference *has* exploitability 0.0162; it *is* not 0.0162.

### F12-B24 · S1 · meaning — one-pager: "3 ПАС / 2 НЕУСПЕХ, честно червено"
- **Where:** onePagerBg.md "Ключови резултати (измерени)", last bullet — "Резултат: **3 ПАС / 2 НЕУСПЕХ**, честно червено."
- **EN:** "Harness: **3 PASS / 2 FAIL**, honestly red."
- **Now → Proposed:** "Резултат: **3 ПАС / 2 НЕУСПЕХ**, честно червено." → "Проверки: **3 успешни / 2 неуспешни**; неуспешните са оставени като такива."
- **Why:** In this chapter "пас" is the poker action, so "3 ПАС" reads as three passes. "честно червено" (honestly red) means nothing in Bulgarian.

### F12-B25 · S1 · meaning — one-pager bullet "Експлоатативен…": "добре овластен модел", "намалена с +0.38"
- **Where:** onePagerBg.md — "- *Експлоатативен по подразбиране, а не адаптивен.* Средната разлика е намалена с **+0.38**, но средното обучение е **-0.22**: срещу единствения добре овластен модел на противника моделът улавя **83%** от наличната експлоатация от първата половина нататък и никога не се подобрява. Той експлоатира **61% по-силно от Наш, като същевременно е 59 пъти по-експлоатируем**, и само срещу пасивни опоненти."
- **EN:** "Mean gap closed **+0.38** but mean **learning -0.22**: against the one well-powered opponent the model captures **83%** of available exploitation from the first half onward and never improves. It exploits **61% harder than Nash while being 59x more exploitable**, and only against passive opponents."
- **Now → Proposed:** (the quote above) → "- *Експлоатиращ по подразбиране, но не адаптивен.* Срещу единствения противник, при който експериментът има достатъчна статистическа мощност („Винаги пас“), моделът (Qwen2.5-7B, 120 раздавания) още от първата половина на сесията улавя **83%** от наличната експлоатация и не се подобрява; при другите два противника грешката е ±0.53–0.80. Срещу набора от ботове той печели **0.177 жетона на раздаване срещу 0.110 за равновесието** при експлоатируемост 0.357 срещу 0.006, като близо 90% от предимството идва от пасивния и случайния противник."
- **Why:**
  - "добре овластен модел на противника" means an *empowered model*; *well-powered* is about statistical power, and it refers to the opponent, not a model.
  - "намалена с +0.38": T05.
  - "Експлоатативен" is not a Bulgarian word.
  - The content changes (the noise-driven mean, the ratio to a near-zero denominator, "only against passive") are argued in F12-C04 and F12-C05.

### F12-B26 · S2 · calque — one-pager: "половинчато опровергано", "накараха … да изчезне"
- **Where:** onePagerBg.md — "Обяснението за Кун (набор печалби с 4 стойности) беше **половинчато опровергано** на Ледюк: 15 стойности на печалбата накараха предвидения артефакт да изчезне, но насочването все още не се появи (`r = +0.062`)."
- **EN:** "The Kuhn explanation (a 4-value payoff alphabet) was **half-refuted** on Leduc: 15 payoff values made the predicted artefact vanish, but steering still failed to appear"
- **Now → Proposed:** (the quote above) → "Обяснението за Кун (само 4 възможни стойности на печалбата) беше **наполовина опровергано** в Ледюк: при 15 стойности предвиденият артефакт изчезна, но насочване пак не се появи (`r = +0.062`)."
- **Why:** "половинчато" means half-hearted, not half. "накараха … да изчезне" is a calque of *made … vanish*. The game takes "в Ледюк", not "на Ледюк".

### F12-B27 · S2 · meaning — one-pager: "не може да я извади", "изказаните/играните"
- **Where:** onePagerBg.md — "Хипотезата преди това беше „знае правилната честота, не може да я извади“; данните казват обратното. Оценени като стратегии, *изказаните* честоти са много по-лоши от *играните*"
- **EN:** "The hypothesis going in was "knows the right frequency, cannot sample it"; the data says the reverse. Scored as strategies, *stated* frequencies are far worse than *played* ones"
- **Now → Proposed:** (the quote above) → "Изходната хипотеза беше „моделът знае правилната честота, но не може да я възпроизведе при избора на действие“; данните показват обратното. Оценени като стратегии, *заявените* честоти са много по-лоши от *изиграните*"
- **Why:** "не може да я извади" (cannot pull it out) does not mean *cannot sample it*. The summary uses "заявени/изиграни", not "изказани/играни".

### F12-B28 · S2 · meaning — one-pager "Връзка с дисертацията": inverted agency
- **Where:** onePagerBg.md — "Първият принос дава отрицателен резултат, който е ценен: поведенческата адаптация *липсва* в контекста, поради което трябва да се изгради експлицитен модел на противника, вместо да се приема за даденост. Вторият принос определя границата, измерена върху един график - 61% повече експлоатация при 59 пъти по-голяма експлоатируемост, но само срещу слаби опоненти. Третият принос осигурява разлагане по решения и протокол за измерване."
- **EN:** "Contribution #1 gets a negative result worth having … Contribution #2 gets its frontier measured on one plot … Contribution #3 gets the per-decision decomposition and the measurement protocol."
- **Now → Proposed:** (the quote above) → "За първия принос се получава ценен отрицателен резултат: адаптация само от историята в контекста не се появява, затова моделът на противника трябва да се изгради изрично, а не да се предполага, че ще възникне сам. За втория принос компромисът е измерен в една графика: повече експлоатация (0.177 срещу 0.110 жетона на раздаване) при много по-висока експлоатируемост (0.357 срещу 0.006), и то главно срещу слаби противници. За третия принос главата дава разлагането по решения и протокола за измерване."
- **Why:** The BG makes each contribution the agent ("gives", "determines", "provides"). In the EN, each contribution *receives* something from this chapter. For the 59× ratio, see F12-C05.

### F12-B29 · S2 · calque/overclaim — one-pager "Отворени въпроси"
- **Where:** onePagerBg.md — "Назованото поправяне е `Q(s,a)` на ARDT: оценител на връщането, зависим единствено от състоянието, не може да различи „това състояние е лошо“ от „*това действие* е лошо“, поради което τ обхождането противоречи на теорията"
- **EN:** "The named fix is ARDT's `Q(s,a)`: a state-only return estimator cannot tell "this state is bad" from "*this action* is bad", which is why the tau sweep contradicts theory"
- **Now → Proposed:** (the quote above) → "Най-вероятното решение е `Q(s,a)` на ARDT (още непроверено): оценител на възвръщаемостта, който зависи само от състоянието, не може да различи „това състояние е лошо“ от „*това действие* е лошо“ - вероятно затова серията експерименти по τ противоречи на теорията"
- **Why:** "Назованото поправяне" is a calque. "τ обхождането" repeats *sweep* → "обхождане" (F07-T09). "връщане": T01. The fix is untested (F12-C08).

### F12-B30 · S2 · terminology — *self-play* as "самообучение" (T03)
- **Where:** onePagerBg.md "**Проблем.**" — "без функция на стойността и без самообучение"; the summary occurrence is in F12-B02.
- **EN:** "no value function, no self-play"
- **Now → Proposed:** "без функция на стойността и без самообучение" → "без функция на стойността и без самоигра"
- **Why:** "самообучение" means self-study or self-learning, a different notion (T03).

## T — Glossary-level terminology

### F12-T01 · S1 · "return conditioning → условно връщане" (freq 10); "conditioning on an outcome → условност върху изход"
- **Where:** `llmPipeline/glossary_settled.md`. Also 'adversarially robust return conditioning → условно връщане с устойчивост…' and the figure mapping 'DT: exploitability vs return conditioning' → '…срещу условно връщане'. Printed in step 12 §§ 12.2–12.4, 12.7 and the one-pager (F12-B04).
- **Now → Proposed:** return conditioning → "обуславяне по възвръщаемостта"; conditioning on an outcome → "обуславяне по изхода"; return-conditioned → "обусловен по възвръщаемостта"; conditioning target → "целева стойност за обуславяне".
- **Why:** "условно връщане" reads as a conditional refund, so the chapter's central term means nothing to a Bulgarian reader. The glossary contradicts itself: it already has "return-to-go conditioning → обуславяне по остатъчна възвръщаемост" and "minimax return conditioning → минимаксно обуславяне по възвръщаемост".

### F12-T02 · S1 · "return-to-go → очаквана възвръщаемост до края" (freq 4)
- **Where:** glossary_settled.md; also "minimax return-to-go → минимакс очаквана възвръщаемост до края", "minimax return → минимакс доходност", while "returns-to-go → остатъчна възвръщаемост" (F12-B05, B10).
- **Now → Proposed:** return-to-go → "остатъчна възвръщаемост"; minimax return-to-go → "минимаксна остатъчна възвръщаемост"; minimax return → "минимаксна възвръщаемост".
- **Why:** The return-to-go is the *realised* sum of future rewards, and "очаквана" (expected) inverts the Paster argument. The glossary already holds the right form, "остатъчна", in two entries.

### F12-T03 · S2 · "self-play → самообучение" (freq 43)
- **Where:** glossary_settled.md: "self-play → самообучение", "self-play loop → цикъл на самообучение", "self-play training → обучение чрез самообучение", but "self-play-trained → обучен чрез самоигра", "self-play reinforcement learning → обучение чрез самоигра".
- **Now → Proposed:** self-play → "самоигра" (on first use „игра срещу копие на самия себе си“); self-play loop → "цикъл на самоигра".
- **Why:** "самообучение" is self-study, and "обучение чрез самообучение" is a tautology. With frequency 43, this reaches many chapters.

### F12-T04 · S2 · "sequence models → последователни модели" (freq 5)
- **Now → Proposed:** → "модели на последователности" (the glossary already has "sequence modeling → моделиране на последователности").
- **Why:** "последователен" means consistent or successive. The error reaches the chapter title in the TOC (F12-B19).

### F12-T05 · S2 · "gap closed → разликата е намалена"
- **Now → Proposed:** as a metric, → "затворена част от разликата" (the share of the equilibrium-to-best-response gap that is captured).
- **Why:** The metric is a fraction, not an amount by which something was reduced. The entry produced "невъзможна разлика е намалена с +1.59" and "Средната разлика е намалена с +0.38" (F12-B23, B25).

### F12-T06 · S2 · "offline → извън линия"
- **Now → Proposed:** → "офлайн" (as in the settled "offline data → офлайн данни", "offline phase → офлайн фаза"), or "върху предварително записани данни".
- **Why:** "извън линия" is a calque of *off-line* and is not used in Bulgarian ML writing (F12-B02, B22).

### F12-T07 · S2 · poker table terms: "checking → проверка", "street → улица", "high board → висока маса", "board texture → текстура на дъската"
- **Now → Proposed:** checking → "чек (пропускане на хода без залог)"; street → "рунд на залагане" (already the entry for "betting street"); high board → "висока обща карта"; board texture → "състав на общите карти".
- **Why:** "проверка" means verification. The pilot found the same for "проверява" (F07-B26), and here it garbles the Leduc finding (F12-B17). "маса" is the card table and "дъска" a board. With "fold → пас" also settled, "пасува, когато проверката е безплатна" cannot be read at all.

### F12-T08 · S2 · Decision Transformer / ARDT names disagree between the two glossaries
- **Where:** curated `terminology_EN_BG.md`: "Decision Transformer → Трансформатор за решения", "ARDT → Устойчив на противник трансформатор за решения". Settled: "decision transformer → трансформър за вземане на решения" (13), "adversarially robust decision transformer → устойчив на противникови атаки трансформър…". The chapter also has "трансфърмъра" and "Decision Transformer".
- **Now → Proposed:** Treat both as system names and keep them in Latin ("Decision Transformer (DT)", "ARDT"), per the brief's rule for system names. Give a gloss on first use: „трансформър за вземане на решения“; for ARDT, „Decision Transformer, устойчив спрямо най-лошия противник“.
- **Why:** "трансформатор" is the electrical device. "противникови атаки" suggests adversarial perturbation attacks, whereas ARDT is robust to a worst-case *opponent policy*.

### F12-T09 · S3 · "greedy decoding → алчен избор на последователност"
- **Now → Proposed:** → "алчно декодиране (избор на най-вероятния токен на всяка стъпка)"
- **Why:** Greedy decoding works token by token (F12-B18).

### F12-T10 · S3 · "supervised sequence modelling → супервизирано моделиране на последователности"
- **Now → Proposed:** → "моделиране на последователности чрез обучение с учител"
- **Why:** The glossary itself has "supervised learning → обучение с учител", and "супервизирано" is a calque (F12-B07).

### F12-T11 · S2 · relabel pair: "relabel target → цел за преозначаване", "relabeling → преетикетиране"
- **Now → Proposed:** one verb for both: relabeling → "преетикетиране"; relabel target → "целева стойност при преетикетирането".
- **Why:** One operation gets two words within the same section (F12-B10, figure mapping F12-G03).

## C — Content

### F12-C01 · S1 · One-pager headline: "LLM 0.833" is the scripted stub, not a language model
- **Where:** onePagerBg.md first bullet (two lines): "- *Двата номинални обекта на стъпката завършват последни.* **BC 0.055 << ARDT 0.469 < DT 0.799 < LLM" / "  0.833**, спрямо Наш **0.0162**. Клонирането достига до 0.04 жетона от Наш чрез копиране на почти равновесие на Наш стратегия, докато DT прекарва същата стратегия през канал за условно връщане, носещ предимно късмет - условното връщане тук активно унищожава информация."; onePager.md l. 33–36.
- **Problem:** The 0.833 row in `results/comparison_SMOKE_stub.json` has `"backend": "scripted-reasoner(offline-stub)"`, a scripted placeholder. The real models score 0.25–0.33 (report table: gpt-oss-20b 0.250–0.332, Qwen2.5-7B 0.303–0.318, OpenThinker3-7B 0.288). That ranks them *ahead* of ARDT and DT, so "the two nominal subjects finish last" is true only for the DT. "стъпката" is stale naming, and "почти равновесие на Наш стратегия" is ungrammatical. Separately, the DT row varies between retrains (0.671 → 0.799, report "Training variance").
- **Now → Proposed:** the two BG lines → "- *Обикновеното клониране бие DT и ARDT.* **BC 0.055 < ARDT 0.469 < DT 0.799** спрямо равновесие **0.0162**; реалните езикови модели са между **0.25 и 0.33** (заглушката без езиков модел: 0.833). Клонирането остава на 0.04 жетона от равновесието, като копира почти равновесна стратегия, докато DT прекарва същата стратегия през обуславяне по възвръщаемостта, която носи предимно късмет - тук обуславянето активно унищожава информация." EN l. 33–36 → "- *Plain cloning beats DT and ARDT.* **BC 0.055 < ARDT 0.469 < DT 0.799** against Nash **0.0162**; the real LLMs score **0.25–0.33** (the scripted offline stub: 0.833). Cloning lands within 0.04 chips of Nash by copying a near-Nash policy, while the DT routes that same policy through a return-conditioning channel carrying mostly luck — conditioning actively destroys information here."

### F12-C02 · S1 · The Kuhn "collapse" is a spike in exploitability; the BG says "спад" (a drop)
- **Where:** summaryBg.md § 12.4 — "Резултатът е, че условното връщане **променя** стратегията съществено, но не я **насочва**: експлоатируемостта остава непроменена в диапазона на реалните **добити цели**, с рязък спад при една конкретна стойност - модалната печалба, която в Кун е печалбата от **пас**."; summaryEn.md l. 84–85 "exploitability is flat across the range of real target returns, with a sharp / collapse at one specific value"; report_bg l. 76 "със силен спад".
- **Problem:** The subject of the sentence is exploitability, and at R = −1 it *rises*: 1.85 chips vs 0.75–0.82 at the other targets (`results/dt_experiments_SMOKE.json`), and 1.98 in the report's fine sweep. The DT's play collapses; its exploitability spikes. The EN "collapse" is ambiguous. The BG "рязък спад" (sharp drop) states the opposite: that the DT is *best* at the modal payoff. "добити цели" (mined/obtained goals) does not mean *real target returns*.
- **Now → Proposed:** (the quote above) → "Резултатът е, че обуславянето по възвръщаемостта **променя** стратегията съществено, но не я **насочва**: експлоатируемостта остава почти една и съща в целия диапазон на реално постижимите целеви стойности, с изключение на рязък скок (до ≈ 1.9 жетона) при една конкретна стойност - най-честата печалба, която в Кун е печалбата при пас." EN l. 84–85: "with a sharp collapse at one specific value" → "except for a sharp spike (to ≈ 1.9 chips) at one specific value". The later "Сривът"/"collapse" can stay, because it refers to the *play*.

### F12-C03 · S2 · "Equilibrium mixes at 0.68" and "none bluffs the Jack": Kuhn has a family of equilibria
- **Where:** summaryBg.md § 12.5 — "Всеки тестван бекенд залага със стойност краля с вероятност 1.00, докато равновесието изисква смесване при 0.68, и никой не блъфира с валето изобщо при обикновена подкана."; summaryEn.md l. 110–112; onePagerBg.md "докато залагането за стойност на „Поп“ при 1.00, където Наш смесва при 0.68, струва **0.1%**"; onePager.md l. 55.
- **Problem:**
  1. The first player's equilibria in Kuhn form a one-parameter family: bluff the Jack with α ∈ [0, 1/3] and bet the King with 3α (Kuhn 1950; see F12-S01). Betting the King at 1.00 (α = 1/3) and never bluffing (α = 0) are *each* equilibrium actions; only the combination is not. So the equilibrium does not "require 0.68": 0.68 is the member CFR reached at 5,000 iterations. The 50,000-iteration CFR used for figs. 74–75 bets the King at 0.56 (`p_bet_nash["3"] = 0.5606` in the decomposition and elicitation JSON). The "deviation from Nash" axis of fig. 74 is therefore measured against one member of the family, and this is also why the King "failure" costs only 0.1 %.
  2. "None bluffs the Jack at all" holds for the sampled comparison (24 samples, T = 0.7). The logprob-extracted strategy of gpt-oss-20b bluffs at 0.13 (`frequency_elicitation_openai_gpt-oss-20b.json`, `executed["1"] = 0.132`), which is visible in fig. 75.
  3. "Every backend" includes the stub, which bluffs at 1.00.
  4. Language: "бекенд" is an anglicism, "залага със стойност" a calque, and the King is "поп".
- **Now → Proposed:** (the summaryBg quote) → "Всеки от тестваните реални модели залага за стойност с поп с вероятност 1.00, докато изчисленото с CFR равновесие смесва с 0.68, и при обикновена подкана нито един не блъфира с вале в извадка от 24 опита на информационно множество. (В Кун равновесията на първия играч образуват еднопараметрично семейство - блъф с вале с вероятност α ∈ [0, 1/3] и залог с поп с вероятност 3α,[^kuhn1950] така че поотделно и двете поведения са равновесни; неравновесна е само комбинацията им.)"; onePagerBg "където Наш смесва при 0.68" → "където изчисленото равновесие смесва с 0.68". EN l. 110–112: "Every backend tested value-bets the King with probability 1.00 where equilibrium mixes at 0.68, and none bluffs the Jack at all under a plain prompt." → "Every real model tested value-bets the King with probability 1.00 where the CFR equilibrium mixes at 0.68, and none bluffs the Jack under a plain prompt in 24 samples per information set. (Kuhn's first-player equilibria form a one-parameter family — bluff the Jack with α ∈ [0, 1/3], bet the King with 3α — so each behaviour alone is an equilibrium action; only the combination is not.)"; onePager.md l. 55 "where Nash mixes at 0.68" → "where the CFR equilibrium mixes at 0.68".

### F12-C04 · S2 · "In-context adaptation did not emerge" is broader than the evidence, which also contains the opposite result
- **Where:** summaryBg.md § 12.6 second paragraph ("Като се има предвид наблюдаемата история на една сесия в контекст, моделът **не** се адаптира: той улавя 83% от наличната експлоатация срещу тривиално пасивен противник още от първата половина на сесията и не показва никакво подобрение (средно обучение $-0.22$). Това, което изглежда като моделиране на противника, всъщност е фиксирано предварително убеждение, благоприятстващо разпуснат-агресивни стратегии.") and the takeaway "- **Адаптация към съперника в контекста не се появява**, така че е необходим експлицитен модел на противника, а не да се приема за даденост - пряко свързано с първия принос на дисертацията."; summaryEn.md l. 142–145, 168–169; one-pager (F12-B25, B28).
- **Problem:**
  1. The evidence is one model (Qwen2.5-7B-Instruct, CoT prompt), 120 hands per opponent, only the last **20** hands in context (`context_hands: 20`), and three opponents, of which only AlwaysPass is conclusive (gap closed 0.826 ± 0.075; first half 0.824, second half 0.827) (`results/opponent_modeling_qwen2.5-7b-instruct.json`).
  2. "Mean learning −0.22" averages in the two underpowered cells (AlwaysBet −0.52 with gap-closed SE ±0.80; TightPassive −0.15, ±0.53), so it is noise.
  3. The same models *do* change their play when *told* the opponent type. The bluff rate against a folder minus the rate against a calling station (`adaptation_delta`, `evaluation.py`) is +0.67 / +0.79 / +0.25 for gpt-oss-20b, +0.00 / +0.42 / +0.21 for Qwen2.5-7B and +0.92 for OpenThinker3-7B (comparison JSON files). What is missing is *inference from history*, not responsiveness. That is a sharper conclusion for C1: an explicit model whose output is handed to the policy.
  4. Published work shows adaptation with frontier models and scaffolding: a prompted GPT-4 agent (Guo et al. 2023) and memory-equipped agents (Lin & Hou 2026) (F12-S04).
- **Now → Proposed:**
  - § 12.6 paragraph → "Когато историята на сесията (последните 20 раздавания) е подадена в контекста, моделът (Qwen2.5-7B-Instruct) **не** се адаптира: срещу тривиално пасивен противник той улавя 83% от наличната експлоатация още в първата половина на сесията и не се подобрява във втората (0.824 срещу 0.827); при другите два противника резултатът не е статистически надежден. Това, което изглежда като моделиране на противника, всъщност е фиксирано предварително убеждение, благоприятстващо разпуснато-агресивна игра. Когато обаче типът на противника е *описан* в подканата, моделите променят честотата на блъфиране с до 0.92 - липсва изводът от историята, а не способността да се реагира на описание."
  - takeaway → "- **Моделът не изведе противника от историята в контекста** (един модел със 7 млрд. параметъра, прозорец от 20 раздавания), но реагира, когато типът на противника му е съобщен; затова моделът на противника трябва да се изгради изрично и резултатът му да се подава на стратегията - пряко свързано с първия принос на дисертацията."
  - EN l. 142–145 → "Given the last 20 hands of the session in context, the model (Qwen2.5-7B-Instruct) does **not** adapt: against a trivially passive opponent it captures 83% of the available exploitation in the first half and no more in the second (0.824 vs 0.827); the other two opponents are underpowered. What looks like opponent modelling is a fixed loose-aggressive prior. Told the opponent's type in the prompt, however, the models shift their bluffing by up to 0.92 — what is missing is inference from history, not responsiveness to a description."
  - EN l. 168–169 → "- **The model did not infer its opponent from in-context history** (one 7B model, a 20-hand window) but did respond when told the opponent's type, so the opponent model must be built explicitly and its output passed to the policy — directly relevant to the first thesis contribution."

### F12-C05 · S2 · "The entire gain comes from passive and random opponents" is false by fig. 76; "59×" has a near-zero denominator
- **Where:** summaryBg.md § 12.6 — "езиковият модел **експлоатира с 61% по-силно от равновесната игра, като същевременно е 59 пъти по-експлоатируем** - но цялата печалба идва от пасивни и случайни противници."; summaryEn.md l. 137–138; one-pager (F12-B25, B28) and onePager.md l. 47–48, 60–61.
- **Problem:**
  1. From `results/exploitation_qwen2.5-7b-instruct.json` (LLM minus Nash, chips per hand): AlwaysPass +0.206, AlwaysBet +0.062, TightPassive −0.041, LooseAggressive +0.036, Thresholdish −0.008, Random +0.148. AlwaysPass and Random give 0.354 of the net 0.402 (88 %); the aggressive bots also contribute.
  2. 59× is 0.357 / 0.0061, where the denominator is CFR's residual at 50,000 iterations. At 5,000 iterations (0.0162) the same ratio is 22×, so the ratio measures CFR convergence, not the model. State absolute values.
  3. "The LLM" is Qwen2.5-7B-Instruct playing a *fixed* strategy extracted with 12 model calls. This is its default policy, not adaptive play (one seed, 4,000 hands per bot).
- **Now → Proposed:** (the BG quote) → "езиковият модел (Qwen2.5-7B-Instruct) **печели средно 0.177 жетона на раздаване срещу 0.110 за равновесната игра (с 61% повече), но експлоатируемостта му е 0.357 жетона срещу 0.006** - и близо 90% от предимството идва от пасивния и случайния противник." EN l. 136–138 → "…the language model (Qwen2.5-7B-Instruct) **wins 0.177 chips per hand against 0.110 for equilibrium play (61% more), while its exploitability is 0.357 chips against 0.006** — and nearly 90% of the advantage comes from the passive and random opponents." onePager.md l. 47–48: "It exploits **61% harder than Nash while being 59x more / exploitable**, and only against passive opponents." → "It wins **61% more than Nash (0.177 vs 0.110 chips/hand) at an exploitability of 0.357 vs 0.006 chips**, mostly against passive and random opponents."; l. 60–61 "61% more exploitation for 59x the / exploitability, only against weak opposition" → "61% more exploitation at 0.357 vs 0.006 chips of exploitability, mostly against weak opposition".

### F12-C06 · S2 · "Scale is irrelevant" / "A 7B model matches a 20B model": gpt-oss-20b has 3.6B active parameters
- **Where:** summaryBg.md § 12.5 — "Модел от 7B съвпада с модел от 20B, защото играта възнаграждава правилното смесване, а не знанието или мащаба."; summaryEn.md l. 112–113; onePagerBg.md bullet 5 (full line starting "- *Мащабът е без значение, а предимството на големите езикови модели принадлежи на Кун.*"); onePager.md l. 49–53.
- **Problem:** gpt-oss-20b is a mixture-of-experts model with 21B total but **3.6B active** parameters per token, released in MXFP4 (Hugging Face model card; OpenAI model card, arXiv:2508.10925). Qwen2.5-7B is dense. In compute per token, the "7B" is the larger model, and the two also differ in training (a reasoning model vs an instruct model). Three models on one toy game support no statement about scale. The same bullet's Leduc claim is corrected in F12-C07. Language: "Модел от 7B съвпада" (coincides), "принадлежи на Кун", "незаконни" (glossary: недопустими), "пас, когато проверката е безплатна" (T07).
- **Now → Proposed:**
  - summaryBg quote → "Модел със 7 млрд. параметъра (Qwen2.5-7B) се представя наравно с gpt-oss-20b - модел със смес от експерти с 21 млрд. параметъра общо, но само 3.6 млрд. активни при всеки токен; при три модела и една опростена игра това не позволява извод за ролята на мащаба."
  - onePagerBg bullet 5 (whole line) → "- *Размерът на модела не обяснява класацията, а предимството на езиковите модели важи само за Кун.* **Qwen2.5-7B побеждава gpt-oss-20b (3.6 млрд. активни параметъра) с +0.162 жетона на раздаване** при 20 хил. раздавания на двойка, строго транзитивно. В Ледюк големият езиков модел е неразличим от DT (`-0.463` срещу `-0.454`) и губи средно срещу слабите противници (`-0.071` при `+0.582` за равновесието; печели само срещу двата пасивни типа), като **100%** от вероятностната маса за недопустими действия се дължи на едно-единствено погрешно схващане: отказ от ръката, когато чекът е безплатен."
  - EN l. 112–113 "A 7B model matches a 20B model, because the game rewards correct mixing rather than knowledge or scale." → "A 7B model (Qwen2.5-7B) matches gpt-oss-20b — a mixture-of-experts model with 21B total but only 3.6B active parameters per token — so three models on one toy game say nothing general about scale."
  - onePager.md l. 49: "*Scale is irrelevant, and the LLM edge belongs to Kuhn.*" → "*Model size does not explain the ranking, and the LLM edge belongs to Kuhn.*"; "gpt-oss-20B by +0.162" → "gpt-oss-20b (3.6B active parameters) by +0.162".

### F12-C07 · S2 · Leduc: "the collapse disappears" next to a figure with two new dips; "cannot beat weak opponents at all"
- **Where:** summaryBg.md § 12.4 — "**Сривът изчезва точно както предвижда обяснението - и насочването все още не се наблюдава** (Пирсън $r = +0.062$)."; summaryEn.md l. 94–95, l. 150 "cannot beat weak opponents at all,"; onePager.md l. 51 (the BG one-pager and summary are covered by F12-C06 and F12-B17).
- **Problem:**
  1. At the modal return (−1, 20.1 % of steps) the DT is 0.18 SE from the other targets (`results/leduc_stage0.json`, `modal_gap_se`), so the Kuhn notch indeed does not reproduce. But fig. 73 shows two sharp dips that the text never mentions: at 0 (−0.80 ± 0.07; 17.4 % of steps, the second most common return) and at −5 (−0.88 ± 0.06), both deeper than the modal point (−0.45 ± 0.02). A reader sees two collapses next to "the collapse disappears". The dip at 0 may be the same mechanism, shifted to the second most common return.
  2. "Cannot beat weak opponents at all": in `results/leduc_llm_qwen2.5-7b-instruct.json` the model beats CallingStation (+0.31 ± 0.14) and LoosePassive (+0.22 ± 0.16). It loses on average (−0.071 vs +0.582 for Nash).
- **Now → Proposed:** (the BG quote) → "**Спадът при най-честата възвръщаемост изчезва, както предвижда обяснението, но насочване пак не се наблюдава** (Пирсън $r = +0.062$); остават обаче два необяснени спада - при 0 (втората по честота възвръщаемост) и при $-5$." EN l. 94–95 correspondingly: "**The notch at the modal return disappears as the explanation predicts — but steering still does not appear** (Pearson $r = +0.062$); two unexplained dips remain, at 0 (the second most common return) and at $-5$." EN l. 150: "cannot beat weak opponents at all," → "loses on average to weak opponents (winning only against the two passive types),"; onePager.md l. 51 "and cannot beat weak opponents at all" → "and loses on average to weak opponents".

### F12-C08 · S2 · The ARDT fix is untested, and ARDT's target is exact only for deterministic transitions
- **Where:**
  - summaryBg.md § 12.3, last paragraph: "Измерена върху **Кун** с умишлено опростен заместител, отчитащ само състоянието, целта за преозначаване се изменя монотонно с $\tau$, както изисква теорията - но експлоатируемостта е *най-ниска* от оптимистичната страна, което е белегът на липсващия аргумент на **действието**, а не доказателство срещу **ARDT**.[^tang2024]"
  - takeaway 1: "- **Обуславянето на величина, която агентът не контролира, не може да го насочва.** Демонстрирано в две игри; това е причината преетикетирането на ARDT - а не самият трансформър за вземане на решения - да се прехвърля към фиксирани покер логове."
  - takeaway 2: "- **Публикуваният ARDT преетикетира със стойност на състояние-действие.** Възпроизвеждането на ползата от метода изисква $\tilde{Q}(s,a)$, а не $V(s)$ - идентифицираното и подкрепено с доказателства решение за Глава 13."
  - summaryEn.md l. 76–78, 159–163.
- **Problem:**
  1. The V(s)-vs-Q̃(s,a) explanation is a hypothesis. No Q̃ variant was run, and the report itself says "Targets #3–4 test the proxy, not ARDT" (Limitations 2). "the signature of" and "evidence-backed fix" overstate it.
  2. ARDT's minimax target equals the true worst-case return only when transitions are deterministic. ARDT's first author's follow-up says so explicitly (F12-S06). Poker has chance nodes (the deal; the Leduc board card), so ARDT's relabelled target still carries card luck. It is not simply "controllable".
  3. "Demonstrated on two games" and "does not control": the effect was observed on two toy games with one small DT (SMOKE profile), and the agent partly controls the return. The general result is Paster et al.'s Theorem 2.1.
- **Now → Proposed:**
  - § 12.3 paragraph → "Измерена върху **Кун** с умишлено опростен заместител, който отчита само състоянието, целевата стойност при преетикетирането се изменя монотонно с $\tau$, както изисква теорията - но експлоатируемостта е *най-ниска* от оптимистичната страна. Най-вероятната причина е, че действието липсва като аргумент на оценката; вариант с $\tilde{Q}(s,a)$ още не е изпълнен, така че резултатът нито опровергава, нито потвърждава ARDT.[^tang2024]"
  - takeaway 1 → "- **Обуславянето по величина, която агентът контролира само отчасти, не насочва поведението му.** Наблюдавано е в две опростени игри и съответства на теорема 2.1 на Paster и др.; затова за записани покер партии по-обещаващо е преетикетирането на ARDT, а не самият DT - при условие че се отчетат и случайните ходове (раздаването на картите), при които минимаксната цел на ARDT вече не е точна.[^tang2025]"
  - takeaway 2 → "- **Публикуваният ARDT преетикетира със стойност на двойката състояние-действие.** Възпроизвеждането на ползата от метода най-вероятно изисква $\tilde{Q}(s,a)$, а не $V(s)$ - това е следващата стъпка, която още предстои да се провери."
  - EN l. 77–78: "which is the signature of the missing action argument rather than evidence against ARDT." → "The most likely cause is the missing action argument; a $\tilde{Q}(s,a)$ variant has not been run, so this neither refutes nor confirms ARDT."
  - EN l. 159–161 → "- **Conditioning on a quantity the agent only partly controls does not steer it.** Observed on two toy games and consistent with Paster et al.'s Theorem 2.1; it is why ARDT's relabeling, not the Decision Transformer itself, is the more promising route for recorded poker logs — provided chance events (the deal) are handled, where ARDT's minimax target is no longer exact."
  - EN l. 162–163 → "- **The published ARDT relabels with a state-action value.** Reproducing the method's benefit most likely requires $\tilde{Q}(s,a)$, not $V(s)$ — the next step, still to be tested."

### F12-C09 · S2 · Stale references to chapters 13–14 and "step" naming; the candidate's TOC comment is not applied
- **Where:** summaryEn.md l. 32 "Chapter 13's Playtech logs", l. 100 "carries into Chapter 13", l. 121 "the Chapter 14 evaluation framework", l. 163 "fix for Chapter 13", l. 64 "the raw step's claim"; summaryBg.md "Step 13" (F12-B02), "Глава 14" (F12-B15), "Глава 13" (F12-C08 takeaway 2 and the paragraph below), "в суровия текст" (F12-B11); onePagerBg/onePager "стъпката" / "The step's" (F12-C01).
- **Problem:** Chapters 13–15 were never written, and the Playtech-log chapter does not exist. The candidate's comment on the TOC (p. 2), "maybe its time to change all emntion of steps into chapters", is **not applied** here: "Step 13", "стъпката", "the raw step's", "The step's" remain.
- **Now → Proposed:**
  - summaryBg.md § 12.4: "Това е аргументът, който се пренася в Глава 13. При фиксирани логове трансформърът с обуславяне по връщането е неподходящият инструмент - и стойността на преетикетирането при ARDT се състои именно в това, че то заменя неконтролируема **цел на обуславяне** с контролируема." → "Това е основният извод на главата: при обучение върху записани партии DT, обусловен по възвръщаемостта, е неподходящ инструмент, а предимството на преетикетирането при ARDT е, че заменя целева стойност, която агентът не контролира, с такава, която зависи главно от собствените му действия."
  - EN l. 100–102 → "This is the chapter's main conclusion: on recorded logs, a return-conditioned Decision Transformer is the wrong instrument, and the value of ARDT's relabeling is that it replaces a conditioning target the agent does not control with one that depends mainly on its own actions."
  - EN l. 31–32 → "The appeal for this dissertation is that it works entirely **offline**, on a fixed dataset — the regime of recorded game logs, where self-play is unavailable."
  - EN l. 120–121 "…for reporting per-decision diagnostics rather than a single exploitability number in the Chapter 14 evaluation framework." → "…for reporting per-decision diagnostics rather than a single exploitability number."
  - EN l. 64–65 "(the raw step's claim that $\tau = 0.9$ is pessimistic is inverted)" → "(the chapter's original plan wrongly called $\tau = 0.9$ pessimistic)"
  - The other occurrences are fixed in F12-B02, B11, B15, C01 and C08.

### F12-C10 · S2 · The chapter never says which language models were tested, or that the numbers are the author's own runs
- **Where:** summaryBg.md / summaryEn.md §§ 12.5–12.6. "езиковият модел", "ЕМ", "бекенд" appear, but no model is named anywhere in the chapter. Only fig. 74's suptitle and fig. 75's panel titles name one.
- **Problem:** The results come from three local open-weight models (gpt-oss-20b; Qwen2.5-7B-Instruct; OpenThinker3-7B, an SFT of Qwen2.5-7B-Instruct), served by LM Studio 0.4.20 on an RTX 5090 at T = 0.7 (report header; `EXECUTION_NOTES.md`). Most of §§ 12.5–12.6 (decomposition, zoo, adaptation, Leduc) is Qwen2.5-7B-Instruct alone. A reader of "the language model exploits 61 % harder…" cannot tell that it is a 7B model, not a frontier system. The quantisation of the Qwen and OpenThinker weights is not recorded anywhere.
- **Now → Proposed:** after "Втората парадигма изцяло пропуска обучението: опишете правилата на английски и оставете езиков модел да играе." add: "Тествани са три модела с отворени тегла, изпълнявани локално (LM Studio 0.4.20, температура 0.7): gpt-oss-20b, Qwen2.5-7B-Instruct и OpenThinker3-7B (Qwen2.5-7B-Instruct, дообучен за разсъждения). Ако не е посочено друго, резултатите по-долу са за Qwen2.5-7B-Instruct; всички числа са от собствени измервания." EN (after l. 107 "…let a language model play."): "Three open-weight models were run locally (LM Studio 0.4.20, temperature 0.7): gpt-oss-20b, Qwen2.5-7B-Instruct and OpenThinker3-7B (a reasoning fine-tune of Qwen2.5-7B-Instruct). Unless stated otherwise, the results below are for Qwen2.5-7B-Instruct; all numbers are the author's own measurements." Record the GGUF quantisation in the report.

## S — Sources

### F12-S01 · S2 · SOURCE_GAPS row: "Kuhn's equilibrium and exploitability can be computed exactly" → cite Kuhn (1950) and chapter 2
- **Where:** summaryBg.md § 12.4 — "Равновесието и експлоатируемостта на **Кун покер** могат да бъдат изчислени точно, поради което въпросът може да бъде решен, а не само обсъждан."
- **Proposal (cite):** "…могат да бъдат изчислени точно, поради което…" → "…могат да бъдат изчислени точно (вж. глава 2),[^kuhn1950] поради което…". Footnote: `[^kuhn1950]: Kuhn, H. W. (1950). "A Simplified Two-Person Poker." In H. W. Kuhn & A. W. Tucker (Eds.), *Contributions to the Theory of Games*, Vol. I (Annals of Mathematics Studies 24), pp. 97–103. Princeton University Press. DOI 10.1515/9781400881727-010.`
- **How verified:** The Crossref record for the DOI gives the title, author H. W. Kuhn and container "Contributions to the Theory of Games (AM-24), Volume I"; Crossref lists 1951 and pp. 97–104 for the De Gruyter edition, while the 1950 Princeton printing is usually cited as pp. 97–103. The equilibrium family used in F12-C03 was checked against the Wikipedia summary of the paper, not the original. The exact exploitability is computed by exhaustive best response over the 12 information sets (chapter 2). The step-02 footnote with the same label drops the "A" from the title; fix it there too. Because footnote labels are shared across the bundle (F07-X01), this marker needs the central prefix fix.

### F12-S02 · S2 · ARDT footnote names the wrong co-authors
- **Where:** summaryBg.md / summaryEn.md footnote — "[^tang2024]: Tang, Zhang, Gu et al., *Adversarially Robust Decision Transformer*, NeurIPS 2024 (arXiv:2407.18414) - Section 3 и Algorithm 1."
- **Proposal (correct):** "Tang, Zhang, Gu et al.," → "Tang, X., Marques, A., Kamalaruban, P. & Bogunovic, I.," (in both files).
- **How verified:** The arXiv abstract page gives the authors and "NeurIPS 2024". HTML v2 confirms the chapter's statements: § 3 is titled "Adversarially Robust Decision Transformer"; Eq. 6 is the expectile loss; Eq. 7 gives the α → 0 min / α → 1 max limits; Algorithm 1 sets α = 0.01 on line 1 and relabels with Q̃ν(s_t, a_t); the two estimators are fitted alternately with α and 1 − α. No "Zhang" or "Gu" is an author. (The HTML numbers the relabel line 11; report_en says "line 7". Check the PDF before citing a line.)

### F12-S03 · S2 · TextArena footnote supports nothing in its sentence, and its title is wrong
- **Where:** summaryBg.md § 12.5 — "Поведенческото проучване тук не е просто по-удобно от самоанализа - то е по-точно.[^guertler2025]"; footnote "Guertler et al., *TextArena: A Framework for Text-Based Game Environments*, 2025 (arXiv:2504.11442)."
- **Problem:** TextArena is a collection of 57+ text games with a TrueSkill leaderboard. It says nothing about behavioural probing versus self-report. The sentence reports the chapter's own measurement. The arXiv title is just "TextArena". The step's `textarena_agent.py` is an optional bridge that produced no results.
- **Proposal (remove):** "то е по-точно.[^guertler2025]" → "то е по-точно (собствено измерване)." Delete the footnote, or, if TextArena should be cited at all, correct it to `Guertler, L., Cheng, B., Yu, S., Liu, B., Choshen, L. & Tan, C., *TextArena*, 2025 (arXiv:2504.11442).` and attach it to "Втората парадигма … да играе." as an example of text-game environments. Verified on the arXiv abstract page (v2, 24 May 2025).

### F12-S04 · S2 · The LLM section cites no prior work on LLM poker agents, although directly comparable studies exist
- **Where:** summaryBg.md §§ 12.5–12.6 (no source for the LLM claims except the misplaced TextArena note).
- **Problem:** Lin et al. (ICLR 2026) evaluate Qwen2.5-3B/7B/72B, Qwen3-8B, Llama3-8B, GPT-4.1-mini, GPT-4o and o4-mini on Kuhn, Leduc and Limit Hold'em against CFR+. They report that LLMs cannot approximate equilibrium strategies and show a "knowing-doing gap" in which actions diverge from stated reasoning. That is the same games, one of the same models, and a result that bears on "stated vs executed". Guo et al. (2023) show a prompted GPT-4 agent adapting its play to different opponents in Leduc, which bears on F12-C04. Without them, a reader cannot place the chapter's negative results.
- **Proposal (cite):** after the sentence added in F12-C10, add: "Сходни експерименти в Кун, Ледюк и Лимит Холдем показват, че и по-големи модели не се доближават до равновесна игра, а действията им често се разминават със заявените разсъждения[^lin2026]; подкана с изрично разсъждение за противника позволява на GPT-4 да адаптира играта си[^guo2023]." Footnotes: `[^lin2026]: Lin, M., Dai, E., Liu, H. et al., *How Far Are LLMs from Professional Poker Players? Revisiting Game-Theoretic Reasoning with Agentic Tool Use*, ICLR 2026 (arXiv:2602.00528).` and `[^guo2023]: Guo, J., Yang, B., Yoo, P., Lin, B. Y., Iwasawa, Y. & Matsuo, Y., *Suspicion-Agent: Playing Imperfect Information Games with Theory of Mind Aware GPT-4*, 2023 (arXiv:2309.17277).`
- **How verified:** arXiv abstract pages for both. The Lin et al. HTML v1 was checked for models, games, the CFR+ baseline and the knowing–doing gap; ICLR 2026 acceptance comes from the arXiv comment only. Guo et al. is arXiv only (v3, 2024).

### F12-S05 · S3 · Spot check: Chen 2021 and Paster 2022 are correct; Paster's own fix and the chapter's own example are not identified
- **Where:** footnotes `chen2021`, `paster2022`; summaryBg.md § 12.2.
- **Findings:**
  - `chen2021`: title, authors (Chen, Lu, Rajeswaran, Lee, Grover, Laskin, Abbeel, Srinivas, Mordatch) and arXiv:2106.01345 checked on the arXiv abstract page; the NeurIPS 2021 venue was not re-checked.
  - `paster2022`: correct. The v2 PDF prints "36th Conference on Neural Information Processing Systems (NeurIPS 2022)" on p. 1. Theorem 2.1 states that a goal is consistently achievable iff conditioning on it leaves the transition probabilities unchanged. The paper's illustration is a gambling environment (Fig. 1).
  - The one-step bandit and its "1.00 (measured)" come from the author's own simulation (`exploration/luck_vs_skill_coinflip.py`, n = 39,985), not from Paster et al.
  - Paster et al.'s remedy, ESPER (conditioning on cluster-average returns), is not mentioned, although it is the direct answer to "luck". ARDT answers the *adversary*.
- **Proposal (optional):** after "…елемент на случайност.[^paster2022]" add: "Paster и др. предлагат вместо това обуславяне по средната възвръщаемост на клъстери от сходни траектории (ESPER), която не зависи от случайността на средата." In the formula line (F12-B03), add "(собствена симулация)" after "(измерено)".

### F12-S06 · S2 · Missing source for ARDT's limitation under chance (supports F12-C08)
- **Proposal (cite):** new footnote for the rewritten takeaway 1 in F12-C08: `[^tang2025]: Tang, X., Cheng, Z. & Kumar, S., *Robust Adversarial Reinforcement Learning in Stochastic Games via Sequence Modeling*, Reliable ML Workshop @ NeurIPS 2025 (arXiv:2510.11877).`
- **How verified:** arXiv abstract (authors, workshop acceptance) and HTML. It says "Q^ARDT represents the accurate worst-case return only when the state transition function T is deterministic. This assumption hinders ARDT to generate robust policy in stochastic games." Its experiments are small synthetic stage games, and it is a workshop paper, so cite it for the limitation, not as an established fix.

## X — Structure

### F12-X01 · S3 · The one-pager's headline result (cloning beats DT and ARDT) is absent from the chapter
- **Where:** summaryBg.md § 12.4. Behavioural cloning is never mentioned in the chapter, although it leads the one-pager and the report, and it is the strongest evidence that "conditioning destroys information".
- **Fix:** after the first paragraph of § 12.4 add: "На същите данни обикновеното поведенческо клониране достига експлоатируемост 0.055 жетона - близо до равновесието (0.016) - срещу 0.799 за DT: обуславянето по възвръщаемостта активно унищожава информация (стойността за DT варира между повторни обучения, 0.67–0.80)." EN: "On the same data plain behavioural cloning reaches 0.055 chips of exploitability — close to Nash (0.016) — against 0.799 for the DT: return conditioning actively destroys information (the DT value varies between retrains, 0.67–0.80)."

### F12-X02 · S3 · Half-empty pages 219 and 221
- **Where:** bundle p. 219 (≈ 55 % blank) and p. 221 (≈ 45 % blank). Figs. 72 and 74 float to the next page at full width.
- **Fix:** Re-check after F12-G03–G05, whose shorter figures should fit. If the gaps remain, `{width=90%}` on figs. 72–73 keeps text at ≥ 8.7 pt (fs 10 × 0.99 × 0.9 and fs 10 × 0.866 × 1.0 respectively; apply it only to fig. 72 if fig. 73 is still tight).
