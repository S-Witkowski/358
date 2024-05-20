from .state import State
from settings import WIDTH, HEIGHT
import pygame as pg

class GameEnd(State):
    def __init__(self, game_controller):
        super().__init__(game_controller)
        self.game_controller = game_controller
        self.game_end_summary = False

    def check_input(self, mouse_keys, mouse_pos, mouse_rel, event):
        self.game_controller.gui_interface.check_input(mouse_keys, mouse_pos, mouse_rel, event)
        self.game_controller.space_interface.check_input(mouse_keys, mouse_pos, mouse_rel, event)

    def update(self):
        if not self.game_end_summary:
            self.game_controller.gui_interface.show_label(
                rect=(self.widht*0.4, self.height*0.1, self.widht*0.2, self.height*0.2), 
                text=f"Game ended, {self.game_controller.score_board.get_winner().name} wins!", 
                id_="GameEndSummary"
            )
            self.game_controller.gui_interface.show_button(
                rect=(self.widht*0.4, self.height*0.35, self.widht*0.2, self.height*0.2), 
                callback=self.cleanup,
                text=f"End game", 
                id_="EndGameButton"
                )
            self.game_end_summary = True
    
    def cleanup(self):
        self.done = True

    def render(self, screen):
        self.game_controller.space_interface.render(screen)
        self.game_controller.gui_interface.render()