from poker.cards import parse_cards
from poker.eval import evaluate_five, evaluate_hand

import pytest


def test_straight_flush():
    cards = parse_cards("As Ks Qs Js Ts")
    score = evaluate_five(cards)

    assert score == (8, 14)


def test_four_of_a_kind():
    cards = parse_cards("Ah Ad Ac As Kd")
    score = evaluate_five(cards)

    assert score == (7, 14, 13)


def test_full_house():
    cards = parse_cards("Ah Ad Ac Ks Kd")
    score = evaluate_five(cards)

    assert score == (6, 14, 13)


def test_flush():
    cards = parse_cards("2h 5h 8h Jh Kh")
    score = evaluate_five(cards)

    assert score == (5, 13, 11, 8, 5, 2)


def test_ace_high_straight():
    cards = parse_cards("As Kd Qc Jh Ts")
    score = evaluate_five(cards)

    assert score == (4, 14)


def test_ace_low_straight():
    cards = parse_cards("As 2d 3c 4h 5s")
    score = evaluate_five(cards)

    assert score == (4, 5)


def test_three_of_a_kind():
    cards = parse_cards("Qh Qd Qs Ac 9h")
    score = evaluate_five(cards)

    assert score == (3, 12, 14, 9)


def test_two_pair():
    cards = parse_cards("Ah Ad Kc Ks 7h")
    score = evaluate_five(cards)

    assert score == (2, 14, 13, 7)


def test_one_pair():
    cards = parse_cards("Ah Ad Kc Qs 9h")
    score = evaluate_five(cards)

    assert score == (1, 14, 13, 12, 9)


def test_high_card():
    cards = parse_cards("Ah Kd 9c 7s 2h")
    score = evaluate_five(cards)

    assert score == (0, 14, 13, 9, 7, 2)


def test_straight_flush_beats_four_of_a_kind():
    straight_flush = evaluate_five(parse_cards("As Ks Qs Js Ts"))
    four_of_a_kind = evaluate_five(parse_cards("Ah Ad Ac As Kd"))

    assert straight_flush > four_of_a_kind


def test_pair_of_aces_beats_pair_of_kings():
    pair_of_aces = evaluate_five(parse_cards("Ah Ad Kc Qs 9h"))
    pair_of_kings = evaluate_five(parse_cards("Kh Kd Ac Qs 9h"))

    assert pair_of_aces > pair_of_kings


def test_higher_kicker_wins():
    king_kicker = evaluate_five(parse_cards("Ah Ad Kc 8s 3h"))
    queen_kicker = evaluate_five( parse_cards("As Ac Qd 8h 3c"))

    assert king_kicker > queen_kicker


def test_evaluate_hand_rejects_four_cards():
    cards = parse_cards("As Kh Qd Jc")
    with pytest.raises(ValueError):
        evaluate_hand(cards)