#!/usr/bin/env python
try:
    import sys
    import abc
    import pygame as pg
    from typing import Tuple
    from threading import Timer
    from models.enums import GameMode
    from settings import LABEL_COLOR, TEXT_SIZE_REL, BUTTON_COLOR, DEFAULT_TEXT_SIZE
except ImportError as err:
    print("Fail loading a module in file:", __file__, "\n", err)
    sys.exit(2)


class AbstractGUIElement(metaclass=abc.ABCMeta):
    """"""
    def __init__(self, screen, id_, rect, text="", text_size=DEFAULT_TEXT_SIZE, color=LABEL_COLOR, text_size_relative=True):
        self.screen = screen
        self.id_ = id_
        self.rect = pg.Rect(rect)
        if text_size_relative:
            self.text_size = int(TEXT_SIZE_REL*screen.get_width())
        else:
            self.text_size = text_size
        self.color = color
        self.text = text    
    
    @abc.abstractmethod
    def render(self):
        pass

    def update(self):
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

    def __init__(self, screen, id_, rect, callback, text, text_size_relative=True):
        AbstractGUIElement.__init__(self, screen=screen, id_=id_, rect=rect, text=text, text_size_relative=text_size_relative)
        self.callback = callback
        self.font = pg.font.SysFont('arial', self.text_size, bold=1)
        self.text_surface = self.font.render(self.text, True, self.color)
        text_size_ = self.font.size(self.text)

        self.rect = (rect[0], rect[1],
                     text_size_[0] + 2 * Button.text_margin[0],
                     text_size_[1] + 2 * Button.text_margin[1])
        self.rect = pg.Rect(self.rect)
        self.text_pos = (self.rect[0] + (self.rect[2] - text_size_[0])/2,
                         self.rect[1] + (self.rect[3] - text_size_[1])/2)
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
                self.callback()
            else:
                self.pressed = False


class Label(AbstractGUIElement):
    def __init__(self, screen, id_, rect, text, timeout=0, text_size_relative=True):
        AbstractGUIElement.__init__(self, screen=screen, id_=id_, rect=rect, text=text, text_size_relative=text_size_relative)
        self.font = pg.font.SysFont('arial', self.text_size, bold=1)
        self.timeout = timeout
        self.init_text = text
        self.expired = False
        if timeout != 0:
            self.timer = Timer(timeout, self.expire)
            self.timer.start()
            self.alpha = LABEL_COLOR[2]

    def update_text(self, text: str):
        self.text = f"{self.init_text} | score: {text}"

    def expire(self):
        self.expired = True

    def render(self):
        if self.text != "":
            if self.timeout != 0:
                if self.alpha > 30:
                    self.alpha = max(0, self.alpha - self.timeout)
                    text_surface = self.font.render(self.text, True, self.color)
                    text_surface.set_alpha(self.alpha)
                    self.screen.blit(text_surface, self.rect)
            else:
                text_surface = self.font.render(self.text, True, self.color)
                self.screen.blit(text_surface, self.rect)

    def check_mouse(self, pos, down):
        """ No action on click for text label """
        pass

class Icon(AbstractGUIElement):
    hover_color = (200, 200, 200)
    no_hover_color = (100, 100, 100)

    def __init__(self, screen: pg.Surface, id_: str, rect: Tuple[int], image, game_mode: GameMode = None):
        AbstractGUIElement.__init__(self, screen=screen, id_=id_, rect=rect)
        self.screen = screen
        self.game_mode = game_mode
        self.image = image
        self.rect = pg.Rect(rect)
        self.rect = self.image.get_rect(center = self.rect.center)
        self.hover = False
        self.clicked = False

        self.label = Label(screen=screen, id_="temp", rect=(0, 0, 0, 0), text=self.game_mode.name)

    def update(self):
        pass

    def render_on_icon_label(self):
        if self.hover:
            self.label.render()
    
    def render(self):
        self.image.set_alpha(255) if self.hover else self.image.set_alpha(200)
        self.screen.blit(self.image, self.rect)
        self.render_on_icon_label()

    def check_mouse(self, pos, down):
        if self.rect.collidepoint(pos):
            self.hover = True
            self.label.rect = (pos[0], pos[1], self.rect[2], self.rect[3])
        else:
            self.hover = False

        if down and self.hover:
            self.clicked = True 
        else:
            self.clicked = False