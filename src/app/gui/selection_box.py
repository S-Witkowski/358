
import pygame as pg
from models.enums import GameMode
from gui.elements import Icon, AbstractGUIElement
from utils import load_and_transform_image


class GameModeSelectionBox(AbstractGUIElement):
    def __init__(self, screen, rect, text="", text_size=15, color=(245, 245, 245), id_="GameModeSelectionBox"):
        AbstractGUIElement.__init__(self, screen, text, text_size, color, id_)
        self.box_x, self.box_y, self.box_width, self.box_height = rect[0], rect[1], rect[2], rect[3]
        self.rect = pg.Rect(rect)
        size_factor = 0.15
        box_width = rect[2]
        box_height = rect[3]

        icon_position = [
            (self.box_x + box_width/3 - box_width/6, self.box_y + box_height/2 - box_height/4),
            (self.box_x + box_width/3 - box_width/6, self.box_y + box_height/2 + box_height/4),
            (self.box_x + box_width/1.5 - box_width/6, self.box_y + box_height/2 + box_height/4),
            (self.box_x + box_width/1.5 - box_width/6, self.box_y + box_height/2 - box_height/4), 
            (self.box_x + box_width/1.5 + box_width/6, self.box_y + box_height/2 - box_height/4),
            (self.box_x + box_width/1.5 + box_width/6, self.box_y + box_height/2 + box_height/4),
            ]
        self.group = [
            Icon(screen, 
                 icon_position[0],
                 load_and_transform_image("icons", f"{GameMode.Clubs.name.lower()}.png", space_width=rect[2], size_factor=size_factor),
                 GameMode.Clubs
            ),
            Icon(screen, 
                icon_position[1],
                load_and_transform_image("icons", f"{GameMode.Spades.name.lower()}.png", space_width=rect[2], size_factor=size_factor),
                GameMode.Spades
            ),
            Icon(screen, 
                icon_position[2],
                load_and_transform_image("icons", f"{GameMode.Diamonds.name.lower()}.png", space_width=rect[2], size_factor=size_factor),
                GameMode.Diamonds
            ),
            Icon(screen, 
                icon_position[3],
                load_and_transform_image("icons", f"{GameMode.Hearts.name.lower()}.png", space_width=rect[2], size_factor=size_factor),
                GameMode.Hearts
            ),
            Icon(screen, 
                icon_position[4],
                load_and_transform_image("icons", f"{GameMode.NoTricks.name.lower()}.png", space_width=rect[2], size_factor=size_factor),
                GameMode.NoTricks
            ),
            Icon(screen, 
                icon_position[5],
                load_and_transform_image("icons", f"{GameMode.NoTrump.name.lower()}.png", space_width=rect[2], size_factor=size_factor),
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
            if not self.icon_selected and icon.clicked:
                self.icon_selected = icon

