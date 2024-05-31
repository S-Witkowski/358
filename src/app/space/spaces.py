import pygame as pg
import random

from space.base import CardSpace
from card.sprite import CardSprite

from models.scores_models import PlayerInfo
from models.enums import Suit, CardValue, PlayerPosition

from settings import MARIGIN_PERC, LOOT_SPACE_VISIBILITY
from utils import sort_cards, load_and_transform_image


class Deck(CardSpace):
    def __init__(self, name: str, x: int, y: int, width: int, height: int, id_: str):
        super().__init__(name, x, y, width, height, id_)
        self.cards: list[CardSprite] = []
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

class PlayerSpace(CardSpace):
    def __init__(self, name: str, x: int, y: int, width: float, height: float, id_: str, player_info: PlayerInfo, mouse_from=False, mouse_to=False, card_visibility=False):
        super().__init__(name, x, y, width, height, id_, mouse_to=mouse_to, mouse_from=mouse_from, card_visibility=card_visibility)
        self.loot_box_space = None
        self.player_info = player_info
        # self.image = load_and_transform_image("game_space.jpg", space_width=width, size_factor=1)

    def add_loot_box_space(self):
        self.loot_box_space = CardSpace(
            f"{self.name}Loot", 
            self.rect[0], self.rect[1] + self.rect[3]*(1+MARIGIN_PERC), self.rect[2], self.rect[3], 
            id_=f"{self.id_}LootSpace",
            card_visibility=LOOT_SPACE_VISIBILITY
            )

    def clean(self):
        super().clean()
        self.loot_box_space.cards = []

    def _sort_active_player_cards(self):
        """Update player cards"""
        if not self.clicked_card:
            if self.mouse_from:
                self.cards = sort_cards(self.cards)

    def adjust_card_position_in_space(self):
        self._sort_active_player_cards()
        super().adjust_card_position_in_space()

class GameSpace(CardSpace):
    def __init__(self, name: str, x: int, y: int, width: float, height: float, id_: str):
        super().__init__(name, x, y, width, height, id_, mouse_to=True, mouse_from=False, card_visibility=True)
        self.full = False
        self.first_card_on_table = None
        self.image = load_and_transform_image("game_space.jpg", space_width=width, size_factor=1)

    def update(self):
        if not self.first_card_on_table and len(self.cards) == 1:
            self.first_card_on_table = self.cards[0]
        elif self.first_card_on_table and len(self.cards) == 0:
            self.first_card_on_table = None

        if len(self.cards) == 3:
            self.full = True
        elif len(self.cards) < 3:
            self.full = False
        else:
            raise ValueError(f"GameSpace should have 3 cards or less, found {len(self.cards)}")
        
    def adjust_card_position_in_space(self):
        if self.cards:
            for card in self.cards:
                if card.space_history[-2].player_info.player_position == PlayerPosition.First:
                    card.move_topleft((self.rect[0] + 0.5*self.rect[2] - card.rect[2]/2, self.rect[1] + self.rect[3]*0.5))
                elif card.space_history[-2].player_info.player_position == PlayerPosition.Second:
                    card.move_topleft((self.rect[0] + 0.45*self.rect[2] - card.rect[2]/2, self.rect[1] + self.rect[3]*0.4))
                elif card.space_history[-2].player_info.player_position == PlayerPosition.Third:
                    card.move_topleft((self.rect[0] + 0.55*self.rect[2] - card.rect[2]/2, self.rect[1] + self.rect[3]*0.3))

    def clean(self):
        """If there are three cards on the table, clean game_space and set every player space to transfer_done=False status """
        self.cards = []
        self.full = False