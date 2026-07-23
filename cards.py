from dataclasses import dataclass

RANKS = "23456789TJQKA"
SUITS = "cdhs"


@dataclass(frozen=True)
class Card:
    rank: str
    suit: str

    def __post_init__(self):
        if self.rank not in RANKS:
            raise ValueError("Invalid rank: ", self.rank)

        if self.suit not in SUITS:
            raise ValueError("Invalid suit: ", self.suit)

    def __str__(self):
        return self.rank + self.suit


#my_card = Card("K", "b")
#print(my_card)

def parse_card(text):
    rank = text[0].upper()
    suit = text[1].lower()

    return Card(rank, suit)

def parse_cards(text):
    card_texts = text.split()
    cards = []

    for card_text in card_texts:
        card = parse_card(card_text)
        cards.append(card)

    return cards

#my_cards = parse_cards("As Kh 7d")
#for card in my_cards:
    print(card.rank, card.suit)

def create_deck() -> list[Card]:
    return [ Card(rank, suit) for rank in RANKS for suit in SUITS]

