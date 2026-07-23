import pytest

from poker.cards import parse_cards
from poker.exact import exact_equity_completed_board


def test_exact_completed_board_equity():
    player_cards = parse_cards("Ah 7d")
    board = parse_cards("As Kc Kd 4h 2s")

    results = exact_equity_completed_board(player_cards,board)

    assert results["total_hands"] == 990
    assert results["wins"] == 834
    assert results["ties"] == 6
    assert results["losses"] == 150

    assert results["win_probability"] == pytest.approx( 834 / 990)
    assert results["tie_probability"] == pytest.approx(6 / 990)
    assert results["loss_probability"] == pytest.approx(150 / 990)
    assert results["equity"] == pytest.approx(837 / 990)


def test_exact_enumeration_requires_full_board():
    player_cards = parse_cards("Ah 7d")
    incomplete_board = parse_cards("As Kc Kd")

    with pytest.raises(ValueError):
        exact_equity_completed_board(player_cards,incomplete_board)