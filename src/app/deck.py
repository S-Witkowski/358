from models.enums import Suit, CardValue
from sprites import Card, CardSprite
from space import CardSpace
import random


class Deck(CardSpace):
    def __init__(self, name: str, x: int, y: int, width: int, height: int, id_: str):
        super().__init__(name, x, y, width, height, id_)
        self.cards = []
        for suit in Suit:
            for value in CardValue:
                self.cards.append(
                    CardSprite(
                        suit=suit, 
                        value=value,
                        space=self, 
                        x=0,
                        y=0,
                        space_width=width,
                        back_up=True
                        )
                    )
                
        self._shuffle()
        self.adjust_card_position_in_space()

    def _shuffle(self):
        random.shuffle(self.cards)
        
    def deal(self, num_cards: int, space: CardSpace):
        for _ in range(num_cards):
            if self.cards:
                self.transfer(self.cards[0], space)
