"""Tests for InfoSetNode."""
import pytest
from cfr.info_set_node import InfoSetNode


class TestGetStrategy:
    def test_uniform_when_no_regret(self):
        node = InfoSetNode(3)
        strat = node.get_strategy(1.0)
        assert strat == pytest.approx([1/3, 1/3, 1/3])

    def test_positive_regret_dominates(self):
        node = InfoSetNode(3)
        node.regret_sum = [10.0, 0.0, 0.0]
        strat = node.get_strategy(1.0)
        assert strat == pytest.approx([1.0, 0.0, 0.0])

    def test_mixed_regrets_negative_ignored(self):
        node = InfoSetNode(3)
        node.regret_sum = [6.0, -5.0, 4.0]
        strat = node.get_strategy(1.0)
        assert strat == pytest.approx([0.6, 0.0, 0.4])

    def test_strategy_sum_updated(self):
        node = InfoSetNode(2)
        node.regret_sum = [3.0, 1.0]
        node.get_strategy(2.0)  # reach = 2.0
        # strategy = [0.75, 0.25], weighted by 2.0
        assert node.strategy_sum == pytest.approx([1.5, 0.5])

    def test_strategy_sum_accumulates(self):
        node = InfoSetNode(2)
        node.get_strategy(1.0)  # uniform → [0.5, 0.5]
        node.get_strategy(1.0)  # uniform → [0.5, 0.5]
        assert node.strategy_sum == pytest.approx([1.0, 1.0])


class TestGetCurrentStrategy:
    def test_does_not_update_strategy_sum(self):
        node = InfoSetNode(3)
        node.regret_sum = [6.0, 0.0, 4.0]
        strat = node.get_current_strategy()
        assert strat == pytest.approx([0.6, 0.0, 0.4])
        assert node.strategy_sum == [0.0, 0.0, 0.0]  # unchanged

    def test_uniform_when_no_regret(self):
        node = InfoSetNode(2)
        strat = node.get_current_strategy()
        assert strat == pytest.approx([0.5, 0.5])


class TestGetAverageStrategy:
    def test_uniform_when_no_training(self):
        node = InfoSetNode(3)
        avg = node.get_average_strategy()
        assert avg == pytest.approx([1/3, 1/3, 1/3])

    def test_after_accumulation(self):
        node = InfoSetNode(2)
        node.strategy_sum = [3.0, 1.0]
        avg = node.get_average_strategy()
        assert avg == pytest.approx([0.75, 0.25])

    def test_two_actions(self):
        node = InfoSetNode(2)
        node.strategy_sum = [5.0, 5.0]
        assert node.get_average_strategy() == pytest.approx([0.5, 0.5])
