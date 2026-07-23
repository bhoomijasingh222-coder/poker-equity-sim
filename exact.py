from itertools import combinations

from poker.cards import create_deck
from poker.eval import evaluate_hand


def exact_equity_completed_board(player_cards, board):
    if len(player_cards) != 2:
        raise ValueError("The player must have exactly two cards")

    if len(board) != 5:
        raise ValueError("Exact enumeration requires a completed five-card board")

    known_cards = player_cards + board

    if len(known_cards) != len(set(known_cards)):
        raise ValueError("Duplicate cards were entered")

    remaining_deck = []

    for card in create_deck():
        if card not in known_cards:
            remaining_deck.append(card)

    player_score = evaluate_hand(player_cards + board)

    wins = 0
    ties = 0
    losses = 0
    equity_share = 0.0
    total_hands = 0

    possible_opponent_hands = combinations(remaining_deck, 2)

    for opp_hand in possible_opponent_hands:
        opponent_hand = list(opp_hand)

        opponent_score = evaluate_hand(opponent_hand + board)

        total_hands = total_hands + 1

        if player_score > opponent_score:
            wins += 1
            equity_share += 1.0

        elif player_score == opponent_score:
            ties += 1
            equity_share += 0.5

        else:
            losses += 1

    
    win_p = wins / total_hands
    tie_p = ties / total_hands
    loss_p = losses / total_hands
    equity = equity_share / total_hands

    return { "wins": wins,
        "ties": ties,
        "losses": losses,
        "total_hands": total_hands,
        "win_probability": win_p,
        "tie_probability": tie_p,
        "loss_probability": loss_p,
        "equity": equity}

