"""Tests for the Leduc Poker game engine.

Thorough coverage since this engine is reused across steps.
"""
import pytest
from cfr.leduc_poker import (
    FOLD, CHECK_CALL, RAISE, NUM_ACTIONS, NUM_CARDS,
    ACTION_NAMES, RANK_NAMES, ANTE, RAISE_AMOUNTS, MAX_RAISES_PER_ROUND,
    card_rank, card_str, get_all_deals, ALL_DEALS,
    _hand_strength, showdown_winner, LeducState, action_to_str,
)


# ── Helper functions ──────────────────────────────────────────────

class TestCardHelpers:
    def test_card_rank_jacks(self):
        assert card_rank(0) == 0
        assert card_rank(1) == 0

    def test_card_rank_queens(self):
        assert card_rank(2) == 1
        assert card_rank(3) == 1

    def test_card_rank_kings(self):
        assert card_rank(4) == 2
        assert card_rank(5) == 2

    def test_card_str_suits(self):
        # Even cards = 's', odd cards = 'h'
        assert card_str(0) == 'Js'
        assert card_str(1) == 'Jh'
        assert card_str(2) == 'Qs'
        assert card_str(3) == 'Qh'
        assert card_str(4) == 'Ks'
        assert card_str(5) == 'Kh'

    def test_action_to_str(self):
        assert action_to_str(FOLD) == 'f'
        assert action_to_str(CHECK_CALL) == 'c'
        assert action_to_str(RAISE) == 'r'


class TestHandStrength:
    def test_pair_beats_high_card(self):
        # Jack pair vs King high card
        assert _hand_strength(0, 1) > _hand_strength(4, 2)  # J pair > K no-pair

    def test_higher_pair_beats_lower_pair(self):
        # King pair vs Jack pair
        assert _hand_strength(4, 5) > _hand_strength(0, 1)

    def test_higher_rank_beats_lower_no_pair(self):
        # King no-pair vs Jack no-pair (community = Queen)
        assert _hand_strength(4, 2) > _hand_strength(0, 2)

    def test_same_rank_no_pair_is_tie(self):
        # Two jacks (different suits), community is Queen → neither pairs
        assert _hand_strength(0, 2) == _hand_strength(1, 2)


class TestShowdownWinner:
    def test_player0_wins_higher_rank(self):
        # P0 has King(4), P1 has Jack(0), community Queen(2) → no pairs, K > J
        assert showdown_winner((4, 0), 2) == 1

    def test_player1_wins_higher_rank(self):
        # P0 has Jack(0), P1 has King(4), community Queen(2)
        assert showdown_winner((0, 4), 2) == -1

    def test_tie_same_rank(self):
        # P0 has Js(0), P1 has Jh(1), community Queen → tie
        assert showdown_winner((0, 1), 2) == 0

    def test_pair_beats_higher_rank(self):
        # P0 has Jack(0), P1 has King(4), community Jack(1) → P0 pairs
        assert showdown_winner((0, 4), 1) == 1

    def test_both_pair_higher_wins(self):
        # P0 has King(4), P1 has Jack(0), community King(5) → P0 pairs
        assert showdown_winner((4, 0), 5) == 1


# ── Deal generation ───────────────────────────────────────────────

class TestDeals:
    def test_all_deals_count(self):
        assert len(ALL_DEALS) == 120  # 6 * 5 * 4

    def test_no_duplicate_cards_in_deal(self):
        for c0, c1, cc in ALL_DEALS:
            assert len({c0, c1, cc}) == 3

    def test_all_cards_in_range(self):
        for c0, c1, cc in ALL_DEALS:
            for c in (c0, c1, cc):
                assert 0 <= c < NUM_CARDS

    def test_get_all_deals_matches_constant(self):
        assert get_all_deals() == ALL_DEALS


# ── LeducState basics ────────────────────────────────────────────

class TestLeducStateInit:
    def test_initial_state(self):
        s = LeducState((0, 4), 2)
        assert s.cards == (0, 4)
        assert s.community == 2
        assert s.round == 0
        assert s.bets == [ANTE, ANTE]  # [1, 1]
        assert s.history == ""
        assert not s.is_terminal()
        assert s.current_player() == 0

    def test_initial_legal_actions(self):
        s = LeducState((0, 4), 2)
        # No raise yet → can check/call or raise, NOT fold
        assert s.legal_actions() == [CHECK_CALL, RAISE]


# ── Action mechanics ─────────────────────────────────────────────

class TestApplyAction:
    def test_apply_action_returns_new_state(self):
        s = LeducState((0, 4), 2)
        s2 = s.apply_action(CHECK_CALL)
        assert s2 is not s
        assert s.history == ""       # original unchanged
        assert s2.history != ""      # new state has history

    def test_check_check_round0_advances_to_round1(self):
        s = LeducState((0, 4), 2)
        s = s.apply_action(CHECK_CALL)  # P0 checks
        s = s.apply_action(CHECK_CALL)  # P1 checks → round 1
        assert s.round == 1
        assert '/' in s.history
        assert not s.is_terminal()
        assert s.bets == [ANTE, ANTE]

    def test_fold_after_raise_is_terminal(self):
        s = LeducState((0, 4), 2)
        s = s.apply_action(RAISE)      # P0 raises
        s = s.apply_action(FOLD)       # P1 folds
        assert s.is_terminal()
        assert s.folded == 1  # player 1 folded

    def test_raise_increases_bets(self):
        s = LeducState((0, 4), 2)
        s = s.apply_action(RAISE)  # P0 raises by 2 in round 0
        assert s.bets[0] == ANTE + RAISE_AMOUNTS[0]  # 1 + 2 = 3
        assert s.bets[1] == ANTE  # still 1

    def test_call_after_raise_equalizes_bets(self):
        s = LeducState((0, 4), 2)
        s = s.apply_action(RAISE)       # P0 raises → bets [3, 1]
        s = s.apply_action(CHECK_CALL)  # P1 calls → bets [3, 3], round advances
        assert s.bets == [3, 3]
        assert s.round == 1

    def test_raise_reraise_round0(self):
        s = LeducState((0, 4), 2)
        s = s.apply_action(RAISE)  # P0 raises → bets [3, 1]
        s = s.apply_action(RAISE)  # P1 re-raises → bets [3, 5]
        assert s.bets == [3, 5]
        assert s.num_raises[0] == 2  # max raises hit
        # P0 can only fold or call now
        assert RAISE not in s.legal_actions()
        assert sorted(s.legal_actions()) == [FOLD, CHECK_CALL]

    def test_full_game_to_showdown(self):
        """check-check, check-check → showdown."""
        s = LeducState((4, 0), 2)  # K vs J, community Q
        s = s.apply_action(CHECK_CALL)  # P0 checks
        s = s.apply_action(CHECK_CALL)  # P1 checks → round 1
        s = s.apply_action(CHECK_CALL)  # P0 checks
        s = s.apply_action(CHECK_CALL)  # P1 checks → showdown
        assert s.is_terminal()
        assert s.folded == -1   # nobody folded
        assert s.history == 'cc/cc'

    def test_round2_raise_amount(self):
        """In round 2, raise size is 4."""
        s = LeducState((0, 4), 2)
        # Round 0: check-check
        s = s.apply_action(CHECK_CALL)
        s = s.apply_action(CHECK_CALL)
        # Round 1: raise
        assert s.round == 1
        s = s.apply_action(RAISE)
        assert s.bets[0] == ANTE + RAISE_AMOUNTS[1]  # 1 + 4 = 5


# ── Legal actions ────────────────────────────────────────────────

class TestLegalActions:
    def test_fold_only_when_facing_raise(self):
        s = LeducState((0, 4), 2)
        assert FOLD not in s.legal_actions()  # no raise yet
        s = s.apply_action(RAISE)
        assert FOLD in s.legal_actions()      # facing raise

    def test_raise_capped_at_max(self):
        s = LeducState((0, 4), 2)
        s = s.apply_action(RAISE)  # raise 1
        s = s.apply_action(RAISE)  # raise 2 (max)
        assert RAISE not in s.legal_actions()

    def test_terminal_state_no_actions(self):
        s = LeducState((0, 4), 2)
        s = s.apply_action(RAISE)
        s = s.apply_action(FOLD)
        assert s.legal_actions() == []


# ── Information sets ─────────────────────────────────────────────

class TestInfoSets:
    def test_round0_format(self):
        s = LeducState((3, 4), 2)  # P0 has card 3
        info = s.get_info_set(0)
        assert info == "3|"   # card_id | empty history

    def test_round0_with_actions(self):
        s = LeducState((3, 4), 2)
        s = s.apply_action(RAISE)  # P0 raises
        # Now it's P1's turn; P1's info set:
        info = s.get_info_set(1)
        assert info == "4|r"

    def test_round1_includes_community(self):
        s = LeducState((3, 4), 2)
        s = s.apply_action(CHECK_CALL)
        s = s.apply_action(CHECK_CALL)  # → round 1
        info = s.get_info_set(0)
        assert info == "3:2|cc/"  # card:community|history

    def test_different_suits_different_info_sets(self):
        """Cards 0 and 1 are both Jacks but produce different info sets."""
        s0 = LeducState((0, 4), 2)
        s1 = LeducState((1, 4), 2)
        assert s0.get_info_set(0) != s1.get_info_set(0)  # "0|" vs "1|"

    def test_player_cannot_see_opponent_card(self):
        s = LeducState((0, 4), 2)
        info0 = s.get_info_set(0)
        info1 = s.get_info_set(1)
        assert '0' in info0 and '4' not in info0
        assert '4' in info1 and '0' not in info1  # card 0 not visible to P1


# ── Utilities ────────────────────────────────────────────────────

class TestGetUtility:
    def test_fold_utility_folder_loses(self):
        # P0 raises, P1 folds → P1 loses their ante
        s = LeducState((0, 4), 2)
        s = s.apply_action(RAISE)
        s = s.apply_action(FOLD)
        assert s.get_utility(0) == 1.0   # P0 wins P1's ante
        assert s.get_utility(1) == -1.0  # P1 loses ante

    def test_fold_utility_after_reraise(self):
        # P0 raises, P1 re-raises, P0 folds
        s = LeducState((0, 4), 2)
        s = s.apply_action(RAISE)   # P0 bets [3,1]
        s = s.apply_action(RAISE)   # P1 bets [3,5]
        s = s.apply_action(FOLD)    # P0 folds
        assert s.get_utility(0) == -3.0  # P0 loses 3 chips
        assert s.get_utility(1) == 3.0   # P1 wins 3 chips

    def test_showdown_winner_gets_opponents_bet(self):
        # K vs J, community Q → K wins (no pair, higher rank)
        s = LeducState((4, 0), 2)
        for _ in range(4):  # check-check-check-check
            s = s.apply_action(CHECK_CALL)
        assert s.is_terminal()
        assert s.get_utility(0) == 1.0   # K wins J's ante
        assert s.get_utility(1) == -1.0  # J loses

    def test_showdown_tie_zero(self):
        # Js vs Jh, community Q → same rank, no pair → tie
        s = LeducState((0, 1), 2)
        for _ in range(4):
            s = s.apply_action(CHECK_CALL)
        assert s.get_utility(0) == 0.0
        assert s.get_utility(1) == 0.0

    def test_pair_wins_showdown(self):
        # P0 has J(0), P1 has K(4), community J(1) → P0 pairs, wins
        s = LeducState((0, 4), 1)
        for _ in range(4):
            s = s.apply_action(CHECK_CALL)
        assert s.get_utility(0) == 1.0
        assert s.get_utility(1) == -1.0

    def test_max_raises_both_rounds_utility(self):
        """Full raise game: raise-raise-call / raise-raise-call → showdown.
        K(4) vs J(0), community Q(2) → K wins.
        Round 0 pot: raise + re-raise + call = each committed 1+2+2 = ante + raise + call_raise = 5
        Actually: P0 raises→[3,1], P1 reraises→[3,5], P0 calls→[5,5]. Round 1: same with 4.
        """
        s = LeducState((4, 0), 2)
        # Round 0: raise, re-raise, call
        s = s.apply_action(RAISE)       # P0 [3,1]
        s = s.apply_action(RAISE)       # P1 [3,5]
        s = s.apply_action(CHECK_CALL)  # P0 [5,5] → round 1
        # Round 1: raise, re-raise, call
        s = s.apply_action(RAISE)       # P0 [9,5]
        s = s.apply_action(RAISE)       # P1 [9,13]
        s = s.apply_action(CHECK_CALL)  # P0 [13,13] → showdown
        assert s.is_terminal()
        assert s.bets == [13, 13]
        assert s.get_utility(0) == 13.0   # K wins
        assert s.get_utility(1) == -13.0


# ── Constants sanity ─────────────────────────────────────────────

class TestConstants:
    def test_action_values(self):
        assert FOLD == 0
        assert CHECK_CALL == 1
        assert RAISE == 2
        assert NUM_ACTIONS == 3

    def test_game_params(self):
        assert ANTE == 1
        assert RAISE_AMOUNTS == [2, 4]
        assert MAX_RAISES_PER_ROUND == 2
        assert NUM_CARDS == 6
