from enum import Enum
import random

class CardValue(Enum):
    Deuce = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13
    Ace = 14

class Suit(Enum):
    Clubs = 0
    Diamonds = 1
    Hearts = 2
    Spades = 3

class GameMode(Enum):
    Clubs = 0
    Diamonds = 1
    Hearts = 2
    Spades = 3
    NoTrump = 4
    NoTricks = 5

# class Card:
#     suit: Suit = None
#     value: CardValue = None
#     game_mode: GameMode = None
#     def __init__(self, suit, value):
#         self.suit = suit
#         self.value = value

#     def __repr__(self):
#         return f"{self.value.name} of {self.suit.name}"
    
#     def __gt__(self, other):
#         return self.value.value > other.value.value
    
#     def __lt__(self, other):
#         return self.value.value < other.value.value
    

