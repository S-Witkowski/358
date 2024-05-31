import pygame as pg
from typing import Optional

from card.base import Card

class CardSpace:
    """
    Base class for card space.
    Gathers cards into spaces because every card has to belong somewhere.
    """
    card_offset = 20
    text_size_rel = 0.05
    alpha = 128

    def __init__(self, name: str, x: int, y: int, width: float, height: float, id_: str, image=None, mouse_from=False, mouse_to=False):
        self.name = name
        self.rect = pg.Rect(x, y, width, height)
        self.id_ = id_
        self.image = image
        self.mouse_from = mouse_from
        self.mouse_to = mouse_to

        self.cards: list[Card] = []
        self.clicked_card: Card = None

        self.label = None
        self.text_size = int(self.rect[2]*self.text_size_rel)
        self.locked = False

    def __str__(self) -> str:
        return self.name

    def add_label(self, gui_interface):
        if not self.label:
            self.label = gui_interface.show_label(
                    rect=self.rect,
                    text=f"{self.name}", 
                    id_=f"CardSpaceLabel{self.id_}",
                    )
            self.label.rect[1] = self.label.rect[1] - self.label.text_size
        
    def _add(self, card):
        self.cards.append(card)

    def _remove(self, card):
        self.cards.remove(card)

    def clean(self):
        self.cards = []

    def lock(self):
        self.locked = True
    
    def unlock(self):
        self.locked = False
            
    def transfer(self, card, new_space):
        """Transfer Card from current space to the new_space"""
        self._remove(card)
        new_space._add(card)
        card.add_new_space(new_space)

    def flip_cards(self):
        for card in self.cards: 
            card.flip()

    def adjust_card_position_in_space(self):
        if self.cards:
            x_offset = self.rect[0]
            for card in self.cards:
                if not card.moving:
                    card.move_topleft((x_offset, self.rect[1]))
                    x_offset += self.card_offset
                if self.mouse_from:
                    card.back_up = False

    def update(self):
        pass

    def render_cards(self, screen):
        for card in self.cards:
            card.render(screen)
    
    def render(self, screen):
        if self.image:
            self.image.set_alpha(self.alpha)
            screen.blit(self.image, (self.rect.topleft))