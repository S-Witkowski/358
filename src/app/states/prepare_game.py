from .state import State
from space import CardSpace
from deck import Deck
import pygame as pg
from utils import load_and_transform_image
from settings import CARD_SPACE_HEIGHT_PERC, MARIGIN_PERC


class GamePrepare(State):
    """ State where game prepare is happening:
    1. Setting game mode selecting player
    2. Choosing game mode
    3. Choosing trash_cards
    4. Game start
    """
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
        self.deck = Deck("Deck", self.widht*0.35, self.height*(MARIGIN_PERC+0.02), self.widht*0.3, self.height*0.15, id_="DeckSpace")
        self.game_controller.space_interface.add(self.deck)
        self.game_controller.space_interface.add(CardSpace(
            "Pick", 
            self.widht*MARIGIN_PERC, self.height*(1-CARD_SPACE_HEIGHT_PERC-MARIGIN_PERC), self.widht*0.3, self.height*CARD_SPACE_HEIGHT_PERC, 
            id_="PickSpace", 
            mouse_from=False, 
            mouse_to=False)
        )
        
        # score_board - new game mode picking player, table info update
        self.game_controller.score_board.update_current_game_mode_picking_player_space()  
        self.game_controller.table_info.all_cards = self.deck.cards

    def deal_first_cards(self):
        self.deck.deal(6, self.game_controller.space_interface.get_by_id("PlayerSpace1"))
        self.deck.deal(6, self.game_controller.space_interface.get_by_id("PlayerSpace2"))
        self.deck.deal(6, self.game_controller.space_interface.get_by_id("PlayerSpace3"))
        self.deck.deal(4, self.game_controller.space_interface.get_by_id("PickSpace"))
        self.game_controller.space_interface.adjust_all_space_card_position()

    def update_first_stage(self):
        """ 
        First stage of GamePrepare:
        1. 6 cards dealt for every player
        2. 4 cards dealt for picking box
        3. Game mode selectionbox showed
        """
        if not self.first_stage:
            self.post_init()
            self.deal_first_cards()
            self.game_mode_selection_box = self.game_controller.gui_interface.show_selection_box(
                rect=(self.widht*0.375, self.height*0.3, self.widht*0.25, self.height*0.25), 
                id_="GameModeSelectionBox",
                available_game_mode_names=self.game_controller.score_board.game_mode_picking_player_space.player_info.available_game_mode_names
            )
            self.first_stage = True
            print(f"First stage ended")
        return self.first_stage 

    def update_second_stage(self): # player interaction needed to pass
        """
        Second stage of GamePrepare:
        1. Check if correct GameMode was choosen
        2. Show label about picked game mode
        3. Update table_info and score_board by game_mode_selected
        4. Close selection box

        """
        if self.first_stage:
            # Player decides game mode
            if not self.second_stage and not self.game_mode_selected:
                if self.game_controller.score_board.game_mode_picking_player_space.mouse_from and self.game_mode_selection_box.icon_selected:
                    # check if game mode is correct -> update_player_game_mode_picked should return True in that case
                    if self.game_controller.score_board.update_player_game_mode_picked(self.game_mode_selection_box.icon_selected.game_mode):
                        self.game_mode_selected = self.game_mode_selection_box.icon_selected.game_mode
                    else:
                        self.game_controller.gui_interface.show_label(
                            rect=(self.game_mode_selection_box.box_x + self.widht*0.3/3, self.game_mode_selection_box.box_y - self.height*0.3/3 - 20), 
                            text=f"{self.game_mode_selection_box.icon_selected.game_mode.name} can't be selected!", 
                            timeout=3,
                            id_="GameModeNotSelectedLabel"
                        )
                        self.game_mode_selection_box.icon_selected = None
                # AI decides game mode -> update_player_game_mode_picked always returns True
                elif not self.game_controller.score_board.game_mode_picking_player_space.mouse_from:
                    pg.time.wait(1000)
                    self.game_mode_selected = self.game_controller.AI.choose_game_mode(self.game_controller.score_board.game_mode_picking_player_space)
                    self.game_mode_selection_box.simulate_selecting_icon(self.game_mode_selected)
                    self.game_controller.score_board.update_player_game_mode_picked(self.game_mode_selected)

                # if seleced game mode is correct, show label
                if self.game_mode_selected:
                    self.game_controller.gui_interface.show_label(
                        rect=self.game_mode_selection_box.rect, 
                        text=f"{self.game_mode_selected.name} selected!", 
                        timeout=3,
                        id_="GameModeSelectedLabel"
                    )
                    pg.time.wait(1000)
                    self.game_controller.table_info.game_mode_selected = self.game_mode_selected
                    self.game_controller.score_board.change_starting_current_score(self.game_mode_selected)
                    self.game_controller.gui_interface.hide_by_id("GameModeSelectionBox")
                    self.second_stage = True
                    print(f"Second stage ended")

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

                 # flips cards if active player picked game mode and set trash_mouse_to
                if self.game_controller.score_board.game_mode_picking_player_space.mouse_from:
                    pick_space.flip_cards()
                    trash_mouse_to = True
                else:
                    trash_mouse_to = False

                # transfer cards from pick_space to game_mode_picking_player_space
                for card in pick_space.cards.copy():
                    pick_space.transfer(card, self.game_controller.score_board.game_mode_picking_player_space)
                pick_space.clean()

                # add trash space and show hint label
                self.game_controller.space_interface.add(CardSpace(
                    "Trash", 
                    self.widht*0.45, self.height*0.6, self.widht*0.1, self.height*CARD_SPACE_HEIGHT_PERC, 
                    id_="TrashSpace", 
                    image=load_and_transform_image("trash_space.png", space_width=self.widht*0.1, size_factor=1),
                    mouse_from=False, mouse_to=trash_mouse_to
                    )
                )
                self.game_controller.gui_interface.show_label(
                    rect=(self.widht*0.35, self.height*0.5, self.widht*0.2, self.height*0.2), 
                    text=f"Put 4 redundant cards in space below to start round!", 
                    timeout=0,
                    id_="TrashHintLabel"
                )
                self.game_controller.space_interface.adjust_all_space_card_position()
                self.third_stage = True
                print(f"Third stage ended")

        return self.third_stage

    def update_fourth_stage(self): # player interaction needed to pass
        """
        Fourth stage of GamePrepare:
        1. Transfer 4 cards from player to trash
        """
        if self.third_stage:
            if not self.fourth_stage:
                trash_space = self.game_controller.space_interface.get_by_id("TrashSpace")
                # if AI decides
                if not self.game_controller.score_board.game_mode_picking_player_space.mouse_from:
                    trash_cards = self.game_controller.AI.choose_trash_cards(self.game_controller.score_board.game_mode_picking_player_space)
                    for card in trash_cards:
                        self.game_controller.score_board.game_mode_picking_player_space.transfer(card, trash_space)

                if len(trash_space.cards) == 4:
                    trash_space.lock()
                    trash_space.flip_cards()
                    self.game_controller.table_info.trashed_cards = trash_space.cards

                    self.game_controller.gui_interface.show_label(
                        rect=(self.widht*0.4, self.height*0.35, self.widht*0.2, self.height*0.2), 
                        text=f"Cards in trash! Click Start game to start game!", 
                        timeout=3,
                        id_="CardsInTrashLabel"
                    )
                    self.game_controller.space_interface.adjust_all_space_card_position()
                    self.fourth_stage = True
                    print(f"Fourth stage ended")
        return self.fourth_stage
    
    def update_fifth_stage(self): # player interaction needed to pass
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
            self.game_controller.space_interface.adjust_all_space_card_position()
            self.done = True

        if self.fourth_stage:
            if not self.fifth_stage:
                self.game_controller.gui_interface.show_button(
                    rect=(self.widht*0.4, self.height*0.35, self.widht*0.2, self.height*0.2), 
                    callback=deal_remaining_cards,
                    text=f"Start round", 
                    id_="RoundStartButton"
                    )
                self.fifth_stage = True
                print(f"Fifth stage ended")
        return self.fifth_stage

    def update(self):
        for space in self.game_controller.space_interface.space_list:
            space.add_label(self.game_controller.gui_interface)

        self.game_controller.gui_interface.update()
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
        self.game_controller.gui_interface.hide_by_id("RoundStartButton")
        self.game_controller.gui_interface.hide_by_id("TrashHintLabel")

        self.game_controller.space_interface.hide_by_id("TrashSpace", self.game_controller.gui_interface)
        self.game_controller.space_interface.hide_by_id("DeckSpace", self.game_controller.gui_interface)
        self.game_controller.space_interface.hide_by_id("PickSpace", self.game_controller.gui_interface)

        for player in self.game_controller.score_board.players:
            player.label.update_text(str(player.player_info.current_score))

    def check_input(self, mouse_keys, mouse_pos, mouse_rel, event):
        self.game_controller.gui_interface.check_input(mouse_keys, mouse_pos, mouse_rel, event)
        self.game_controller.space_interface.check_input(mouse_keys, mouse_pos, mouse_rel, event)
