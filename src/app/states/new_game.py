
from .state import State
from models.scores_models import PlayerInfo
from models.enums import PlayerPosition
from space import PlayerSpace
from scores import ScoreBoard

from settings import CARD_SPACE_HEIGHT_PERC, MARIGIN_PERC, TEXT_SIZE_REL, BUTTON_COLOR

PLAYER_WIDTH_REL = 0.2

class GameNew(State):
    def __init__(self, game_controller):
        super().__init__(game_controller)
        self.game_controller = game_controller
        self.widht = self.game_controller.screen.get_width()
        self.height = self.game_controller.screen.get_height()

        self.game_controller.space_interface.add(
            PlayerSpace(
                "You", 
                self.widht*PLAYER_WIDTH_REL*2, self.height*(1-MARIGIN_PERC-CARD_SPACE_HEIGHT_PERC-CARD_SPACE_HEIGHT_PERC), self.widht*PLAYER_WIDTH_REL, self.height*CARD_SPACE_HEIGHT_PERC, 
                id_="PlayerSpace1", 
                player_info=PlayerInfo(player_position=PlayerPosition.First), 
                mouse_from=True, mouse_to=False
                )
            )
        self.game_controller.space_interface.add(
            PlayerSpace(
                "Bot 1", 
                self.widht*MARIGIN_PERC, self.height*0.3, self.widht*PLAYER_WIDTH_REL, self.height*CARD_SPACE_HEIGHT_PERC, 
                id_="PlayerSpace2", 
                player_info=PlayerInfo(player_position=PlayerPosition.Second),
                mouse_from=False, mouse_to=False
                )
            )
        self.game_controller.space_interface.add(
            PlayerSpace(
                "Bot 2", 
                self.widht*(1-PLAYER_WIDTH_REL-MARIGIN_PERC), self.height*0.3, self.widht*PLAYER_WIDTH_REL, self.height*CARD_SPACE_HEIGHT_PERC, 
                id_="PlayerSpace3", 
                player_info=PlayerInfo(player_position=PlayerPosition.Third), 
                mouse_from=False, mouse_to=False
                )
            )
        
        for space in self.game_controller.space_interface.space_list:
            space.add_label(self.game_controller.gui_interface)

        self.game_controller.score_board = ScoreBoard(
            [
                self.game_controller.space_interface.get_by_id("PlayerSpace1"), 
                self.game_controller.space_interface.get_by_id("PlayerSpace2"), 
                self.game_controller.space_interface.get_by_id("PlayerSpace3")
            ]
        )

        self.game_controller.gui_interface.show_score_board_box(
            rect=(self.widht*MARIGIN_PERC, self.height*(MARIGIN_PERC), self.widht*0.1, self.height*0.1),
            score_board=self.game_controller.score_board,
            id_="ScoreBoardIcon"
            )
        self.game_started = False

    def show_game_started_menu(self):

        self.game_controller.gui_interface.show_button(
            rect=(self.widht*0.4, self.height*0.35, self.widht*0.2, self.height*0.2), 
            callback=self.next_state,
            text=f"Start new game",
            id_="NewGameButton"
            )
        
        self.game_controller.gui_interface.show_button(
            rect=(self.widht*0.4, self.height*0.45, self.widht*0.2, self.height*0.2), 
            callback=self.exit_state,
            text=f"Exit game", 
            id_="EndGameButton"
            )
        
    def update_game_started(self):
        if not self.game_started:
            self.show_game_started_menu()
            self.game_started = True

    def update(self):
        self.game_controller.space_interface.update()
        self.update_game_started()

    def render(self, screen):
        self.game_controller.space_interface.render(screen)
        self.game_controller.gui_interface.render()

    def cleanup(self):
        self.game_controller.gui_interface.hide_by_id("NewGameButton")
        self.game_controller.gui_interface.hide_by_id("EndGameButton")

    def check_input(self, mouse_keys, mouse_pos, mouse_rel, event):
        self.game_controller.gui_interface.check_input(mouse_keys, mouse_pos, mouse_rel, event)
        self.game_controller.space_interface.check_input(mouse_keys, mouse_pos, mouse_rel, event)



        
