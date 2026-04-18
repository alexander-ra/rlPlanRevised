"""Tests for all CFR trainer variants.

Tests focus on:
- Correct number of info sets (936 for full-traversal variants)
- Game value is finite and in a reasonable range
- Strategies sum to ~1.0
- Variant-specific invariants (e.g., CFR+ non-negative regrets)
"""
import random
import pytest
from cfr.cfr_trainer import LeducTrainer
from cfr.cfrplus_trainer import LeducCFRPlusTrainer
from cfr.mccfr_external_trainer import LeducExternalSamplingTrainer
from cfr.mccfr_outcome_trainer import LeducOutcomeSamplingTrainer


# ── Vanilla CFR ──────────────────────────────────────────────────

class TestVanillaCFR:
    @pytest.fixture(scope="class")
    def trained(self):
        """Train once, reuse across tests in this class."""
        trainer = LeducTrainer()
        game_val = trainer.train(iterations=30)
        return trainer, game_val

    def test_produces_936_info_sets(self, trained):
        trainer, _ = trained
        assert len(trainer.node_map) == 936

    def test_game_value_finite(self, trained):
        _, game_val = trained
        assert game_val == game_val  # not NaN
        assert abs(game_val) < 10    # reasonable magnitude

    def test_game_value_negative(self, trained):
        """Player 0 acts first → slight disadvantage in Leduc."""
        _, game_val = trained
        assert game_val < 0

    def test_strategies_sum_to_one(self, trained):
        trainer, _ = trained
        for info_set, (node, _) in trainer.node_map.items():
            avg = node.get_average_strategy()
            assert sum(avg) == pytest.approx(1.0, abs=1e-6), f"Failed at {info_set}"

    def test_history_recorded(self, trained):
        trainer, _ = trained
        assert len(trainer.game_value_history) > 0
        assert len(trainer.iteration_history) > 0
        assert trainer.iteration_history[-1] == 30

    def test_get_strategy_table(self, trained):
        trainer, _ = trained
        table = trainer.get_strategy_table()
        assert len(table) == 936
        # Each entry should have valid action names
        for info_set, strat in table.items():
            assert sum(strat.values()) == pytest.approx(1.0, abs=1e-6)
            for key in strat:
                assert key in ('fold', 'check/call', 'raise')

    def test_node_map_legal_actions_consistent(self, trained):
        trainer, _ = trained
        for info_set, (node, legal_actions) in trainer.node_map.items():
            assert node.num_actions == len(legal_actions)
            # All legal actions should be valid Leduc actions
            for a in legal_actions:
                assert a in (0, 1, 2)


# ── CFR+ ─────────────────────────────────────────────────────────

class TestCFRPlus:
    @pytest.fixture(scope="class")
    def trained(self):
        trainer = LeducCFRPlusTrainer()
        game_val = trainer.train(iterations=30)
        return trainer, game_val

    def test_produces_936_info_sets(self, trained):
        trainer, _ = trained
        assert len(trainer.node_map) == 936

    def test_game_value_finite(self, trained):
        _, game_val = trained
        assert game_val == game_val
        assert abs(game_val) < 10

    def test_regrets_non_negative(self, trained):
        """CFR+ floors regrets to zero after each iteration."""
        trainer, _ = trained
        for info_set, (node, _) in trainer.node_map.items():
            for r in node.regret_sum:
                assert r >= 0.0, f"Negative regret at {info_set}"

    def test_strategies_sum_to_one(self, trained):
        trainer, _ = trained
        for info_set, (node, _) in trainer.node_map.items():
            avg = node.get_average_strategy()
            assert sum(avg) == pytest.approx(1.0, abs=1e-6)

    def test_strategy_table_valid(self, trained):
        trainer, _ = trained
        table = trainer.get_strategy_table()
        assert len(table) == 936


# ── MCCFR External Sampling ─────────────────────────────────────

class TestMCCFRExternal:
    @pytest.fixture(scope="class")
    def trained(self):
        random.seed(42)
        trainer = LeducExternalSamplingTrainer()
        game_val = trainer.train(iterations=500)
        return trainer, game_val

    def test_produces_info_sets(self, trained):
        trainer, _ = trained
        # Sampling may not visit all 936 in 500 iters, but should find many
        assert len(trainer.node_map) > 400

    def test_game_value_finite(self, trained):
        _, game_val = trained
        assert game_val == game_val  # not NaN
        assert abs(game_val) < 50    # looser bound for sampling

    def test_strategies_sum_to_one(self, trained):
        trainer, _ = trained
        for info_set, (node, _) in trainer.node_map.items():
            avg = node.get_average_strategy()
            assert sum(avg) == pytest.approx(1.0, abs=1e-6)

    def test_history_recorded(self, trained):
        trainer, _ = trained
        assert len(trainer.game_value_history) > 0
        assert trainer.iteration_history[-1] == 500

    def test_strategy_table(self, trained):
        trainer, _ = trained
        table = trainer.get_strategy_table()
        assert len(table) > 0
        for strat in table.values():
            assert sum(strat.values()) == pytest.approx(1.0, abs=1e-6)


# ── MCCFR Outcome Sampling ──────────────────────────────────────

class TestMCCFROutcome:
    @pytest.fixture(scope="class")
    def trained(self):
        random.seed(123)
        trainer = LeducOutcomeSamplingTrainer(epsilon=0.6)
        game_val = trainer.train(iterations=500)
        return trainer, game_val

    def test_produces_info_sets(self, trained):
        trainer, _ = trained
        # Outcome sampling visits fewer info sets per iteration
        assert len(trainer.node_map) > 100

    def test_game_value_finite(self, trained):
        _, game_val = trained
        assert game_val == game_val  # not NaN
        # Outcome sampling is high-variance, allow wider bounds
        assert abs(game_val) < 100

    def test_strategies_sum_to_one(self, trained):
        trainer, _ = trained
        for info_set, (node, _) in trainer.node_map.items():
            avg = node.get_average_strategy()
            assert sum(avg) == pytest.approx(1.0, abs=1e-6)

    def test_epsilon_stored(self, trained):
        trainer, _ = trained
        assert trainer.epsilon == 0.6

    def test_strategy_table(self, trained):
        trainer, _ = trained
        table = trainer.get_strategy_table()
        assert len(table) > 0

    def test_custom_epsilon(self):
        """Verify epsilon parameter is respected."""
        t = LeducOutcomeSamplingTrainer(epsilon=0.3)
        assert t.epsilon == 0.3


# ── Cross-variant consistency ────────────────────────────────────

class TestCrossVariant:
    """All trainers should share the same node_map interface."""

    @pytest.mark.parametrize("TrainerClass", [
        LeducTrainer,
        LeducCFRPlusTrainer,
        LeducExternalSamplingTrainer,
        LeducOutcomeSamplingTrainer,
    ])
    def test_trainer_has_required_attributes(self, TrainerClass):
        t = TrainerClass() if TrainerClass != LeducOutcomeSamplingTrainer else TrainerClass(0.6)
        assert hasattr(t, 'node_map')
        assert hasattr(t, 'game_value_history')
        assert hasattr(t, 'iteration_history')
        assert hasattr(t, 'train')
        assert hasattr(t, 'get_strategy_table')

    @pytest.mark.parametrize("TrainerClass", [
        LeducTrainer,
        LeducCFRPlusTrainer,
        LeducExternalSamplingTrainer,
        LeducOutcomeSamplingTrainer,
    ])
    def test_train_returns_float(self, TrainerClass):
        random.seed(99)
        t = TrainerClass() if TrainerClass != LeducOutcomeSamplingTrainer else TrainerClass(0.6)
        val = t.train(iterations=5)
        assert isinstance(val, float)
