
import pygame as pg
from settings import WIDTH, HEIGHT
from models import Suit, CardValue, GameMode
from typing import Tuple, List
from gui.interface import GuiInterface
from utils import load_and_transform_image
from space import SpaceInterface, CardSpace
from deck import Deck
from states.prepare_game import GamePrepare

SPACE_HEIGHT = HEIGHT*0.15

class Game:
    players = []
    spaces = []
    deciding_player = None
    def __init__(self, screen):
        self.gui_interface = GuiInterface(screen)
        self.space_interface = SpaceInterface(screen)
        self.game_prepare = GamePrepare(screen, self.gui_interface, self.space_interface)
        self.screen = screen
        self.game_started = False
        self.quit = False
        self.card_selected = None
        self.active_player = None
        self.game_mode_selected = None
        self.deck = None

    def update(self):
        self.game_prepare.update()
        
    def render(self):
        self.game_prepare.render()

    def get_event(self, event):
        selected_offset_x, selected_offset_y = 0, 0
        self.gui_interface.check_mouse(False)
        if event.type == pg.QUIT:
            self.quit = True

        if event.type == pg.MOUSEBUTTONDOWN:
            self.gui_interface.check_mouse(True)
            for c in self.game_prepare.game_mode_picking_player.cards:
                if event.button == 1:  
                    if c.rect.collidepoint(event.pos):
                        self.card_selected = c
                        selected_offset_x = self.card_selected.rect.x - event.pos[0]
                        selected_offset_y = self.card_selected.rect.y - event.pos[1]

                        
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1 and self.card_selected:
                trash_space = self.game_prepare.space_interface.get_by_id("TrashSpace")
                if trash_space and trash_space.rect.colliderect(self.card_selected.rect) and len(trash_space.cards) <= 3: # 4 cards -> len(cards) = 3
                    self.game_prepare.game_mode_picking_player.transfer(self.card_selected, trash_space)                
                self.card_selected = None         

        if event.type == pg.MOUSEMOTION:
            if self.card_selected:
                self.card_selected.rect.x = event.pos[0] + selected_offset_x
                self.card_selected.rect.y = event.pos[1] + selected_offset_y



