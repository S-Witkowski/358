from .state import State
from settings import WIDTH, HEIGHT
import pygame as pg

class GameEnd(State):
    def __init__(self, game_controller):
        super().__init__(game_controller)
        self.game_controller = game_controller

    def check_input(self, mouse_keys, mouse_pos, mouse_rel, event):
        self.game_controller.gui_interface.check_input(mouse_keys, mouse_pos, mouse_rel, event)
        self.game_controller.space_interface.check_input(mouse_keys, mouse_pos, mouse_rel, event)

    def update(self):
        self.game_controller.gui_interface.show_button(
            (WIDTH*0.5,HEIGHT*0.5), 
            callback=self.cleanup,
            text=f"End game", 
            color=(245, 245, 245), 
            id_="EndGameButton"
            )
    
    def cleanup(self):
        self.done = True

    def render(self, screen):
        self.game_controller.space_interface.render(screen)
        self.game_controller.gui_interface.render()