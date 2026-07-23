from collections import Counter
from itertools import combinations

from poker.cards import Card
from poker.cards import parse_cards

RANKS = "23456789TJQKA"
RANK_NAMES = {2: "Two",
    3: "Three",
    4: "Four",
    5: "Five",
    6: "Six",
    7: "Seven",
    8: "Eight",
    9: "Nine",
    10: "Ten",
    11: "Jack",
    12: "Queen",
    13: "King",
    14: "Ace"}


RANK_PLURALS = {
    2: "Twos",
    3: "Threes",
    4: "Fours",
    5: "Fives",
    6: "Sixes",
    7: "Sevens",
    8: "Eights",
    9: "Nines",
    10: "Tens",
    11: "Jacks",
    12: "Queens",
    13: "Kings",
    14: "Aces"}


def get_rank_value(rank):
    value = RANKS.index(rank) + 2
    return value


def evaluate_five(cards):
    if len(cards) != 5:
        raise ValueError("Exactly five cards are required")

    values = []

    for card in cards:
        value = get_rank_value(card.rank)
        values.append(value)

    values = sorted(values, reverse=True)

    counts = Counter(values)

    suits = [card.suit for card in cards]

    groups = []
    pairs = []
    for value, count in counts.items():
        group = (count, value)
        groups.append(group)
        if count == 2:
            pairs.append(value)

    groups = sorted(groups, reverse=True)
    pairs = sorted(pairs, reverse=True)

    is_flush = len(set(suits)) == 1

    straight_high = straight_high_card(values)
    is_straight = straight_high is not None


# STRAIGHT FLUSH
    if is_straight and is_flush :
        return (8, straight_high)

# FOUR OF A KIND
    if groups[0][0] == 4:
        four_rank = groups[0][1]
        kicker = groups[1][1]
        return (7, four_rank, kicker)

#FULL HOUSE
    if groups[0][0] == 3 and groups[1][0] == 2:
        return (6, groups[0][1], groups[1][1])

#FLUSH
    if is_flush:
        return (5, *values)

#STRAIGHT
    if is_straight:
        return (4, straight_high)

# THREE OF A KIND
    if groups[0][0] == 3:
        triple_rank = groups[0][1]
        kickers = [groups[1][1],groups[2][1]]
        return (3, triple_rank, *kickers)

# TWO PAIR
    if len(pairs) == 2:
        kickers = []
        for value, count in counts.items():
            if count == 1:
                kickers.append(value)
        kicker = max(kickers)
        return (2, pairs[0], pairs[1], kicker)

# ONE PAIR
    if len(pairs) == 1:
        pair_rank = pairs[0]
        kickers = []
        for value, count in counts.items():
            if count == 1:
                kickers.append(value)
        kickers = sorted(kickers, reverse=True)
        return (1, pair_rank, *kickers)

# HIGH CARD
    return (0, *values)


def straight_high_card(values):
    unique_values = sorted(set(values), reverse=True)

    if unique_values == [14, 5, 4, 3, 2]:
        return 5

    if len(unique_values) != 5:
        return None

    if unique_values[0] - unique_values[4] == 4:
        return unique_values[0]

    return None


def evaluate_hand(cards):
    if len(cards) < 5 or len(cards) > 7:
        raise ValueError("A poker hand requires between 5 and 7 cards")

    possible_hands = combinations(cards, 5)
    scores = []
    for combo in possible_hands:
        score = evaluate_five(list(combo))
        scores.append(score)

    best_score = max(scores)
    return best_score


def describe_hand(score):
    category = score[0]

    if category == 8:
        high_card = score[1]

        if high_card == 14:
            return "Royal flush"
        return (RANK_NAMES[high_card] + "-high straight flush")

    if category == 7:
        four_rank = score[1]
        kicker = score[2]
        return ("Four of a kind of " + RANK_PLURALS[four_rank] + ", with a " + RANK_NAMES[kicker] + " kicker")

    if category == 6:
        triple_rank = score[1]
        pair_rank = score[2]
        return ("Full House with 3: " + RANK_PLURALS[triple_rank] + " and 2: " + RANK_PLURALS[pair_rank])

    if category == 5:
        high_card = score[1]
        return (RANK_NAMES[high_card] + "-high flush")

    if category == 4:
        high_card = score[1]
        return (RANK_NAMES[high_card] + "-high straight")

    if category == 3:
        triple_rank = score[1]
        kickers = [score[2], score[3]]
        return ("Three of a kind with " + RANK_PLURALS[triple_rank] + "with highest kicker: " + RANK_NAMES[kickers[0]] + "and 2nd highest:  " + RANK_NAMES[kickers[1]] )

    if category == 2:
        higher_pair = score[1]
        lower_pair = score[2]
        kicker = score[3]

        return ("Two pair of " + RANK_PLURALS[higher_pair] + " and " + RANK_PLURALS[lower_pair] + ", with a " + RANK_NAMES[kicker] + " kicker")

    if category == 1:
        pair_rank = score[1]
        kickers = [score[2], score[3], score[4]]

        return ("One pair of " + RANK_PLURALS[pair_rank] + ", with the following kickers in descending order:" + RANK_NAMES[kickers[0], kickers[1], kickers[2]] )

    high_card = score[1]

    return RANK_NAMES[high_card] + "-high"
