# Преглед на блоковете, преведени автоматично

Тези девет блока бяха **оставени на английски** от основния превод. Преведени са автоматично с локален езиков модел и след това проверени машинно: числата, формулите в `$...$`, имената и Markdown форматирането съвпадат с оригинала.

**Какво се иска от вас:** прочетете българския текст отдясно и преценете дали *звучи като вас* и дали смисълът е верен. Машината провери фактите, но не и гласа. Това е единственото място в целия корпус, където текстът е написан от модел, а не от преводаческия процес.

Ако някой блок не ви харесва, кажете и го връщаме на английски или го пренаписвате ръчно.


---

## 1. `step01/report_bg.md`

**Оригинал (английски):**

```
**Methodology note:** "Best rolling-100 avg" is the maximum of the 100-episode moving
average over the entire training curve. This metric is fair regardless of ранно спиране:
it measures пикова способност, not where training happened to end. Step budgets are matched
(DQN: 750K, PPO: 500K).
```

**Превод (български):**

```
**Методологична бележка:** „Най-добра средна стойност (подвижна 100)“ е максимумът на 100-епизодния подвижен
среден по цялата крива на обучение. Тази метрика е справедлива независимо от ранно спиране:
тя измерва пиковата способност, а не къде обучението се е случило да приключи. Бюджетите за стъпки са съпоставени
(DQN: 750K, PPO: 500K).
```

---

## 2. `step09/summary/summaryBg.md`

**Оригинал (английски):**

```
**Съгласуване 1 (ледюк).** I predicted PSRO would drive Leduc exploitability below $0.5$
within 20 iterations. Measured, it fell from $4.75$ to $2.16$ — a clear, roughly monotone
decline, but nowhere near $0.5$. This is **genuine slow convergence**, not a bug: Kuhn hit
machine zero in 6 rounds, but Leduc's game tree is far larger, and a population of 20 *pure*
best responses is simply too small to closely approximate its mixed Nash. The "< 0.5 in 20"
target was optimistic. The lesson — exploitability decreases as the population grows — holds;
the *rate* is the scaling wall, and it rhymes with Step 8's global-vs-local scaling finding.
```

**Превод (български):**

```
**Съгласуване 1 (Ледюк).** Прогнозирах, че PSRO ще намали експлоатируемостта на Ледюк под $0.5$ в рамките на 20 итерации. Измерено, тя спадна от $4.75$ до $2.16$ - ясно, приблизително монотонно намаление, но далеч от $0.5$. Това е **истинска бавна сходимост**, а не грешка: Кун достигна машинна нула за 6 рунда, но игровото дърво на Ледюк е много по-голямо и популация от 20 *чисти* най-добри отговора просто е твърде малка, за да апроксимира плътно неговия смесен Наш. Целта „< 0.5 за 20“ беше оптимистична. Изводът - експлоатируемостта намалява с нарастването на популацията - остава валиден; *скоростта* е мащабиращата пречка и тя се вписва в откритието от Стъпка 8 за глобално спрямо локално мащабиране.
```

---

## 3. `step09/summary/summaryBg.md`

**Оригинал (английски):**

```
**Съгласуване 2 (Goofspiel $K=4$).** I predicted non-increasing exploitability. At $K=3$
it converged to $0$ чисто; at $K=4$ it oscillates between $\sim\!1.4$ and $\sim\!2.0$ and
does not settle. This is the one result I cannot yet fully explain, and per the workflow I am
**documenting it, not fixing it**. Two concrete suspects for a follow-up session: the
Goofspiel PSRO driver never de-duplicates best-response policies (so the meta-game can stall
on repeats), and a pure-strategy population is likely too weak to represent the larger game's
mixed meta-Nash. Flagged as an open code item, not a validated result.
```

**Превод (български):**

```
**Съгласуване 2 (Goofspiel $K=4$).** Прогнозирах намаляваща експлоатируемост. При $K=3$ тя се сближи до $0$ напълно; при $K=4$ тя осцилира между $\sim\!1.4$ и $\sim\!2.0$ и не се установява. Това е единственият резултат, който все още не мога да обясня напълно и съгласно работния процес аз го **документирам, а не го коригирам**. Две конкретни подозрения за последваща сесия: драйверът на PSRO за Goofspiel никога не премахва дублиращите се стратегии за най-добър отговор (така че мета-играта може да спре поради повторения) и популация от чисти стратегии вероятно е твърде слаба, за да представи смесения мета-Наш на по-голямата игра. Маркирано като отворен елемент в кода, а не като валидиран резултат.
```

---

## 4. `step10/summary/summaryBg.md`

**Оригинал (английски):**

```
**Reconciliation (kept prediction → what actually happened).** I framed poker as a skill ladder and
expected Leduc's meta-game to be mostly transitive. Measured, it depends entirely on *which
population you decompose*. A population of **best responses** (PSRO) is mostly **cyclic**
($\approx0.45$ transitive, 27 three-cycles): the best response beats the current mixture, a newer
best response beats *that*, and so on — Balduzzi's spinning-top in action. A population of
**моментни снимки на траекториите на обучение** (the league) is mostly **transitive** ($\approx0.94$-$0.98$),
because later snapshots are usually stronger than earlier ones, forming a ladder. Neither is a bug;
the transitive/cyclic ratio is a property of the *population*, and choosing how you build the
population is choosing whether you see a wheel or a ladder.
```

**Превод (български):**

```
**Съгласуване (запазена прогноза -> това, което действително се случи).** Аз формулирах покера като стълбица на уменията и очаквах мета-играта на Ледюк да бъде предимно транзитивна. Измерено, тя зависи изцяло от *коя популация разложите*. Популация от **най-добри отговори** (PSRO) е предимно **циклична** ($\approx0.45$ транзитивна, 27 трицикъла): най-добрият отговор побеждава текущата смес, по-нов най-добър отговор побеждава *него*, и така нататък - въртящият се пумпал на Balduzzi в действие. Популация от **моментни снимки на траекториите на обучение** (лигата) е предимно **транзитивна** ($\approx0.94$-$0.98$), защото по-късните моментни снимки обикновено са по-силни от по-ранните, образувайки стълбица. Нито едното не е грешка; съотношението транзитивно/циклично е свойство на *популацията*, а изборът как да изградите популацията е избор дали ще видите колело или стълбица.
```

---

## 5. `step10/summary/summaryBg.md`

**Оригинал (английски):**

```
**Съгласуване (kept prediction → what actually happened).** I predicted a *monotone* decrease in
експлоатируемост. Smoke's 15 epochs oblige — a clean drop that ends at its minimum. But scale's 120
epochs tell the real story: exploitability falls steeply to a minimum near epoch 60 (минимална експлоатируемост при основен отговор
$\approx1.21$, мета-Наш равновесие bottoming $\approx1.32$ then holding a $\approx1.60$ plateau), and then
**regresses** back up to $\approx2.05$ / $\approx2.96$ by epoch 119. The best agents are the *frozen
snapshots* from mid-run; the *live* основни агенти се влошават късно, преследвайки своите експлоатьори (churn /
частично забравяне). This is only visible once training is long enough — a непрекъсната лига is not a
monotonically improving one. The remedy (untested here) is съхраняване на най-добрия модел / population
регуляризация. Methodologically it echoes Step 9: **scale reveals what smoke hides.**
```

**Превод (български):**

```
**Съгласуване (запазена прогноза -> какво всъщност се случи).** Прогнозирах *монотонно* намаляване на
експлоатируемостта. Smoke's 15 епохи се подчиняват - чисто спадане, което завършва в своя минимум. Но scale's 120
епохи разказват истинската история: експлоатируемостта пада рязко до минимум около епоха 60 (минимална експлоатируемост при основен отговор
$\approx1.21$, мета-Наш равновесие достига дъно $\approx1.32$ и след това поддържа плато $\approx1.60$), и след това
**регресира** обратно до $\approx2.05$ / $\approx2.96$ към епоха 119. Най-добрите агенти са *замразените
моментни снимки* от средата на изпълнението; *активните* основни агенти се влошават късно, преследвайки своите експлоатьори (churn /
частично забравяне). Това е видимо само когато обучението е достатъчно дълго - една непрекъсната лига не е
монотонно подобряваща се. Лекарството (нетествано тук) е съхраняване на най-добрия модел / регуляризация на популацията. Методологически това отразява Стъпка 9: **мащабът разкрива това, което smoke скрива.**
```

---

## 6. `step11/summary/summaryBg.md`

**Оригинал (английски):**

```
**Съгласуване (kept prediction -> what actually happened).** I predicted a symmetric position
would give a symmetric credit spread ($<0.15$). The first run gave $0.54$ — a red FAIL — with
Player 0 winning ~2x its fair share across three independent scripts. Suspecting the engine before
the prediction, I found the mechanism: **~99.5% of random SLS games end in a deadlock** (all live
hands empty), so the winner is decided by a most-chips **tie-break** — whose lowest-index rule
quietly handed seat 0 its edge. An **unbiased random tie-break** fixed it: symmetric spread
$0.54\to 0.013$, all-random winners now uniform. It also revealed that an impressive $\sim 0.87$
hero win-rate had been the *same* artifact (the hero always sat in seat 0); the fair number is
$\sim 0.41$. The lesson: in a game that almost always ends in a near-tie, the tie-break rule is the
most load-bearing line in the engine, and a symmetric *position* is not a symmetric *outcome* until
it is unbiased.
```

**Превод (български):**

```
**Съгласуване (запазена прогноза -> какво всъщност се случи).** Прогнозирах, че симетрична позиция
ще даде симетрично разпределение на кредита ($<0.15$). Първото изпълнение даде $0.54$ - червен FAIL - с
Играч 0 печелещ ~2x своя справедлив дял в три независими скрипта. Подозрявайки механиката преди
прогнозата, открих механизма: **~99.5% от случайните SLS игри завършват със задънена улица** (всички живи
ръце празни), така че победителят се решава чрез най-много чипове **развръзка при равенство** - чието правило с най-нисък индекс тихо даде предимство на място 0. **Безпристрастна случайна развръзка при равенство** го поправи: симетрично разпределение $0.54\to 0.013$, победителите вече са равномерни. Това също разкри, че впечатляващ $\sim 0.87$ процент на победа на героя е бил *същият* артефакт (героят винаги е седял на място 0); справедливият брой е
$\sim 0.41$. Урокът: в игра, която почти винаги завършва с почти равенство, правилото за развръзка при равенство е най-натовареният ред в механиката, и симетрична *позиция* не е симетричен *изход*, докато не бъде безпристрастна.
```

---

## 7. `step11/summary/summaryBg.md`

**Оригинал (английски):**

```
**Съгласуване (запазена прогноза -> какво всъщност се случи).** My single-config runs used the
default $\alpha=0.3$ and showed the coalition signal collapse at scale — which I first read as "the
proxy credit is too weak once training is longer." The sweep overturned that completely: **$\alpha$
is the dominant knob, and $0.3$ is a dead zone.** Coalitions emerge significantly *only at low
$\alpha$* (at $\alpha\approx 0$ the Shapley agent beats sparse by $+0.038$, ~4.4x), while *every*
$\alpha\ge 0.3$ cell is negative — the sparse всичко или нищо term drowns the coalition signal.
Two further surprises: the effect **grows with game size** (opposite to my "smoke-positive /
scale-null" read, which was an artifact of holding $\alpha=0.3$ at both tiers), and the **cheap
proxy beats the expensive контрафактичен**. So the primary thesis signal (коалиционно формиране) is
real and robust — I had simply measured it in the one regime where the sparse term hides it. The
fix is "weight the coalition credit heavily," not "compute a truer credit."
```

**Превод (български):**

```
**Съгласуване (запазена прогноза -> какво всъщност се случи).** Моите експерименти с един конфигурационен файл използваха стойността по подразбиране $\alpha=0.3$ и показаха, че коалиционният сигнал изчезва при мащаб - което първоначално тълкувах като „прокси кредитът е твърде слаб, когато обучението е по-дълго“. Прегледът на параметрите напълно обърна това: **$\alpha$ е доминиращият параметър, а $0.3$ е мъртва зона.** Коалиции възникват значително *само при ниски стойности на $\alpha$* (при $\alpha\approx 0$ агентът Shapley побеждава оскъдната базова линия с $+0.038$, ~4.4x), докато *всяка* клетка с $\alpha\ge 0.3$ е отрицателна - оскъдният всичко или нищо член заглушава коалиционния сигнал.
Две допълнителни изненади: ефектът **нараства с размера на играта** (обратното на моето „smoke-положително / мащаб-нула“ тълкуване, което беше артефакт от фиксирането на $\alpha=0.3$ и на двете нива), и **евтиният прокси побеждава скъпия контрафактичен**. Така че основният сигнал на тезата (коалиционно формиране) е реален и устойчив - просто го измерих в единствения режим, в който оскъдният член го скрива. Решението е „да се придаде голяма тежест на коалиционния кредит“, а не „да се изчисли по-точен кредит“.
```

---

## 8. `step11/summary/summaryBg.md`

**Оригинал (английски):**

```
**Reconciliation (kept prediction -> what actually happened).** I expected a large cyclic
component and, at first, saw a near-perfect skill ladder (cyclic $\sim 0.07$). That was partly the
seat-0 bug (the *Shapley credit* section) and partly **pool composition**: the default baseline pool *is* a skill ladder. A
coalition pool (fixed-ally + betrayer strategies) pushes the cyclic ratio to $\sim 0.57$-$0.69$ — a
large нетранзитивна компонента, която силно потвърждава *посоката* на прогнозата, но остава
**честно под строго доминиране** (cyclic$^2$ малко под $0.5$). Основният заподозрян за
остатъка е, че **2-type projection discards 3-/4-player coalition effects** — a tensor-native
decomposition is the open question. Neither reading is a bug; which population you build decides
whether SLS looks like a wheel or a ladder.
```

**Превод (български):**

```
**Съгласуване (запазена прогноза -> какво всъщност се случи).** Очаквах голяма циклична компонента и първоначално видях почти перфектна стълба на умения (cyclic $\sim 0.07$). Това беше отчасти грешката в seat-0 (разделът *Shapley credit*) и отчасти **съставът на популацията**: базовата популация по подразбиране *е* стълба на умения. Популация с коалиции (фиксиран съюзник + стратегии „предател“) повишава цикличното съотношение до $\sim 0.57$-$0.69$ - голяма нетранзитивна компонента, която силно потвърждава *посоката* на прогнозата, но остава **честно под строго доминиране** (cyclic$^2$ малко под $0.5$). Основният заподозрян за остатъка е, че **2-type projection discards 3-/4-player coalition effects** - разлагане, естествено за тензори, е отвореният въпрос. Нито едното тълкуване не е грешка; коя популация изграждаш решава дали SLS изглежда като колело или стълба.
```

---

## 9. `step12/report_bg.md`

**Оригинал (английски):**

```
**Artifact caveat (read once).** Two results were **retracted mid-session** and appear here only
as retractions: an in-context-learning result of `+1.59` gap closed (impossible — see §Prediction
vs reality, R5) and a ледюк LLM score of `−0.83` жетони/ръка produced by a faulty decoder (R6).
The Nash reference differs by CFR budget — `0.0162` жетони at 5,000 iterations (comparison table),
`0.0061` at 50,000 (follow-on experiments); both are ≈0. OpenThinker3's `plain`-prompt row is not
comparable to its CoT row (34% of its probability mass goes to non-action tokens under a plain
prompt).

**How to read this report.** The core build answers the raw step's five validation targets. The
follow-on experiments were added because those five targets rank the methods without explaining
them. Every claim is tied to a named artifact under `implementation/step12/implementation/`.
```

**Превод (български):**

```
**Забележка относно артефакта (прочетете веднъж).** Два резултата бяха **оттеглени по време на сесията** и се появяват тук само като оттегляния: резултат от обучение в контекста с намалена разлика от `+1.59` (невъзможно - виж §Прогноза срещу реалност, R5) и резултат за Ледюк Холдем от голям езиков модел от `−0.83` жетона/ръка, получен чрез дефектен декодер (R6). Референтният Nash се различава според бюджета на CFR - `0.0162` жетона при 5,000 итерации (сравнителна таблица), `0.0061` при 50,000 (последващи експерименти); и двете стойности са ≈0. Редът с `plain`-подкана на OpenThinker3 не е сравним с реда му с CoT (34% от вероятностната му маса отива към токени, които не са действия при обикновена подкана).

**Как да четете този доклад.** Основният набор от резултати отговаря на петте цели за валидиране на суровата стъпка. Последващите експерименти бяха добавени, защото тези пет цели класират методите, без да ги обясняват. Всяко твърдение е свързано с именуван артефакт в `implementation/step12/implementation/`.
```
