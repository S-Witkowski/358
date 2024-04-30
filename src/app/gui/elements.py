#!/usr/bin/env python
try:
    import sys
    import abc
    import pygame as pg
    from typing import Tuple
    from threading import Timer
    from models import GameMode
except ImportError as err:
    print("Fail loading a module in file:", __file__, "\n", err)
    sys.exit(2)


class AbstractGUIElement(metaclass=abc.ABCMeta):
    def __init__(self, screen, text="", text_size=15, color=(0, 0, 0), id_=""):
        self.screen = screen
        self.text = text
        self.text_size = text_size
        self.color = color
        self.id_ = id_

    @abc.abstractmethod
    def render(self):
        pass

    @abc.abstractmethod
    def check_mouse(self, pos, down):
        pass

class Button(AbstractGUIElement):
    inner_color = (191, 191, 191)
    inner_pressed_color = (153, 153, 153)
    frame_color = (77, 77, 77)
    frame_thickness = 1
    frame_pressed_thickness = 2
    text_color = (0, 0, 0)
    text_pressed_color = (255, 255, 255)
    text_margin = (3, 3)

    def __init__(self, screen, rect, onclick, text="", text_size=15, color=(0, 0, 0), id_=""):
        AbstractGUIElement.__init__(self, screen, text, text_size, color, id_)
        self.onclick = onclick
        self.font = pg.font.SysFont('arial', self.text_size, bold=1)
        self.text_surface = self.font.render(self.text, True, color)
        text_size = self.font.size(self.text)
        self.rect = (rect[0], rect[1],
                     text_size[0] + 2 * Button.text_margin[0],
                     text_size[1] + 2 * Button.text_margin[1])
        self.text_pos = (self.rect[0] + (self.rect[2] - text_size[0])/2,
                         self.rect[1] + (self.rect[3] - text_size[1])/2)
        self.pressed = False

    def render(self):
        if self.pressed:
            pg.draw.rect(self.screen, Button.inner_pressed_color, self.rect)
            pg.draw.rect(self.screen, Button.frame_color, self.rect,
                             Button.frame_pressed_thickness)
        else:
            pg.draw.rect(self.screen, Button.inner_color, self.rect)
            pg.draw.rect(self.screen, Button.frame_color, self.rect, Button.frame_thickness)

        self.screen.blit(self.text_surface, self.text_pos)

    def check_mouse(self, pos, down):
        if (self.rect[0] < pos[0] < self.rect[0] + self.rect[2] and
                self.rect[1] < pos[1] < self.rect[1] + self.rect[3]):
            if down:
                self.pressed = True
                self.onclick()
            else:
                self.pressed = False


class Label(AbstractGUIElement):
    def __init__(self, screen, pos, text="", text_size=15, color=(0, 0, 0), timeout=3, id_=""):
        AbstractGUIElement.__init__(self, screen, text, text_size, color, id_)
        self.font = pg.font.SysFont('arial', self.text_size, bold=1)
        self.pos = pos
        self.expired = False
        if timeout != 0:
            self.timer = Timer(timeout, self.expire)
            self.timer.start()

    def expire(self):
        self.expired = True

    def render(self):
        if self.text != "":
            text_surface = self.font.render(self.text, True, self.color)
            self.screen.blit(text_surface, self.pos)

    def check_mouse(self, pos, down):
        """ No action on click for text label """
        pass

class Icon(AbstractGUIElement):
    hover_color = (127, 127, 127)
    no_hover_color = (228, 228, 228)

    def __init__(self, screen: pg.Surface, pos: Tuple[int], image, game_mode: GameMode = None, id_=""):
        AbstractGUIElement.__init__(self, screen, id_)
        self.screen = screen
        self.game_mode = game_mode
        self.image = image
        self.rect = self.image.get_rect(center = pos)
        self.hover = False
        self.clicked = False

    def update(self):
        pass
    
    def render(self):
        hover_rect = pg.Surface((self.image.get_width(), self.image.get_height()))
        hover_rect.fill(self.hover_color) if self.hover else hover_rect.fill(self.no_hover_color)
        self.screen.blit(hover_rect, self.rect)
        self.screen.blit(self.image, self.rect)

    def check_mouse(self, pos, down):
        if self.rect.collidepoint(pos):
            self.hover = True
        else:
            self.hover = False

        if down and self.hover:
            self.clicked = True 
        else:
            self.clicked = False

