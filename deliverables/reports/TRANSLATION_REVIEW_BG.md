# Ръчен преглед на българския превод

Архив на ръчния преглед. Авторът направи оставащите избори на 25.09.2026 г.;
решенията са записани и в `deliverables/finalReview/GLOSSARY_DECISIONS.md`.


## 1. Уеднаквена терминология (решено, приложено)

Тези избори са направени от автора и вече са приложени в целия корпус, в речника и в `terminology_EN_BG.md`. Броевете по-долу са проверка, че не е останал конкуриращ вариант.

| Понятие | Избран термин | Отхвърлени | Остатъци |
|---|---|---|---|
| reinforcement learning | **обучение с подкрепление** | обучение с подсилване | 0 ✓ |
| bucket (абстракция) | **клъстер** | кофа, кош | 0 ✓ |
| LLM agent | **агент с голям езиков модел** | LLM агент | 0 ✓ |
| critic | **оценител** | критик (самостоятелно) | 0 ✓ |
| free-for-all | **игри всеки срещу всеки** | FFA игри | 0 ✓ |
| game AI | **игрови изкуствен интелект** | изкуствен интелект в игрите | 0 ✓ |
| Leduc | **Ледюк (главна буква)** | Leduc, ледюк, Ледик | 0 ✓ |
| subgame | **подигра** | под-игра | 0 ✓ |

_Забележка: `актьор-критик` е запазено като устойчиво словосъчетание; етикетите `LLM` в таблици с резултати също са запазени, за да съвпадат с английския доклад и фигурите._


## 1б. Допълнителни избори (решено)

| Понятие | Избран вариант |
|---|---|
| Kuhn в българския текст | **Кун** (главна буква) |
| blueprint | **план**; „схема“ остава само когато означава диаграма или начин на действие |
| Hold'em в българския текст | **Холдем**; заглавията на английски статии остават в оригинал |
| self-play | **игра срещу себе си** |
| bootstrapping на стойности | **самоподкрепяне (bootstrapping)** при първа употреба |
| oracle (алгоритмичен) | **предсказвач** |
| имена на цитирани автори | латиница в текущия текст |
| имена на ботове и агенти | имената от кода и фигурите на латиница |

## 2. Заглавие в YAML срещу заглавие в текста

За глави 2, 4, 9, 10, 11 и 12 авторът избра формулировката от видимото заглавие.
Подзаглавието в YAML `title:` вече съвпада с нея във всеки от тези файлове.

## 3. Блокове, преведени с езиков модел

Девет цитатни блока бяха **оставени на английски** от основния превод (вашите коментари „Съгласуване“ / „Reconciliation“ / „Artifact caveat“). Преведени са автоматично и проверени машинно: числа, формули, имена и форматиране съвпадат с оригинала.

**Решение на автора:** българският текст на всичките девет блока (P1–P9) е одобрен.

Английският оригинал и българският превод са един до друг тук: [TRANSLATION_REVIEW_BLOCKS_BG.md](TRANSLATION_REVIEW_BLOCKS_BG.md)


## 4. Останал английски текст (вероятно умишлен)

**Решение на автора:** заглавията на статии и имената на автори в блоковете
„Прочетете повече“ остават на английски. Списъкът по-долу е архив на проверката.

- `step01/summary/summaryBg.md:30` > Безплатно: <http://incompleteideas.net/book/the-book-2nd.html>
- `step01/summary/summaryBg.md:52` > <https://spinningup.openai.com/en/latest/spinningup/rl_intro.html>
- `step01/summary/summaryBg.md:79` > Безплатно: <http://incompleteideas.net/book/the-book-2nd.html>
- `step01/summary/summaryBg.md:96` > Безплатно: <http://www.masfoundations.org/download.html>
- `step01/summary/summaryBg.md:115` > Безплатно: <http://incompleteideas.net/book/the-book-2nd.html>
- `step01/summary/summaryBg.md:140` > Безплатно: <http://incompleteideas.net/book/the-book-2nd.html>
- `step02/summary/summaryBg.md:26` > Безплатно: <http://www.masfoundations.org/download.html>
- `step02/summary/summaryBg.md:144` > **Прочетете повече:** Kuhn, H.W. (1950). "Simplified Two-Person Poker." *Contributions to the Theo
- `step03/summary/summaryBg.md:63` > **Прочетете повече:** Browne, C. и др. (2012). "A Survey of Monte Carlo Tree Search Methods." *IEE
- `step04/summary/summaryBg.md:158` > **Допълнителна литература:** <https://www.cs.cmu.edu/~gilpin/papers/extensive.JACM.pdf> · <https:/
- `step04/summary/summaryBg.md:200` > **Допълнително четене:** <https://www.cs.cmu.edu/~sandholm/imperfect_recall_abstraction.arxiv14.pd
- `step04/summary/summaryBg.md:241` > **Допълнителна литература:** <https://www.cs.cmu.edu/~gilpin/papers/extensive.JACM.pdf> · <https:/
- `step08/summary/summaryBg.md:194` > **Прочетете повече:** Ganzfried, S. & Sandholm, T. (2015), *op. cit.* - Theorem 1 is exactly the
- `step08/summary/summaryBg.md:195` > guarantee this table exhibits on Kuhn (най-лошият случай $\ge v^*$), and its minimax step is the
- `step09/summary/summaryBg.md:35` > **Прочетете повече:** Zhang, K., Yang, Z. & Başar, T. (2021). "Multi-Agent Reinforcement Learning:
- `step10/summary/summaryBg.md:100` > **Прочетете повече:** Balduzzi, D. и др. (2019). „Open-ended Learning in Symmetric Zero-sum Games“
- `step11/summary/summaryBg.md:33` > **Прочетете повече:** Nash, Shapley, Shubik & Hausner (1950s), *So Long Sucker* (the game itself);
- `step11/summary/summaryBg.md:76` > **Прочетете повече:** Shapley, L. S. (1953). "A value for n-person games." *Contributions to the T
- `step11/summary/summaryBg.md:77` > Games*; Chalkiadakis, Elkind & Wooldridge (2011), *Computational Aspects of Cooperative Game
- `step11/summary/summaryBg.md:106` > **Прочетете повече:** the Step 09 MARL stack (this repo) for MAPPO with a centralized critic; and 
- `step11/summary/summaryBg.md:107` > и др. (2022) on **piKL** - regularizing toward a behavioral prior instead of Nash, the n-играчен
- `step11/summary/summaryBg.md:129` > **Прочетете повече:** Balduzzi, D. и др. (2019). „Open-ended Learning in Symmetric Zero-sum Games“
- `step12/summary/summaryBg.md:42` > **Прочетете повече:** Paster, McIlraith & Ba, *You Can't Count on Luck: Why Decision Transformers 
- `step12/summary/summaryBg.md:63` > **Прочетете повече:** Tang, Zhang, Gu и др., *Adversarially Robust Decision Transformer*, NeurIPS 
- `step12/summary/summaryBg.md:92` > **Прочетете повече:** Guertler и др., *TextArena: A Framework for Text-Based Game Environments*, 2

_Общо: 25 реда._

## 5. Вече поправено машинно (не изисква преглед)

- `теглои` / `теглоите` → `тегла` / `теглата`
- `оракул` / `оракъл` → `предсказвач` (по ваше решение)
- `задна тегло` → `апостериорно тегло`
- `Людък` / `Людек` → `Ледюк`; `Leduc` → `Ледюк` в прозата
- разделител за хиляди → запетая (`264,192`)
- едностраничниците → `Резюме` (беше 5 различни термина)
- `подигра` / `подучастък` → `под-игра` (мнозинство 117 срещу 9)
- `Безопасно експлоатиране` / `използване на експлойти` → `Безопасна експлоатация`
- дълго и средно тире → обикновено тире (1,649 замени)
- 17 латински букви в кирилски думи (`неврoнното`, `играчeн`)
- 11 незатворени кавички „ ; баланс сега 459/459
- етикети `Read more` / `Прочетете още` → `Прочетете повече`
- 70 записа в речника + 9 за `под-игра`, записани в `glossary.db`
