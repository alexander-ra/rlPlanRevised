6.1 Lossless abstraction (Gilpin & Sandholm 2007)
 
 
 
Gilpin, A. & Sandholm, T. "Lossless abstraction of imperfect information games," Journal of the ACM, Vol. 54, No. 5 (2007). PDF: https://www.cs.cmu.edu/~gilpin/papers/extensive.JACM.pdf
 
The first paper to formalise when merging info sets is provably equilibrium-preserving, and the first to give an algorithm that finds all such merges automatically. Practical milestone: GameShrink + linear programming solved Rhode Island Hold'em (3.1 billion game-tree nodes) — at the time, four orders of magnitude larger than any poker game previously solved.
 
Explicit route
 
The setting. Games with ordered signals (Definition 2.1): multi-player sequential games of imperfect information where actions are observable and signals (cards, in poker) come from a partially ordered set whose ordering captures strength. Crucially, the paper does not operate on the game tree directly; it operates on the much smaller signal tree (Definition 3.1), whose paths enumerate possible sequences of public and private signals through the game. For Rhode Island Hold'em the signal tree has 6.6 M nodes vs 3.1 B in the game tree — roughly $470 \times$ smaller.
 
The criterion (Definition 3.2 — ordered game isomorphism). Two subtrees rooted at sibling nodes $x, y$ of the filtered signal tree are ordered game isomorphic if there exists a bijection $f: N(x) \to N(y)$ between their children such that:
 
 
 
 
 
the edge weights $(x, w)$ and $(y, f(w))$ are equal (probability-preserving),
 
 
 
the subtrees rooted at $w$ and $f(w)$ are themselves ordered game isomorphic (recursive condition),
 
 
 
base case at the leaves: the utilities $u^r(\tilde z, \vartheta)$ and $u^r(\tilde z, \vartheta')$ match for every possible continuation $\tilde z$ of opponent signals.
 
Condition (3) is the load-bearing one — utility identity for every opponent continuation is what makes the merge strategically harmless against an arbitrary opponent strategy, not merely against the average.
 
The transformation (Definition 3.3). Coarsens the information filter so the two isomorphic information structures $\vartheta$ and $\vartheta'$ become a single one $\vartheta \cup \vartheta'$. The agent now treats both as the same info set when choosing actions.
 
The guarantee (Theorem 3.4 — main equilibrium result). Let $\hat\sigma^$ be a Nash equilibrium of the abstracted game $\hat G$. Construct $\sigma$ on the original game $G$ by playing, at every original info set, the same action distribution that $\hat\sigma^$ plays at the merged abstract info set. Then $\sigma$ is a Nash equilibrium of $G$. The lift from abstract Nash to original Nash is constructive (an explicit copy) and exact (no error term).
 
The algorithm (Algorithm 2: GameShrink, Theorem 4.1). Iterate over sibling-pairs in the signal tree level by level; whenever two siblings pass the ordered-game-isomorphic check, merge them via a union-find data structure on the filter. Runtime $\tilde O(n^2)$ where $n$ is the signal-tree node count — sublinear in the size of the game tree on any non-trivial game. Theorem 4.1 establishes completeness: GameShrink finds every lossless merge this transformation can produce.
 
What to remember.
 
 
 
 
 
The signal tree, not the game tree, is the natural object for lossless abstraction. Memorising this saves wasted effort when scaling to larger games.
 
 
 
Suit isomorphism in Leduc is the simplest non-trivial instance of ordered game isomorphism: the suit-permutation group acts on the signal tree without changing leaf utilities, so all signal-tree subtrees that differ only by suit satisfy Definition 3.2 by inspection. The Hold'em case fails because suits affect leaf utilities through flushes — Definition 3.2 condition (3) is violated, so the merge is not lossless there.
 
 
 
Lossless implies free. Theorem 3.4 says the merge costs zero exploitability. The only price is running GameShrink itself, which is sublinear in the game tree.
 
 
 
The criterion is binary in this paper. Section 5.1 sketches the relaxation to a threshold on bipartite-matching cost — the first proposed lossy extension of GameShrink, and the conceptual ancestor of the bounded-error approach in §6.2 and the EMD-quantified comparison in §6.3.
 
Implicit route — permutation- and group-equivariant encoders
 
The Deep-RL counterpart to "merge isomorphic info sets" is "use a network architecture whose weights enforce the isomorphism by construction." A function $f_\theta$ is equivariant under a group $\mathcal{G}$ acting on inputs if $f_\theta(g \cdot s) = g \cdot f_\theta(s)$ for all $g \in \mathcal{G}$. Two anchor references:
 
 
 
 
 
Zaheer et al. 2017, "Deep Sets," NeurIPS — networks invariant under permutations of input elements; the canonical building block for unordered card collections.
 
 
 
Cohen & Welling 2016, "Group Equivariant Convolutional Networks," ICML — generalises CNN translation-equivariance to arbitrary discrete groups, including the symmetric group acting on suits.
 
A suit-equivariant encoder over $S_4$ would, by construction, produce identical features for J♠ and J♥ — exactly the merge Gilpin's transformation does explicitly. No clustering pass is needed; the symmetry is baked into the parametrisation. This pattern appears wrapped into Deep CFR-style architectures (step 5) and the large-scale poker networks of step 6.
 
Why these are not the same theorem
 
Gilpin's Theorem 3.4 is a constructive Nash-preservation result: it produces an explicit lift from abstract equilibrium to original equilibrium, and the lift is exact. Equivariance is an architectural symmetry of the function class with no equilibrium implication: an equivariant network composed with regret matching, gradient descent, or a value head can in principle still output a non-Nash strategy. The symmetry is a useful inductive bias, not a guarantee.
 
6.2 Bounded imperfect-recall (Kroer & Sandholm 2016)
 
 
 
Kroer, C. & Sandholm, T. "Imperfect-Recall Abstractions with Bounds in Games," Conference on Economics and Computation (EC) 2016. PDF: https://www.cs.cmu.edu/~sandholm/imperfect_recall_abstraction.arxiv14.pdf
 
The first general, algorithm-agnostic solution-quality guarantee for Nash equilibria computed in imperfect-recall abstractions of extensive-form games — the regime where the agent is deliberately allowed to forget past information in order to merge info sets that would otherwise stay separate. Provides the missing $\varepsilon_{\text{abs}}$ bound that §3.1 promised.
 
Explicit route
 
The setting. Imperfect-recall abstractions break Lanctot et al.'s [2009, "Monte Carlo Sampling for Regret Minimization in Extensive Games"] earlier skew well-formed framework into a richer class. The original game $\Gamma$ is the perfect-recall refinement; the abstracted game $\Gamma'$ is its imperfect-recall coarsening.
 
The criterion (Definition 1: CRSWF — Chance-Relaxed Skew Well-Formed games). $\Gamma'$ is a CRSWF abstraction of $\Gamma$ if for every pair of merged info sets $I, \tilde I \in P(I')$ there exists a leaf-bijection $\varphi: Z_I \to Z_{\tilde I}$ and per-pair scaling/error constants $(\delta_{I,\tilde I}, \varepsilon^R_{I,\tilde I}, \varepsilon^D_{I,\tilde I}, \varepsilon^0_{I,\tilde I})$ controlling four quantities at every leaf $z$:
 
 
 
 
 
Reward error, $\bigl|u_i(z) - \delta_{I,\tilde I} u_i(\varphi(z))\bigr| \le \varepsilon^R_{I,\tilde I}(z)$ — utilities can differ but only up to a per-pair scale-and-bias.
 
 
 
Leaf-probability error, $\bigl|\pi_0(z[I], z) - \pi_0(\varphi(z)[I], \varphi(z))\bigr| \le \varepsilon^0_{I,\tilde I}(z)$ — chance probabilities can differ.
 
 
 
Distribution error, $\bigl|\pi_0(z[I])/\pi_0(I) - \pi_0(\varphi(z)[\tilde I])/\pi_0(\tilde I)\bigr| \le \varepsilon^D_{I,\tilde I}(z[I])$ — conditional chance distributions can differ.
 
 
 
+ 5. Action-sequence consistency (combinatorial conditions on opponent and self moves along merged paths).
 
The CRSWF generalisation over Lanctot et al.'s skew-well-formed scheme is conditions 2 + 3, which decouple absolute and conditional chance probabilities — this is what lets imperfect-recall abstractions merge info sets when chance probabilities differ "by a small amount everywhere."
 
The bounds (Theorems 1 & 2 — main results). For any CRSWF abstraction $\Gamma'$ of $\Gamma$:
 
 
 
 
 
Theorem 1. A strategy $\sigma$ with bounded immediate regret $r_{I'}$ at each abstracted info set $I'$ implements an $\varepsilon$-self-trembling equilibrium in any perfect-recall refinement, with $\varepsilon$ a sum-over-info-sets weighted by reach probability:  $$\varepsilon_i = \max_{\vec a \in X^b_i(r)} \sum_{j \in H_i,\, j \le l} \sum_{I \in D^{\vec a, j}_r} \pi^\sigma_{-i}(I) \biggl( \max_{\tilde I \in P(I')}\Bigl[\delta_{I,\tilde I}\, r(I') + 2\!\!\sum_{s \in I} \tfrac{\pi^\sigma(s)}{\pi^\sigma(I)} \bigl(\varepsilon^0_{I,\tilde I}(s) + \varepsilon^R_{I,\tilde I}(s)\bigr) + \varepsilon^D_{I,\tilde I}\Bigr] \biggr)$$  The reach-weighting is critical for CFR-style algorithms: regret at $I$ only converges weighted by $\pi^\sigma_{-i}(I)$, so error terms get weighted the same way.
 
 
 
Theorem 2. A Nash equilibrium $\sigma$ of the abstract game implements an $\varepsilon$-Nash equilibrium in the perfect-recall refinement, with the same form as Theorem 1 but without the regret term.
 
Both bounds are tighter than the Lanctot et al. predecessor by giving each error term a per-pair probability weighting rather than a maximum over leaves. The paper notes this can reduce the bound exponentially in expressive cases. Concretely: where Lanctot's bound made $(I_A, I_K)$ — pair of aces vs pair of kings — appear as dissimilar as $(I_A, I_2)$ — aces vs twos — Kroer's reach-weighted bound correctly captures that $I_A$ and $I_K$ are strategically much closer.
 
Computational hardness (Theorem 3). Computing the bound-minimising CRSWF abstraction — i.e., picking the partition that gives the smallest $\varepsilon$ for a given info-set budget — is NP-complete, even when restricted to a single-player game with tree height 2. The proof is by reduction from clustering.
 
The clustering escape hatch (Proposition 2). When the action-sequence consistency conditions (4 + 5) are satisfied for all candidate merges and the scaling variables $\delta_{I,\tilde I}$ are fixed, the bound function $d(I, \tilde I) = \text{cost-of-merging}$ becomes a metric on info sets. Single-level abstraction then reduces to k-centre / k-clustering in a metric space, where Gonzalez's [1985] greedy algorithm gives a 2-approximation in polynomial time. Multi-level abstraction is still hard, but level-by-level clustering is the practical algorithm that follows.
 
What to remember.
 
 
 
 
 
The bound is constructive and reach-weighted. Each merge contributes to $\varepsilon_{\text{abs}}$ in proportion to how often it is reached during play. Rare info sets can be merged aggressively without hurting overall exploitability.
 
 
 
NP-hard exactly, polynomial in the metric-space special case. This is why every practical poker abstraction since 2010 has been a clustering pipeline — the clustering reduction is the right computational target.
 
 
 
The $\varepsilon_{\text{abs}}$ floor of §3.1 is now a number, not a vibe. Plug in concrete $\varepsilon^R, \varepsilon^0, \varepsilon^D$ values for any proposed lossy merge and Theorem 2 returns a guaranteed exploitability ceiling.
 
 
 
Forward link to §6.3. Picking the right distance function for the clustering step is the missing piece of this paper; Johanson et al. 2013 (next subsection) supply EMD as the empirically-validated answer.
 
Implicit route — finite-memory recurrent / transformer policies
 
The Deep-RL counterpart to "deliberately forget past information" is "use a sequence model with a bounded-capacity hidden state." The Information Bottleneck Lagrangian on the per-timestep representation $z_t$ forms the continuous analogue:
 
$$\mathcal{L}{\text{IB}}(\theta) = \mathbb{E}\bigl[-\log p\theta(a_t \mid z_t)\bigr] + \beta \cdot I_\theta(z_t; h_{\le t})$$
 
penalising the mutual information $I(z_t; h_{\le t})$ of the hidden state $z_t$ with the full history $h_{\le t}$. As $\beta$ grows, the model is forced to forget more of the history; as $\beta \to 0$, perfect recall is recovered.
 
 
 
 
 
Tishby & Zaslavsky 2015, "Deep Learning and the Information Bottleneck Principle," IEEE ITW — the framing of training under an IB constraint as a rate–distortion problem.
 
 
 
Alemi et al. 2017, "Deep Variational Information Bottleneck," ICLR — VIB: a tractable variational upper bound on $I(z; h)$ that turns the IB Lagrangian into a standard SGD loss with a KL term.
 
The recurrent / transformer architecture choice corresponds to which histories the model can express in $z_t$ at all (an LSTM hidden state of width $d$ caps representable past at roughly $d$ floats; a transformer with context length $L$ caps it at $L$ tokens of attention). Either is a continuous, gradient-tunable version of Kroer's discrete partition coarseness.
 
Why these are not the same theorem
 
Kroer's Theorem 2 gives a constructive, data-independent bound: plug in the per-merge $\varepsilon^R, \varepsilon^0, \varepsilon^D$ and read off a guaranteed exploitability ceiling for the recovered Nash strategy. The IB / VIB bound is on $I(z; h)$, an information-theoretic distance over the training distribution — there is no implication for exploitability against an arbitrary opponent, no Nash-preservation theorem, and the bound is asymptotic (large-data, large-model) rather than instance-wise.
 
6.3 Quality measurement via EMD (Johanson, Burch, Valenzano & Bowling 2013)
 
 
 
Johanson, M., Burch, N., Valenzano, R. & Bowling, M. "Evaluating State-Space Abstractions in Extensive-Form Games," AAMAS 2013, pp. 271–278. PDF: https://poker.cs.ualberta.ca/publications/AAMAS13-abstraction.pdf
 
The paper that supplied two missing pieces of the explicit-abstraction pipeline: a distance function for the clustering step that §6.2 reduces to, and a direct evaluator of abstraction quality that does not require already having the full-game equilibrium for comparison. Both pieces are now industry standard for poker AI.
 
Explicit route
 
The setting. Lossy abstraction in the §6.2 framework reduces to clustering once you fix a distance function between info sets. The natural earlier choice — expected hand strength $E[HS]$, a scalar summarising "what fraction of opponent hands does mine beat in expectation" — collapses too much: it cannot tell the difference between a "made hand" (e.g. a low pair, narrow distribution near $E[HS]$) and a "drawing hand" (e.g. suited high cards, bimodal distribution far from $E[HS]$). The two require different play.
 
The features (Hand Strength Distributions). Instead of the scalar $E[HS]$, store the full histogram of end-of-game hand strengths obtained by rolling out unseen cards: a probability distribution over $[0, 1]$ binned into $k$ buckets, one histogram per (hole cards, board, round) tuple. Two hands with identical $E[HS]$ but different shapes (peaked vs bimodal) now have different feature vectors.
 
The distance metric (Definition 1: Earth Mover's Distance). EMD between two histograms $p, q$ over a 1D bin grid is the minimum work to convert one into the other:
 
$$\text{EMD}(p, q) = \inf_\gamma \mathbb{E}_{(x, y) \sim \gamma} \bigl|x - y\bigr|$$
 
over couplings $\gamma$ with marginals $p$ and $q$. On 1D histograms this reduces to the $L_1$ distance between cumulative distribution functions. Two strategically equivalent hands (same shape) get distance $0$; an "all-strength" vs "all-potential" pair gets a large distance even when their means coincide.
 
The clustering pipeline. Compute HSD features per info set per round, run k-means with the EMD metric (triangle-inequality acceleration per Elkan 2003 + k-means++ initialisation per Arthur & Vassilvitskii 2007 + multi-restart). Output: a partition with $k$ buckets per round. The paper also uses imperfect recall (in the §6.2 sense) to reallocate buckets across rounds — the agent forgets which preflop bucket it was in once the flop arrives, freeing more buckets for the round where they matter.
 
The evaluator (CFR-BR metric). Direct measurement of abstraction quality, independent of any specific solving algorithm: CFR-BR (Johanson et al. 2012) converges to the closest representable Nash approximation the abstraction can express — the strategy that minimises real-game exploitability subject to being constant on each abstract info set. Unlike measuring CFR's output, this isolates abstraction error from solving error. In their experiments CFR-BR strategies have exploitability as low as $\frac{1}{3}$ of the corresponding CFR strategies, confirming that the abstraction itself is rarely the bottleneck — it is the abstract-game equilibrium that drifts away from real-game-Nash.
 
Empirical results (Texas hold'em). Two factorial comparisons on equal info-set budgets:
 
 
 
 
 
Distribution-aware vs expectation-based. HSD + EMD strictly dominates $E[HS]$-based clustering on exploitability and on one-on-one win rate against fixed opponents.
 
 
 
Imperfect vs perfect recall. Imperfect-recall abstractions outperform perfect-recall at matched info-set budget — the bucket-reallocation freedom that §6.2 quantified is empirically worth more than the lost continuity.
 
What to remember.
 
 
 
 
 
EMD is not a vibe; it is the right metric. $E[HS]$ collapses bimodal distributions; EMD does not. Any lossy abstraction whose distance function ignores hand potential is leaving exploitability on the table.
 
 
 
CFR-BR separates abstraction error from solving error. When the deliverable's §8 Pareto frontier is built, "abstract-CFR exploitability" and "abstract-CFR-BR exploitability" are different axes, and the gap between them is itself diagnostic.
 
 
 
The distance function is the design surface that matters. Once a sensible distance is fixed, $k$-means + a budget gives the rest of the pipeline almost for free.
 
 
 
EMD on hand-strength distributions is one specific choice, not the canonical one. Subsequent work (Ganzfried & Sandholm 2014; Brown et al. 2015 on potential-aware imperfect-recall abstraction) generalises the feature to multi-step distributions; a 2024 frontier instance is the KrwEmd metric (Fu et al. 2025, AAAI 2026 — see §11 for the forward pointer).
 
Implicit route — VIB rate–distortion curves and Wasserstein autoencoders
 
The Deep-RL counterpart to "EMD as the abstraction-quality knob" is "Wasserstein distance as the latent-space objective." Two anchor references:
 
 
 
 
 
Alemi et al. 2017, "Deep Variational Information Bottleneck," ICLR — variational tractable form of the IB Lagrangian. The resulting rate–distortion curve (test loss vs $I(z; s)$) is structurally identical to this step's §8 Pareto frontier (info-set count vs $\Delta_{\text{abs}}$): both sweep "compression budget" against "task quality" along a single axis.
 
 
 
Tolstikhin et al. 2018, "Wasserstein Auto-Encoders," ICLR — replaces the KL term in a VAE / VIB by the Wasserstein distance between the aggregated posterior and the prior. Wasserstein and EMD are the same object. Where Johanson uses EMD on hand-strength histograms to merge info sets, a WAE uses Wasserstein on latent codes to shape the encoder.
 
The Pareto curve from §8 of this report and the rate–distortion curve from a VIB / WAE are the same plot. They differ only in the parameterisation of "abstraction": discrete bucket count $k$ on one axis vs continuous bits-of-$z$ on the other.
 
Why these are not the same theorem
 
Johanson et al.'s result is empirical: HSD + EMD outperforms $E[HS]$ at matched info-set budget on real Texas hold'em data, and CFR-BR provides an algorithm-independent quality score. There is no closed-form bound; the validation is repeated runs and statistical significance. The VIB / WAE literature is information-theoretic: bounds on $I(z; s)$ and Wasserstein-2 between aggregated posterior and prior are formal, but they are statements about a learned encoder's compression behaviour, not about the resulting policy's exploitability. Composing the implicit objective with a CFR-style outer loop preserves neither the formal information bound (which assumes i.i.d. data) nor the empirical superiority over scalar features (which is conditional on the network actually learning the right histogram features).
 
6.4 Safe subgame solving (Brown & Sandholm 2017)
 
 
 
Brown, N. & Sandholm, T. "Safe and Nested Subgame Solving for Imperfect-Information Games," NeurIPS 2017 (Best Paper). PDF: https://arxiv.org/pdf/1705.02955v3
 
The technique that closes §3.3: accept that any chosen abstraction has $\varepsilon_{\text{abs}} > 0$ and patch the error at runtime by re-solving specific subgames at higher fidelity, with a guarantee that the patched strategy is no more exploitable than the abstract blueprint. Together with §6.5 (nested), these were the load-bearing components of Libratus, the first AI to defeat top humans in heads-up no-limit Texas hold'em.
 
Explicit route — why isolated subgame solving fails (Coin Toss)
 
The paper opens with a counterexample called Coin Toss (Section 2). A coin lands Heads or Tails with equal probability, only $P_1$ sees the outcome. $P_1$ chooses Sell or Play. The Sell EVs are $+0.5$ if Heads and $-0.5$ if Tails. If Play, $P_2$ guesses the coin's side; correct guess pays $P_1 = -1$, wrong pays $P_1 = +1$. The optimal $P_2$ strategy in the Play subgame is not a function of the Play subgame alone — it depends on the EV of the Sell action $P_1$ would have taken in the unreached subgame. If Sell's EV from Heads is $+0.5$, $P_2$ plays Heads with probability $\tfrac{1}{4}$; if Sell's EV from Heads is $-0.5$ (lucky/unlucky swapped), $P_2$ plays Heads with probability $\tfrac{3}{4}$. Same subgame in isolation, opposite optimal strategy.
 
This is the central pathology that all naive subgame solving in imperfect-info games walks into.
 
Explicit route — the safe subgame-solving family
 
The paper builds a four-step ladder of techniques on the same scaffold: an augmented subgame containing $S$ plus extra "alternative-payoff" nodes that encode what $P_1$ could have achieved by not entering $S$. Solving the augmented subgame and using its $P_2$ strategy in $S$ gives a runtime patch.
 
 
 
 
 
Unsafe (§4.1) — augmented subgame is just $S$ with the blueprint reach probabilities at the root. No safety guarantee. Coin Toss exploits this for arbitrary loss.
 
 
 
Resolve (§4.2) — adds an "opt-out" $P_1$ action $a'T$ at the top of every infoset $I_1 \in S{\textit{top}}$, with payoff equal to $\text{CBV}^{\sigma_2}(I_1)$ — the value $P_1$ achieves by counterfactual best response against the blueprint. Forces the resolved $P_2$ strategy in $S$ to be at least as good as the blueprint.
 
 
 
Maxmargin (§4.3, after Moravčík et al. 2016) — same scaffold, but maximises $\min_{I_1 \in S_{\textit{top}}} M^{\sigma^S}(I_1)$ where $M^{\sigma^S}(I_1) = \text{CBV}^{\sigma_2}(I_1) - \text{CBV}^{\sigma^S_2}(I_1)$. Resolve only forces margins nonnegative; Maxmargin spreads the strict improvement across $I_1$.
 
 
 
Reach (§5 — paper's main new contribution). Considers gifts: if at some prior infoset $I_1' \cdot a' \sqsubset I_1$ along the path to $I_1$, $P_1$ could have chosen a strictly better action $a^$ rather than $a'$, then the difference $\text{CBV}^{\sigma_2}(I_1', a^) - \text{CBV}^{\sigma_2}(I_1', a')$ is a gift the abstract blueprint paid forward. We can let $P_1$'s value at $I_1$ rise by that gift in the augmented subgame, freeing $P_2$ to focus exploitability-reduction on infosets where there were no gifts.
 
The reach margin is
 
$$M_r^{\sigma^S}(I_1) = M^{\sigma^S}(I_1) + \sum_{I_1' \cdot a' \sqsubseteq I_1, P(I_1') = P_1} \bigl\lfloor g^{\sigma_2^{-S}}(I_1', a')\bigr\rfloor$$
 
where $\lfloor g \rfloor$ is a lower bound on the gift that does not require knowing the strategies in subgames other than $S$.
 
The safety guarantee (Theorem 1). For Reach-Maxmargin solving with lower-bound gifts on a set of disjoint subgames, let $\sigma'_2$ be the strategy that uses $\sigma^S_2$ in each $S$ and $\sigma_2$ elsewhere. Then if $\pi^{BR(\sigma'_2)}1(I_1) > 0$ for some $I_1 \in S{\textit{top}}$,
 
$$\textit{exp}(\sigma'2) \le \textit{exp}(\sigma_2^{-S}) - \sum{h \in I_1} \pi^{\sigma_2}_{-1}(h) M_r^{\sigma^S}(I_1)$$
 
i.e., strictly better than past safe techniques whenever any margin is positive. Reach-Resolve and Reach-Maxmargin both inherit Maxmargin's safety; Reach-Resolve does better in practice with estimates (next item).
 
The estimates extension (Theorem 2). The previous techniques use the conservative alternative payoff $\text{CBV}^{\sigma_2}(I_1)$. If you replace it with an estimate $\widetilde{CBV}^{\sigma_2}(I_1)$ of the equilibrium value $\text{CBV}^{\sigma^*_2}(I_1)$, you trade the "no worse than blueprint" guarantee for a quality-vs-estimate-accuracy bound:
 
$$\textit{exp}(\sigma'2) \le \textit{exp}(\sigma^*2) + 2\Delta, \qquad \Delta = \max{S \in \mathbb{S}, I_1 \in S{\textit{top}}} \bigl|\text{CBV}^{\sigma^*_2}(I_1) - \widetilde{CBV}^{\sigma_2}(I_1)\bigr|$$
 
In practice, even very poor abstract strategies produce surprisingly good value estimates (the paper notes a $0.02$-of-full-game abstraction with strategy exploitability $112\text{mbb/h}$ but value-estimation error of only $\sim 2\text{mbb/h}$), so Theorem 2 yields strategies substantially better than the blueprint despite formally giving up the blueprint floor.
 
What to remember.
 
 
 
 
 
The augmented-subgame scaffold is the right mental model. Every safe subgame-solving technique is a different choice of alternative-payoff nodes glued onto $S$.
 
 
 
Reach is a strict improvement on Maxmargin with the same theoretical guarantee — it never does worse, often does better, costs nothing extra to compute.
 
 
 
Estimates beat conservative bounds in practice. Theorem 2 gives the right framing: subgame solving with reasonable equilibrium-value estimates is the production-grade technique.
 
 
 
None of this is action translation. Action translation (§3.2 translators 1–3) is what you do when the opponent plays an off-tree action and you have no live solver. §6.5 dispatches that case differently.
 
Implicit route — ReBeL: belief-state value networks
 
The Deep-RL counterpart to "use a tabular subgame solver at runtime, seeded by an abstract blueprint's $\text{CBV}$ values" is "use a neural value head $V_\phi(\text{public-belief-state})$ to seed the live solve, and learn $V_\phi$ end-to-end."
 
 
 
 
 
Brown, Bakhtin, Lerer & Gong 2020, "Combining Deep Reinforcement Learning and Search for Imperfect-Information Games" (ReBeL), NeurIPS — trains a NN that maps a public belief state (a probability distribution over both players' private information at a given public node) to an EV vector. At runtime, runs CFR on a depth-limited subgame where leaves are evaluated using $V_\phi$ rather than rolling out to terminal. Generalises AlphaZero-style search to imperfect-info games.
 
 
 
Moravčík, Schmid, Burch et al. 2017, "DeepStack: Expert-Level Artificial Intelligence in Heads-Up No-Limit Poker," Science — earlier and simultaneous; uses a NN to evaluate counterfactual values at the leaves of a depth-limited live solve. Proof of concept that NN-augmented subgame solving works in human-scale poker.
 
In both, the explicit safety theorems of this section do not directly transfer — the leaf evaluator is approximate by construction. But the structural pattern (live solve + scaffolded alternative payoffs) is identical to Brown & Sandholm's tabular form; the NN replaces the $\text{CBV}^{\sigma_2}$ table.
 
Why these are not the same theorem
 
Theorem 1 is a conservative, deterministic exploitability bound: $\textit{exp}(\sigma'2) \le \textit{exp}(\sigma_2^{-S}) - \sum \pi M_r$, with no reliance on the blueprint being good. Theorem 2 trades determinism for a $2\Delta$ slack against the true minimally-exploitable strategy. ReBeL / DeepStack provide neither in closed form: their guarantee is asymptotic — as $V\phi$'s training error goes to zero, the live-solve solution converges toward an exact subgame Nash. In practice this is excellent; in theory there is no upfront $\varepsilon$ to read off.
 
6.5 Nested subgame solving (Brown & Sandholm 2017)
 
 
 
Same paper as §6.4 (Section 7). The contribution that makes §3.2's translator catalogue obsolete in production-grade systems.
 
Explicit route
 
The setup. §3.2 covered the action-translation problem: when the opponent plays a $0.7\times\text{pot}$ bet but the abstraction only contains $0.5\times\text{pot}$ and $1\times\text{pot}$, the agent must convert the off-tree action to one in the abstraction before responding. Translators (nearest-action, probability-split, pseudo-harmonic) are systematically exploitable: a sophisticated opponent can engineer bet sizes that lie on the worst point of the translator's grid.
 
The fix. Instead of translating, re-solve a fresh subgame in real time that includes the off-tree action $a$, using the techniques of §6.4 to ground the new solve in the existing blueprint. Two variants:
 
 
 
 
 
Inexpensive — when $P_1$ chooses off-tree $a$ at node $h$, generate a subgame $S$ rooted at $h \cdot a$ that contains the response strategy for $a$ (and only $a$). Solve $S$ via Reach-Resolve / Reach-Maxmargin with alternative payoffs from the blueprint. Append $\sigma^S$ to the existing blueprint to form an extended blueprint $\sigma'$ that now contains $a$. Repeat as further off-tree actions appear (the nested part).
 
 
 
Expensive — root the subgame at $h$ rather than $h \cdot a$, recomputing the entire response set $A(h)$. Larger, sometimes higher-quality, but slow if $h$ is high in the tree.
 
Theoretically, both inherit §6.4's guarantees in the live-solved subgame: the new strategy is no more exploitable than the blueprint within $S$, with optional Theorem-2 estimate-bound treatment for the alternative payoffs.
 
Empirical impact. On heads-up no-limit Texas hold'em, the paper reports that nested subgame solving's exploitability against off-tree opponent bets is multiple orders of magnitude lower than every prior action-translation method. Specifically: the Libratus-era benchmark tables in §8 of the paper show Reach-Estimate + Distributional reducing exploitability versus the leading translator by factors ranging from $\sim 10\times$ on small abstractions to $\sim 100\times$ on heavily-abstracted games.
 
What to remember.
 
 
 
 
 
Nested subgame solving replaces action translation entirely in any system that can afford a live CFR solve. The translators of §3.2 are now best understood as the fallback for systems without that compute budget.
 
 
 
The recursion is shallow in practice. Most real off-tree actions do not chain — opponents play one weird bet, the agent re-solves, and the new abstract tree absorbs it.
 
 
 
Compute cost is the only reason translators still exist. A live CFR solve takes seconds-to-minutes; an action translator is microseconds. For low-latency settings (online play, embedded poker apps) the translator is unavoidable; for engine-vs-engine matches, nested solving wins.
 
Implicit route — depth-limited search with NN value heads
 
The Deep-RL counterpart to "re-solve a fresh subgame containing the off-tree action" is depth-limited search with a learned value head, exactly the AlphaZero / MuZero / ReBeL pattern at the imperfect-information end of the spectrum.
 
 
 
 
 
Schrittwieser et al. 2020, "Mastering Atari, Go, Chess and Shogi by Planning with a Learned Model" (MuZero), Nature — perfect-information analogue: a NN learns environment dynamics + value, and search expands in the learned model. The off-tree-action problem dissolves because the model can simulate any action.
 
 
 
Brown et al. 2020, ReBeL (cited in §6.4) — extends this pattern to imperfect-information games. Off-tree actions are handled by simply running CFR in a fresh depth-limited subgame containing them, with the leaf evaluator $V_\phi$ standing in for what the explicit method computes from blueprint $\text{CBV}$ values.