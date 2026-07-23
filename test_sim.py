import pytest

from poker.cards import parse_cards
from poker.sim import estimate_equity


def test_royal_flush_on_board_always_ties_heads_up():
    player_cards = parse_cards("2c 3d")
    board = parse_cards("As Ks Qs Js Ts")

    results = estimate_equity(player_cards=player_cards, board=board, num_opponents=1, simulations=100)

    assert results["wins"] == 0
    assert results["ties"] == 100
    assert results["losses"] == 0

    assert results["win_probability"] == 0
    assert results["tie_probability"] == 1
    assert results["loss_probability"] == 0
    assert results["equity"] == pytest.approx(0.5)


def test_private_royal_flush_always_wins():
    player_cards = parse_cards("As Ks")
    board = parse_cards("Qs Js Ts 2d 3c")

    results = estimate_equity(player_cards=player_cards, board=board, num_opponents=1, simulations=100)

    assert results["wins"] == 100
    assert results["ties"] == 0
    assert results["losses"] == 0
    assert results["equity"] == pytest.approx(1.0)



def test_probabilities_sum_to_one():
    player_cards = parse_cards("As Qs")
    board = parse_cards("Js 7s 2d")

    results = estimate_equity(player_cards, board, num_opponents=1, simulations=1000)
    probability_total = (results["win_probability"] + results["tie_probability"] + results["loss_probability"])

    assert probability_total == pytest.approx(1.0)


def test_counts_equal_simulation_total():
    player_cards = parse_cards("As Qs")
    board = parse_cards("Js 7s 2d")

    results = estimate_equity(player_cards, board, num_opponents=1,simulations=1000)

    outcome_total = (results["wins"] + results["ties"] + results["losses"])
    assert outcome_total == 1000


def test_equity_is_valid_probability():
    player_cards = parse_cards("As Qs")
    board = parse_cards("Js 7s 2d")

    results = estimate_equity( player_cards, board, num_opponents=1, simulations=1000)

    assert 0 <= results["equity"] <= 1