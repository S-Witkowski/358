
import pygame as pg
from settings import WIDTH
from models import GameMode
from gui.elements import Icon, AbstractGUIElement
from utils import load_and_transform_image


class GameModeSelectionBox(AbstractGUIElement):
    def __init__(self, screen, pos, text="", text_size=15, color=(245, 245, 245), id_="GameModeSelectionBox"):
        AbstractGUIElement.__init__(self, screen, text, text_size, color, id_)
        self.box_x, self.box_y = pos
        self.rect = pg.Rect(pos, pos)
        self.group = [
            Icon(screen, 
                 (self.box_x*1.2, self.box_y*1.2),
                 load_and_transform_image("icons", f"{GameMode.Clubs.name.lower()}.png", space_width=WIDTH*0.4, size_factor=0.15),
                 GameMode.Clubs
            ),
            Icon(screen, 
                (self.box_x*1.5, self.box_y*1.8),
                load_and_transform_image("icons", f"{GameMode.Spades.name.lower()}.png", space_width=WIDTH*0.4, size_factor=0.15),
                GameMode.Spades
            ),
            Icon(screen, 
                (self.box_x*1.2, self.box_y*1.8),
                load_and_transform_image("icons", f"{GameMode.Diamonds.name.lower()}.png", space_width=WIDTH*0.4, size_factor=0.15),
                GameMode.Diamonds
            ),
            Icon(screen, 
                (self.box_x*1.5, self.box_y*1.2),
                load_and_transform_image("icons", f"{GameMode.Hearts.name.lower()}.png", space_width=WIDTH*0.4, size_factor=0.15),
                GameMode.Hearts
            ),
            Icon(screen, 
                (self.box_x*1.8, self.box_y*1.2),
                load_and_transform_image("icons", f"{GameMode.NoTricks.name.lower()}.png", space_width=WIDTH*0.4, size_factor=0.15),
                GameMode.NoTricks
            ),
            Icon(screen, 
                (self.box_x*1.8, self.box_y*1.8),
                load_and_transform_image("icons", f"{GameMode.NoTrump.name.lower()}.png", space_width=WIDTH*0.4, size_factor=0.15),
                GameMode.NoTrump
            )
        ]
        self.icon_selected = None
        self.expired = False

    def expire(self):
        self.expired = True

    def update(self):
        pass

    def render(self):
        pg.draw.rect(self.screen, self.color, self.rect)
        for icon in self.group:
            icon.render()
    
    def check_mouse(self, pos, down):
        for icon in self.group:
            icon.check_mouse(pos, down)
            if icon.clicked:
                self.icon_selected = icon

