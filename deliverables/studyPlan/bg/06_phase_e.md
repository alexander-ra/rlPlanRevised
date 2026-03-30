## 6. Етап E — Многоагентни динамики (Стъпки 9–11)

### 6.1 Преглед на етапа

Предишните етапи се фокусираха върху игри с несъвършена информация за двама играчи. Етап E ще прехвърли изследването към многоагентни среди (multi-agent settings), където възникват нови предизвикателства: нестационарност^36^ от едновременно обучаващи се агенти, разпределяне на заслугите (credit assignment) в среди със съвместни награди и появата на коалиции^41^. Стъпка 9 въвежда парадигми за многоагентно обучение с подкрепление (MARL), като CTDE^37^ и PSRO^38^, Стъпка 10 преминава към мащабиране чрез базирано на популация обучение^39^ и еволюционна теория на игрите, а Стъпка 11 прилага тези инструменти към формирането на коалиции в игри "всеки срещу всеки" (free-for-all) — изкристализирайки теоретичната празнина, която лежи в сърцевината на Принос 2.

### 6.2 Стъпка 9 — Многоагентно обучение с подкрепление (MARL) — Координация, конкуренция и комуникация

**Връзка с приносите.** Тази стъпка ще предостави алгоритмичния речник за разширяване на дисертацията от сценарии с двама играчи към многоагентни среди. Парадигмата CTDE^37^ въвежда архитектурния модел — централизирано обучение, децентрализирано изпълнение — използван в останалата част от дисертацията. Алгоритъмът PSRO^38^ предоставя базирана на популации рамка, свързана с дефинирането на безопасност в многоагентни популации (Принос 2). LOLA^40^ допринася с идеята за моделиране на динамиката на обучение на противника, разширявайки байесовото моделиране от Стъпка 7 от статичен извод към динамично предвиждане (Принос 1).

**Литература.**

1. Lowe, R., Wu, Y., Tamar, A., Harb, J., Abbeel, P. and Mordatch, I. (2017). "Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments." *Advances in Neural Information Processing Systems (NeurIPS).*
2. Rashid, T., Samvelyan, M., de Witt, C.S., Farquhar, G., Foerster, J. and Whiteson, S. (2018). "QMIX: Monotonic Value Function Factorisation for Deep Multi-Agent Reinforcement Learning." *Proceedings of the International Conference on Machine Learning (ICML).*
3. Yu, C., Velu, A., Vinitsky, E., Gao, J., Wang, Y., Baez, A. and Fishi, S. (2022). "The Surprising Effectiveness of PPO in Cooperative Multi-Agent Games." *Advances in Neural Information Processing Systems (NeurIPS).*
4. Foerster, J., Chen, R.Y., Al-Shedivat, M., Whiteson, S., Abbeel, P. and Mordatch, I. (2018). "Learning with Opponent-Learning Awareness." *Proceedings of the International Conference on Autonomous Agents and Multiagent Systems (AAMAS).*
5. Lanctot, M., Zambaldi, V., Gruslys, A., Lazaridou, A., Tuyls, K., Pérolat, J., Silver, D. and Graepel, T. (2017). "A Unified Game-Theoretic Approach to Multiagent Reinforcement Learning." *Advances in Neural Information Processing Systems (NeurIPS).*
6. Sukhbaatar, S., Szlam, A. and Fergus, R. (2016). "Learning Multiagent Communication with Backpropagation." *Advances in Neural Information Processing Systems (NeurIPS).*

**Практически задачи.**

- Конструиране на тестова среда с матрични игри (Дилемата на затворника (Prisoner's Dilemma), Съвпадащи монети (Matching Pennies), Лов на елен (Stag Hunt), Битка на половете (Battle of the Sexes)) с математически доказани равновесия на Наш.
- Имплементиране на независими PPO агенти като база за сравнение (baseline), демонстрираща провалите, дължащи се на нестационарност^36^ в многоагентни среди.
- Имплементиране на MADDPG (централизиран критик, децентрализирани актьори) и MAPPO (PPO с централизирана функция на стойността) като представители на CTDE^37^.
- Имплементиране на PSRO^38^ с базирано на популацията изчисление на мета-Наш (meta-Nash) и оракул (oracle) за най-добър отговор, базиран на обучение с подкрепление (RL); верифициране на сходимостта към равновесие на Наш върху Kuhn Poker^19^ и Leduc Hold'em^20^.
- Интегриране на диференцируем комуникационен канал CommNet с MADDPG; оценяване на ползата от емергентната комуникация при кооперативни задачи.
- Изготвяне на таблица със сравнителна оценка: независимо обучение спрямо CTDE спрямо PSRO във всички тестови среди и в играта Goofspiel.

### 6.3 Стъпка 10 — Базирано на популация обучение и Еволюционна теория на игрите

**Връзка с приносите.** Базираното на популация обучение (Population-based training, PBT) и архитектурата на лигата AlphaStar ще бъдат изследвани като примери за имплицитно моделиране на противника в мащаба на популацията, допълвайки експлицитното байесово моделиране от Стъпка 7 (Принос 1). Декомпозицията "пумпал" (spinning top decomposition)^42^ — отличаваща реалното подобряване на уменията от нетранзитивното циклиране — ще бъде възприета в методологията за оценка (Принос 3). Емпиричният игрово-теоретичен анализ (EGTA^43^) ще предостави анализ на мета-Наш равновесието, разширявайки оценката на експлоатируемостта към популационни постановки.

**Литература.**

1. Jaderberg, M., Dalibard, V., Osindero, S., Czarnecki, W.M. et al. (2017). "Population Based Training of Neural Networks." *Препринт.*
2. Jaderberg, M., Czarnecki, W.M., Dunning, I. et al. (2019). "Human-Level Performance in First-Person Multiplayer Games with Population-Based Deep Reinforcement Learning." *Science*, 364(6443), pp. 859–865.
3. Vinyals, O., Babuschkin, I., Czarnecki, W.M. et al. (2019). "Grandmaster Level in StarCraft II Using Multi-Agent Reinforcement Learning." *Nature*, 575(7782), pp. 350–354.
4. Balduzzi, D., Garnelo, M., Bachrach, Y., Czarnecki, W.M., Pérolat, J., Jaderberg, M. and Graepel, T. (2019). "Open-Ended Learning in Symmetric Zero-Sum Games." *Proceedings of the International Conference on Learning Representations (ICLR).*
5. Tuyls, K., Pérolat, J., Lanctot, M. et al. (2018). "A Generalised Method for Empirical Game Theoretic Analysis." *Proceedings of the International Conference on Autonomous Agents and Multiagent Systems (AAMAS).*
6. Hofbauer, J. and Sigmund, K. (2003). "Evolutionary Game Dynamics." *Bulletin of the American Mathematical Society*, 40(4), pp. 479–519.

**Практически задачи.**

- Имплементиране на симулатор на репликаторна динамика (replicator dynamics) върху матрични игри; верифициране на сходимост към равновесия на Наш и еволюционно стабилни стратегии за игрите Дилемата на затворника (Prisoner's Dilemma), Ястреб и гълъб (Hawk-Dove) и Лов на елен (Stag Hunt), както и циклиране при Камък-Ножица-Хартия. Генериране на фазови портрети.
- Имплементиране на декомпозицията "пумпал"^42^ (Balduzzi et al., 2019); прилагане към матриците на печалбите (payoff matrices) в мета-играта PSRO^38^ от Стъпка 9 и към мета-играта на лигата от тази стъпка. Изчисляване на транзитивното съотношение (transitive ratio) като диагностична метрика.
- Изграждане на PBT лига за Leduc Hold'em^20^ с три роли на агенти (основни агенти, основни експлоататори, експлоататори на лигата), приоритизирано намиране на мачове (matchmaking), периодично "замразяване" на агенти и обновления на популацията тип "изследване-експлоатация" (explore-exploit).
- Провеждане на EGTA^43^ анализ: конструиране на емпиричната формална игра върху популацията на лигата и изчисляване на мета-Наш равновесието; проверка дали експлоатируемостта на мета-Наш сместа (meta-Nash mixture) не превишава тази на най-добрия индивидуален агент.
- Провеждане на сравнителна оценка: лига срещу PSRO (Стъпка 9) срещу единичен агент, обучаващ се чрез самоигра, срещу MCCFR^23^ стратегия на Наш (Стъпка 3), с измерване на експлоатируемост, Ело рейтинг, ефективно разнообразие на популацията и клъстеризиране на стратегиите.

### 6.4 Стъпка 11 — Динамично формиране на коалиции в конкурентни игри "Всеки срещу всеки"

**Връзка с приносите.** Тази стъпка изкристализира централната теоретична празнина на дисертацията. При игри с двама играчи безопасната експлоатация използва равновесието на Наш като еталон за безопасност (Стъпка 8). При free-for-all игри с N играчи равновесието на Наш е едновременно изчислително непостижимо и стратегически недостатъчно — то игнорира коалиционните структури. Регуляризационният подход piKL на Bakhtin et al. (2022) предполага замяна на безопасността, базирана на равновесие, с безопасност, базирана на поведенчески априорни вероятности (behavioral-prior-based safety) – преход, който Принос 2 ще се стреми да формализира. Разпознаването на коалиции ще разшири моделирането на противника от индивидуални типове играчи към многоагентна социална структура (Принос 1). Декомпозицията на стойностите на Shapley^44^ (Shapley-value credit decomposition), комбинирана с EGTA^43^, ще предостави основата за N-плейърната методология за оценка (Принос 3).

**Литература.**

1. Sharan, M. and Adak, C. (2024). "Reinforcing Competitive Multi-Agents for Playing 'So Long Sucker'." *Препринт.*
2. De Carufel, J.-L. and Jerade, M.R. (2024). "So Long Sucker: Endgame Analysis." *Препринт.*
3. Bakhtin, A., Wu, D.J., Lerer, A., Gray, J., Jacob, A.P., Farina, G., Miller, A.H. and Brown, N. (2022). "Mastering the Game of No-Press Diplomacy via Human-Regularized Reinforcement Learning and Planning." *Препринт.*
4. Chalkiadakis, G., Elkind, E. and Wooldridge, M. (2011). *Computational Aspects of Cooperative Game Theory.* Morgan and Claypool.
5. Wang, J., Zhang, Y., Kim, T.-K. and Gu, Y. (2020). "Shapley Q-value: A Local Reward Approach to Solve Global Reward Games." *Proceedings of the 34th AAAI Conference on Artificial Intelligence.*

**Практически задачи.**

- Изграждане на верифицирана среда за играта So Long Sucker^45^ с проследяване на коалициите, богато представяне на състоянията и валидиране на коректността спрямо анализа на ендгейм (endgame analysis) от De Carufel и Jerade (2024).
- Имплементиране на модул за засичане на коалиции, който извлича имплицитни съюзи въз основа на наблюдаваното поведение при поставяне на чипове (chip-placement) чрез използване на матрици за помощ/вреда, с което моделирането на противника от Стъпка 7 се разширява до многоагентен извод за съюзи.
- Адаптиране на Shapley Q-value^44^ декомпозиция към конкурентна среда "всеки срещу всеки", разпределяйки заслугата (credit) за всяко действие сред всички играчи според маргиналните им коалиционни приноси.
- Обучение чрез самоигра на MAPPO агенти за четирима играчи със Shapley-декомпозирани награди; сравнение със стандартна базова линия с редки награди (sparse-reward baseline), репликираща Sharan и Adak (2024).
- Прилагане на EGTA^43^ (от Стъпка 10) за конструиране на тензора на печалбите за четирима играчи и изчисляване на мета-Наш върху популацията агенти; прилагане на декомпозицията "пумпал"^42^ за количествено измерване на нетранзитивната структура на коалиционните динамики.
- Изготвяне на сравнителна оценка: агенти, осъзнаващи коалиции, срещу агенти с редки награди, срещу случайни базови линии, измервайки процент победи, честота на формиране на коалиции, Shapley вариация и продължителност на играта.