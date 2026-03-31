# Step 13 — Behavioral Analysis Pipelines + Real-World Data

**Duration:** 14 days (Tier 2)  
**Dependencies:** Step 7 (Opponent Modeling), Step 12 (Sequence Models + LLM Agents)  
**Phase:** F — Data-Driven Approaches  
**Freshness Note:**  
- ArXiv search: '"behavioral cloning" poker player modeling' (Mar 2026) — 0 results. Confirms the field remains niche; most poker behavioral work is in industry, not academic preprints.  
- ArXiv search: "collusion detection online poker" (Mar 2026) — 0 results. Collusion detection in poker is almost entirely industry-internal (Playtech, PokerStars, etc.) with very few public papers.  
- ArXiv search: "poker player style classification machine learning" (Mar 2026) — 0 results.  
- ArXiv search: "collusion detection multiplayer game anomaly" (Mar 2026) — 0 results.  
- ArXiv search: "fraud detection online gaming behavioral anomaly" (Mar 2026) — 0 results.  
- ArXiv search: "player modeling game behavior representation learning" (Mar 2026) — 9 results. Relevant:  
  - Wang et al. (Apr 2024) "player2vec: A Language Modeling Approach to Understand Player Behavior in Games" (arXiv:2404.04234) — **directly relevant.** Extends a long-range Transformer to player behavior data. In-game events treated as words in sentences → self-supervised player representation learning. Learns embeddings that capture behavioral patterns. *Core — the closest published work to what this step builds for poker.*  
  - Kim et al. (Jan 2025, ICPR 2024) "A Framework for Mining Collectively-Behaving Bots in MMORPGs" (arXiv:2501.10461) — Trajectory representation learning + DBSCAN clustering to detect bot collectives. *Supplementary — relevant methodology for detecting coordinated (colluding) players in poker, same principle: learn embeddings → cluster → flag anomalous groups.*  
- ArXiv search: "offline reinforcement learning behavioral data imitation game" (Mar 2026) — 4 results. Relevant:  
  - Kumar, Hong, Singh & Levine (Apr 2022, ICLR 2022) "When Should We Prefer Offline Reinforcement Learning Over Behavioral Cloning?" (arXiv:2204.05618) — **critical for this step.** Characterizes when offline RL outperforms BC: sparse rewards, noisy data, long horizons. Poker has all three. *Core — directly answers the design question: should the Playtech pipeline use BC or offline RL?*  
- Known foundational papers (not found via keyword search — most are domain-specific or conference proceedings):  
  - DeLong & Bhatt (2020) "Towards Collusion Detection in Poker" — pattern-based collusion detection. *Referenced in oldSources/docPlan_EN.md.*  
  - Yan & Browne (2016) "Collusion Detection in Online Poker" — statistical approaches. *Referenced in oldSources/docPlan_EN.md.*  
  - Johanson et al. (2009) "Data-Biased Robust Counter Strategies" — exploiting behavioral data. *Already covered in Step 7.*  
  - Southey et al. (2005) "Bayes' Bluff: Opponent Modelling in Poker" — Bayesian player modeling. *Already covered in Step 7.*  
  - Ganzfried & Sun (2016/2018) "Bayesian Opponent Exploitation in Imperfect-Information Games" — *Already covered in Step 7; referenced for continuity.*  
- Cross-reference from Step 12: Poker state tensor encoding (cards, position, pot, stacks, betting history) prototyped on Kuhn/Leduc data → this step applies it to Playtech data. Paster et al. (2022) stochasticity warning → must condition on decision EV, not raw outcomes.  
- Cross-reference from Step 11: Coalition detector (help/harm matrices) as collusion detection prototype. Prediction logged in Step 11's Learning Log: the same behavioral inference principle transfers to real poker data.  
- Cross-reference from Step 7: Bayesian opponent model (hand range inference from actions) provides the methodological foundation for player behavior modeling.  
- Field assessment: **Behavioral analysis of real poker data is overwhelmingly industry-internal. The academic literature on poker player modeling is sparse (Southey 2005, Ganzfried 2016, a few others) and the collusion detection literature is nearly nonexistent publicly. The biggest recent development is player2vec (Wang et al., 2024: representation learning from game behavior data via Transformers) which directly validates this step's approach. The Kumar et al. (2022) BC vs offline RL paper provides critical guidance for pipeline design. This step's Playtech data work has PhD NOVELTY potential — very few public demonstrations of ML on real poker behavioral data exist.**

---

> **Contribution Alignment:** This step will apply the behavioral adaptation methodology from Steps 7, 8, and 12 to anonymized industry data, providing practical validation for Contribution 1. The behavioral deviation from equilibrium play measured on real player data will quantify exploitation opportunities relevant to Contribution 2.


## Phase 1: Intuition (1 day)

The goal: understand WHY real-world behavioral data is different from simulated data (and harder), WHAT you can extract from poker hand histories (player styles, anomalies, collusion signals), and HOW this connects everything from Steps 7–12 into a practical pipeline. The key mental shift: in Steps 2–11, you've been building game solvers and opponent models. Now you flip the perspective — instead of computing WHAT the optimal strategy is, you analyze WHAT actual humans DO, and use the gap between their behavior and theory to classify, model, and detect anomalies.

End of day: you should be able to explain to a non-expert: "Online poker sites like Playtech record every hand played — who bet, how much, who folded, who won. That's millions of hands. From this data, we can learn: (1) what kind of player someone is — aggressive vs passive, loose vs tight, predictable vs erratic; (2) whether someone is playing suspiciously — maybe two accounts are controlled by the same person and they're helping each other at the same table (collusion); and (3) whether a bot is playing instead of a human, because bots behave with inhuman consistency. To do all this, we need a DATA PIPELINE that converts raw hand histories into structured tensors, trains models on them, and flags anomalies. That pipeline is what this step builds."

### Videos

- **Andrew Ng — "Machine Learning Engineering for Production (MLOps)" lecture series**  
  https://www.youtube.com/playlist?list=PLkDaE6sCZn6GMoA0wbpJLi3t34Gd8l0aK  
  Duration: Pick 2–3 videos (~20m each) covering data pipelines, data validation, and feature engineering  
  *Not game-specific, but THE reference for building real-world ML pipelines. You'll need data cleaning, feature validation, and train/test splitting discipline that simulation-based Steps 2–11 didn't require. Watch for: data drift, label noise, feature engineering best practices.*

- **Sentdex / Applied AI — "Poker AI" tutorials**  
  Search YouTube: "poker AI python tutorial" or "poker hand history analysis python"  
  Duration: varies  
  *Look for any tutorial that parses hand history files (PokerStars .txt format or similar). The parsing logic is transferable to Playtech data with format adaptation.*

- **DataCamp / StatQuest — "Clustering and Anomaly Detection" tutorials**  
  Search YouTube: "anomaly detection clustering DBSCAN isolation forest"  
  Duration: ~15m each  
  *Quick refresher on the unsupervised methods you'll use for style clustering and collusion detection: DBSCAN (density-based clusters → finds collusion groups), Isolation Forest (anomaly scoring → flags bots), and k-means (player style archetypes).*

### Blog Posts / Accessible Reads

- **Playtech internal documentation (if accessible)**  
  *Your Playtech connection gives you access to anonymized hand histories. Before touching the data, understand: what format is it in? What fields are available? Are there privacy constraints? What's the data volume per day/week?*

- **PokerTracker / Hold'em Manager documentation**  
  https://www.pokertracker.com/ | https://www.holdemmanager.com/  
  *These are the most popular player tracking tools used by commercial poker players. They extract exactly the player statistics (VPIP, PFR, AF, WTSD, W$SD, etc.) that define player styles. Read their stat definitions — these are the feature engineering targets for your pipeline.*

- **Wikipedia — "Online poker collusion"**  
  https://en.wikipedia.org/wiki/Cheating_in_online_poker  
  *Overview of collusion types: information sharing (signaling hole cards), chip dumping (intentionally losing to a partner), soft play (not betting against a partner). Each collusion type produces specific statistical signatures you can detect.*

- **2+2 Forums — "Bot detection and collusion" discussions**  
  https://forumserver.twoplustwo.com/  
  *Community wisdom on collusion and bot indicators. Practitioners often describe subtle signals (timing tells, bet sizing patterns, session co-occurrence) that don't appear in academic papers. Skim a few threads for feature engineering ideas.*

---

## Phase 2: Exploration (2 days)

### Day 1: Playtech Data Familiarization + Parsing

1. **Obtain and inspect Playtech data:**
   - Work with your Playtech contact to get a dataset of anonymized hand histories
   - Target: ~50K–100K hands from cash game tables (6-max or full-ring)
   - **Inspect the raw format:**
     ```python
     import pandas as pd
     
     # Load a sample of hand histories
     # Format will depend on Playtech's export — likely CSV, JSON, or proprietary
     sample = pd.read_csv('playtech_hands_sample.csv')  # or equivalent
     print(sample.columns.tolist())
     print(sample.head(10))
     print(f"Total hands: {len(sample)}")
     print(f"Unique players: {sample['player_id'].nunique()}")
     print(f"Date range: {sample['timestamp'].min()} to {sample['timestamp'].max()}")
     ```
   - **Key questions to answer:**
     - How many hands per player on average?
     - What's the distribution of table sizes? (2-max, 6-max, 9-max)
     - What stakes are covered?
     - Are there enough hands per player for meaningful modeling? (Rule of thumb: need 500+ hands for stable statistics)
   - **Privacy checklist:** Ensure all player IDs are anonymized (no real identifiers), confirm with Playtech that this data use is approved for academic research

2. **Build the hand history parser:**
   - 🔴 HAND-CODE the parser — this is thesis-critical infrastructure:
     ```python
     class PlaytechHandParser:
         """Parse Playtech hand histories into structured HandRecord objects.
         
         This is the data ingestion layer. Every downstream analysis depends on
         correct parsing. Validate THOROUGHLY.
         """
         
         def __init__(self, raw_data_path):
             self.raw_data_path = raw_data_path
             self.hands = []
         
         def parse_hand(self, raw_hand):
             """Convert one raw hand history into a structured HandRecord."""
             record = HandRecord()
             record.hand_id = raw_hand['hand_id']
             record.timestamp = pd.Timestamp(raw_hand['timestamp'])
             record.table_id = raw_hand['table_id']
             record.table_size = raw_hand['max_players']
             record.stakes = (raw_hand['small_blind'], raw_hand['big_blind'])
             record.players = self.parse_players(raw_hand)
             record.actions = self.parse_actions(raw_hand)
             record.board = self.parse_board(raw_hand)
             record.results = self.parse_results(raw_hand)
             return record
         
         def parse_actions(self, raw_hand):
             """Parse the action sequence into structured Action objects.
             Each action: (player_id, round, action_type, amount, timestamp)
             
             round ∈ {preflop, flop, turn, river}
             action_type ∈ {fold, check, call, bet, raise, all_in}
             amount: normalized by big blind
             """
             actions = []
             for raw_action in raw_hand['actions']:
                 action = Action(
                     player_id=raw_action['player'],
                     round=raw_action['street'],
                     action_type=raw_action['type'],
                     amount=raw_action['amount'] / raw_hand['big_blind'],
                     timestamp=raw_action.get('time', None)
                 )
                 actions.append(action)
             return actions
     ```
   - Validate parser against a few hands you can trace manually

### Day 2: Feature Engineering + Initial Statistics

3. **Apply the state tensor encoding from Step 12:**
   - 🔴 Scale up the Kuhn/Leduc encoding to real poker:
     ```python
     class PokerStateEncoder:
         """Encode real poker game states into fixed-dim tensors.
         
         Extension of Step 12's Kuhn encoding to full Hold'em:
         - cards: 52-dim one-hot for hole cards (2 cards), 52-dim for board (up to 5)
         - position: one-hot over table positions (BTN, SB, BB, UTG, MP, CO, etc.)
         - pot: normalized pot / effective_stack
         - stacks: all players' stacks / initial stack
         - betting_history: sequence of (action_type, amount) tuples per round
         - round_flag: preflop/flop/turn/river
         - n_active_players: how many players remain
         - SPR: stack-to-pot ratio (a key poker concept)
         """
         
         def __init__(self, max_players=6):
             self.max_players = max_players
             self.card_encoder = CardEncoder()  # 52-card one-hot
             
         def encode_state(self, hand_record, action_idx):
             """Encode the game state AT a specific action point.
             
             This gives us (state, action) pairs for every decision in the hand.
             One hand with 10 decisions → 10 training examples.
             """
             state = hand_record.get_state_at(action_idx)
             
             cards_enc = self.card_encoder.encode(state.hole_cards)   # [52*2]
             board_enc = self.card_encoder.encode(state.board_cards)  # [52*5]
             position = self.encode_position(state.position)          # [max_players]
             pot_norm = [state.pot / state.effective_stack]            # [1]
             stacks = self.encode_stacks(state.player_stacks)         # [max_players]
             history = self.encode_betting_history(state.action_seq)   # [4 * max_actions_per_round * 2]
             round_flag = self.encode_round(state.current_round)      # [4]
             n_active = [state.n_active / self.max_players]            # [1]
             spr = [state.stack / max(state.pot, 1e-6)]               # [1]
             
             return np.concatenate([
                 cards_enc, board_enc, position, pot_norm,
                 stacks, history, round_flag, n_active, spr
             ])
     ```

4. **Compute standard poker statistics per player:**
   - 🔴 Implement the PokerTracker-style player stats:
     ```python
     class PlayerStatistics:
         """Compute standard poker player statistics from hand histories.
         
         These stats define the 'behavioral fingerprint' of each player.
         The classic axes from poker literature:
         - VPIP × PFR → loose/tight × passive/aggressive
         - AF × WTSD → aggression × showdown tendency
         """
         
         def __init__(self, player_id, hands):
             self.player_id = player_id
             self.hands = [h for h in hands if player_id in h.players]
             
         def vpip(self):
             """Voluntarily Put $ In Pot (preflop): % of hands where player
             voluntarily put money in the pot (not forced blind).
             Tight players: <20%, Loose players: >35%"""
             voluntary = sum(1 for h in self.hands 
                           if self.voluntarily_entered(h))
             return voluntary / len(self.hands) if self.hands else 0
         
         def pfr(self):
             """Preflop Raise: % of hands where player raised preflop.
             Passive: PFR < VPIP/2, Aggressive: PFR ≈ VPIP"""
             raised = sum(1 for h in self.hands 
                         if self.raised_preflop(h))
             return raised / len(self.hands) if self.hands else 0
         
         def af(self):
             """Aggression Factor: (bets + raises) / calls.
             Passive: AF < 1.5, Aggressive: AF > 2.5"""
             bets_raises = sum(self.count_bets_raises(h) for h in self.hands)
             calls = sum(self.count_calls(h) for h in self.hands)
             return bets_raises / max(calls, 1)
         
         def wtsd(self):
             """Went To Showdown: % of hands (when seeing flop) that reached showdown.
             Low WTSD (<25%): selective, gives up easily
             High WTSD (>35%): calling station, hard to bluff"""
             saw_flop = [h for h in self.hands if self.saw_flop(h)]
             if not saw_flop:
                 return 0
             showed = sum(1 for h in saw_flop if self.went_to_showdown(h))
             return showed / len(saw_flop)
         
         def w_sd(self):
             """Won $ at Showdown: of hands that went to showdown, % won.
             Indicates hand selection quality at showdown.
             Good players: >50%, Bad players: <45%"""
             showdown_hands = [h for h in self.hands if self.went_to_showdown(h)]
             if not showdown_hands:
                 return 0
             won = sum(1 for h in showdown_hands if self.won_at_showdown(h))
             return won / len(showdown_hands)
         
         def three_bet(self):
             """3-bet %: how often a player re-raises a preflop raise.
             Indicator of range strength and aggression vs. position."""
             opportunities = sum(1 for h in self.hands 
                               if self.had_3bet_opportunity(h))
             threebet = sum(1 for h in self.hands 
                          if self.three_betted(h))
             return threebet / max(opportunities, 1)
         
         def cbet(self):
             """Continuation Bet %: how often the preflop raiser bets on flop.
             High cbet (>65%): aggressive, hard to play against
             Low cbet (<40%): gives up easily on missed boards"""
             opportunities = sum(1 for h in self.hands 
                               if self.had_cbet_opportunity(h))
             cbets = sum(1 for h in self.hands if self.continuation_bet(h))
             return cbets / max(opportunities, 1)
         
         def get_style_vector(self):
             """Return the full behavioral fingerprint as a vector.
             This vector is the feature space for style clustering."""
             return np.array([
                 self.vpip(), self.pfr(), self.af(), 
                 self.wtsd(), self.w_sd(), self.three_bet(), self.cbet()
             ])
     ```

5. **Initial data exploration:**
   - Compute stats for all players with 500+ hands
   - Plot the VPIP × PFR scatter plot — this is the classic player type map:
     - Top-left: Loose-Passive ("calling station")
     - Top-right: Loose-Aggressive ("maniac")
     - Bottom-left: Tight-Passive ("rock/nit")
     - Bottom-right: Tight-Aggressive ("TAG" — the most common winning style)
   - How many players fall in each quadrant?
   - Any obvious outliers? (Extreme stats might be bots or collusion)

---

## Phase 3: Targeted Reading (3 days)

### Paper 1: Wang, Honari-Jahromi, Katsarou, Mikheeva, Panagiotakopoulos, Asadi & Smirnov — "player2vec: A Language Modeling Approach to Understand Player Behavior in Games" (2024)
**Link:** https://arxiv.org/abs/2404.04234

- **READ:** Entire paper carefully
  - KEY INSIGHT: In-game events treated as tokens (like words in NLP), player behavior = sequence of tokens → Transformer learns embeddings that capture behavioral patterns.
  - Architecture: Long-range Transformer on event sequences, pre-trained in self-supervised manner (masked event prediction, similar to BERT)
  - What emerges: embedding space clusters by behavior type without any labels — similar players (playstyle, skill level) cluster together
- **PhD Connection:** This is EXACTLY what you should build for poker data. Your "events" are poker actions (fold/check/call/bet/raise with sizing). Your "sentences" are hands. Your "documents" are player histories. player2vec validates the approach; your poker-specific version creates the behavioral embeddings for style classification and anomaly detection.
- **Adaptation needed:** player2vec uses general game events (movement, interaction, purchase). Poker events have richer structure: position, street, sizing, relative to pot. Your encoding should be more structured than raw tokenization.

### Paper 2: Kumar, Hong, Singh & Levine — "When Should We Prefer Offline Reinforcement Learning Over Behavioral Cloning?" (2022, ICLR)
**Link:** https://arxiv.org/abs/2204.05618

- **READ:** Sections 1–4 (Introduction, Problem Setup, Theoretical Analysis, Experiments)
  - KEY INSIGHT: BC outperforms offline RL when data is expert-quality and narrowly distributed. Offline RL wins when: (a) rewards are sparse, (b) data is noisy/suboptimal, (c) horizons are long.
  - Poker data satisfies ALL conditions where offline RL wins: rewards are sparse (only final payoff), data is noisy (human play is imperfect), horizons are long (multi-street decisions).
- **SKIM:** Specific experimental domains (Atari, MuJoCo)
- **PhD Connection:** This paper answers the design question for the Playtech pipeline. Behavioral cloning (predict what the player DID) is the baseline → it gives you style classification. Offline RL (learn what the player SHOULD DO) is the upgrade → it gives you deviation detection (gap between what they did and what an optimal agent would do). Both are needed.

### Paper 3: DeLong & Bhatt — "Towards Collusion Detection in Poker" (2020)
**Source:** Search Google Scholar; may be a conference paper or technical report

- **READ:** The full paper (likely short)
  - Collusion patterns: information sharing, chip dumping, soft play
  - Detection approaches: statistical deviation from expected play, co-occurrence analysis, action correlation between suspected colluders
- **KEY OBSERVATION:** Collusion detection is fundamentally about finding COORDINATED DEVIATIONS from independent play. Two players who INDEPENDENTLY play strangely are just bad players. Two players who play strangely in a CORRELATED way (always at the same table, always benefiting each other) are potentially colluding.
- **PhD Connection:** Direct Contribution #3 material. Your coalition detector from Step 11 (help/harm matrices) is the structural analog: in SLS, the coalition is explicit (chip placement). In poker, the coalition is hidden (information sharing). Same detection problem, different observation space.

### Paper 4: Yan & Browne — "Collusion Detection in Online Poker" (2016)

- **READ:** Statistical approaches section
  - What statistical signatures indicate collusion?
  - How do you distinguish collusion from normal variance in poker?
  - What sample sizes are needed for statistically significant detection?
- **SKIM:** Experimental methodology
- **PhD Connection:** The statistical grounding for Step 13's collusion experiment. You need to know what signals are meaningful vs noise.

### Paper 5: Southey, Bowling, Larson, Piccione, Burch, Billings & Rayner — "Bayes' Bluff: Opponent Modelling in Poker" (2005)
**Link:** Already studied in Step 7 — REVISIT with real data lens

- **RE-READ:** Section 3 (Bayesian opponent model) with a focus on data requirements
  - How many hands does the Bayesian model need before the posterior is useful?
  - What priors did they use? (Mixtures of known strategy types)
  - How does this compare to the player2vec embedding approach?
- **PhD Connection:** Bayes' Bluff is the THEORY for player modeling. player2vec is the EMBEDDING. Your pipeline combines both: use player2vec-style embeddings to discover player types (unsupervised), then use Bayesian modeling (from Step 7) to refine the model per player with real-time data.

### Supplementary Reading (skim as time permits):

- **Kim et al. (2025) — "A Framework for Mining Collectively-Behaving Bots in MMORPGs"** (arXiv:2501.10461): Trajectory representation learning + DBSCAN for bot detection. SKIM for: embedding architecture, clustering approach, evaluation metrics. The methodology transfers: replace MMORPG trajectories with poker hand histories.

- **Ganzfried, Wang & Chiswick (2022/2024) — "Opponent Modeling in Multiplayer Imperfect-Information Games"**: Already studied in Step 7. RE-SKIM for: how does multi-player modeling extend to 6-player table data? Does the computational cost change with real data?

- **Paster, McIlraith & Ba (2022) — "You Can't Count on Luck"** (from Step 12): RE-READ Section 3 Theorem 2.1 with Playtech data in mind. This tells you that conditioning Decision Transformer on win/loss outcomes in poker data will learn CARD LUCK, not STRATEGIC SKILL. The fix for Step 13: don't use outcomes as the return signal — use a proxy for decision quality (e.g., EV estimate from a solver, or deviation from known ranges).

### Math Flags:

🔢 **Bayesian posterior update for player type estimation** — Revisit from Step 7. Work through the update for a concrete example: Player X has played 100 hands, 35% VPIP, 25% PFR. Given a prior over 4 archetypes (TAG, LAG, Nit, Fish), compute the posterior. How many hands until the posterior concentrates?  
**WHY this can't be substituted by algorithmic understanding:** The posterior convergence rate directly determines the minimum data requirement per player. If convergence requires 500 hands, players with fewer hands can't be reliably typed — this constrains your pipeline's coverage.

🔢 **player2vec embedding loss function** — Understand the self-supervised training objective (masked event prediction or next-event prediction). How does the loss relate to behavioral consistency? (High-loss players = inconsistent behavior = either adapting or deliberately varying.)  
**WHY this can't be substituted by algorithmic understanding:** The loss landscape tells you about behavioral CONSISTENCY, which is itself a feature for anomaly detection (bots have unusually low loss = unusually consistent behavior).

---

## Phase 4: Implementation (6 days)

### Project: Playtech Behavioral Analysis Pipeline — From Hand Histories to Player Profiles, Style Classification, and Collusion Detection

| Component | AI Tag | Justification |
|-----------|--------|---------------|
| Hand history parser (Playtech format) | 🔴 HAND-CODE | Data pipeline is thesis-critical infrastructure. Must understand every field, every edge case. |
| State tensor encoder (full Hold'em) | 🔴 HAND-CODE | Extension of Step 12's prototype to real poker. The encoding IS the thesis representation. |
| Player statistics computation (VPIP, PFR, AF, etc.) | 🔴 HAND-CODE | Feature engineering for player modeling — must understand each stat's semantic meaning. |
| player2vec-style embedding model | 🟡 AI-ASSISTED | Use HuggingFace Transformer as base, adapt for poker event tokenization. Architecture is standard; tokenization design is original. |
| Behavioral cloning model (predict human actions) | 🟡 AI-ASSISTED | Network architecture is standard (MLP/Transformer on state encoding). Design of input features is original. |
| Style clustering (k-means / DBSCAN) | 🟢 AI-GENERATED | Standard ML clustering — use scikit-learn. Focus on INTERPRETING results, not coding them. |
| Collusion detection module | 🔴 HAND-CODE | Novel application — extends Step 11's coalition detector to real poker data. Must hand-code the detection logic. |
| Evaluation metrics + visualizations | 🟡 AI-ASSISTED | Analysis code with manual domain interpretation. |

**Day 1 — Complete Data Pipeline**

- 🔴 Finalize the hand history parser (started in Phase 2):
  - Handle edge cases: missing data, unusual table sizes, all-in situations, split pots, ante games
  - Data validation: check for impossible states (negative stacks, impossible card combinations, action sequences that violate poker rules)
  ```python
  class DataValidator:
      """Validate parsed hand records for consistency."""
      
      def validate_hand(self, hand):
          errors = []
          # Card validation: no duplicate cards across hole cards + board
          all_cards = []
          for p in hand.players:
              all_cards.extend(p.hole_cards if p.hole_cards else [])
          all_cards.extend(hand.board if hand.board else [])
          if len(all_cards) != len(set(all_cards)):
              errors.append(f"Duplicate cards in hand {hand.hand_id}")
          
          # Stack validation: stacks should be non-negative after every action
          running_stacks = {p.id: p.starting_stack for p in hand.players}
          for action in hand.actions:
              if action.amount:
                  running_stacks[action.player_id] -= action.amount
                  if running_stacks[action.player_id] < -0.01:
                      errors.append(f"Negative stack at action {action}")
          
          # Pot validation: sum of all bets should equal final pot
          total_bets = sum(a.amount for a in hand.actions if a.amount)
          if abs(total_bets - hand.final_pot) > 0.01:
              errors.append(f"Pot mismatch: bets={total_bets}, pot={hand.final_pot}")
          
          return errors
  ```
- Build the full pipeline: raw data → parse → validate → store structured records
- Generate dataset summary statistics: hands per player histogram, stakes distribution, table size distribution

**Day 2 — Behavioral Cloning Baseline**

- 🟡 Train a behavioral cloning model on Playtech data:
  ```python
  class PokerBehavioralCloningModel(nn.Module):
      """Predict human action from game state.
      
      Input: state tensor from PokerStateEncoder
      Output: action distribution (fold, check, call, bet_small, bet_medium, bet_large, all_in)
      
      This is the BASELINE for everything:
      - High accuracy = model captures player behavior well
      - Per-player accuracy = how PREDICTABLE is each player
      - Action where model is wrong = SURPRISING actions = potential anomalies
      """
      
      def __init__(self, state_dim, n_actions=7):
          super().__init__()
          self.network = nn.Sequential(
              nn.Linear(state_dim, 256),
              nn.ReLU(),
              nn.Dropout(0.2),
              nn.Linear(256, 128),
              nn.ReLU(),
              nn.Dropout(0.2),
              nn.Linear(128, n_actions)
          )
      
      def forward(self, state):
          return F.log_softmax(self.network(state), dim=-1)
  ```
- Train on 80% of data, validate on 20%
- **Key metrics:**
  - Overall action prediction accuracy (baseline: ~55-65% for good models on poker data)
  - Accuracy by street (preflop should be highest — fewer variables)
  - Accuracy by position (button should be most predictable — more information)
  - Accuracy by player archetype (TAGs should be most predictable — consistent strategy)
- **Connection to Step 12:** Compare BC accuracy with the DT results from Step 12 (on Kuhn data). How much harder is real poker than Kuhn?

**Day 3 — Player Embedding Model (player2vec for Poker)**

- 🟡 Build a player2vec-style embedding:
  ```python
  class PokerPlayer2Vec:
      """Learn player embeddings from action sequences.
      
      Approach: treat each hand as a 'sentence' and each action as a 'token'.
      Token = (position, street, action_type, sizing_bucket, rel_pot)
      
      Train a Transformer encoder to predict masked actions (BERT-style)
      or next actions (GPT-style). The resulting embeddings capture 
      behavioral patterns.
      """
      
      def __init__(self, vocab_size, embed_dim=64, n_heads=4, n_layers=2):
          self.tokenizer = PokerActionTokenizer()
          self.model = TransformerEncoder(
              vocab_size=vocab_size,
              embed_dim=embed_dim,
              n_heads=n_heads,
              n_layers=n_layers
          )
      
      def tokenize_hand(self, hand_record, player_id):
          """Convert a player's actions in one hand to tokens.
          
          Token vocabulary:
          - Position tokens: BTN, SB, BB, UTG, MP, CO
          - Street tokens: PREFLOP, FLOP, TURN, RIVER
          - Action tokens: FOLD, CHECK, CALL, BET_SMALL, BET_MED, BET_LARGE, ALL_IN
          - Special: [PAD], [MASK], [SEP] (between hands)
          """
          tokens = [self.tokenize_position(hand_record, player_id)]
          for action in hand_record.get_player_actions(player_id):
              tokens.append(self.tokenizer.encode(action))
          return tokens
      
      def build_player_sequence(self, player_id, hands, max_hands=100):
          """Concatenate multiple hands into one long sequence per player.
          Separate hands with [SEP] tokens."""
          full_sequence = []
          for hand in hands[:max_hands]:
              hand_tokens = self.tokenize_hand(hand, player_id)
              full_sequence.extend(hand_tokens)
              full_sequence.append(self.tokenizer.sep_token)
          return full_sequence
      
      def get_player_embedding(self, player_id, hands):
          """Get the learned embedding for a player.
          Use the [CLS]-like representation: average pool the encoder outputs."""
          sequence = self.build_player_sequence(player_id, hands)
          outputs = self.model.encode(sequence)
          return outputs.mean(dim=0)  # Player embedding vector
  ```
- Train on ALL players' action sequences (self-supervised — no labels needed)
- Extract embeddings for all players with 500+ hands
- **Visualization:** t-SNE / UMAP of player embeddings. Do natural clusters emerge?
  - Compare with the manual VPIP×PFR quadrants from Phase 2 — do the clusters match?
  - Any surprising clusters? (e.g., a tight cluster of bots would show as unusually dense)

**Day 4 — Style Classification**

- 🟢 Apply clustering to player embeddings + stat vectors:
  ```python
  from sklearn.cluster import KMeans, DBSCAN
  from sklearn.preprocessing import StandardScaler
  
  # Option A: Cluster on stat vectors (interpretable)
  stat_vectors = np.array([player.get_style_vector() for player in players])
  scaler = StandardScaler()
  scaled = scaler.fit_transform(stat_vectors)
  
  kmeans = KMeans(n_clusters=4, random_state=42)  # 4 classic archetypes
  labels = kmeans.fit_predict(scaled)
  
  # Name the clusters by examining centroids
  for i in range(4):
      centroid = scaler.inverse_transform(kmeans.cluster_centers_[i])
      print(f"Cluster {i}: VPIP={centroid[0]:.2f}, PFR={centroid[1]:.2f}, "
            f"AF={centroid[2]:.2f}, WTSD={centroid[3]:.2f}")
  
  # Option B: Cluster on player2vec embeddings (richer, less interpretable)
  embeddings = np.array([model.get_player_embedding(p.id, p.hands) 
                          for p in players])
  dbscan = DBSCAN(eps=0.5, min_samples=5)
  dbscan_labels = dbscan.fit_predict(embeddings)
  ```
- **Key experiments:**
  1. **Archetype validation:** Do the 4 clusters correspond to known poker archetypes (TAG, LAG, Nit, Fish)?
  2. **Embedding vs stats:** Does player2vec discover finer-grained styles beyond the 4 classic types?
  3. **Temporal stability:** Split each player's hands into first half and second half. Do they stay in the same cluster? (If not → the player changed style, which is an interesting behavioral signal)
  4. **Outlier detection:** Which players don't fit ANY cluster well? These are candidates for bot or collusion investigation.

**Day 5 — Collusion Detection**

- 🔴 Build the collusion detection module — the step's most original component:
  ```python
  class CollusionDetector:
      """Detect potential collusion in multi-player poker tables.
      
      Collusion signals (from DeLong & Bhatt, Yan & Browne):
      1. Session co-occurrence: colluders play the same tables together
         at unusually high rates
      2. Chip dumping: one player consistently loses large pots to a 
         specific other player (losing on purpose)
      3. Soft play: player A never bets/raises against player B when
         A has a strong hand (protecting a partner)
      4. Information advantage: colluder B's winrate spikes when colluder A
         is present (A shares private information)
      
      Extension from Step 11: in SLS, help/harm matrices tracked chip
      placement between players. Here, help/harm tracks monetary transfer
      and action modification between table-mates.
      """
      
      def __init__(self, hand_records):
          self.hands = hand_records
          self.player_pairs = self.build_co_occurrence_matrix()
      
      def build_co_occurrence_matrix(self):
          """How often does each pair of players appear at the same table?"""
          pairs = {}
          for hand in self.hands:
              players = hand.player_ids
              for i, p1 in enumerate(players):
                  for p2 in players[i+1:]:
                      pair = tuple(sorted([p1, p2]))
                      pairs[pair] = pairs.get(pair, 0) + 1
          return pairs
      
      def co_occurrence_anomaly(self, pair, total_hands_per_player):
          """Is this pair appearing together suspiciously often?
          
          Expected co-occurrence: (hands_A * hands_B) / total_hands_at_table_size
          If actual >> expected → suspicious
          """
          actual = self.player_pairs.get(pair, 0)
          p1_hands = total_hands_per_player[pair[0]]
          p2_hands = total_hands_per_player[pair[1]]
          # Simplified expected: proportional to both players' activity
          expected = (p1_hands * p2_hands) / self.total_table_slots
          if expected == 0:
              return 0
          return actual / expected  # Ratio > 3.0 = suspicious
      
      def chip_dumping_score(self, pair):
          """Does one player lose to the other unusually often?
          
          Metric: net transfer from P1 to P2 in hands where both are present.
          Compare with expected transfer under independent play.
          """
          shared_hands = self.get_shared_hands(pair)
          if len(shared_hands) < 50:
              return 0  # Not enough data
          
          net_transfer = 0
          for hand in shared_hands:
              p1_result = hand.get_result(pair[0])
              p2_result = hand.get_result(pair[1])
              # If P1 lost AND P2 won in the same hand
              if p1_result < 0 and p2_result > 0:
                  net_transfer += abs(p1_result)
          
          # Normalize by expected variance
          expected_transfer = len(shared_hands) * self.average_pot / 2
          return net_transfer / max(expected_transfer, 1)
      
      def soft_play_score(self, pair):
          """Does player A play passively against player B compared to others?
          
          Metric: A's aggression factor vs B compared to A's AF vs rest.
          If AF_vs_B << AF_vs_others → A is playing softly against B.
          """
          af_vs_partner = self.compute_af_against(pair[0], pair[1])
          af_vs_others = self.compute_af_against_others(pair[0], pair[1])
          
          if af_vs_others == 0:
              return 0
          return 1 - (af_vs_partner / af_vs_others)  # > 0.5 = suspicious
      
      def detect_collusion(self, threshold=0.7):
          """Composite collusion score for each player pair.
          Combines co-occurrence, chip dumping, and soft play signals."""
          suspicious_pairs = []
          for pair in self.player_pairs:
              co_occur = self.co_occurrence_anomaly(pair, self.hands_per_player)
              chip_dump = self.chip_dumping_score(pair)
              soft_play = self.soft_play_score(pair)
              
              # Weighted composite (weights tunable)
              composite = 0.3 * min(co_occur / 3, 1) + \
                         0.4 * chip_dump + \
                         0.3 * soft_play
              
              if composite > threshold:
                  suspicious_pairs.append((pair, composite, {
                      'co_occurrence': co_occur,
                      'chip_dumping': chip_dump,
                      'soft_play': soft_play
                  }))
          
          return sorted(suspicious_pairs, key=lambda x: x[1], reverse=True)
  ```
- **Test on synthetic collusion first:**
  - Inject known collusion patterns into a subset of the data (e.g., duplicate a player's hands, modify actions to simulate soft play). Does the detector find them?
  - This is the VALIDATION — if the detector can't find synthetic collusion, it won't find real collusion.
- **Run on real data:**
  - List top 20 suspicious pairs
  - Manual review: do the flagged pairs show genuine suspicious patterns, or is it noise?
  - **Connection to Step 11:** Compare the detection methodology with the SLS coalition detector. What's different? (In SLS, coalitions are visible through chip placement. In poker, coalitions are HIDDEN — detection requires statistical inference.)

**Day 6 — Integration + Decision Transformer on Real Data**

- 🟡 Apply the Decision Transformer pipeline from Step 12 to Playtech data:
  ```python
  # Use the PokerTrajectoryDataset from Step 12, now with real data
  real_dataset = PokerTrajectoryDataset(
      game_type='holdem',
      data_source='playtech',
      hands=parsed_hands
  )
  
  # Train DT on real poker data
  dt_model = DecisionTransformerModel(config)
  train_dt(dt_model, real_dataset)
  
  # KEY EXPERIMENT: Paster et al. warning in practice
  # Compare return conditioning with EV-based conditioning:
  #
  # Version A: condition on raw outcome (chips won/lost)
  # Version B: condition on decision quality proxy
  #   (e.g., deviation from GTO play → lower deviation = higher "return")
  
  # Measure: which version produces actions closer to GTO?
  ```
- **Final comparison:**
  | Method | Action Prediction Acc. | Style Classification | Collusion Signal | Notes |
  |--------|----------------------|---------------------|-----------------|-------|
  | Player stats (VPIP/PFR/AF) | N/A | ✅ 4 archetypes | ❌ No | Baseline |
  | Behavioral Cloning | ~60%? | ✅ via error patterns | Partial | Standard ML |
  | player2vec embeddings | N/A (self-supervised) | ✅ fine-grained | ✅ outlier detection | Best for clustering |
  | Decision Transformer | ~60%? | ❌ Not designed for this | ❌ Not designed | Baseline from Step 12 |
  | Collusion Detector | N/A | N/A | ✅ composite score | Novel combination |

### Deliverables:
- [ ] Playtech hand history parser — robust, validated, handles edge cases
- [ ] Full Hold'em state tensor encoder — extending Step 12's prototype to real poker
- [ ] Player statistics computation (VPIP, PFR, AF, WTSD, W$SD, 3-bet, C-bet) for all players
- [ ] Behavioral cloning model trained on Playtech data with accuracy by street/position/archetype
- [ ] player2vec-style embedding model producing per-player behavioral vectors
- [ ] Style clustering: k-means archetypes + DBSCAN on embeddings + visualizations
- [ ] Collusion detection module with co-occurrence, chip dumping, and soft play signals
- [ ] Synthetic collusion injection + detection validation
- [ ] Decision Transformer applied to real poker data (from Step 12 pipeline)
- [ ] Comparison table: stats vs BC vs embeddings vs DT on Playtech data

### Validation:
- **Parser:** Successfully parse 100% of well-formed hands. Validator catches injected errors (duplicate cards, negative stacks).
- **State encoder:** Encoding dimension consistent across all table sizes. No NaN/Inf values. Normalized features are in [0, 1].
- **BC model:** Prediction accuracy > 55% (random baseline for 7 action types = 14%). Accuracy by archetype: TAG > LAG > Fish (TAGs are more predictable).
- **player2vec:** Embedding clusters match VPIP×PFR quadrants (visual validation). Intra-cluster similarity > inter-cluster similarity.
- **Style clustering:** 4 k-means clusters correspond to recognizable archetypes. Temporal stability > 70% (players mostly stay in same cluster).
- **Collusion detection:** Detects 100% of injected synthetic collusion at the chosen threshold. False positive rate on known-clean data < 5%.

---

## Phase 5: Consolidation (2 days)

### Day 1 — Survey Skim + Cross-References

- **Reference skim:** Kim et al. (2025) — "Mining Collectively-Behaving Bots in MMORPGs"  
  https://arxiv.org/abs/2501.10461  
  *Skim their trajectory representation + DBSCAN pipeline. Compare with your poker pipeline: how do they handle variable-length trajectories? What clustering parameters did they use? Can their evaluation methodology (comparing detected clusters against known bot accounts) be adapted for collusion evaluation?*

- **Supplementary skim:** Ganzfried (2025) — "Consistent Opponent Modeling"  
  https://arxiv.org/abs/2508.17671  
  *From Step 7 freshness scan. Re-skim with data pipeline lens: the consistent modeling algorithm could be applied to your Playtech data to produce per-player strategy estimates. How would this compare with BC for understanding player behavior?*

- **Supplementary skim:** Paster et al. (2022) — Final re-read  
  *Third visit (Steps 12, 13 reading, now consolidation). Confirm your understanding of why raw outcomes ≠ decision quality in stochastic environments. Document the specific fix for Step 13: Playtech DT should condition on EV-based metrics, not chip outcomes.*

- **Forward scan:** Search Google Scholar for recent papers on "poker collusion detection," "online gambling fraud machine learning," or "player behavior analysis iGaming." Most results will be industry blogs or conference proceedings rather than arXiv papers. Note any relevant findings.

### Day 2 — PhD Mapping + One-Pager + Learning Log

- **Write the mandatory one-pager** (Section 4.7 format). Commit to repo.
- **Update the Learning Log** (`learningLog.md`):
  - **Connections:**
    - [Step 2] Kuhn/Leduc Nash equilibrium → [Step 13] Nash strategy as the "reference point": deviations from Nash-like play are the SIGNAL for player classification. A player who folds 60% preflop deviates from most computed equilibria — that deviation IS the behavioral feature.
    - [Step 3] CFR agent data → [Step 13] CFR solver produces near-Nash strategies that serve as the DATA GENERATOR for the DT training in Step 12, and as the COMPARISON BASELINE for real player behavior. Real players deviate from CFR solutions — the deviation distribution defines their style.
    - [Step 7] Bayesian opponent model → [Step 13] The Bayesian model (prior over player types → posterior from observed actions) is the THEORY behind player2vec: player2vec automates what Bayes' Bluff did manually by learning the "prior space" from data and computing "posteriors" as embeddings. They're the same function in different mathematical languages.
    - [Step 7] Hand range inference → [Step 13] In Step 7, you inferred what CARDS a player holds from their actions. In Step 13, you infer what TYPE of player they are from their action history. Same Bayesian inference, different target variable.
    - [Step 8] Safe exploitation → [Step 13] The deviation between real player behavior and GTO play (measured by the BC model's errors, or by the exploitability of the inferred strategy) IS the exploitation opportunity. Safe exploitation theory (Step 8) says: exploit this deviation, but only to the extent that you stay safe. The Playtech pipeline quantifies the deviation — Step 8's theory determines how to respond.
    - [Step 11] Coalition detector (SLS) → [Step 13] Collusion detector (poker). Same principle: detect coordinated behavior between agents who should be playing independently. SLS: chip placement patterns. Poker: co-occurrence + chip dumping + soft play. The detector architecture carries directly from SLS to poker — just different input features.
    - [Step 12] State tensor encoding (Kuhn/Leduc) → [Step 13] State tensor encoding (full Hold'em/Playtech). The prototype becomes the real pipeline. Same architectural decisions, larger dimensions.
    - [Step 12] DT stochasticity warning (Paster et al.) → [Step 13] Confirmed on real data: conditioning on outcomes conflates luck and skill. The fix: condition on decision quality metrics or deviation from GTO, not raw chipcount.
    - [Step 12] Comparison table (CFR vs DT vs ARDT vs BC vs LLM on Kuhn) → [Step 13] Extended comparison table on Playtech data. Same evaluation methodology, scaled up.
  - **Confusions:**
    - [Step 13] The collusion detection module produces a ranked list of suspicious pairs. But what's the GROUND TRUTH? In Playtech data, we don't know which pairs are actually colluding (unless Playtech provides labels). Without ground truth, how do we evaluate detection accuracy beyond the synthetic injection test? → PARTIALLY ADDRESSED (synthetic injection validates the methodology; real-world validation requires Playtech feedback or known cases)
    - [Step 13] player2vec learns embeddings in a self-supervised way — no labels needed. But the embedding quality depends on the tokenization design (what counts as a "token"? How is bet sizing discretized?). Small tokenization changes might produce very different embeddings. How sensitive is this? → OPEN (ablation study needed — try 3-4 tokenization schemes and compare embedding quality)
    - [Step 13] Temporal stability of player style: some players CHANGE their style (e.g., tilt → become loose-aggressive after a bad beat). The current pipeline treats each player as a static entity. How to detect style SHIFTS? → OPEN (potential Contribution #1 extension: dynamic behavioral adaptation modeling)
    - [Step 7→13] Bayesian opponent model requires a PRIOR over player types. Where does the prior come from? In Step 7, it was assumed or hand-crafted. In Step 13, the clustering results could DEFINE the prior: the 4 (or N) cluster centroids IS the prior distribution. This closes the loop: data → clusters → prior → Bayesian update → refined model. → PARTIALLY ADDRESSED (architecture identified but not implemented end-to-end)
    - [Step 11→13] The SLS coalition detector uses a simple threshold on help/harm net scores. The poker collusion detector uses a weighted composite of co-occurrence, chip dumping, and soft play. Is there a principled way to SET the threshold/weights? (If too aggressive → false positives; too conservative → misses real collusion.) → OPEN (ROC analysis on synthetic collusion can help, but real-world calibration needs Playtech feedback)
    - [Step 12→13] ARDT (adversarially robust) on real poker data: the poker environment is MUCH more complex than Kuhn. Does ARDT still produce meaningful strategies when data coverage is sparse? (Real players don't visit all information sets equally.) → OPEN (tested briefly in Day 6, but needs deeper investigation)

### PhD Connection

This step is the PRACTICAL CORE of the thesis — it connects all theoretical work to real-world application:

- **Contribution #1 (Behavioral Adaptation Framework):** The pipeline IS the framework:
  - State tensor encoding → behavioral representation
  - player2vec embeddings → style discovery (unsupervised)
  - Bayesian player modeling (from Step 7) → online style refinement
  - BC model → action prediction baseline
  - Temporal analysis → style shift detection (future extension)
  - Together: a complete framework for representing, classifying, and tracking player behavior from raw game data. This is directly publishable as a pipeline paper + Playtech case study.

- **Contribution #2 (Multi-Agent Safe Exploitation):** The real-world data establishes the empirical basis:
  - The gap between real player behavior and GTO play (measured here) is the EXPLOITATION OPPORTUNITY.
  - Step 8's safe exploitation theory + Step 13's behavioral pipeline = a complete SYSTEM: detect opponent weakness from data → exploit it safely.
  - In the N-player setting (6-max tables): the multi-player modeling challenges from Steps 9–11 meet real data.

- **Contribution #3 (Evaluation Methodology):** The collusion detection module is a direct contribution:
  - Collusion detection in online poker is an OPEN PROBLEM with very few published solutions.
  - Your approach (co-occurrence analysis + chip dumping + soft play + player2vec-based anomaly detection) combines techniques from Steps 7, 11, and 12 into a novel detection pipeline.
  - This is directly relevant to the fraud/risk career path (5/5 fraud job postings map to Steps 7, 8, 13).
  - Playtech co-authorship potential: if the detection pipeline finds real anomalies in Playtech data, the resulting paper has both academic and industry value.

- **Bridge to Step 14:** The evaluation metrics developed here (action prediction accuracy, style classification accuracy, collusion detection precision/recall) feed into the formal evaluation framework of Step 14. Step 14 asks "how do we evaluate agents?" — Step 13 provides the real-world data benchmark.

- **November publication target:** Step 13's pipeline + Playtech case study is the STRONGEST candidate for the first publication. It combines: (a) novel methodology (player2vec for poker + collusion detection), (b) real-world data (Playtech), (c) practical value (iGaming industry), (d) accessible framing (fraud detection). A paper titled "Behavioral Analysis and Collusion Detection in Online Poker via Transformer-Based Player Embeddings" would be suitable for IEEE Transactions on Games, AAAI Workshop on AI for Social Good, or a similar venue.

---

## Exit Checklist

- [ ] Playtech hand history parser robust and validated (100% parse rate on well-formed hands)
- [ ] Full Hold'em state tensor encoder working across all table sizes
- [ ] Player statistics (VPIP, PFR, AF, WTSD, W$SD, 3-bet, C-bet) computed for all players with 500+ hands
- [ ] VPIP × PFR scatter plot showing expected player type distribution
- [ ] Behavioral cloning model trained with action prediction accuracy > 55%
- [ ] BC accuracy breakdown by street, position, and player archetype documented
- [ ] player2vec model trained; per-player embeddings extracted
- [ ] Embedding visualization (t-SNE/UMAP) showing natural behavioral clusters
- [ ] Style clustering: k-means 4-archetype + interpretable cluster descriptions
- [ ] Temporal stability test: >70% of players remain in same cluster across time splits
- [ ] Collusion detection module with co-occurrence, chip dumping, and soft play scores
- [ ] Synthetic collusion injection detected at >90% recall
- [ ] Decision Transformer from Step 12 applied to Playtech data (Paster et al. warning confirmed)
- [ ] Comparison table: stats vs BC vs embeddings vs DT completed
- [ ] Can explain from memory: VPIP/PFR/AF meaning and thresholds for each player archetype
- [ ] Can explain from memory: how player2vec embeds are computed (tokenization + self-supervised Transformer)
- [ ] Can explain from memory: three collusion signals and why each indicates fraud
- [ ] Can explain from memory: why BC is the right baseline and when offline RL improves over it (Kumar et al.)
- [ ] All 🔴 components hand-coded (parser, state encoder, player stats, collusion detector)
- [ ] One-pager written and committed
- [ ] Learning Log updated (connections from Steps 2–12 + collusion-specific confusions + pub candidate noted)
- [ ] PhD connection documented (pipeline = Contribution #1, exploitation gap = Contribution #2, collusion = Contribution #3, publication candidate identified)
- [ ] Step notes committed to repo

> **[P8] Change-Point Detection for collusion:** Add Bayesian online changepoint detection (Adams & MacKay 2007) as a signal in the collusion detection composite score. Same algorithm from Step 7 applied to detect collusion onset / bot behavior changes in player timelines. ~0.5d absorbed within 14d allocation.

> **[P10] GAIL/IRL Fallback:** If behavioral cloning accuracy < 55% on action prediction, explore **IQ-Learn** (Garg et al., 2021) as an inverse RL alternative. IQ-Learn is already in supplementary references — this promotes it to documented Plan B.

