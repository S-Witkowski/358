import pygame as pg
import functools 
import math

from space.base import CardSpace
from space.spaces import PlayerSpace
from card.sprite import CardSprite
from settings import FPS

class SpaceInterface:
    """Supports all space objects and renders them.
    Also contains card movement logic
    """
    base_speed = 2
    def __init__(self, clock):
        self.clock = clock
        self.moving_card_speed = self.base_speed
        self.space_list: list[CardSpace] = []
        self.hand_cards: list[CardSprite] = []
        self.input_card_moved: dict[CardSprite, CardSpace | None] = {} # card moved by player
        self.cards_moving: dict[CardSprite, CardSpace] = {} # other type of cards movement
        self.cards_stop_moving: list[CardSprite] = []

    def load_hand_cards(self):
        for space in self.space_list:
            if space.mouse_from:
                self.hand_cards.extend(space.cards)

    def get_clicked_card(self):
        """Gets the list of all clicked cards and evaluates which one is on the top, then return it as clicked_card """
        self.load_hand_cards()
        clicked_cards = []
        for card in self.hand_cards:
            if card.clicked and card not in clicked_cards:
                clicked_cards.append(card)
        if clicked_cards:
            clicked_card = functools.reduce(lambda a, b: a if a.clicked_pos[0] - a.rect[0] < b.clicked_pos[0] - b.rect[0] else b, clicked_cards)
            for card in self.hand_cards:
                if card != clicked_card:
                    card.clicked = False
                    card.clicked_pos = None
            return clicked_card

    def add(self, space: CardSpace):
        self.space_list.append(space)

    def add_loot_box_space(self, player: PlayerSpace):
        player.add_loot_box_space()
        if hasattr(player, "loot_box_space"):
            if player.loot_box_space:
                self.space_list.append(player.loot_box_space)

    def get_by_id(self, id_: str):
        for element in self.space_list:
            if hasattr(element, "id_") and element.id_ == id_:
                return element

    def hide_by_id(self, id_: str, gui_interface):
        for element in self.space_list:
            if hasattr(element, "id_") and element.id_ == id_:
                gui_interface.hide_by_id(f"CardSpaceLabel{element.id_}")
                self.space_list.remove(element)
                break

    def move_to_space(self, card, new_space):
        if not card in self.cards_moving.keys():
            self.cards_moving[card] = new_space
            card.moving = True
    
    def add_card_to_stop_moving(self, card):
        self.cards_stop_moving.append(card)
        card.moving = False

    def render(self, screen):
        for space in self.space_list:
            space.render(screen)
        for space in self.space_list:
            space.render_cards(screen)

    def update_cards_moving(self):
        if self.cards_stop_moving:
            for card in self.cards_stop_moving:
                if card in self.cards_moving.keys():
                    del self.cards_moving[card]
            self.cards_stop_moving = []
    
    def update_moving_cards_handle(self):
        if self.cards_moving:
            for card, new_space in self.cards_moving.items():
                if card.moving:
                    # check if card can be moved
                    if new_space.locked:
                        self.add_card_to_stop_moving(card)
                        card.space.adjust_card_position_in_space()
                        continue

                    # get destination
                    if card.moving_pos:
                        dest = card.moving_pos
                    else:
                        dest = new_space.rect[0] + new_space.rect[2]/2, new_space.rect[1] + new_space.rect[3]/2

                    current_pos = card.rect.topleft
                    dx = dest[0] - current_pos[0]
                    dy = dest[1] - current_pos[1]
                    angle = math.atan2(dy, dx)

                    # if card is close enough to the destination, then stop moving
                    if card.space.mouse_from or (abs(dx) < self.moving_card_speed and abs(dy) < self.moving_card_speed):
                        card.space.transfer(card, new_space)
                        self.add_card_to_stop_moving(card)
                        new_space.adjust_card_position_in_space()
                        continue

                    # calculate new position
                    new_x = round(current_pos[0] + self.moving_card_speed * math.cos(angle))
                    new_y = round(current_pos[1] + self.moving_card_speed * math.sin(angle))
                    card.move_topleft((new_x, new_y))

    def update(self):
        """ Handles all moving cards"""
        self.moving_card_speed = self.base_speed * self.clock.tick(FPS)
        for space in self.space_list:
            space.update()
        self.update_moving_cards_handle()
        self.update_cards_moving()

    def adjust_all_space_card_position(self):
        for space in self.space_list:
            space.adjust_card_position_in_space()
                
    def check_input(self, mouse_keys, mouse_pos, mouse_rel, event, rule_validation_callback=None):
        for card in self.hand_cards:
            card.check_input(mouse_keys, mouse_pos, mouse_rel, event)
        # implement movement for clicked card
        clicked_card = self.get_clicked_card()
        if clicked_card:
            if clicked_card.space.mouse_from and event.type == pg.MOUSEMOTION:
                clicked_card.move_topleft(mouse_pos)

            # check if card is inside space: clicked_card -> self.input_card_moved
            for space in self.space_list:
                # card collide with space - potential move needs to be validated in next function call
                if clicked_card.check_rect_collision_with_space(space):
                    self.input_card_moved[clicked_card] = space
                    break
            if not self.input_card_moved or self.input_card_moved[clicked_card] == None:
                self.input_card_moved[clicked_card] = None

        # check if card from input_card_moved is dropped
        if self.input_card_moved:
            for k, v in self.input_card_moved.items():
                input_card_moved = k
                input_card_moved_space = v
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:            
                if input_card_moved_space and input_card_moved_space.mouse_to:
                    if rule_validation_callback:
                        if rule_validation_callback(input_card_moved):
                            self.move_to_space(input_card_moved, input_card_moved_space)
                        else:
                            self.adjust_all_space_card_position()
                    else:
                        self.move_to_space(input_card_moved, input_card_moved_space)

                # if card outside of any valid space, go back to prev space
                else:
                    self.adjust_all_space_card_position()

                self.input_card_moved = {}