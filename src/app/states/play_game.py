import pygame as pg
from gui.interface import GuiInterface
from .state import State
from models import GameMode, Suit
from space import GameSpace, CardSpace, PlayerSpace
from settings import WIDTH, HEIGHT

import functools 

SPACE_HEIGHT = HEIGHT*0.15
SPACE_WIDTH = WIDTH*0.1

class GamePlay(State):
    def __init__(self, game_controller):
        super().__init__(game_controller)
        self.game_controller = game_controller
        self.post_init_flag = False
        self.game_space = None
        self.next_turn = True

    def post_init(self):
        """ Called after the previous state is finished"""
        if not self.post_init_flag:
            print(f"Initializing state: {self}")
            self.game_mode_picking_player_space = self.prev_state.game_mode_picking_player
            self.game_mode_selected = self.prev_state.game_mode_selected
            self.player_spaces = self.prev_state.players
            
            self._prepare_spaces()
            self.current_turn_order = self.get_turn_order(self.game_mode_picking_player_space)
            self.current_player_space = None
            self.post_init_flag = True

    def _prepare_spaces(self):
        self.game_space = GameSpace("Game", WIDTH*0.7, HEIGHT*0.2, WIDTH*0.3, HEIGHT*0.3, id_="GameSpace")
        self.game_controller.space_interface.add(self.game_space)

        self.game_controller.space_interface.get_by_id("PlayerSpace1").add_loot_box_space(
            CardSpace("Player1Loot", WIDTH*0.4, HEIGHT*0.3, SPACE_WIDTH, SPACE_HEIGHT, id_="Player1LootSpace")
        )

        self.game_controller.space_interface.get_by_id("PlayerSpace2").add_loot_box_space(
            CardSpace("Player2Loot", WIDTH*0.4, HEIGHT*0.5, SPACE_WIDTH, SPACE_HEIGHT, id_="Player2LootSpace")
        )

        self.game_controller.space_interface.get_by_id("PlayerSpace3").add_loot_box_space(
            CardSpace("Player3Loot", WIDTH*0.4, HEIGHT*0.7, SPACE_WIDTH, SPACE_HEIGHT, id_="Player3LootSpace")
        )
    
        for space in self.game_controller.space_interface.space_list:
            space.add_label(self.game_controller.gui_interface)
        print(f"Active spaces: {self.game_controller.space_interface.space_list}")

    def get_turn_order(self, taking_player: PlayerSpace):
        start_pos = self.player_spaces.index(taking_player)
        if start_pos == 0:
            order = [taking_player, self.player_spaces[1], self.player_spaces[2]]
        elif start_pos == 1:
            order = [taking_player, self.player_spaces[2], self.player_spaces[0]]
        elif start_pos == 2:
            order = [taking_player, self.player_spaces[0], self.player_spaces[1]]
        else:
            raise ValueError("Starting order isn't correctly specified.")
        return order
    
    def choose_best_card(self):
        cards_on_table = self.game_space.cards
        pg.time.wait(1000)
        if self.game_mode_selected == GameMode.Clubs:
            same_suit_cards = [card for card in self.current_player_space.cards if card.suit == Suit.Clubs]
            if same_suit_cards:
                return same_suit_cards[-1]
            else:
                return self.current_player_space.cards[0]

    def check_cards_in_game_space(self):
        return self.game_space.cards
    
    def get_strongest_card_in_game_space(self):
        if self.game_space.cards:
            pass
    
    def decide_strongest_card_player(self):
        strongest_card = functools.reduce(lambda x, y: x if x > y else y, self.game_space.cards) # now it is from game_space
        strongest_card_player = strongest_card.space_history[-2]
        player_space_loot_box = strongest_card_player.loot_box_space
        self.game_space.transfer_all(player_space_loot_box)
        return strongest_card_player

    def new_turn(self):
        if self.game_space.full:
            pg.time.wait(1000)
            # game_space full with 3 cards - decide which card won and update new turn order
            strongest_card_player = self.decide_strongest_card_player()
            self.current_turn_order = self.get_turn_order(strongest_card_player)
            print(f"strongest card from: {strongest_card_player}, new order: {list(self.current_turn_order)}")
            self.next_turn = True

        if self.next_turn: # new turn, reset next_turn status and get new player
            self.current_player_space = self.current_turn_order.pop(0)
            self.next_turn = False
            print(f"new turn for new player: {self.current_player_space}")

    def wait_for_player_input(self):
        if self.current_player_space.mouse_from and not self.next_turn:
            if self.game_space.cards:
                for card in self.game_space.cards:
                    if card.space_history[-2] == self.current_player_space:
                        print(f"Player card in game_space: {card}")
                        self.next_turn = True
                        break

    def wait_for_bot_input(self):
        if not self.current_player_space.mouse_from and not self.next_turn:
            if self.game_space.cards:
                if [card.space_history[-2] == self.current_player_space for card in self.game_space.cards]: # if bot card not in game space
                    choosed_best_card = self.choose_best_card()
                    choosed_best_card.flip()
                    self.current_player_space.transfer(choosed_best_card, self.game_space)
                    print(f"bot card in {self.game_space}: {choosed_best_card}")
                    self.next_turn = True
            else:
                choosed_best_card = self.choose_best_card()
                choosed_best_card.flip()
                self.current_player_space.transfer(choosed_best_card, self.game_space)
                print(f"bot card in {self.game_space}: {choosed_best_card}")
                self.next_turn = True    

    def check_end_game(self):
        cards_total_in_player_space = sum([len(player_space.cards) for player_space in self.player_spaces])
        if cards_total_in_player_space == 0:
            print("Round ended!")
            self.done = True

    def update(self):
        """Implement update method to update game state"""
        self.post_init()
        self.game_controller.space_interface.update()
        self.new_turn()
        self.wait_for_player_input()
        self.wait_for_bot_input()
        self.check_end_game()
            
    def render(self, screen):
        self.game_controller.space_interface.render(screen)
        self.game_controller.gui_interface.render()

    def check_input(self, mouse_keys, mouse_pos, mouse_rel, event):
        self.game_controller.gui_interface.check_input(mouse_keys, mouse_pos, mouse_rel, event)
        self.game_controller.space_interface.check_input(mouse_keys, mouse_pos, mouse_rel, event)