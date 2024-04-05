
import os
import pygame as pg
from settings import WIDTH, HEIGHT
from sprites import Game

class Control():

    def __init__(self):
        pg.init()
        pg.display.set_caption("358")
        bounds = (WIDTH, HEIGHT)
        self.screen = pg.display.set_mode(bounds)
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = 60
        self.keys = pg.key.get_pressed()
        self.done = False
        self.state = Game(self.screen)

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.done = True
            self.state.get_event(event)


    # def change_state(self):
    #     if self.state.done:
    #         self.state.cleanup()
    #         self.state_name = self.state.next
    #         self.state.done = False
    #         self.state = self.state_dict[self.state_name]
    #         self.state.entry()


    def run(self):
        while not self.done:
            if self.state.quit:
                self.done = True
            # now = pg.time.get_ticks()
            self.event_loop()
            # self.change_state()
            self.state.update(self.keys)
            self.state.render()
            pg.display.update()
            self.clock.tick(self.fps)