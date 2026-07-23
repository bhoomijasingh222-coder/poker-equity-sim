from dataclasses import dataclass


@dataclass
class Card:
    rank: str
    suit: str

    def __str__(self):
        return self.rank + self.suit


my_card = Card("A", "s")

print(my_card)
