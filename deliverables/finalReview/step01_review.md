# Step 01 — final review

**Summary:** The chapter reads well and its theory sections are mostly accurate, but the part that carries its own results does not hold together. (1) Text, figures and data describe three different experiments. The printed Fig. 1 is a 100K-step SB3 DQN run with the RL Zoo's tuned hyperparameters (best rolling-100 222.4). The report and one-pager describe an earlier 750K-step "matched" run (293.9). The summary's "stays around 30" matches neither. Fig. 2 almost certainly plots the wrong custom PPO run: 730 episodes, best rolling-100 180.3, where the text reports 543 episodes and 202.2. The training logs the plots are built from are gitignored and missing, and the custom runs are unseeded, so neither figure can be regenerated as it stands (F01-C01, G02, G03). (2) Both figures print entirely in English, at 4.3–7.5 pt. (3) The Bulgarian text is fluent but still has meaning errors: "политика на работа" (on-policy), "отстъпена" (discounted), "почти случайна мода", "сходява". Six English terms are left in the text (Atari Games, TD learning, TD target, Partially Observable MDP, GAE Lambda, TRPO with no gloss). Several of these come from settled glossary entries (T). Of the candidate's 36 August comments, 29 are applied, 2 are partly applied (#37, #38) and 5 are not (#22, #33, #39, #43, #54; see F01-B01, B14, B23–B27). The history paragraph and the Shoham & Leyton-Brown footnote need source corrections (C04, S02).
**Counts:** S1 11 · S2 41 · S3 7   (by category: G 3 · B 29 · T 12 · C 8 · S 6 · X 1)

Conventions in this file: quotes are **raw markdown** from `summaryBg.md` / `onePagerBg.md` / `summaryEn.md` / `onePager.md` (including `**`, `*`, `$`), so read this file as source, not rendered. Proposals keep the chapter's current " - " dashes, decimal points and "17,176"-style thousands, because those are fixed centrally. Counts for this chapter: " - " as a dash 54 (summary) + 11 (one-pager); decimal points 13 + 14; comma thousands separators 3 + 3; bold spans 98 vs 49 in the EN summary and 28 vs 18 in the one-pager (≈ 59 pipeline-added). Page numbers are PDF pages of `allSummaries_bg.pdf`. The printed folio is one lower: the chapter runs PDF pp. 8–18, printed pp. 7–17. Printed sizes are matplotlib size × (17.6 cm print width ÷ saved image width). Body text is 10.9 pt, so the floor is ≈ 8.2 pt. **Shared footnote labels (F07-X01):** chapter 1 is the *first* definition of `[^shoham2008]` (also used by chapters 2, 7 and 8) and of `[^suttonbarto2018]` (also used by chapter 3). The bundle therefore prints chapter 1's text for all of them, which is why S02 and B27 matter beyond this chapter.

## G — Figures

### F01-G01 · S1 · Bulgarian captions for both figures
- **Where:** summaryBg.md, image alt text of figs. 1–2 (bundle pp. 17–18). They print as "Фигура 1: DQN comparison - Custom vs SB3" and "Фигура 2: PPO comparison - Custom vs SB3" (known corpus-wide defect).
- **Now → Proposed:**
  - "![DQN comparison - Custom vs SB3](dqn_comparison.png)" → "![DQN върху CartPole-v1: собствената реализация срещу SB3. Плъзгаща се средна на наградата за 100 епизода (оцветено - ± едно стандартно отклонение в прозореца); пунктирната линия е целта 475, вертикалната - краят на обучението на собствения агент.](dqn_comparison_bg.png)"
  - "![PPO comparison - Custom vs SB3](ppo_comparison.png)" → "![PPO върху LunarLander-v3: собствената реализация срещу SB3. Плъзгаща се средна на наградата за 100 епизода (оцветено - ± едно стандартно отклонение в прозореца); пунктирната линия е целта 200, вертикалната - краят на обучението на собствения агент.](ppo_comparison_bg.png)"
- **Fix:** replace the alt text. The `_bg.png` targets exist only after the fixes in G02/G03. Until then keep `dqn_comparison.png` / `ppo_comparison.png`. The captions assume the single-panel, window-100 layout proposed there. With two panels, add "Вляво - наградата във всеки епизод; вдясно - …". The EN alt text should get the same content.

### F01-G02 · S1 · Fig. 1 (DQN): all English, prints at 4.3–7.5 pt, footnote not produced by the committed code, cannot be re-rendered
- **Where:** `renders/ch01/p017_f1.png` (bundle p. 17) — caption "DQN comparison - Custom vs SB3"; source `implementation/step01/compare_sb3.py` → `deliverables/reports/step01/figures/dqn_comparison.png`, copied to `summary/`.
- **Problem:**
  1. Everything is English: the suptitle, "Raw Episode Rewards", "Rolling Average (window = 100 ep)", "Episode", "Reward", "Rolling Avg Reward (100 ep)", legends "Custom DQN / SB3 DQN / Target (475)", "Custom stopped (ep 1011)", and the footnote "SB3 DQN trained for 1,255 episodes total (100 K env steps); plot shows first 1,061 episodes." No `_bg.png` exists. The script reads TensorBoard logs from `implementation/step01/logs/`, which is gitignored and absent. `verify_reproducible.py` records exactly this: the re-render "came back with 50 episodes … and no Custom DQN curve".
  2. Legibility: the image is 1931 px at 150 dpi (12.9 in) and prints at 17.6 cm, so the scale is 0.538. Ticks, axis labels and legend 11 → 5.9 pt; panel titles 13 → 7.0 pt; suptitle 14 → 7.5 pt; the "Custom stopped" note and the footnote 8 → 4.3 pt. Effective ppi 279, so the image is sharp, just small.
  3. The printed footnote says "(100 K env steps)", but the committed script hard-codes `f"… (750 K env steps); plot shows first …"` (l. 304). The PNG came from an uncommitted edit, so a re-run would label the 100K run as 750K. Its content also contradicts the text (see F01-C01).
  4. The two side-by-side panels at 13 in wide leave half of p. 16 blank, because the figure floats to p. 17 (X01).
- **Fix:** `compare_sb3.py`:
  - (a) Data: replace the "most entries" heuristic in `read_last_tb_run` with an explicit run per algorithm, e.g. `DQN_RUN = "events.out.tfevents.<final run>"` (see G03 for why the heuristic fails). On first read, write our per-episode rewards and steps to `implementation/step01/custom_results_cache.json` (committed, like `sb3_results_cache.json`) and plot from the cache afterwards. Because the logs are gone and neither `dqn/train.py` nor `ppo/train.py` sets a seed, re-train once with a seed: add `"seed": 0` to both configs, and add `torch.manual_seed`, `np.random.seed` and `env.reset(seed=…)` on the first reset. Then update every number that changes (summary, one-pager, report EN/BG).
  - (b) The SB3 run follows the decision in C01. Make the footnote use `total_timesteps` instead of the literal "750 K", or drop the footnote and move the counts into the text.
  - (c) Layout: drop the raw-reward panel, which the text never refers to: `fig, ax = plt.subplots(figsize=(7.0, 3.4))`. No suptitle, since the caption carries it. In `figure_style()`: `font.size` 11 → 10.5, `axes.titlesize` 13 → 11. Replace the `ax1.text(… f"Custom\nstopped\n(ep {our_n})", fontsize=8 …)` note with a legend entry on the `axvline` (`label="Custom stopped"`). Remove `fig.text(…, fontsize=8, …)`. `savefig(dpi=150)` → `dpi=300`. Printed scale becomes ≈ 0.96, so 10.5 prints at ≈ 10 pt. If both panels stay, use `figsize=(8.4, 3.4)` with the same fonts, which prints at ≈ 8.5 pt.
  - (d) Mapping (`figure_labels.json`): 'Custom DQN' → 'Собствен DQN'; 'Custom PPO' → 'Собствен PPO' (T08); 'Rolling Average (window = 100 ep)' → 'Плъзгаща се средна (прозорец 100 епизода)' (the current 'плъзгаща средна (window = 100 ep)' leaves English and starts lower-case); 'Rolling Avg Reward (100 ep)' → 'Плъзгаща се средна награда (100 епизода)'; 'Target (475)' → 'Цел (475)', 'Target (200)' → 'Цел (200)'; 'Episode' → 'Епизод', 'Reward' → 'Награда' (the glossary gives them lower-case); 'Raw Episode Rewards' → 'Награда във всеки епизод'; 'DQN on CartPole-v1 — Custom vs SB3' → 'DQN върху CartPole-v1 - собствена реализация срещу SB3'; new key 'Custom stopped' → 'Край на обучението'. The runtime key 'Custom\nstopped\n(ep 0)' was captured without logs and cannot match. Remove it once the label no longer contains the episode number.
  - Then `python scripts/figures/render_bg_figures.py --only step01`, copy both PNG pairs from `figures/` to `summary/`, and rebuild.

### F01-G03 · S1 · Fig. 2 (PPO): plots the wrong custom run (730 episodes, peak 180.3) and a 50-episode window, contradicting the text; English; 4.3–7.5 pt
- **Where:** `renders/ch01/p018_f1.png` (bundle p. 18) — caption "PPO comparison - Custom vs SB3"; `compare_sb3.py` → `ppo_comparison.png`; the report's `final_metrics.png` uses the same data.
- **Problem:**
  1. The figure prints "Custom stopped (ep 730)", and the blue rolling average peaks at ≈ 200 around episode 310 and stays at 140–190 afterwards. The text says the custom PPO "crosses the 200 target around episode 543 (264K steps)" and early-stopped with Avg(100) = 202.2. The report and one-pager give a best rolling-100 of 203.6. `final_metrics.png`, built from the same data, prints **180.3**. That is the peak of Run 1 (`[64,64]`, 300K steps: "Peak avg 179.9, never crossing 200", which `ppo/train.py` only samples at rollout boundaries). The final run early-stopped at 264,192 steps, so it has fewer episodes than the 300K-step Run 1. In commit de7456b (6 Apr) `read_last_tb_run` changed from "most recent file" to "file with the most entries", which selects Run 1. I could not confirm this from the logs, which are absent, but the episode counts (730 vs 543) and 180.3 ≈ 179.9 leave little doubt.
  2. The right panel uses `window=50`, while the text, report and one-pager reason in rolling-100 terms.
  3. Same English and legibility problems as G02: scale 0.538; 11 → 5.9 pt; 13 → 7.0 pt; 14 → 7.5 pt; 8 → 4.3 pt. The mapping entry 'PPO on LunarLander-v3 — Custom vs SB3' → 'PPO на LunarLander-v3 — Custom срещу SB3' also leaves "Custom" in English.
- **Fix:** Apply G02 (a) to (d). In `plot_ppo_comparison`, set `window: int = 50` → `100`. Select the final run explicitly (or re-train with a seed, G02 a). Mapping: 'PPO on LunarLander-v3 — Custom vs SB3' → 'PPO върху LunarLander-v3 - собствена реализация срещу SB3'. After re-rendering, check the numbers against the text: crossing episode, 202.2, 203.6. Update `final_metrics.png` and the report table (§4.3) from the same cache.

## B — Bulgarian language

### F01-B01 · S1 · English left in the text (incl. comment #38 not applied)
- **Where:** summaryBg.md §§ 1.1, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9
- **EN:** "learned to play Atari games from raw pixels" / "All of dynamic programming, TD learning, and deep RL build on variations of this equation" / "The TD target is computed using this frozen copy" / "The formal extension is the **Partially Observable MDP** (POMDP)" / "(GAE lambda)" / "Trust Region Policy Optimization (TRPO, Schulman et al., 2015)"
- **Now → Proposed:**
  - "когато DQN на DeepMind се научава да играе Atari Games, използвайки само сурови пиксели." → "когато DQN на DeepMind се научава да играе игри на Atari само по суровите пиксели на екрана."
  - "DQN показа, че може да се научи да играе 49 Atari Games директно от суров пикселов вход" → "DQN показа, че може да се научи да играе 49 игри на Atari директно по суровите пиксели на екрана"
  - "като Atari Games - а не в класически" → "като игрите на Atari - а не в класически"
  - "Цялото динамично програмиране, TD learning и дълбокото обучение с подкрепление се основават на вариации на това уравнение." → "Динамичното програмиране, обучението с темпорална разлика (temporal-difference learning, TD) и дълбокото обучение с подкрепление се основават на вариации на това уравнение."
  - "всеки следващ метод - метод Монте Карло, TD learning, DQN, PPO - може" → "всеки следващ метод - методът Монте Карло, TD обучението, DQN, PPO - може"
  - "TD learning е по-изгодно от динамичното програмиране, тъй като не изисква модел. То е по-изгодно и от метода Монте Карло, защото се учи онлайн" → "TD обучението има предимство пред динамичното програмиране, защото не изисква модел, а пред метода Монте Карло - защото се учи онлайн"
  - "TD target се изчислява с помощта на това замразено копие." → "Целевата стойност на TD се изчислява с помощта на това замразено копие."
  - "Формалното разширение е **Partially Observable MDP** (POMDP), който включва функция за наблюдение" → "Формалното разширение е **частично наблюдаемият марковски процес на вземане на решения** (Partially Observable MDP, POMDP)[^kaelbling1998], който включва функция за наблюдение"
  - "(**GAE Lambda**)" → "(параметъра $\lambda$ на GAE)"
  - "**Trust Region Policy Optimization** (TRPO, Schulman и др., 2015)[^trpo] се справи с това" → "Оптимизацията на стратегията в доверителна област (Trust Region Policy Optimization, TRPO; Schulman и др., 2015)[^trpo] се справи с това"
- **Why:** English prose in the BG bundle (pp. 8, 11, 12, 13, 14, 16, 17). The glossary itself has "atari games → игри на Atari", so the pipeline skipped it. The TD, POMDP and TRPO targets come from glossary entries that map to English (T03). The curated rule 1 allows the English name only in parentheses after a BG term. "по-изгодно" (more profitable) for *beneficial* is also fixed. The candidate's comment #38 ("Temporal Difference Learning", on "tD learning", p. 16) is only partly applied: the capital was fixed but the English stayed. For `[^kaelbling1998]` see S04.

### F01-B02 · S1 · meaning — on-policy rendered "политика на работа"
- **Where:** summaryBg.md § 1.8 (2×); onePagerBg.md "**Подход.**"
- **EN:** "It is on-policy (uses fresh data from the current policy), which avoids stale data issues." / "Being on-policy, PPO is less sample-efficient than off-policy methods like DQN" / "(policy-gradient, on-policy)"
- **Now → Proposed:**
  - "Тъй като е **политика на работа** (използва пресни данни от **текущата стратегия**), той избягва проблемите със застояли данни." → "Тъй като се обучава **по текущата си стратегия** (on-policy) и използва само пресни данни, събрани с нея, той избягва проблемите с остарели данни."
  - "Като **политика на работа**, PPO е по-малко **ефективен по отношение на пробите** в сравнение с **извънполитикови** методи като DQN" → "Тъй като се обучава по текущата си стратегия, PPO използва данните по-малко ефективно от методите, които се обучават извън текущата стратегия (off-policy), като DQN"
  - onePagerBg: "(градиент на политиката, политика на работа)" → "(градиент на стратегията, обучение по текущата стратегия)"
- **Why:** "политика на работа" means "work policy" or "working policy", which says nothing about learning from one's own current policy. It is a settled glossary entry (T01), so step 03 inherits it (2×). "застояли данни" means stagnant data; *stale* is "остарели". "пробите" (test specimens) is T07.

### F01-B03 · S2 · terminology — "политика" for policy and "извънполитиков" for off-policy
- **Where:** summaryBg.md §§ 1.2, 1.5, 1.6, 1.7; onePagerBg.md "**Подход.**"
- **EN:** "**Policy-based** methods (like PPO) learn the policy directly" / "**Policy Iteration** alternates…" / "uses the max operator to be **off-policy** — it learns about the optimal policy even while following an exploratory one" / "**SARSA** is the on-policy cousin of Q-learning" / "the 'deadly triad' of off-policy + function approximation + bootstrapping" / "It is off-policy, which is sample-efficient" / "(value-based, off-policy)"
- **Now → Proposed:**
  - "**Методите, базирани на политика** (като PPO) научават политиката директно." → "**Методите, базирани на стратегията** (като PPO), научават самата стратегия директно."
  - "**Итерация на политиката** редува два етапа." → "**Итерация на стратегията** редува два етапа."
  - "използва оператора max, за да бъде **извънполитиково** - то се учи относно оптималната стратегия дори докато следва експериментална такава." → "използва оператора max и затова се обучава **извън текущата стратегия** (off-policy): научава оптималната стратегия дори докато следва друга, експериментална стратегия."
  - "**SARSA** е вариантът на Q-обучението, който работи по текущата политика - той актуализира" → "**SARSA** е аналогът на Q-обучението, който се обучава по текущата стратегия (on-policy) - той актуализира"
  - "докато следва под-оптимална изследователска стратегия." → "докато следва неоптимална изследователска стратегия."
  - "(„смъртоносната троица“ от извънполитиково + апроксимация на функция + самоподкрепяне)" → "(„смъртоносната триада“[^suttonbarto2018]: обучение извън текущата стратегия + апроксимация на функции + бутстрапинг)"
  - "Като извънполитиков метод, тя е ефективна по отношение на пробите" → "Тъй като се обучава извън текущата стратегия, той използва данните ефективно"
  - onePagerBg: "(базиран на стойност, извънполитиков)" → "(базиран на стойността, с обучение извън текущата стратегия)"
- **Why:** The curated `terminology_EN_BG.md` fixes Policy → "Стратегия", and the rest of the chapter follows it. In § 1.5 the heading "Итерация на политиката" sits next to "оценка на стратегия" for the same object. "то се учи относно" is a calque of *learns about*. "под-оптимална" is not Bulgarian spelling. "троица" suggests the Trinity; "триада" is the academic word (T12). The candidate's own word "експериментална" (comment #47) is kept. This is glossary-level (T01, T02).

### F01-B04 · S1 · meaning — *discounted* rendered "отстъпена"
- **Where:** summaryBg.md § 1.7 "**Как работи.**"
- **EN:** "the target (reward + discounted max Q-value of the next state)"
- **Now → Proposed:** "(награда плюс отстъпена максимална Q-стойност на следващото състояние)" → "(награда плюс дисконтираната максимална Q-стойност на следващото състояние)"
- **Why:** "отстъпена" means "conceded / handed over". The chapter defines "дисконтиране" two pages earlier.

### F01-B05 · S1 · meaning — "почти случайна мода"
- **Where:** summaryBg.md § 1.9.1, bullet "**График на изследване.**"
- **EN:** "wastes many episodes in near-random mode"
- **Now → Proposed:** "води до загуба на много епизоди в почти случайна мода." → "води до загуба на много епизоди в почти случаен режим."
- **Why:** "мода" is fashion (or the statistical mode). An operating mode is "режим". The settled entry "mode → мода" has no sense split (T06).

### F01-B06 · S2 · meaning — "100-episode average" rendered "average per episode"
- **Where:** summaryBg.md §§ 1.7, 1.8 (the "В нашата реализация от Глава 1…" paragraphs)
- **EN:** "(achieving a 100-episode average of 477.5 against a 475 target)" / "(100-episode average of 202.2 against a 200 target)"
- **Now → Proposed:**
  - "(постигайки средна стойност за епизод от 477.5 спрямо цел от 475)" → "(средна награда за последните 100 епизода 477.5 при цел 475)"
  - "(средна стойност за епизод от 202.2 при цел от 200)" → "(средна награда за последните 100 епизода 202.2 при цел 200)"
- **Why:** "средна стойност за епизод" is the per-episode mean. The success criterion is the mean over 100 consecutive episodes, and a reader cannot compare it with the "плъзгаща средна" of § 1.9.

### F01-B07 · S2 · meaning — "(с бюджет от 264K стъпки)"; "персонализиран"
- **Where:** summaryBg.md § 1.9.2
- **EN:** "Our custom PPO crosses the 200 target around episode 543 (264K steps)."
- **Now → Proposed:** "Нашият персонализиран PPO преминава целта от 200 около епизод 543 (с бюджет от 264K стъпки)." → "Нашият собствен PPO преминава целта от 200 около епизод 543 (след 264K стъпки)."
- **Why:** The budget was 500K. 264K is where the target was crossed, as the next sentence of the chapter says. "персонализиран" means personalized, whereas § 1.9.1 correctly says "собствен" (T08). Re-check 543 after G03.

### F01-B08 · S1 · grammar — "сходява", "не е сходим"
- **Where:** summaryBg.md §§ 1.5, 1.9.2
- **EN:** "It is guaranteed to converge to the optimal policy." / "It converges to the optimal value function" / "still climbing but not converged"
- **Now → Proposed:**
  - "Гарантирано е, че тя сходява към оптималната стратегия." → "Гарантирано е, че процесът достига оптималната стратегия."
  - "Тя сходява към оптималната функция на стойността" → "Тя клони към оптималната функция на стойността"
  - "все още се покачва, но не е сходим." → "все още се покачва и не е достигнал сходимост."
- **Why:** "сходява" is not a Bulgarian verb (as in F07-B03; it recurs in 8 chapters, T11). "не е сходим" means "is not convergent", a property of a series, not of a training run. Policy iteration terminates in finitely many steps on a finite MDP, so "достига" is exact. Value iteration converges only in the limit, hence "клони".

### F01-B09 · S2 · calques — § 1.9 comparison section
- **Where:** summaryBg.md §§ 1.9.1, 1.9.3
- **EN:** "The gap comes from three implementation-level differences:" / "an adaptive schedule that gives faster feedback" / "across diverse, long-training domains like Atari games" / "custom implementations allow surgical modifications"
- **Now → Proposed:**
  - "Разликата се дължи на три различия на ниво изпълнение:" → "Разликата се дължи на три различия в реализацията:"
  - "адаптивен план, който осигурява по-бърза обратна връзка" → "адаптивен график, който осигурява по-бърза обратна връзка"
  - "в разнообразни и дългосрочни области на обучение като" → "в разнообразни области с дълго обучение като"
  - "персонализираните реализации дават възможност за прецизни модификации" → "собствените реализации дават възможност за прецизни модификации"
- **Why:** "изпълнение" is execution, not implementation. The same bullet list calls the ε schedule "график", while "план" means a plan. "дългосрочни области" means "long-term domains". "персонализирани" is T08. The PPO paragraph's "подпомагат по-дългите серии от изпълнения" is rewritten in C03.

### F01-B10 · S2 · terminology — bootstrapping, bias, tradeoff
- **Where:** summaryBg.md § 1.6
- **EN:** "using a bootstrap: the current estimate…" / "The bootstrapping introduces some bias, but in practice this tradeoff is overwhelmingly favorable."
- **Now → Proposed:**
  - "използвайки самоподкрепяне: текущата оценка" → "използвайки бутстрапинг (обновяване на оценка чрез други оценки): текущата оценка"
  - "**Самоподкрепянето** въвежда известно **пристрастие**, но в практиката тази размяна е изключително благоприятна." → "Бутстрапингът въвежда известно отместване (bias), но на практика този компромис е силно изгоден."
- **Why:** "самоподкрепяне" is an ad-hoc coinage no reader will recognise, and the corpus has four renderings of the concept (T05). "пристрастие" is prejudice; statistical bias is "отместване" (T06). "размяна" (an exchange) for *tradeoff* is a calque, and the curated file has "компромис". The two bold spans are not in the EN.

### F01-B11 · S2 · meaning — divergence rendered "разминаване"
- **Where:** summaryBg.md § 1.7, item "**Целева мрежа.**"
- **EN:** "which causes oscillation and divergence"
- **Now → Proposed:** "което води до колебания и разминаване." → "което води до колебания и дори до разходимост на обучението."
- **Why:** "разминаване" means two things passing each other, or a mismatch. Divergence of an iterative method is "разходимост" (T06).

### F01-B12 · S2 · typography/terminology — lower-case "q"
- **Where:** summaryBg.md § 1.7 (6×); onePagerBg.md "**Подход.**"
- **Now → Proposed:**
  - "извежда q-стойности за всички действия" → "извежда Q-стойности за всички действия"
  - "действието с най-висока q-стойност" → "действието с най-висока Q-стойност"
  - "отделно копие на q-мрежата" → "отделно копие на Q-мрежата"
  - "Тя може да надценява q-стойности" → "Той може да надценява Q-стойностите"
  - "q-мрежата в DQN е стандартен" → "Q-мрежата в DQN е стандартен"
  - "съпоставя състояния към q-стойности" → "съпоставя на състоянията Q-стойности"
  - onePagerBg: "q-мрежа `[4->128->128->2]`" → "Q-мрежа `[4->128->128->2]`"
- **Why:** Q is the notation of the Q-function. The same paragraphs write "Q-стойност" and "Q-обучение", and one sentence opens with a lower-case letter. The glossary entry "q-network → q-мрежа" causes it (T09). "Тя" → "Той": gender, see B22.

### F01-B13 · S2 · meaning — circular definition "Стратегия: стратегията на агента"
- **Where:** summaryBg.md § 1.2
- **EN:** "**Policy** ($\pi$): the agent's strategy."
- **Now → Proposed:** "- **Стратегия** ($\pi$): стратегията на агента. Тя може да бъде" → "- **Стратегия** ($\pi$): правилото, по което агентът избира действията си. Тя може да бъде"
- **Why:** Policy and strategy share one Bulgarian word, so the definition defines the term by itself.

### F01-B14 · S2 · cross-reference names a heading that does not exist (comment #37 partly applied)
- **Where:** summaryBg.md § 1.3
- **EN:** "*Information Sets — When You Cannot See Everything*, below, deals with that."
- **Now → Proposed:** "Разделът „Информационни множества - когато не виждате всичко“ по-долу разглежда този въпрос." → "Разделът „Информационни множества - когато не можете да видите всичко“ по-долу разглежда този въпрос."
- **Why:** The candidate's comment "раздел 4? не става ясно къде точно" was applied by naming the section, but the quoted title does not match the heading printed on p. 11 and in the TOC.

### F01-B15 · S2 · headings — PPO gloss and capital after the dash
- **Where:** summaryBg.md headings §§ 1.5, 1.6, 1.8 (they also print in the bundle TOC)
- **Now → Proposed:**
  - "## PPO - Оптимизация на проксималната стратегия" → "## PPO - оптимизация на стратегията с ограничение на близостта"
  - "## Динамично програмиране - При наличие на модел" → "## Динамично програмиране - при наличие на модел"
  - "## Обучение с темпорална разлика - Обучение без модел" → "## Обучение с темпорална разлика - обучение без модел"
- **Why:** *Proximal* qualifies the optimization, not the policy. "проксималната стратегия" is a calque from the settled glossary, and the curated gloss for PPO is "оптимизация на стратегията с ограничение на близостта" (T04). A capital letter after a dash inside a heading copies English title case. The other headings in the chapter are lower-case after the dash.

### F01-B16 · S2 · terminology — GAE (and its source)
- **Where:** summaryBg.md § 1.8 "**Архитектура.**"
- **EN:** "The value network enables Generalized Advantage Estimation (GAE), which provides low-variance advantage estimates for the policy gradient."
- **Now → Proposed:** "Мрежата за стойности позволява прилагането на обобщено изчисляване на предимството (GAE), което осигурява нискодисперсностни оценки на предимството, използвани при **градиента на стратегията**." → "Мрежата за стойности позволява прилагането на обобщената оценка на предимството (generalized advantage estimation, GAE)[^gae2016], която дава оценки на предимството с ниска дисперсия за **градиента на стратегията**."
- **Why:** *Estimation* is "оценка", and the curated file has "Обобщена оценка на предимството". The settled entry says "изчисляване" (T10). "нискодисперсностни" is an ad-hoc compound. For the footnote see S04.

### F01-B17 · S2 · terminology — return rendered "възнаграждения"
- **Where:** summaryBg.md § 1.8, first paragraph
- **EN:** "to increase the probability of actions that lead to high returns"
- **Now → Proposed:** "които водят до високи възнаграждения." → "които водят до висока възвръщаемост."
- **Why:** The chapter defines return as "възвръщаемост" (§ 1.3, curated file). "възнаграждение" is a third word next to "награда", and it reads as reward.

### F01-B18 · S2 · calques — "Контролната версия", "Терминът в скобите"
- **Where:** summaryBg.md § 1.6
- **EN:** "The term in brackets is the **TD error**" / "The control version of this idea is **Q-learning**"
- **Now → Proposed:**
  - "Терминът в скобите е **TD грешка**" → "Изразът в скобите е **TD грешката**"
  - "Контролната версия на тази идея е **Q-обучение** (Watkins, 1989):[^watkins1989]" → "Вариантът на тази идея за задачата за управление е **Q-обучението** (Watkins, 1989):[^watkins1989]"
- **Why:** "контролна версия" means a check or reference version. *Control* here is the control problem (управление), as in "алгоритъм за управление" in § 1.1. A "термин" is a word of terminology; the bracketed expression is a quantity (compare F07-B16 "членове").

### F01-B19 · S2 · terminology — "частично наблюдавани"
- **Where:** summaryBg.md § 1.4
- **EN:** "These are **partially observable** settings."
- **Now → Proposed:** "Това са **частично наблюдавани** среди." → "Това са **частично наблюдаеми** среди."
- **Why:** *Observable* means "наблюдаем", while "наблюдаван" means "observed". This is also the word in the POMDP name (B01).

### F01-B20 · S2 · calque — "адресираха нестабилността", "трика"
- **Where:** summaryBg.md § 1.7 "**Защо DQN е важна…**"
- **EN:** "DQN's two tricks — replay and target networks — addressed the instability, making deep value-based RL practical for the first time."
- **Now → Proposed:** "Двата трика на DQN - повторение на натрупан опит и целеви мрежи - адресираха нестабилността, правейки дълбокото обучение с подкрепление, базирано на стойност, практично за първи път." → "Двата похвата на DQN - повторението на натрупан опит и целевата мрежа - ограничиха нестабилността и за първи път направиха практически приложимо дълбокото обучение с подкрепление, базирано на стойности."
- **Why:** "адресирам" in the sense of *address a problem* is an anglicism. "трик" is colloquial, and the same section says "Два ключови похвата".

### F01-B21 · S2 · terminology — within-chapter inconsistencies
- **Where:** summaryBg.md §§ 1.7–1.9; onePagerBg.md
- **Now → Proposed:**
  - clipping (curated "Изрязана сурогатна цел"; the chapter also has "изрязаната цел"):
    - "заменя ограничението с много по-прост механизъм: **отсичане**." → "заменя ограничението с много по-прост механизъм: **изрязване**."
    - "PPO отсича това отношение в диапазона" → "PPO изрязва това отношение до диапазона"
    - "(**отсичане**, GAE, структура на **разгръщане**)" → "(изрязване, GAE, структура на разгръщането)"
    - onePagerBg: "изрязан заместител при `eps=0.2`" → "изрязана сурогатна цел при `eps=0.2`"
  - grammatical gender of DQN and PPO (the chapter says "Нашият собствен DQN", "неговата", "Той може да усвоява"):
    - "**Защо DQN е важна в сравнение с предишните методи:**" → "**Защо DQN е важен в сравнение с предишните методи:**"
    - "И най-важното - тя научава алчна детерминистична стратегия" → "И най-важното - той научава алчна детерминистична стратегия"
    - "PPO на SB3 вероятно би достигнала целта." → "PPO на SB3 вероятно би достигнал целта."
  - replay buffer (the chapter says "повторение на натрупан опит"):
    - "до остаряла информация в буфера за възпроизвеждане" → "до остаряла информация в буфера за повторение на опита"
- **Why:** Each concept should have one word, and each algorithm one gender. Each pair above appears within this chapter. "възпроизвеждане" (playback) comes from a settled entry (T12).

### F01-B22 · S2 · one-pager — meaning errors
- **Where:** onePagerBg.md
- **EN:** "neural equilibrium finding (Chapter 5)" / "supplies the implementation vocabulary every later chapter assumes" / "236K steps inside its budget" / "(5 episodes is ~100 steps early and ~2500 once solved)" / "0.001 plus best-model checkpointing" / "SB3's defaults are tuned for robustness across environments, not for classic control" / "The claim is a task-specific advantage, not a better algorithm." / "which is exactly what the exploitation work in Chapters 7-8 needs" / "(target networks, trust regions, advantage normalisation)" / "whether the sample-efficiency edge measured here … of two small, well-conditioned control tasks"
- **Now → Proposed:**
  - "намиране на **невронно** равновесие (Глава 5)" → "намиране на равновесие с невронни мрежи (Глава 5)"
  - "и директно осигурява речниковия запас за изпълнение, който всяка следваща стъпка предполага." → "и пряко осигурява понятийния апарат за реализацията, който всяка следваща глава предполага."
  - "- 236K стъпки в рамките на бюджета." → "- 236K стъпки преди изчерпването на бюджета."
  - "(5 епизода са приблизително 100 стъпки по-рано и около 2500 след решаването)" → "(5 епизода са около 100 стъпки в началото и около 2500 след решаването)"
  - "0.001 плюс **най-добър модел с контролна точка** превърна" → "стойност 0.001 заедно със запазването на най-добрия модел превърна"
  - "Настройките по подразбиране на SB3 са настроени за **устойчивост** в различни среди, а не за класически контрол" → "Стойностите по подразбиране в SB3 са избрани с оглед на устойчивост в различни среди, а не за класически задачи за управление"
  - "Твърдението е за специфично предимство на задачата, а не за по-добър алгоритъм." → "Твърдението е за предимство при тези конкретни задачи, а не за по-добър алгоритъм."
  - "точно от какво има нужда работата" → "точно от което има нужда работата"
  - "(целеви мрежи, доверителни региони, нормализиране на предимството)" → "(целеви мрежи, доверителни области, нормализиране на предимството)"
  - "предимство по отношение на изискванията за проби" → "предимство в ефективността по отношение на данните"
  - "добре обусловени задачи за контрол" → "добре обусловени задачи за управление"
- **Why:** "невронно равновесие" says the *equilibrium* is neural. "стъпка" is stale naming: the EN has "chapter", and the candidate's TOC comment #1 asks to change "all mention of steps into chapters". "в рамките на бюджета" is read as "within the budget", not "before the budget ran out". "по-рано" means *earlier*, but the EN *early* means at the start of training. "най-добър модел с контролна точка" is a noun pile. "настройките … са настроени" is a tautology. "специфично предимство на задачата" says the task has the advantage. "от какво" is interrogative. *Trust region* is "доверителна област" (the settled glossary has "методи на доверителната област"). "контрол" for *control* is a calque. The "политика" items are in B02/B03, and the q-мрежа item is in B12.

### F01-B23 · S2 · candidate comment #22 not applied — bold in § 1.1
- **Where:** summaryBg.md § 1.1, second paragraph (p. 8). The candidate's comment on "животинската психология" reads: "без болд"
- **Now → Proposed:**
  - "Най-ранната нишка идва от **животинската психология**" → "Най-ранната нишка идва от животинската психология"
  - "през **теорията на оптималното управление**" → "през теорията на оптималното управление"
- **Why:** The fix removed the pipeline-added bold in this paragraph but kept the three spans the EN has. The candidate asked for none. The third span, "**обучението чрез проба и грешка**", disappears with the C04 rewrite. For parity, drop the same bold in summaryEn.md (optional).

### F01-B24 · S3 · candidate comment #33 not applied — "Важното е да се подчертае"
- **Where:** summaryBg.md § 1.1, last paragraph (p. 9). The candidate's comment on "Важното е" reads: "без ударение"
- **Now → Proposed:** "Важното е да се подчертае, че обучението с подкрепление не е просто „машинно обучение с награди“. То представлява самостоятелна рамка" → "Обучението с подкрепление не е просто „машинно обучение с награди“, а самостоятелна рамка"
- **Why:** The emphatic lead-in is unchanged since the proofread build. The source has no stress mark (no U+0301), so the comment refers to the rhetorical emphasis.

### F01-B25 · S3 · candidate comment #43 not applied — "вече е от значение"
- **Where:** summaryBg.md § 1.4, last paragraph (p. 11). The candidate's comment on "а вече е от значение," reads: "е от значение"
- **Now → Proposed:** "Усвояването на информационните множества вече е от значение," → "Усвояването на информационните множества е от значение,"
- **Why:** The companion comment #42 ("Разбирането" → "Усвояването") was applied, but this one was not. The rest of the sentence is in C06.

### F01-B26 · S2 · candidate comment #54 not applied — "MLPs"
- **Where:** summaryBg.md § 1.8, "**Бележка относно невронните мрежи в тази глава.**" (p. 16). The candidate's comment on "и MLPs, ч" reads: "Mlps?"
- **Now → Proposed:** "стандартни MLPs, чиито" → "стандартни многослойни перцептрони (MLP), чиито"
- **Why:** A Latin abbreviation takes no English plural -s in Bulgarian. § 1.7 already expands "многослоен перцептрон (MLP)".

### F01-B27 · S2 · candidate comment #39 not applied — titles of English sources translated
- **Where:** summaryBg.md § 1.2 "Прочетете повече"; footnote `suttonbarto2018` (prints on p. 8). The candidate's comment on the old Sutton & Barto box reads: "не бива да ревеждаме глави на източници които не са на български" (curated rule 7 since then)
- **Now → Proposed:**
  - "> **Прочетете повече:** OpenAI Spinning Up - „Ключови концепции в обучението с подкрепление“" → "> **Прочетете повече:** OpenAI Spinning Up - „Part 1: Key Concepts in RL“"
  - "Гл. 1 (областта); гл. 3 (крайни марковски процеси на вземане на решения); гл. 4 (динамично програмиране); гл. 5 (методи на Монте Карло); гл. 6 (обучение с темпорална разлика)." → "Гл. 1 "Introduction"; гл. 3 "Finite Markov Decision Processes"; гл. 4 "Dynamic Programming"; гл. 5 "Monte Carlo Methods"; гл. 6 "Temporal-Difference Learning"; §11.3 "The Deadly Triad"; гл. 13 "Policy Gradient Methods"."
  - summaryEn.md, same footnote: "Ch. 1 (the field); Ch. 3 (finite Markov decision processes); Ch. 4 (dynamic programming); Ch. 5 (Monte Carlo methods); Ch. 6 (temporal-difference learning)." → "Ch. 1 "Introduction"; Ch. 3 "Finite Markov Decision Processes"; Ch. 4 "Dynamic Programming"; Ch. 5 "Monte Carlo Methods"; Ch. 6 "Temporal-Difference Learning"; §11.3 "The Deadly Triad"; Ch. 13 "Policy Gradient Methods"."
- **Why:** The candidate's rule, now curated rule 7, keeps chapter titles of foreign sources in English. The old reading boxes became a footnote that still translates them. The titles were checked against the book's own table of contents (RLbook2020.pdf from incompleteideas.net), and the Spinning Up H1 against the page. §11.3 and Ch. 13 are added for B03 and S01. The footnote label is shared with chapter 3, whose citation this definition also serves (F07-X01).

### F01-B28 · S3 · typography — "K" / "M" as number suffixes
- **Where:** summaryBg.md "750K", "264K", "500K", "1–2M"; onePagerBg.md "236K", "750K", "500K" (2×), "1–2M"
- **Now → Proposed:** "750K" → "750 хил.", "264K" → "264 хил.", "500K" → "500 хил.", "236K" → "236 хил.", "1–2M" → "1–2 млн." (keep them inside code spans and the report tables)
- **Why:** Latin K/M suffixes are English shorthand, and the chapter itself also writes "264 хиляди стъпки". This is not part of the central decimal decision, so it is listed once here.

### F01-B29 · S3 · polish
- **Where:** summaryBg.md §§ 1.1, 1.5
- **Now → Proposed:**
  - "**Итерация на стойностите** е пряк път." → "**Итерация на стойностите** е съкратен вариант."
  - "в една единствена актуализация" → "в една-единствена актуализация"
  - "привеждането в съответствие на езикови модели (RLHF)" → "съгласуването на езиковите модели с човешките предпочитания (RLHF)"
- **Why:** "пряк път" is a literal *shortcut*. "една-единствена" is written with a hyphen. "привеждане в съответствие" is legal register for *alignment*.

## T — Glossary-level terminology

### F01-T01 · S1 · "on-policy → политика на работа"; "off-policy → извънполитикова / обучение извън политиката"
- **Where:** `llmPipeline/glossary_settled.md`; printed in step 01 (3×, B02) and step 03 (2×).
- **Now → Proposed:** on-policy → "с обучение по текущата стратегия (on-policy)"; off-policy → "с обучение извън текущата стратегия (off-policy)"; keep the English in parentheses on first use.
- **Why:** "политика на работа" means "working policy" and does not express the concept. "извънполитиков" is a coinage built on "политика", which the curated file retired in favour of "стратегия".

### F01-T02 · S2 · settled entries that use "политика" for policy
- **Where:** glossary_settled.md: "policy iteration → итерация на политиката", "policy-based methods → методи, базирани на политика", "greedy deterministic policy → алчна детерминистична политика", "tabular-extracted policies → таблично извлечена политика".
- **Now → Proposed:** → "итерация на стратегията", "методи, базирани на стратегията", "алчна детерминистична стратегия", "таблично извлечени стратегии".
- **Why:** The curated `terminology_EN_BG.md` says Policy → "Стратегия" ("standard in BG"), while the settled file mixes both words, so chapters mix them (B03).

### F01-T03 · S1 · entries whose Bulgarian side is English
- **Where:** glossary_settled.md: "td learning → TD learning", "td error → TD error", "td target → TD target", "partially observable mdp → Partially Observable MDP", "trust region policy optimization → Trust Region Policy Optimization".
- **Now → Proposed:** → "TD обучение (обучение с темпорална разлика)", "TD грешка", "целева стойност на TD", "частично наблюдаем марковски процес на вземане на решения (POMDP)" (the file already has this under "pomdp"), "оптимизация на стратегията в доверителна област (TRPO)".
- **Why:** An English "translation" is inserted as is, and it prints as English in the BG bundle (B01).

### F01-T04 · S2 · "proximal policy optimization → оптимизация на проксималната стратегия"
- **Now → Proposed:** → "оптимизация на стратегията с ограничение на близостта" (the curated gloss)
- **Why:** The two glossaries disagree. The settled form makes *proximal* modify the policy (B15).

### F01-T05 · S2 · bootstrapping — four renderings, one misspelled
- **Where:** "bootstrapping → самоподкрепяне", "bootstrap → буутстрапинг", "bootstrapped target → цел с бутстрапиране", "bootstrap targets → целеви стойности по метода „bootstrap“".
- **Now → Proposed:** one term, "бутстрапинг", glossed on first use as "обновяване на оценка чрез други оценки". Same fix for "bootstrapped target → целева стойност чрез бутстрапинг".
- **Why:** "самоподкрепяне" is not an established term. "буутстрапинг" is misspelled, and report_bg.md prints it. Steps 01 and 05 each use "самоподкрепяне" twice.

### F01-T06 · S2 · statistical and optimization senses: bias, divergence, mode
- **Where:** "bias → пристрастие" (in steps 01, 05, 07, 11), "divergence → разминаване" (steps 01, 05, 09), "mode → мода".
- **Now → Proposed:** bias (statistical) → "отместване"; divergence (of an iteration) → "разходимост" (KL divergence stays "дивергенция", F07-T11); mode → split into "mode (of a distribution) → мода" and "mode (operating) → режим".
- **Why:** "пристрастие" is prejudice. "разминаване" is a mismatch. The unsplit "мода" produced "почти случайна мода" (B05).

### F01-T07 · S2 · "sample-efficient → ефективен по отношение на пробите"; "sample efficiency → ефективност на извадката"
- **Now → Proposed:** → "ефективен по отношение на данните"; "ефективност по отношение на данните (sample efficiency)"
- **Why:** "проба" is a specimen or trial. The two entries translate one concept in two ways. What is meant is how many environment interactions a method needs.

### F01-T08 · S2 · "custom → персонализиран"
- **Where:** figure mapping 'Custom DQN' → 'Персонализиран DQN', 'Custom PPO', 'Custom CFR (Hand-coded)' → 'Персонализиран CFR…', 'Custom\nstopped…'; text in steps 01 (2×), 05, 06.
- **Now → Proposed:** → "собствен" / "собствена реализация"
- **Why:** "персонализиран" means tailored to a person. Step 01's own text also uses "собствен" for the same thing.

### F01-T09 · S2 · "q-network → q-мрежа"
- **Now → Proposed:** → "Q-мрежа"; also check that the pipeline does not lower-case a leading "Q-".
- **Why:** Q is notation (B12). The same file already has "q-values → Q-стойности".

### F01-T10 · S2 · "generalized advantage estimation → обобщено изчисляване на предимството"
- **Now → Proposed:** → "обобщена оценка на предимството" (curated)
- **Why:** The two glossaries disagree, and *estimation* is "оценка" (B16).

### F01-T11 · S2 · the non-word "сходява" recurs across the corpus
- **Where:** summaryBg.md in steps 01 (2), 02 (1), 03 (1), 05 (1), 06 (1), 07 (2), 08 (1), 09 (5): 15 occurrences, found by grep.
- **Now → Proposed:** per context, "клони към" (limit), "се сближава с" (gradual approach), "достига" (finite termination), or a noun phrase with "сходимост".
- **Why:** Not a glossary entry, but a pipeline habit that the pilot fixed only locally (F07-B03). A one-line grep in the central pass catches all of them.

### F01-T12 · S3 · three smaller entries
- **Now → Proposed:** "replay buffer → буфер за възпроизвеждане" → "буфер за повторение на опита" (matches "experience replay → Повторение на натрупан опит"); "deadly triad → смъртоносна троица" → "смъртоносна триада"; the curated file's "Контрафактуалн…" (CFR, counterfactual value) disagrees with the settled "контрафактичн…", which the corpus uses 45 times against 2. Change the curated file, not the text.
- **Why:** Consistency. "троица" suggests the Trinity.

## C — Content

### F01-C01 · S1 · The SB3 DQN results in the text are from a different run than the figure, and "stays around 30" matches neither
- **Where:** summaryEn/Bg § 1.9 intro and § 1.9.1; onePager/onePagerBg "Approach" and "Key results"; report_en/bg §4.1, §4.3.
- **Problem:** Two SB3 DQN runs exist in git.
  - (i) The run of 3 Apr (commit 4a173d2): 750K steps, 17,176 episodes, our lr/buffer/batch/γ/ε schedule, `exploration_fraction=0.36`, `target_update_interval=1000`, net [128,128]. Computed from that cache: rolling-100 below 25 for the first 1,061 episodes, above 100 only from episode ≈ 12,455 (365K steps), best 293.9 at episode 16,404, final 90.0.
  - (ii) The run of 6 Apr (commit de7456b, the current cache, script and **printed figure**): RL Zoo's tuned CartPole settings (lr 2.3e-3, net [256,256], `target_update_interval=10`, `train_freq=256`, `gradient_steps=128`, `exploration_fraction=0.16`, final ε 0.04; verified against rl-baselines3-zoo `hyperparams/dqn.yml`), 100K steps, 1,255 episodes, best rolling-100 222.4 (episode ≈ 694), final 134.3.
  - The text mixes both runs. The 750K, 17,176 episodes, 293.9 and "a fixed 1000-step interval" come from (i). The printed figure and `final_metrics.png` (which prints 222.4 beside a report table saying 293.9) come from (ii). The summary's "never converges — its rolling average stays around 30" describes neither run: it is the first-1,061-episode window of (i). "SB3 uses a fixed 1000-step interval" is false for (ii), and SB3's default is 10,000 (checked in the installed `stable_baselines3/dqn/dqn.py`).
- **Fix (decide one; A is recommended because every text already describes it):**
  - **A: restore run (i).** `git show 4a173d2:implementation/step01/sb3_results_cache.json` (the `sb3_dqn` entry) and the `train_sb3_dqn` of 4a173d2, then re-render the figures (G02). Text:
    - summaryEn: "SB3's DQN, given 750K environment steps (17,176 episodes), never converges — its rolling average stays around 30 and never approaches the target." → "SB3's DQN, given 750K environment steps (17,176 episodes), stays below a rolling average of 25 over the first 1,061 episodes shown in the figure, passes 100 only after about 12,500 episodes (365K steps) and peaks at 293.9, never approaching the target."
    - summaryBg: "DQN на SB3, с предоставени 750K стъпки на средата (17,176 епизода), не успява да се сближи - неговата плъзгаща средна остава около 30 и никога не достига целта." → "DQN на SB3 получава 750K стъпки на средата (17,176 епизода): през първите 1,061 епизода, показани на фигурата, плъзгащата му се средна остава под 25, надхвърля 100 едва след около 12,500 епизода (365K стъпки) и достига най-много 293.9, без да се доближи до целта."
    - summaryEn: "SB3 uses a fixed 1000-step interval." → "In this run SB3 syncs every 1000 steps (its default is 10,000)."
    - summaryBg: "SB3 използва фиксиран интервал от 1000 стъпки." → "В този експеримент SB3 синхронизира на всеки 1000 стъпки (стойността по подразбиране е 10,000)."
    - summaryEn: "Both our implementations and SB3 were given matched hyperparameters and equivalent training budgets." → "SB3 was given our core hyperparameters (learning rate, γ, buffer and network size, ε schedule) and budgets of 750K steps for DQN and 500K for PPO; its remaining settings are SB3 defaults."
    - summaryBg: "На нашите имплементации и на SB3 бяха зададени еднакви хиперпараметри и еквивалентни бюджети за обучение." → "На SB3 бяха зададени основните хиперпараметри на нашите реализации (скорост на обучение, γ, размер на буфера и на мрежата, график на ε) и бюджет от 750K стъпки за DQN и 500K за PPO; останалите настройки са стойностите по подразбиране на SB3."
  - **B: keep run (ii).** Rewrite § 1.9.1, the one-pager and the report around "SB3 with the RL Zoo's tuned CartPole hyperparameters, 100K steps (twice the Zoo's budget), best rolling-100 222.4 at episode ≈ 690, final 134". Drop "matched", "defaults" and the three-cause list, which does not fit a run that syncs every 10 steps and decays ε over 16K steps. Cite the Zoo (Raffin, *RL Baselines3 Zoo*, GitHub, 2020). Note that the Zoo expects 50K steps, so a single-seed failure at 100K needs a second seed before it is reported.

### F01-C02 · S2 · The comparison's causal claims are untested (one unseeded run each), and one large difference is not mentioned
- **Where:** summaryEn/Bg § 1.9.1 last paragraph; onePager "The cause is algorithmic, not unfair tuning"; "Advantage normalisation proved non-negotiable"; summary § 1.8 "The decisive factors were … advantage normalization".
- **Problem:** Each implementation was run once, and neither `dqn/train.py` nor `ppo/train.py` sets a seed. The three listed causes are hypotheses, not ablations. A fourth difference is not mentioned. Our DQN takes a gradient step on every environment step (`agent.train_step()` inside the step loop), while SB3's default `train_freq=4, gradient_steps=1` (not overridden in run (i)) updates every fourth step, and uses Huber instead of MSE loss. With the same budget, SB3 makes about 4× fewer updates, which is a hyperparameter difference. Advantage normalisation and the entropy bonus appear in no recorded iteration (report §3: Run 1 → Run 2 changed only network size and budget).
- **Now → Proposed:**
  - summaryEn: "These are genuine algorithmic choices, not hyperparameter unfairness." → "These are plausible causes, not measured ones: each implementation was run once, without a fixed seed, and a fourth difference is untested — our agent takes a gradient step on every environment step, whereas SB3 (train_freq = 4) updates every fourth step, i.e. about four times fewer updates for the same budget."
  - summaryBg: "Това са истински алгоритмични решения, а не несправедливост при хиперпараметрите." → "Това са правдоподобни причини, а не измерени: всяка реализация е изпълнена веднъж, без фиксирано начално число, а четвърто различие не е проверено - нашият агент прави градиентна стъпка при всяка стъпка на средата, докато SB3 (train_freq = 4) обновява мрежата на всяка четвърта стъпка, т.е. при същия бюджет прави около четири пъти по-малко обновявания."
  - onePager: "The cause is algorithmic, not unfair tuning:" → "The likely causes (untested; one run each) are:" and append to that bullet ", and our agent's gradient step on every environment step against SB3's every fourth"; onePagerBg: "Причината е алгоритмична, а не несправедливо настройване:" → "Вероятните причини (непроверени, по едно изпълнение) са:" and append "както и градиентната стъпка при всяка стъпка на средата при нашия агент срещу всяка четвърта при SB3".
  - onePager (the line wraps before "-500"): "Advantage normalisation proved non-negotiable on rewards spanning" → "Advantage normalisation was kept throughout; rewards span"; onePagerBg: "**Нормализиране на предимството** се оказа незаменимо при награди в диапазона -500 до +300" → "Нормализирането на предимството беше използвано навсякъде (наградите са в диапазона от -500 до +300)".

### F01-C03 · S2 · False: "SB3's … built-in observation normalization"
- **Where:** summaryEn/Bg § 1.9.2; report_en/bg §4.2.
- **Problem:** SB3's PPO has no built-in observation normalization. It needs a `VecNormalize` wrapper, which `compare_sb3.py` does not use. What SB3 does by default is orthogonal initialization (`ortho_init=True`) and advantage normalization *per mini-batch* (`ppo.py` l. 218), whereas ours normalizes per rollout. Both were checked in the installed SB3 2.9.0.
- **Now → Proposed:**
  - summaryEn: "The remaining difference likely comes from SB3's orthogonal weight initialization and built-in observation normalization, which help long runs but may slow early convergence." → "The remaining difference may come from SB3's orthogonal weight initialization and from its normalizing advantages per mini-batch rather than per rollout; with one run per implementation it may also be chance."
  - summaryBg: "Оставащата разлика вероятно се дължи на ортогоналната инициализация на теглата и вградената нормализиране на наблюденията в SB3, които подпомагат по-дългите серии от изпълнения, но могат да забавят ранната сходимост." → "Оставащата разлика може да се дължи на ортогоналната инициализация на теглата в SB3 и на това, че SB3 нормализира предимството във всяка мини-партида, а не в цялото разгръщане; при едно-единствено изпълнение на всяка реализация тя може да е и случайна."
  - Same in report_en/bg §4.2, whose second bullet ("learning rate scheduling") is also not an SB3 default.
- **Why:** The fix also removes the agreement error "вградената нормализиране".

### F01-C04 · S2 · The history of RL misassigns the three threads (checked against Sutton & Barto §1.7)
- **Where:** summaryEn/Bg § 1.1, paragraphs 2–3.
- **Problem:** S&B §1.7 (p. 13 of the book) gives the trial-and-error thread as the one that "originated in the psychology of animal learning" (Thorndike). The third, "less distinct" thread is temporal-difference learning, and Samuel's checkers player (1959) is "the first … learning method that included temporal-difference ideas". The 1988 paper is not Sutton's PhD work (the thesis is 1984, *Temporal Credit Assignment in Reinforcement Learning*, UMass Amherst). In it Sutton "separat[ed] temporal-difference learning from control, treating it as a general prediction method". The optimal-control and TD threads were "fully brought together in 1989 with Chris Watkins's development of Q-learning". The chapter instead says the 1988 work "bridged … animal learning theories and Bellman's dynamic programming".
- **Now → Proposed:**
  - summaryEn: "This is, in essence, the reward signal idea." → "This is, in essence, the reward signal idea, and the start of the trial-and-error thread."; summaryBg: "Това всъщност представлява идеята за сигнал за награда." → "Това всъщност е идеята за сигнал за награда и началото на нишката на обучението чрез проба и грешка."
  - summaryEn: "A third thread came from **trial-and-error learning** in early AI research — Samuel's checkers program (1959)[^samuel1959] learned by playing against itself, adjusting its evaluation function based on wins and losses." → "A third, less distinct thread concerned **temporal-difference** methods: Samuel's checkers program (1959)[^samuel1959] learned by playing against itself, moving its evaluation of a position towards the evaluations of the positions that followed."
  - summaryBg: "Трета нишка идва от **обучението чрез проба и грешка** в ранните изследвания в областта на изкуствения интелект - програмата за дама на Самюел (1959)[^samuel1959] се учи, като играе срещу себе си, коригирайки своята оценъчна функция въз основа на победи и загуби." → "Трета, по-слабо обособена нишка са методите на темпоралната разлика: програмата за дама на Самюел (1959)[^samuel1959] се учи, като играе срещу себе си, и приближава оценката на всяка позиция към оценките на следващите позиции."
  - summaryEn: "These threads stayed separate until the 1980s and 1990s. Sutton's PhD work on temporal-difference learning (1988)[^sutton1988] bridged the gap between animal learning theories and Bellman's dynamic programming. Then Watkins formalized Q-learning (1989),[^watkins1989] giving the field its first clean, model-free control algorithm with convergence guarantees." → "These threads came together in the late 1980s. Sutton (1988)[^sutton1988], building on his 1984 PhD thesis, separated temporal-difference learning from control and treated it as a general prediction method. Watkins's Q-learning (1989)[^watkins1989] then fully joined the temporal-difference and optimal-control threads, giving the field its first clean, model-free control algorithm; its convergence was proved in 1992."
  - summaryBg: "Тези нишки остават отделни до 80-те и 90-те години на миналия век. Докторската работа на Сътън върху обучението с темпорална разлика (1988)[^sutton1988] запълва празнината между теориите за животинското учене и динамичното програмиране на Белман. След това Уоткинс формализира Q-обучението (1989),[^watkins1989] предоставяйки на областта първия ясен, безмоделен алгоритъм за управление със сходимостни гаранции." → "Тези нишки се сливат в края на 80-те години на миналия век. Сътън (1988)[^sutton1988], продължавайки докторската си работа от 1984 г., отделя обучението с темпорална разлика от задачата за управление и го представя като общ метод за прогнозиране. Q-обучението на Уоткинс (1989)[^watkins1989] окончателно обединява нишките на темпоралната разлика и на оптималното управление и дава на областта първия ясен безмоделен алгоритъм за управление; сходимостта му е доказана през 1992 г."
  - footnote `sutton1988` (EN and BG): append "PhD thesis: Sutton, R.S. (1984). *Temporal Credit Assignment in Reinforcement Learning*. University of Massachusetts Amherst." / "Докторска дисертация: Sutton, R.S. (1984). *Temporal Credit Assignment in Reinforcement Learning*. University of Massachusetts Amherst."
- **Verified:** S&B 2nd ed., RLbook2020.pdf, §1.7 (pp. 13–21) and the reference list (Sutton 1984).

### F01-C05 · S2 · "Kuhn Poker with 12 states, DP is trivial"
- **Where:** summaryEn/Bg § 1.5.
- **Problem:** Kuhn poker has 12 *information sets* (6 per player; chapter 2 says so), not 12 states. As a two-player imperfect-information game it is not an MDP that DP solves, which is the point of the chapter's own § 1.4. Chapter 2 solves it with CFR.
- **Now → Proposed:** EN "For Kuhn Poker with 12 states, DP is trivial." → "For an MDP with a dozen states, DP is trivial."; BG "За Кун покер с 12 състояния DP е тривиален." → "За MDP с около дванадесет състояния DP е тривиален."

### F01-C06 · S2 · Stale chapter references
- **Where:** summaryEn/Bg §§ 1.4, 1.7.
- **Problem:** Chapter 5 is titled "Neural Networks for Imperfect-Information Games" / "Невронни мрежи за игри с непълна информация" in both bundles. Its own intro says it "widened from its original Deep CFR focus". Chapters 2–4 (CFR on Kuhn, MCCFR, abstraction) also deal with imperfect-information games, not only 5–8.
- **Now → Proposed:**
  - EN "will come in Chapter 5 (Neural Equilibrium Approximation)." → "will come in Chapter 5 (Neural Networks for Imperfect-Information Games)."; BG "ще бъде представено в Глава 5 (невронно приближение на равновесие)." → "ще бъде представено в Глава 5 (Невронни мрежи за игри с непълна информация)."
  - EN "because the later chapters (5–8) deal entirely with imperfect-information games." → "because Chapters 2–8 deal with imperfect-information games."; BG "защото следващите глави (5–8) се занимават изцяло с игри с **непълна информация**." → "защото главите от 2 до 8 се занимават с игри с непълна информация."
  - The one-pager's "стъпка" is in B22.

### F01-C07 · S2 · TRPO does not compute the Hessian, and PPO's gain is simplicity rather than compute
- **Where:** summaryEn/Bg § 1.8.
- **Problem:** TRPO solves its KL-constrained step with "the conjugate gradient algorithm followed by a line search, which is altogether only slightly more expensive than computing the gradient itself", and avoids forming the matrix (Schulman et al., 2015, §6 and App. C; checked in arXiv:1502.05477). So "(computing the Hessian)" and "substantially cheaper to compute" are inaccurate. The BG "изчислителна мощност" is also F07-T12.
- **Now → Proposed:**
  - EN "but TRPO requires expensive second-order optimization (computing the Hessian)." → "but TRPO has to solve a constrained second-order step (conjugate gradient on the Fisher matrix of the KL constraint, then a line search), which is complicated to implement."
  - BG "но TRPO изисква скъпа оптимизация от втори ред (изчисляване на хесиана)." → "но TRPO трябва да решава ограничена задача от втори ред (спрегнати градиенти върху матрицата на Фишер за ограничението по KL и последващо линейно търсене), което прави реализацията му сложна."
  - EN "It gets TRPO-like stability using only first-order gradients (no Hessian), making it substantially cheaper to compute and easier to implement." → "It gets TRPO-like stability with plain first-order stochastic gradient steps, which makes it much simpler to implement."
  - BG "Тя постига стабилност, сходна с тази на TRPO, като използва единствено градиенти от първи ред (без хесиан), което значително намалява необходимата изчислителна мощност и улеснява имплементацията ѝ." → "Тя постига стабилност, сходна с тази на TRPO, само с обикновени стохастични градиентни стъпки от първи ред, което значително опростява реализацията."

### F01-C08 · S2 · One-pager: "DQN's `max` and PPO's per-state policy are both ill-posed" over an information set
- **Where:** onePager.md / onePagerBg.md "**Open questions.**"
- **Problem:** A policy over information sets is well defined: NFSP runs DQN over them, for example. What breaks is that an action's value depends on the opponent's changing strategy, and a greedy argmax cannot represent a mixed strategy. Heinrich & Silver (2016, arXiv:1603.01121, abstract): on Leduc, "common reinforcement learning methods diverged".
- **Now → Proposed:**
  - EN (two source lines): "over an information set, DQN's `max` and PPO's per-state policy" → "over an information set, an action's value depends on the opponent's strategy, which keeps changing while it learns, and DQN's greedy `max`" and "are both ill-posed, which is why Chapter 2 changes tool rather than scale." → "cannot express the mixed strategies equilibrium play needs, which is why Chapter 2 changes tool rather than scale."
  - BG "върху информационно множество `max` на DQN и стратегията по състояния на PPO са и двете некоректно дефинирани, поради което глава 2 променя инструмента, а не мащаба." → "върху информационно множество стойността на действието зависи от стратегията на противника, която се променя, докато той се учи, а алчният `max` на DQN не може да изрази смесените стратегии, които изисква равновесната игра; затова глава 2 сменя инструмента, а не мащаба."

## S — Sources

### F01-S01 · S2 · SOURCE_GAPS row 1 (value-based vs policy-based methods) → cite Sutton & Barto, Ch. 13, and the algorithm papers
- **Where:** summaryBg.md § 1.2 — "**Методите, базирани на стойност** (като DQN) научават стойността на състоянията или двойките състояние-действие и извеждат стратегия въз основа на тези стойности."
- **Proposal (cite):** Add `[^dqn]` after "(като DQN" and `[^ppo]` after "(като PPO". Append `[^suttonbarto2018]` after the family sentence ("…научават самата стратегия директно.", after B03), and add Ch. 13 to that footnote (B27). EN the same. Verified in the book: the Ch. 13 opening reads "So far in this book almost all the methods have been action-value methods; they learned the values of actions and then selected actions based on their estimated action values … In this chapter we consider methods that instead learn a parameterized policy".

### F01-S02 · S2 · Shoham & Leyton-Brown footnote cites the wrong sections (F07-S05), and chapter 1's copy is the one the bundle prints
- **Where:** footnote `shoham2008` — "Гл. 3–4 (игри в нормална и разгърната форма); гл. 5 (игри в разгърната форма); §3.4 (изчисляване на равновесия) и §4.6 (изчисляване на най-добри отговори) - механизмът в последователна форма под всяка линейна програма в Глава 8;"
- **Problem:** Checked against masfoundations.org/toc.html. Ch. 4 is "Computing Solution Concepts of Normal-Form Games" (not extensive form). §3.4 is "Further solution concepts for normal-form games". §4.6 is "Computing correlated equilibria". The sequence form is §5.2.3 "Computing equilibria: the sequence form", inside §5.2 "Imperfect-information extensive-form games". Ch. 7 "Learning and Teaching" is correct. The publisher is missing. Crossref DOI 10.1017/CBO9780511811654 gives 2008-12-15.
- **Proposal (correct, EN and BG).** The text keeps chapter titles in English (comment #39) and serves all four chapters that share the label:
  - EN: "Ch. 3–4 (normal- and extensive-form games); Ch. 5 (extensive-form games); §3.4 (computing equilibria) and §4.6 (computing best responses), the sequence-form machinery underneath every LP in Chapter 8;" → "Cambridge University Press. DOI 10.1017/CBO9780511811654. Ch. 3 "Introduction to Noncooperative Game Theory: Games in Normal Form"; Ch. 4 "Computing Solution Concepts of Normal-Form Games" (§4.1, the LP for two-player zero-sum games); Ch. 5 "Games with Sequential Actions: Reasoning and Computing with the Extensive Form" (§5.2, imperfect-information games and information sets; §5.2.3, the sequence form underneath every LP in Chapter 8);"
  - BG: "Гл. 3–4 (игри в нормална и разгърната форма); гл. 5 (игри в разгърната форма); §3.4 (изчисляване на равновесия) и §4.6 (изчисляване на най-добри отговори) - механизмът в последователна форма под всяка линейна програма в Глава 8;" → "Cambridge University Press. DOI 10.1017/CBO9780511811654. Гл. 3 "Introduction to Noncooperative Game Theory: Games in Normal Form"; гл. 4 "Computing Solution Concepts of Normal-Form Games" (§4.1 - линейната програма за игри на двама с нулева сума); гл. 5 "Games with Sequential Actions: Reasoning and Computing with the Extensive Form" (§5.2 - игри с непълна информация и информационни множества; §5.2.3 - последователната форма, механизмът под всяка линейна програма в Глава 8);"
- This supersedes F07-S05's wording (which translated the chapter descriptions). Apply the same text to steps 02, 07 and 08, or fix F07-X01.

### F01-S03 · S2 · `mnih2015` footnote: wrong arXiv (it is Double DQN), a duplicate of `dqn`, and misplaced notes
- **Where:** summaryEn/Bg § 1.7 note and footnote `mnih2015` — "arXiv: <https://arxiv.org/abs/1509.06461>"; § 1.8 note ending "е отложено за Глава 5.[^ppo]".
- **Problem:** arXiv:1509.06461 is van Hasselt, Guez & Silver, "Deep Reinforcement Learning with Double Q-learning" (arXiv abstract page). The Nature DQN paper has no arXiv version, and its full reference is already in `[^dqn]`. Both "note on neural networks" paragraphs end with a citation that does not support their sentence, which is about deferring material to Chapter 5. These were added to answer the candidate's "източник" comments on the *first* mention.
- **Proposal (correct):** delete the `[^mnih2015]` reference and its definition; delete the `[^ppo]` at "Глава 5.[^ppo]" / "Chapter 5.[^ppo]"; add the DOI to `[^dqn]`: "*Nature*, 518(7540), 529-533." → "*Nature*, 518(7540), 529-533. DOI 10.1038/nature14236" (Crossref). Reuse arXiv:1509.06461 in S04 for Double DQN.

### F01-S04 · S2 · Unsourced technical claims (verified references to add)
- **Where / Proposal (cite).** The new labels are unique in the corpus (grep):
  - Double DQN, § 1.7: "(решено от Double DQN)" → "(проблем, който Double DQN[^vanhasselt2016] решава)"; EN "(addressed by Double DQN)" → "(addressed by Double DQN[^vanhasselt2016])". `[^vanhasselt2016]: van Hasselt, H., Guez, A. & Silver, D. (2016). "Deep Reinforcement Learning with Double Q-Learning." *Proceedings of the AAAI Conference on Artificial Intelligence*, 30(1). DOI 10.1609/aaai.v30i1.10295. arXiv:1509.06461` [Crossref + arXiv]
  - GAE, § 1.8: marker in B16; EN "Generalized Advantage Estimation (GAE)," → "Generalized Advantage Estimation (GAE)[^gae2016],". `[^gae2016]: Schulman, J., Moritz, P., Levine, S., Jordan, M. & Abbeel, P. (2016). "High-Dimensional Continuous Control Using Generalized Advantage Estimation." *ICLR 2016*. arXiv:1506.02438` [arXiv abstract page, venue in comments]
  - REINFORCE, § 1.8: "Основният алгоритъм **REINFORCE** страда" → "Основният алгоритъм REINFORCE[^williams1992] страда"; EN "The basic REINFORCE algorithm suffers" → "The basic REINFORCE algorithm[^williams1992] suffers". `[^williams1992]: Williams, R.J. (1992). "Simple statistical gradient-following algorithms for connectionist reinforcement learning." *Machine Learning*, 8(3–4), 229–256. DOI 10.1007/BF00992696` [Crossref]
  - POMDP, § 1.4: marker in B01; EN "**Partially Observable MDP** (POMDP)," → "**Partially Observable MDP** (POMDP)[^kaelbling1998],". `[^kaelbling1998]: Kaelbling, L.P., Littman, M.L. & Cassandra, A.R. (1998). "Planning and acting in partially observable stochastic domains." *Artificial Intelligence*, 101(1–2), 99–134. DOI 10.1016/S0004-3702(98)00023-X` [Crossref]
  - Deadly triad, § 1.7: marker in B03 (BG); EN "(the "deadly triad" of off-policy" → "(the "deadly triad"[^suttonbarto2018] of off-policy", with §11.3 added to the footnote (B27). [book §11.3]
  - SB3, § 1.9: "ги сравнихме със Stable-Baselines3 (SB3) - широко" → "ги сравнихме със Stable-Baselines3 (SB3)[^raffin2021] - широко"; EN "against Stable-Baselines3 (SB3) — a widely used" → "against Stable-Baselines3 (SB3)[^raffin2021] — a widely used". `[^raffin2021]: Raffin, A., Hill, A., Gleave, A., Kanervisto, A., Ernestus, M. & Dormann, N. (2021). "Stable-Baselines3: Reliable Reinforcement Learning Implementations." *Journal of Machine Learning Research*, 22(268), 1–8.` [jmlr.org paper page]
  - Sutton 1984 thesis: see C04.

### F01-S05 · S2 · Overclaim, unsourced: "PPO is the default choice for most RL applications today, including RLHF"
- **Where:** summaryEn/Bg § 1.8 "**Why PPO matters…**"
- **Proposal (soften + cite):**
  - EN "PPO is the default choice for most RL applications today, including RLHF for language models." → "PPO has become one of the most widely used deep RL algorithms; it was, for example, the optimizer in the original RLHF pipeline for instruction-following language models.[^ouyang2022]"
  - BG "PPO е предпочитаният избор за повечето RL приложения днес, включително RLHF за езикови модели." → "PPO се превърна в един от най-широко използваните алгоритми на дълбокото обучение с подкрепление; с него например е реализиран първоначалният RLHF процес за езикови модели, които следват инструкции.[^ouyang2022]"
  - `[^ouyang2022]: Ouyang, L., Wu, J., Jiang, X. et al. (2022). "Training language models to follow instructions with human feedback." arXiv:2203.02155.`
- **Verified:** paper text p. 2: "fine-tune our supervised learning baseline to maximize this reward using the PPO algorithm (Schulman et al., 2017)". "Most applications today" has no source and would date quickly.

### F01-S06 · S3 · Spot-check of the key citations
- **Checked correct:**
  - `thorndike1911`: title and year, per the S&B reference list and §1.7 quote of p. 244.
  - `bellman1957`: per the S&B reference list.
  - `samuel1959`: Crossref, 3(3) 210–229.
  - `sutton1988`: Crossref, 3(1) 9–44.
  - `watkins1989` and Watkins & Dayan 1992: Crossref, 8(3–4) 279–292.
  - `dqn` (2013): arXiv:1312.5602. Nature 2015: Crossref, 518(7540) 529–533.
  - `ppo`: arXiv:1707.06347, five authors in this order.
  - `trpo`: PMLR v37, 1889–1897. The author order Schulman, Levine, Abbeel, Jordan, Moritz is the PMLR order; arXiv lists Moritz third.
- **Claim checks:** "49 Atari games" matches the Nature abstract. "surpassing human performance on many of them" is fair: S&B §16.5 reports DQN better than the human tester on 22 games.

## X — Structure

### F01-X01 · S3 · Half-empty p. 16 and a stretched § 1.9 heading
- **Where:** bundle p. 16. The heading "Практическо валидиране - собствени имплементации спрямо Stable-Baselines3" is justified with wide gaps, and two lines of text follow. The rest of the page is blank because Fig. 1 (13 in wide) floats to p. 17.
- **Fix:** The smaller figure from G02 should fit on p. 16. Optionally shorten the heading: "## Практическо валидиране - собствени имплементации спрямо Stable-Baselines3" → "## Практическа проверка - собствени реализации срещу Stable-Baselines3" (curated: Validation → "Проверка" is more native; the chapter elsewhere says "реализация").
