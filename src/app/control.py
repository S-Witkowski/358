
import os
import pygame as pg
from settings import WIDTH, HEIGHT, FPS
from states.prepare_game import GamePrepare
from states.play_game import GamePlay
from states.end_game import GameEnd
from gui.interface import GuiInterface
from space import SpaceInterface

class Control():
    def __init__(self):
        pg.init()
        pg.display.set_caption("358")
        bounds = (WIDTH, HEIGHT)
        self.screen = pg.display.set_mode(bounds)
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = FPS
        self.gui_interface = GuiInterface(self.screen)
        self.space_interface = SpaceInterface()
        self.states = self._load_states()
        self.state_stack = [next(self.states)]
        self.quit = False
        print(f"starting state: {self.state_stack}")

    def _load_states(self):
        for state in [
            GamePrepare(self),
            GamePlay(self),
            GameEnd(self)
        ]:
            yield state

    def _change_state(self):
        if self.state_stack[-1].done:
            print(f"{self.state_stack[-1]} done")
            if isinstance(self.state_stack[-1], GameEnd):
                self.quit = True
                print("Game ended, going to exit")
            else:
                self.state_stack[-1].cleanup()
                state = next(self.states)
                state.enter_state()

    def event_loop(self):
        mouse_keys = pg.mouse.get_pressed()
        mouse_pos = pg.mouse.get_pos()
        mouse_rel = pg.mouse.get_rel()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit = True
            
            self.state_stack[-1].check_input(mouse_keys, mouse_pos, mouse_rel, event)

    def update(self):
        self._change_state()
        self.state_stack[-1].update()
         
    def render(self):
        self.screen.fill((30,30,30))
        self.state_stack[-1].render(self.screen)
        pg.display.update()

    def run(self):
        while not self.quit:
            self.event_loop()
            self.update()
            self.render()
            self.clock.tick(self.fps)