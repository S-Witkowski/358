import pygame as pg
from .state import State
from space import CardSpace, PlayerSpace
from deck import Deck

from settings import WIDTH, HEIGHT

SPACE_HEIGHT = HEIGHT*0.15
SPACE_WIDTH = WIDTH*0.4
DECK_POS = 25, HEIGHT*0.1


class GamePrepare(State):
    def __init__(self, game_controller):
        super().__init__(game_controller)
        self.game_controller = game_controller

        self.deck = None
        self.players = []
        self.game_mode_selection_box = None 
        self.game_mode_picking_player = None
        self.card_selected = None

        self.first_stage = False
        self.second_stage = False
        self.third_stage = False
        self.fourth_stage = False
        self.fifth_stage = False

        self.game_mode_selected = False
    
    def prepare_spaces(self):
        # deck space and all cards on the table
        self.deck = Deck("Deck", *DECK_POS, SPACE_WIDTH, SPACE_HEIGHT, id_="DeckSpace")
        self.game_controller.space_interface.add(self.deck)
        self.game_controller.space_interface.load_all_cards()
        self.cards = self.deck.cards
        print(f"Deck prepared with {len(self.cards)} cards")

        self.game_controller.space_interface.add(PlayerSpace("You", 25, HEIGHT*0.3, SPACE_WIDTH, SPACE_HEIGHT, id_="PlayerSpace1", mouse_from=True, mouse_to=False))
        self.game_controller.space_interface.add(PlayerSpace("Bot 1", 25, HEIGHT*0.5, SPACE_WIDTH, SPACE_HEIGHT, id_="PlayerSpace2", mouse_from=False, mouse_to=False))
        self.game_controller.space_interface.add(PlayerSpace("Bot 2", 25, HEIGHT*0.7, SPACE_WIDTH, SPACE_HEIGHT, id_="PlayerSpace3", mouse_from=False, mouse_to=False))
        self.game_controller.space_interface.add(CardSpace("Pick", 25, HEIGHT*0.9, SPACE_WIDTH, SPACE_HEIGHT, id_="PickSpace", mouse_from=False, mouse_to=False))

        for space in self.game_controller.space_interface.space_list:
            space.add_label(self.game_controller.gui_interface)

        self.players = [
            self.game_controller.space_interface.get_by_id("PlayerSpace1"), 
            self.game_controller.space_interface.get_by_id("PlayerSpace2"), 
            self.game_controller.space_interface.get_by_id("PlayerSpace3")
                        ]
        

    def get_game_mode_picking_player(self):
        self.game_mode_picking_player = self.players[0]
        # self.players[0], self.players[2] = self.players[2], self.players[0]

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
            self.prepare_spaces()
            self.get_game_mode_picking_player()
            self.deal_first_cards()
            self.game_mode_selection_box = self.game_controller.gui_interface.show_selection_box((WIDTH*0.5, HEIGHT*0.3), id_="GameModeSelectionBox")
            self.first_stage = True
            print(f"First stage ended")
        return self.first_stage 

    def update_second_stage(self):
        """
        Second stage of GamePrepare:
        1. Hide selection box
        2. Show label about picked game mode

        """
        if self.first_stage:
            if not self.second_stage and self.game_mode_selection_box.icon_selected and not self.game_mode_selected:
                self.game_controller.gui_interface.show_label(
                    (self.game_mode_selection_box.box_x + WIDTH*0.3/3, self.game_mode_selection_box.box_y - HEIGHT*0.3/3 - 20), 
                    f"{self.game_mode_selection_box.icon_selected.game_mode.name} selected!", color=(245, 245, 245), 
                    timeout=0,
                    id_="GameModeSelectedLabel"
                    )
                self.game_controller.gui_interface.show_icon(
                    (0 + 25, HEIGHT - 25), 
                    self.game_mode_selection_box.icon_selected.image, 
                    game_mode=self.game_mode_selection_box.icon_selected.game_mode, 
                    id_="GameModeSelectedIcon"
                )
                self.game_mode_selected = self.game_mode_selection_box.icon_selected.game_mode
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
                pick_space.flip_cards()
                for card in pick_space.cards.copy():
                    pick_space.transfer(card, self.game_mode_picking_player)
                pick_space.clean()
                self.game_controller.space_interface.add(CardSpace("Trash", WIDTH*0.8, HEIGHT*0.9, SPACE_WIDTH, SPACE_HEIGHT, id_="TrashSpace", mouse_from=False, mouse_to=True))
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
                    self.fourth_stage = True
                    print(f"Fourth stage ended")
        return self.fourth_stage
    
    def update_fifth_stage(self):
        """
        Fifth stage of GamePrepare:
        1. Show start game button
        2. Start game
        """

        def deal_remaining_cards():
            # deal remining cards and END state
            for player in self.players:
                self.deck.deal(10, player)
            self.done = True

        if self.fourth_stage:
            if not self.fifth_stage:
                self.game_controller.gui_interface.show_button(
                    (self.game_mode_selection_box.box_x + WIDTH*0.3/3, self.game_mode_selection_box.box_y - HEIGHT*0.3/3, WIDTH*0.3, HEIGHT*0.3), 
                    callback=deal_remaining_cards,
                    text=f"Start game", 
                    color=(245, 245, 245), 
                    id_="GameModeSelectedButton"
                    )
                self.fifth_stage = True
                print(f"Fifth stage ended")
        return self.fifth_stage


    def update(self):
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
