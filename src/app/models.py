from sprites import Card
from typing import List
from enums import Suit, GameMode

class CardList:
    """Process information about card list with the same suit"""
    def __init__(self, cards: List[Card]) -> None:
        self.cards = cards

    def number_of_cards(self) -> int:
        return len(self.cards)
    
    def total_power_of_cards(self) -> float:
        return sum([float(card) for card in self.cards])
    
    def weakest_card(self) -> Card|None:
        if self.cards:
            min_card = self.cards[0]
            for card in self.cards:
                if card < min_card:
                    min_card = card
            return min_card
            
class CardsDict:
    """Process information about card list with different suits, usually player hand"""
    def __init__(self, cards: List[Card]):
        self.cards = cards
        self.card_dict = {
            Suit.Clubs: [],
            Suit.Diamonds: [],
            Suit.Hearts: [],
            Suit.Spades: []
        }
        for card in self.cards:
            self.card_dict[card.suit].append(card)
        for suit, cards in self.card_dict.items():
            self.card_dict[suit] = CardList(cards) # type: ignore





