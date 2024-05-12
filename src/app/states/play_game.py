import pygame as pg
from .state import State
from space import GameSpace
from rules import Rules
from settings import WIDTH, HEIGHT
from AI.classic import ClassicAI

import functools 

SPACE_HEIGHT = HEIGHT*0.15
SPACE_WIDTH = WIDTH*0.1

class GamePlay(State):
    def __init__(self, game_controller):
        super().__init__(game_controller)
        self.game_controller = game_controller
        self.widht = self.game_controller.screen.get_width()
        self.height = self.game_controller.screen.get_height()

        self.post_init_flag = False
        self.next_turn = True

    def post_init(self):
        """ Called after the previous state is finished"""
        if not self.post_init_flag:
            print(f"Initializing state: {self}")
            self.rules = Rules(self.prev_state.game_mode_selected)
            self.AI = ClassicAI(self.game_controller.table_info, self.rules)

            self._prepare_spaces()
            self.current_turn_order = self.game_controller.score_board.get_turn_order(self.game_controller.score_board.game_mode_picking_player_space)
            self.current_player_space = None
            self.post_init_flag = True

    def _prepare_spaces(self):
        self.game_space = GameSpace("Game", self.widht*0.4, self.height*0.4, self.widht*0.2, self.height*0.2, id_="GameSpace")
        self.game_controller.space_interface.add(self.game_space)

        self.game_controller.space_interface.add_loot_box_space(self.game_controller.space_interface.get_by_id("PlayerSpace1"))
        self.game_controller.space_interface.add_loot_box_space(self.game_controller.space_interface.get_by_id("PlayerSpace2"))
        self.game_controller.space_interface.add_loot_box_space(self.game_controller.space_interface.get_by_id("PlayerSpace3"))

        for space in self.game_controller.space_interface.space_list:
            space.add_label(self.game_controller.gui_interface)
        print(f"Active spaces: {self.game_controller.space_interface.space_list}")
    
    def choose_best_card(self):
        pg.time.wait(1000)
        return self.AI.choose_best_card()
    
    def decide_strongest_card_player(self):
        strongest_card = functools.reduce(
            lambda x, y: self.rules.compare(x, y, self.game_space.first_card_on_table.suit), 
                        self.game_space.cards) 
        strongest_card_player = strongest_card.space_history[-2]
        player_space_loot_box = strongest_card_player.loot_box_space
        self.game_space.transfer_all(player_space_loot_box)
        return strongest_card_player

    def new_turn(self):
        if self.game_space.full:
            pg.time.wait(1000)
            # game_space full with 3 cards - decide which card won and update new turn order
            strongest_card_player = self.decide_strongest_card_player()
            self.game_controller.score_board.update_current_score(strongest_card_player)
            self.current_turn_order = self.game_controller.score_board.get_turn_order(strongest_card_player)
            print(f"strongest card from: {strongest_card_player.name}, new order: {list(self.current_turn_order)}")
            self.next_turn = True

        if self.next_turn: # new turn, reset next_turn status and get new player
            for player in self.game_controller.score_board.players:
                player.label.update_text(player.player_info.current_score)
            self.current_player_space = self.current_turn_order.pop(0)
            self.update_table_info()
            self.next_turn = False
            print(f"new turn for new player: {self.current_player_space.name}")

    def wait_for_player_input(self):
        if self.current_player_space.mouse_from and not self.next_turn:
            if self.game_space.cards:
                for card in self.game_space.cards:
                    if card.space_history[-2] == self.current_player_space:
                        self.next_turn = True

    def wait_for_bot_input(self):
        if not self.current_player_space.mouse_from and not self.next_turn:
            if self.game_space.cards:
                if [card.space_history[-2] == self.current_player_space for card in self.game_space.cards]: # if bot card not in game space
                    choosed_best_card = self.choose_best_card()
                    print(f"{self.current_player_space.name} choosed {choosed_best_card}")
                    self.current_player_space.transfer(choosed_best_card, self.game_space)
                    choosed_best_card.flip()
                    print(f"bot card in {self.game_space.name}: {choosed_best_card}")
                    self.next_turn = True
            else:
                choosed_best_card = self.choose_best_card()
                self.current_player_space.transfer(choosed_best_card, self.game_space)
                choosed_best_card.flip()
                print(f"bot card in {self.game_space.name}: {choosed_best_card}")
                self.next_turn = True    

    def check_end_game(self):
        cards_total_in_player_space = sum([len(player_space.cards) for player_space in self.game_controller.score_board.players])
        if cards_total_in_player_space == 0:
            print("Round ended!")
            self.done = True
            
    def update_table_info(self):
        used_cards = [] 
        for ps in self.game_controller.score_board.players:
            if ps != self.current_player_space:
                used_cards.extend(ps.loot_box_space.cards)
        if self.current_player_space:
            self.game_controller.table_info.hand_cards = self.current_player_space.cards
        if used_cards:
            self.game_controller.table_info.used_cards = used_cards
        if self.game_space.cards:
            self.game_controller.table_info.game_space_cards = self.game_space.cards

    def update(self):
        """Implement update method to update game state"""
        self.post_init()

        self.game_controller.space_interface.update()

        self.update_table_info()
        self.new_turn()
        self.wait_for_bot_input()
        self.wait_for_player_input()
        self.check_end_game()
            
    def render(self, screen):
        self.game_controller.space_interface.render(screen)
        self.game_controller.gui_interface.render()

    def check_input(self, mouse_keys, mouse_pos, mouse_rel, event):
        self.game_controller.gui_interface.check_input(mouse_keys, mouse_pos, mouse_rel, event)
        self.game_controller.space_interface.check_input(mouse_keys, mouse_pos, mouse_rel, event, self.rules)