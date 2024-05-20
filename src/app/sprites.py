
import pygame as pg
from models.enums import Suit, CardValue, GameMode
from space import CardSpace
from utils import load_and_transform_image

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
    
class CardSprite(pg.sprite.Sprite, Card): 
    card_size_factor = 0.12
    game_mode: GameMode = None # type: ignore
    def __init__(self, suit: Suit, value: CardValue, space: CardSpace, x, y, space_width, back_up=False):
        pg.sprite.Sprite.__init__(self) 
        Card.__init__(self, suit, value) 
        self.space = space
        self.back_up = back_up
        self.selected = False
        self.top_image = load_and_transform_image("cards", f"{self.value.name.lower()}_of_{self.suit.name.lower()}.png", space_width=space_width, size_factor=self.card_size_factor)
        self.back_image = load_and_transform_image("back-side.png", space_width=space_width, size_factor=self.card_size_factor)
        self.rect = self.back_image.get_rect(center=(x, y))
        self.image = self.get_render_tuple()[0]
        self.clicked = False
        self.clicked_pos = None
        self.space_history = [self.space]
        self.tuple_repr = (self.suit.value, self.value.value)

    def __repr__(self):
        return f"{self.value.name} of {self.suit.name}"
    
    def add_new_space(self, space: CardSpace):
        self.space_history.append(space)
        self.space = space
    
    def get_current_space(self):
        return self.space_history[-1]
    
    def move_topleft(self, pos):
        self.rect.topleft = pos
    
    def flip(self):
        self.back_up = not self.back_up

    def get_render_tuple(self):
        if self.back_up:
            return self.back_image, (self.rect[0], self.rect[1])
        else:
            return self.top_image, (self.rect[0], self.rect[1])
    
    def update(self):
        pass        

    def render(self, screen):
        screen.blit(*self.get_render_tuple())

    def check_input(self, mouse_keys, mouse_pos, mouse_rel, event):
        if not self.clicked and event.type == pg.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if event.button == 1:
                self.clicked = True
                self.clicked_pos = event.pos
        if self.clicked and event.type == pg.MOUSEBUTTONUP:
            self.clicked = False

    def check_rect_collision_with_space(self, space: CardSpace):
        if space != self.space:
            if self.rect.colliderect(space.rect):
                return True
        else:
            return False
    


    