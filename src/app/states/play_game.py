import pygame as pg
from .state import State
from space.spaces import GameSpace
from settings import WIDTH, HEIGHT
import functools 
from itertools import cycle

SPACE_HEIGHT = HEIGHT*0.15
SPACE_WIDTH = WIDTH*0.1

class GamePlay(State):
    def __init__(self, game_controller):
        super().__init__(game_controller)
        self.game_controller = game_controller
        self.width = self.game_controller.screen.get_width()
        self.height = self.game_controller.screen.get_height()

        self.post_init_flag = False
        self.next_turn = True
        self.next_round = False
        self.ready_next_round = False
        self.end_game = False

        self.stages = cycle([
            self.check_game_space_full,
            self.check_next_round,
            self.check_end_game,
            self.check_new_turn,
            self.wait_for_bot_input,
            self.wait_for_player_input,
            ])

    def post_init(self):
        """ Called after the previous state is finished"""
        if not self.post_init_flag:
            self._prepare_spaces()
            self.current_turn_order = self.game_controller.score_board.get_turn_order(self.game_controller.score_board.game_mode_picking_player_space)
            self.current_player_space = None
            self.post_init_flag = True

    def _prepare_spaces(self):
        self.game_space = GameSpace(
            "Game", 
            self.width*0.4, self.height*0.45, self.width*0.2, self.height*0.2, 
            id_="GameSpace")
        self.game_controller.space_interface.add(self.game_space)

        self.game_controller.space_interface.add_loot_box_space(self.game_controller.space_interface.get_by_id("PlayerSpace1"))
        self.game_controller.space_interface.add_loot_box_space(self.game_controller.space_interface.get_by_id("PlayerSpace2"))
        self.game_controller.space_interface.add_loot_box_space(self.game_controller.space_interface.get_by_id("PlayerSpace3"))

        for space in self.game_controller.space_interface.space_list:
            space.add_label(self.game_controller.gui_interface)
        print(f"Active spaces: {[i.id_ for i in self.game_controller.space_interface.space_list]}")
    
    def choose_best_card(self):
        pg.time.wait(1000)
        return self.game_controller.AI.choose_best_card()
                
    def _decide_strongest_card_player(self):
        strongest_card = self.game_controller.rules.get_game_space_strongest_card(self.game_space.cards, self.game_space.first_card_on_table.suit, self.prev_state.game_mode_selected)
        strongest_card_player = strongest_card.space_history[-2]
        player_space_loot_box = strongest_card_player.loot_box_space
        self.game_controller.gui_interface.show_label(
            rect=(self.width*0.45, self.height*0.4, self.width*0.2, self.height*0.2), 
            text=f"strongest_card {strongest_card} goes to {strongest_card_player.name}", 
            timeout=3,
            id_="TempLabel"
        )
        print(f"decide_strongest_card_player log: strongest_card -> {strongest_card}, strongest_card_player -> {strongest_card_player.name}, player_space_loot_box -> {player_space_loot_box.name}")

        self.render_and_wait()
        for card in self.game_space.cards:
            self.game_controller.space_interface.move_to_space(card, player_space_loot_box)

        return strongest_card_player
        
    def check_game_space_full(self):
        """Check if the game space is full:
            1. If yes, decide the strongest card player
            2. Transfer game space cards to strongest card player loot box
            3. Update score board
            4. Update turn_order
            5. Update table info
            6. Update label
        """
        if self.game_space.full and not self.game_controller.space_interface.cards_moving:
            print(f"check_game_space_full...")
            strongest_card_player = self._decide_strongest_card_player()
            self.game_controller.score_board.update_current_score(strongest_card_player, self.game_controller.table_info.game_mode_selected)
            self.current_turn_order = self.game_controller.score_board.get_turn_order(strongest_card_player)
            self.update_table_info()
            for player in self.game_controller.score_board.players:
                player.label.update_text(str(player.player_info.current_score))
            self.next_turn = True

    def check_end_game(self):
        """Check if game should end"""
        if self.next_round and self.game_controller.score_board.check_game_end(): # last round ended
            print(f"check_end_game...")
            self.done = True
            self.end_game = True

    def __update_ready_next_round(self):
        self.ready_next_round = True

    def check_next_round(self):
        """Check if next round should be started"""

        cards_total_in_player_spaces = sum([len(player_space.cards) for player_space in self.game_controller.score_board.players])
        if cards_total_in_player_spaces == 0: # next round preparation
            self.next_turn = False
            self.next_round = True
            if not self.game_controller.gui_interface.get_by_id("GoToNextRoundButton"):
                self.game_controller.gui_interface.show_button(
                    rect=(self.width*0.4, self.height*0.35, self.width*0.2, self.height*0.2), 
                    callback=self.__update_ready_next_round,
                    text=f"Go to next round", 
                    id_="GoToNextRoundButton"
                )
            if self.ready_next_round:
                print(f"ready_next_round...")
                self.game_controller.score_board.update_score_board_for_next_round()
                self.game_controller.table_info.reset()
                self.done = True
        
    def check_new_turn(self):
        """ Start turn for next player"""
        if self.next_turn and not self.next_round and not self.game_controller.space_interface.cards_moving:
            print(f"check_new_turn...")
            self.game_controller.space_interface.adjust_all_space_card_position()
            self.current_player_space = self.current_turn_order.pop(0)
            self.update_table_info()
            self.next_turn = False
            print(f"new turn for new player: {self.current_player_space.name}")

    def wait_for_player_input(self):
        if self.current_player_space.mouse_from and not self.next_turn and not self.next_round:
            if self.game_space.cards:
                for card in self.game_space.cards:
                    if card.space_history[-2] == self.current_player_space:
                        print(f"player card in {self.game_space.name}: {card}")
                        self.next_turn = True

    def wait_for_bot_input(self):
        if not self.current_player_space.mouse_from and not self.next_turn and not self.next_round:
            if not self.game_controller.space_interface.cards_moving:
                if self.game_space.cards:
                    bot_cards_in_game_space = [card for card in self.game_space.cards if card.space_history[-2] == self.current_player_space]
                    if not bot_cards_in_game_space:
                        choosed_best_card = self.choose_best_card()
                        choosed_best_card.back_up = True
                        self.game_controller.space_interface.move_to_space(choosed_best_card, self.game_space)
                        print(f"{self.current_player_space.name} card {choosed_best_card} moving into {self.game_space.name}...")
                    else:                  
                        print(f"bot card in {self.game_space.name}")
                        self.next_turn = True
                else:
                    choosed_best_card = self.choose_best_card()
                    choosed_best_card.back_up = True
                    self.game_controller.space_interface.move_to_space(choosed_best_card, self.game_space)
                    print(f"{self.current_player_space.name} card {choosed_best_card} moving into {self.game_space.name}...")
            
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
        """Updates once per turn"""
        self.post_init()
        self.game_controller.space_interface.update()
        self.game_controller.gui_interface.update()
        next(self.stages)()
        self.update_table_info()
            
    def render(self, screen):
        self.game_controller.space_interface.render(screen)
        self.game_controller.gui_interface.render()

    def cleanup(self):
        self.game_controller.space_interface.hide_by_id("PlayerSpace1LootSpace", self.game_controller.gui_interface)
        self.game_controller.space_interface.hide_by_id("PlayerSpace2LootSpace", self.game_controller.gui_interface)
        self.game_controller.space_interface.hide_by_id("PlayerSpace3LootSpace", self.game_controller.gui_interface)
        self.game_controller.space_interface.hide_by_id("GameSpace", self.game_controller.gui_interface)
        self.game_controller.gui_interface.hide_by_id("GoToNextRoundButton")
        for p in self.game_controller.score_board.players:
            p.clean()

    def check_input(self, mouse_keys, mouse_pos, mouse_rel, event):
        self.game_controller.gui_interface.check_input(mouse_keys, mouse_pos, mouse_rel, event)
        self.game_controller.space_interface.check_input(mouse_keys, mouse_pos, mouse_rel, event, functools.partial(
            self.game_controller.rules.validate_card,
                first_on_table_suit=self.game_controller.AI.get_first_card_on_table_suit(),
                game_mode_selected=self.game_controller.table_info.game_mode_selected
            )
        )
