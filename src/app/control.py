
import pygame as pg
from settings import FPS

from states.prepare_game import GamePrepare
from states.play_game import GamePlay
from states.end_game import GameEnd
from states.new_game import GameNew

from AI.base import TableInformation, AbstractAI
from AI.classic import ClassicAI
from rules import Rules
from gui.interface import GuiInterface
from space.interface import SpaceInterface
from utils import load_and_transform_image
from logger import create_logger, logger

class Control():
    def __init__(self):
        self.fps = FPS
        self.quit = False
        pg.init()
        self.clock = pg.time.Clock()
        pg.display.set_caption("358")
        self._set_screen()
        self._load_components()
        self.state_stack = [GameNew(self)]
        logger.info(f"starting state: {self.state_stack[-1]}")

    def _set_screen(self):
        info = pg.display.Info()
        self.screen = pg.display.set_mode((info.current_w, info.current_h*0.90), pg.RESIZABLE)
        self.background_image = load_and_transform_image(
            "background.jpg", space_width=self.screen.get_width(), size_factor=1
            )
        
    def _load_components(self):
        self.gui_interface: GuiInterface = GuiInterface(self.screen)
        self.space_interface: SpaceInterface = SpaceInterface(self.clock)
        self.table_info: TableInformation = TableInformation()
        self.rules: Rules = Rules()
        self.AI: AbstractAI = ClassicAI(self.table_info, self.rules)
        create_logger()

    def _change_state(self):
        if self.state_stack[-1].done:
            new_state = None
            if isinstance(self.state_stack[-1], GameNew):
                new_state = GamePrepare(self)
            elif isinstance(self.state_stack[-1], GamePrepare):
                new_state = GamePlay(self)
            elif isinstance(self.state_stack[-1], GameEnd):
                self.quit = True
            elif isinstance(self.state_stack[-1], GamePlay):
                if self.state_stack[-1].end_game:
                    new_state = GameEnd(self)
                else:
                    new_state = GamePrepare(self)
            if new_state:
                self.state_stack[-1].cleanup()
                new_state.enter_state()

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
            elif event.type == pg.VIDEORESIZE:
                self.screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
            self.state_stack[-1].check_input(mouse_keys, mouse_pos, mouse_rel, event)

    def update(self):
        self._change_state()
        self.state_stack[-1].update()
         
    def render(self):
        self.screen.blit(self.background_image, (0,0))
        self.state_stack[-1].render(self.screen)
        pg.display.update()

    def run(self):
        while not self.quit and not self.state_stack[-1].quit:
            self.clock.tick(self.fps)
            self.event_loop()
            self.update()
            self.render()
