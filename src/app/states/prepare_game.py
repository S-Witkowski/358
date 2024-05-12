from .state import State
from space import CardSpace
from deck import Deck

from settings import CARD_SPACE_HEIGHT_PERC, MARIGIN_PERC


class GamePrepare(State):
    def __init__(self, game_controller):
        super().__init__(game_controller)
        self.game_controller = game_controller
        self.widht = self.game_controller.screen.get_width()
        self.height = self.game_controller.screen.get_height()

        self.game_mode_selection_box = None 
        self.card_selected = None

        self.first_stage = False
        self.second_stage = False
        self.third_stage = False
        self.fourth_stage = False
        self.fifth_stage = False

        self.game_mode_selected = False
    def post_init(self):
        """ Called after the previous state is finished"""
        # deck, pick spaces prepared
        self.deck = Deck("Deck", self.widht*0.35, self.height*MARIGIN_PERC, self.widht*0.3, self.height*0.15, id_="DeckSpace")
        self.game_controller.space_interface.add(self.deck)
        self.game_controller.space_interface.add(CardSpace("Pick", self.widht*MARIGIN_PERC, self.height*(0.85-MARIGIN_PERC), self.widht*0.1, self.height*CARD_SPACE_HEIGHT_PERC, id_="PickSpace", mouse_from=False, mouse_to=False))
        
        # table info update
        self.game_controller.score_board.update_current_game_mode_picking_player_space()        
        self.game_controller.space_interface.load_all_cards()
        self.game_controller.table_info.all_cards = self.deck.cards

        print(str(self.game_controller.score_board))

    def deal_first_cards(self):
        self.deck.deal(6, self.game_controller.space_interface.get_by_id("PlayerSpace1"))
        self.deck.deal(6, self.game_controller.space_interface.get_by_id("PlayerSpace2"))
        self.deck.deal(6, self.game_controller.space_interface.get_by_id("PlayerSpace3"))
        self.deck.deal(4, self.game_controller.space_interface.get_by_id("PickSpace"))

    def update_first_stage(self):
        """ 
        First stage of GamePrepare:
        1. 6 cards dealt for every player
        2. 4 cards dealt for picking box
        3. Game mode selectionbox showed
        4. Game mode selected
        """
        if not self.first_stage:
            self.post_init()
            self.deal_first_cards()
            self.game_controller.space_interface.get_by_id("PlayerSpace1").sort_active_player_cards()
            self.game_mode_selection_box = self.game_controller.gui_interface.show_selection_box(
                (self.widht*0.375, self.height*0.3, self.widht*0.25, self.height*0.25), 
                id_="GameModeSelectionBox")
            self.first_stage = True
            print(f"First stage ended")
        return self.first_stage 

    def update_second_stage(self):
        """
        Second stage of GamePrepare:
        1. Check if correct GameMode was choosen
        2. Show label about picked game mode
        3. Close selection box

        """
        if self.first_stage:
            if not self.second_stage and self.game_mode_selection_box.icon_selected and not self.game_mode_selected:
                self.game_controller.gui_interface.show_label(
                    (self.game_mode_selection_box.box_x + self.widht*0.3/3, self.game_mode_selection_box.box_y - self.height*0.3/3 - 20), 
                    f"{self.game_mode_selection_box.icon_selected.game_mode.name} selected!", 
                    color=(245, 245, 245), 
                    timeout=3,
                    id_="GameModeSelectedLabel"
                )
                self.game_controller.gui_interface.show_icon(
                    (self.widht*(MARIGIN_PERC+0.02), (self.height*(MARIGIN_PERC+0.02))), 
                    self.game_mode_selection_box.icon_selected.image, 
                    game_mode=self.game_mode_selection_box.icon_selected.game_mode, 
                    id_="GameModeSelectedIcon"
                )
                # check if game mode is correct
                if self.game_controller.score_board.update_player_game_mode_picked(self.game_mode_selection_box.icon_selected.game_mode):
                    self.game_mode_selected = self.game_mode_selection_box.icon_selected.game_mode
                    self.game_controller.table_info.game_mode_salected = self.game_mode_selected
                    self.game_controller.gui_interface.hide_by_id("GameModeSelectionBox")
                    self.second_stage = True
                    print(f"Second stage ended")
                else:
                    self.game_controller.gui_interface.hide_by_id("GameModeSelectedLabel")
                    self.game_controller.gui_interface.hide_by_id("GameModeSelectedIcon")
                    self.game_controller.gui_interface.show_label(
                        (self.game_mode_selection_box.box_x + self.widht*0.3/3, self.game_mode_selection_box.box_y - self.height*0.3/3 - 20), 
                        f"{self.game_mode_selection_box.icon_selected.game_mode.name} can't be selected!", 
                        color=(245, 245, 245),
                        timeout=3,
                        id_="GameModeNotSelectedLabel"
                    )
                    self.game_mode_selection_box.icon_selected = None

        return self.second_stage
    

    def update_third_stage(self):
        """
        Third stage of GamePrepare:
        1. Transfer 4 cards to player from picking box
        2. Clean picking box
        3. Create space for trash
        """
        if self.second_stage:
            if not self.third_stage:
                pick_space = self.game_controller.space_interface.get_by_id("PickSpace")
                pick_space.flip_cards()
                for card in pick_space.cards.copy():
                    pick_space.transfer(card, self.game_controller.score_board.game_mode_picking_player_space)
                pick_space.clean()
                self.game_controller.space_interface.get_by_id("PlayerSpace1").sort_active_player_cards()
                self.game_controller.space_interface.add(CardSpace("Trash", self.widht*0.45, self.height*(0.55-MARIGIN_PERC), self.widht*0.1, self.height*CARD_SPACE_HEIGHT_PERC, id_="TrashSpace", mouse_from=False, mouse_to=True))
                self.third_stage = True
                print(f"Third stage ended")

        return self.third_stage

    def update_fourth_stage(self):
        """
        Fourth stage of GamePrepare:
        1. Transfer 4 cards from player to trash
        """
        if self.third_stage:
            if not self.fourth_stage:
                if len(self.game_controller.space_interface.get_by_id("TrashSpace").cards) == 4:
                    self.game_controller.space_interface.get_by_id("TrashSpace").flip_cards()
                    self.game_controller.table_info.trashed_cards = self.game_controller.space_interface.get_by_id("TrashSpace").cards
                    self.fourth_stage = True
                    print(f"Fourth stage ended")
        return self.fourth_stage
    
    def update_fifth_stage(self):
        """
        Fifth stage of GamePrepare:
        1. Show start game button
        2. Update score board
        3. Start game
        """

        def deal_remaining_cards():
            # deal remining cards and END state
            for player in self.game_controller.score_board.players:
                self.deck.deal(10, player)
            self.game_controller.space_interface.get_by_id("PlayerSpace1").sort_active_player_cards()

            self.done = True

        if self.fourth_stage:
            if not self.fifth_stage:
                self.game_controller.gui_interface.show_button(
                    (self.game_mode_selection_box.box_x + self.game_mode_selection_box.box_width*0.4, self.game_mode_selection_box.box_y - self.game_mode_selection_box.box_height*0.05, self.widht*0.3, self.height*0.3), 
                    callback=deal_remaining_cards,
                    text=f"Start game", 
                    color=(245, 245, 245), 
                    id_="GameModeSelectedButton"
                    )
                self.fifth_stage = True
                print(f"Fifth stage ended")
        return self.fifth_stage

    def update(self):
        for space in self.game_controller.space_interface.space_list:
            space.add_label(self.game_controller.gui_interface)

        self.game_controller.space_interface.update()
        self.update_first_stage()
        self.update_second_stage()
        self.update_third_stage()
        self.update_fourth_stage()
        self.update_fifth_stage()

    def render(self, screen):
        self.game_controller.space_interface.render(screen)
        self.game_controller.gui_interface.render()

    def cleanup(self):
        self.game_controller.gui_interface.hide_by_id("GameModeSelectionBox")
        self.game_controller.gui_interface.hide_by_id("GameModeSelectedLabel")
        self.game_controller.gui_interface.hide_by_id("GameModeSelectedButton")

        self.game_controller.space_interface.hide_by_id("TrashSpace", self.game_controller.gui_interface)
        self.game_controller.space_interface.hide_by_id("DeckSpace", self.game_controller.gui_interface)
        self.game_controller.space_interface.hide_by_id("PickSpace", self.game_controller.gui_interface)

    def check_input(self, mouse_keys, mouse_pos, mouse_rel, event):
        self.game_controller.gui_interface.check_input(mouse_keys, mouse_pos, mouse_rel, event)
        self.game_controller.space_interface.check_input(mouse_keys, mouse_pos, mouse_rel, event)
