
from models.enums import Suit, CardValue

class Card:
    def __init__(self, suit: Suit, value: CardValue):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.value.name} of {self.suit.name}"
    
    def __repr__(self):
        return f"{self.value.name} of {self.suit.name}"
    
    def __lt__(self, other):
        return float(self) < float(other)
    
    def __gt__(self, other):
        return float(self) > float(other)
    
    def __float__(self):
        return self.value.value + self.suit.value/100