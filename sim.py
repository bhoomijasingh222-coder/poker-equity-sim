import random

from poker.cards import Card, create_deck
from poker.eval import evaluate_hand

def checking_inputs(player_cards: list[Card], board: list[Card],num_opponents: int):
    if len(player_cards) != 2:
        raise ValueError("player must have exactly two hole cards")

    if len(board) > 5:
        raise ValueError("The board cannot contain more than five cards")

    if num_opponents < 1:
        raise ValueError("There must be at least one opponent")

    known_cards = player_cards + board

    if len(known_cards) != len(set(known_cards)):
        raise ValueError("Duplicate cards were entered")

    cards_needed = (2 * num_opponents) + (5 - len(board))

    remaining_cards = 52 - len(known_cards)

    if cards_needed > remaining_cards:
        raise ValueError("Not enough cards remain in the deck")


def simulate_once(player_cards: list[Card], board: list[Card], num_opponents: int, rcg: random.Random,):
    known_cards = player_cards + board
    remaining_deck = [card for card in create_deck() if card not in known_cards]

    cards_needed = 2 * num_opponents + (5 - len(board))
    sampled_cards = rcg.sample(remaining_deck, cards_needed)

    opponent_hands = []
    position = 0

    for opp in range(num_opponents):
        first_card = sampled_cards[position]
        second_card = sampled_cards[position + 1]

        opponent_hand = [first_card, second_card]
        opponent_hands.append(opponent_hand)

        position = position + 2

    completed_board = board + sampled_cards[position:]
    
    
    player_score = evaluate_hand(player_cards + completed_board)
    opponent_scores =[]
    for hand in opponent_hands:
        opponent_score = evaluate_hand(hand + completed_board)
        opponent_scores.append(opponent_score)

    all_scores = [player_score] + opponent_scores
    best_score = max(all_scores)
    winners = []

    for index, score in enumerate(all_scores):
        if score == best_score:
            winners.append(index)


    if 0 not in winners:
        return ("loss", 0)

    elif len(winners) == 1:
        return ("win", 1)

    return ("tie", len(winners))


def estimate_equity(player_cards,board, num_opponents, simulations: int = 50_000):
    checking_inputs(player_cards, board, num_opponents)

    if simulations <= 0:
        raise ValueError("The number of simulations must be positive")

    rcg = random.Random()

    wins = 0
    ties = 0
    losses = 0
    equity_share = 0.0

    for s in range(simulations):
        result, num_winners = simulate_once(player_cards, board, num_opponents, rcg)

        if result == "win":
            wins += 1
            equity_share += 1.0

        elif result == "tie":
            ties += 1
            equity_share += 1.0 / num_winners

        else:
            losses += 1

        win_p =  wins / simulations
        tie_p = ties / simulations
        loss_p = losses / simulations
        equity  =  equity_share / simulations

    return{
        "wins": wins,
        "ties": ties,
        "losses": losses,
        "win_probability": win_p,
        "tie_probability": tie_p,
        "loss_probability": loss_p ,
        "equity": equity,
        "simulations": simulations}

    








