
import pygame as pg
import os
from settings import WIDTH, HEIGHT
from models import Suit, CardValue, GameMode
import random
from typing import Tuple, List

def load_image(*args):
    sourceFileDir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(sourceFileDir, "img", *args)
    return pg.image.load(full_path).convert_alpha()        

class Card(pg.sprite.Sprite): 
    game_mode: GameMode = None # type: ignore
    def __init__(self, suit: Suit, value: CardValue):
        super().__init__() 
        self.suit = suit
        self.value = value
        self.selected = False
        self.back_up = False
        self.init_card()

    def __repr__(self):
        return f"{self.value.name} of {self.suit.name}"
    
    def init_card(self):
        image = self._load_card_image()
        self.image = self._transform_card_size(image)
        self.rect = self.image.get_rect()

    def _load_card_image(self):
        if not self.back_up:
            sourceFileDir = os.path.dirname(os.path.abspath(__file__))
            full_path = os.path.join(sourceFileDir, "img", "cards", f"{self.value.name.lower()}_of_{self.suit.name.lower()}.png")
            return pg.image.load(full_path).convert_alpha()
        else:
            sourceFileDir = os.path.dirname(os.path.abspath(__file__))
            full_path = os.path.join(sourceFileDir, "img", "back-side.png")
            return pg.image.load(full_path).convert_alpha()        
    
    def _transform_card_size(self, image):
        image_w, image_h = image.get_size()
        image_aspect_ratio = image_w / image_h
        card_size_factor = 0.1
        card_size = (WIDTH*card_size_factor, WIDTH*card_size_factor/image_aspect_ratio)
        return pg.transform.scale(image, card_size)
    
    def flip_image(self):
        self.back_up = True
        self.init_card()

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Deck:
    cards = []
    def __init__(self):
        for suit in Suit:
            for value in CardValue:
                self.cards.append(Card(suit, value))

    def shuffle(self):
        random.shuffle(self.cards)
        
    def deal(self, num_cards):
        dealt_cards = []
        for _ in range(num_cards):
            if self.cards:
                dealt_cards.append(self.cards.pop())
        return dealt_cards


class Player:
    cards: List[Card] = []

    def __init__(self, name: str, pos: Tuple, is_active: bool):
        self.name = name
        self.pos = pos
        self.is_active = is_active

    def flip_cards(self):
        for card in self.cards:
            if not self.is_active:
                card.flip_image()

    def reposition_cards(self):
        x_offset = self.pos[0]
        for card in self.cards:
            card.rect.topleft = (x_offset, self.pos[1])
            if self.is_active:
                x_offset += 30
            else:
                x_offset += 5

    def decide_game_mode(self):
        return random.choice(GameMode) # type: ignore

class Icon(pg.sprite.Sprite):

    def __init__(self, game_mode: GameMode, x, y):
        super().__init__()
        self.game_mode = game_mode
        self.image = load_image("icons", f"{self.game_mode.name.lower()}.png")
        self.image = self._transform_image_size(self.image, WIDTH*0.4)
        self.rect = self.image.get_rect(center = (x, y))

        # self.original_image = pg.Surface((70, 70))
        # self.original_image.blit(img, img.get_rect(center = self.original_image.fill((127, 127, 127)).center))
        # self.hover_image = pg.Surface((70, 70))
        # self.hover_image.blit(img, img.get_rect(center = self.hover_image.fill((228, 228, 228)).center))
        # self.image = self.original_image 
        # self.rect = self.image.get_rect(center = (x, y))
        # self.hover = False

    def _transform_image_size(self, image, screen_width):
        image_w, image_h = image.get_size()
        image_aspect_ratio = image_w / image_h
        size_factor = 0.15
        size = (screen_width*size_factor, screen_width*size_factor/image_aspect_ratio)
        return pg.transform.scale(image, size)

    def update(self):
        # self.hover = self.rect.collidepoint(pg.mouse.get_pos())
        # self.image = self.hover_image if self.hover else self.original_image
        pass
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class GameModeSelectionBox(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.box_x, self.box_y = (WIDTH*0.3, HEIGHT*0.3)
        self.rect = pg.Rect((self.box_x, self.box_y), (WIDTH*0.3, HEIGHT*0.3))
        self.group = pg.sprite.Group([
            Icon(GameMode.Clubs, self.box_x*1.2, self.box_y*1.2),
            Icon(GameMode.Spades, self.box_x*1.5, self.box_y*1.8),
            Icon(GameMode.Diamonds, self.box_x*1.2, self.box_y*1.8),
            Icon(GameMode.Hearts, self.box_x*1.5, self.box_y*1.2),
            Icon(GameMode.NoTrump, self.box_x*1.8, self.box_y*1.2),
            Icon(GameMode.NoTricks, self.box_x*1.8, self.box_y*1.8)
        ]) # type: ignore

    def update(self):
        for icon in self.group.sprites():
            if icon.rect.collidepoint(pg.mouse.get_pos()):
                print("selected")

    def draw(self, screen):
        pg.draw.rect(screen, "white", self.rect)
        self.group.draw(screen)


class Game:
    players = []
    deciding_player = None
    def __init__(self, screen):
        self.deck = Deck()
        self.screen = screen
        self.game_started = False
        self.quit = False
        self.card_selected = None
        self.game_mode_selected = None
        self.game_mode_selection_box = GameModeSelectionBox()
    
    def init_players(self):
        player = Player("You", (WIDTH*0.35, HEIGHT*0.7), True)
        bot_1 = Player("Bot 1", (0, 0), False)
        bot_2 = Player("Bot 2", (WIDTH*0.8, 0), False)
        self.players = [player, bot_1, bot_2]

    def create_new_round(self):
        self.init_players()
        self.deck.shuffle()

        for p in self.players:
            p.cards = self.deck.deal(6)
            p.flip_cards()
            p.reposition_cards()

    def update(self, keys):
        if not self.game_started:
            self.create_new_round()
            self.game_started = True
            if not self.game_mode_selected:
                self.game_mode_selection_box.group.update()

    def render(self):
        self.screen.fill((30,30,30))
        for p in self.players:
            for c in p.cards:
                c.draw(self.screen)
        if not self.game_mode_selected:
            self.game_mode_selection_box.draw(self.screen)
    
    def get_event(self, event):
        selected_offset_x, selected_offset_y = 0, 0
        if event.type == pg.QUIT:
            self.quit = True

        if event.type == pg.MOUSEBUTTONDOWN:
            for c in self.players[0].cards:
                if event.button == 1:  
                    if c.rect.collidepoint(event.pos):
                        self.card_selected = c
                        selected_offset_x = self.card_selected.rect.x - event.pos[0]
                        selected_offset_y = self.card_selected.rect.y - event.pos[1]
                        
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                self.card_selected = None         

        if event.type == pg.MOUSEMOTION:
            if self.card_selected:
                self.card_selected.rect.x = event.pos[0] + selected_offset_x
                self.card_selected.rect.y = event.pos[1] + selected_offset_y


