from sprites import Card, CardSprite
from typing import List
from models.enums import Suit

class CardList:
    """Process information about card list with the same suit"""
    def __init__(self, cards: List[CardSprite]) -> None:
        self.cards = cards

    def number_of_cards(self) -> int:
        return len(self.cards)
    
    def total_power_of_cards(self) -> float:
        return sum([float(card) for card in self.cards])
    
    def weakest_card(self) -> CardSprite|None:
        if self.cards:
            min_card = self.cards[0]
            for card in self.cards:
                if card < min_card:
                    min_card = card
            return min_card

    def strongest_card(self) -> CardSprite|None:
        if self.cards:
            max_card = self.cards[0]
            for card in self.cards:
                if card > max_card:
                    max_card = card
            return max_card
            
class CardsDict:
    """Process information about card list with different suits, usually player hand"""
    def __init__(self, cards: List[CardSprite]):
        """
        suit.name: CardList
        example:
        "Clubs": CardList
        """
        self.cards = cards
        self.card_dict = {
            Suit.Clubs.name: [],
            Suit.Diamonds.name: [],
            Suit.Hearts.name: [],
            Suit.Spades.name: []
        }
        if not isinstance(cards, list):
            raise ValueError(f"Wrong type of cards: {type(cards)}, expected list type")
        for card in self.cards:
            self.card_dict[card.suit.name].append(card)
        for suit_name, cards in self.card_dict.items():
            self.card_dict[suit_name] = CardList(cards) # type: ignore

