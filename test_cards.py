import pytest

from poker.cards import Card, create_deck, parse_card, parse_cards


def test_create_one_card():
    card = Card("A", "s")

    assert card.rank == "A"
    assert card.suit == "s"


def test_parse_one_card():
    card = parse_card("Ah")

    assert card == Card("A", "h")


def test_parse_several_cards():
    cards = parse_cards("As Kh 7d")

    assert cards == [Card("A", "s"), Card("K", "h"), Card("7", "d")]


def test_deck_has_52_cards():
    deck = create_deck()

    assert len(deck) == 52


def test_deck_has_no_duplicates():
    deck = create_deck()

    assert len(set(deck)) == 52


def test_invalid_rank():
    with pytest.raises(ValueError):
        Card("X", "s")


def test_invalid_suit():
    with pytest.raises(ValueError):
        Card("A", "x")