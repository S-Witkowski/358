import pygame as pg
import functools 

from models.scores_models import PlayerInfo
from settings import MARIGIN_PERC
from utils import sort_cards, load_and_transform_image
from models.enums import PlayerPosition

class CardSpace:
    card_offset = 20
    text_size_rel = 0.05
    alpha = 128

    def __init__(self, name: str, x: int, y: int, width: float, height: float, id_: str, image=None, mouse_from=False, mouse_to=False):
        self.name = name
        self.rect = pg.Rect(x, y, width, height)
        self.id_ = id_
        self.image = image
        self.mouse_from = mouse_from
        self.mouse_to = mouse_to

        self.cards = []
        self.clicked_card = None
        self.label = None
        self.cards_moving = {} # {card: new_space}
        self.text_size = int(self.rect[2]*self.text_size_rel)
        self.locked = False

    def __str__(self) -> str:
        return self.name

    def add_label(self, gui_interface):
        if not self.label:
            self.label = gui_interface.show_label(
                    rect=self.rect,
                    text=f"{self.name}", 
                    id_=f"CardSpaceLabel{self.id_}",
                    )
            self.label.rect[1] = self.label.rect[1] - self.label.text_size
        
    def add(self, card):
        self.cards.append(card)

    def remove(self, card):
        self.cards.remove(card)

    def clean(self):
        self.cards = []

    def lock(self):
        self.locked = True
    
    def unlock(self):
        self.locked = False
            
    def transfer(self, card, new_space):
        """Transfer Card from current space to the new_space"""
        self.remove(card)
        new_space.add(card)
        card.add_new_space(new_space)

    def flip_cards(self):
        for card in self.cards: 
            card.flip()

    def adjust_card_position_in_space(self):
        if self.cards:
            x_offset = self.rect[0]
            for card in self.cards:
                if card not in self.cards_moving.keys():
                    card.move_topleft((x_offset, self.rect[1]))
                    x_offset += self.card_offset
                if self.mouse_from:
                    card.back_up = False

    def update(self):
        pass

    def render_cards(self, screen):
        for card in self.cards:
            card.render(screen)
    
    def render(self, screen):
        if self.image:
            self.image.set_alpha(self.alpha)
            screen.blit(self.image, (self.rect.topleft))

class PlayerSpace(CardSpace):
    def __init__(self, name: str, x: int, y: int, width: float, height: float, id_: str, player_info: PlayerInfo, mouse_from=False, mouse_to=False):
        super().__init__(name, x, y, width, height, id_, mouse_to=mouse_to, mouse_from=mouse_from)
        self.loot_box_space = None
        self.player_info = player_info
        # self.image = load_and_transform_image("game_space.jpg", space_width=width, size_factor=1)

    def add_loot_box_space(self):
        self.loot_box_space = CardSpace(f"{self.name}Loot", self.rect[0], self.rect[1] + self.rect[3]*(1+MARIGIN_PERC), self.rect[2], self.rect[3], id_=f"{self.id_}LootSpace")

    def clean(self):
        super().clean()
        self.loot_box_space.cards = []

    def _sort_active_player_cards(self):
        """Update player cards"""
        if not self.clicked_card:
            if self.mouse_from:
                self.cards = sort_cards(self.cards)

    def adjust_card_position_in_space(self):
        self._sort_active_player_cards()
        super().adjust_card_position_in_space()

    def move_to_space(self, card, new_space):
        if not card in self.cards_moving.keys():
            self.cards_moving[card] = new_space

class GameSpace(CardSpace):
    def __init__(self, name: str, x: int, y: int, width: float, height: float, id_: str):
        super().__init__(name, x, y, width, height, id_, mouse_to=True, mouse_from=False)
        self.cards = []
        self.full = False
        self.first_card_on_table = None
        self.image = load_and_transform_image("game_space.jpg", space_width=width, size_factor=1)

    def transfer_all(self, new_space: CardSpace):
        self.adjust_card_position_in_space() # adjust position of game space cards before transfer_all
        cards = self.cards.copy()
        for card in cards:
            self.remove(card)
            new_space.add(card)
            card.add_new_space(new_space)

        if self.cards:
            raise ValueError(f"GameSpace should have 0 cards after transfer_all method, found {len(self.cards)}")
        self.full = False
        self.first_card_on_table = None

    def update(self):
        if not self.first_card_on_table and len(self.cards) == 1:
            self.first_card_on_table = self.cards[0]
        elif self.first_card_on_table and len(self.cards) == 0:
            self.first_card_on_table = None

        if len(self.cards) == 3:
            self.full = True
        elif len(self.cards) < 3:
            self.full = False
        else:
            raise ValueError(f"GameSpace should have 3 cards or less, found {len(self.cards)}")
        
    def adjust_card_position_in_space(self):
        if self.cards:
            for card in self.cards:
                if card.space_history[-2].player_info.player_position == PlayerPosition.First:
                    card.move_topleft((self.rect[0] + 0.5*self.rect[2] - card.rect[2]/2, self.rect[1] + self.rect[3]*0.5))
                elif card.space_history[-2].player_info.player_position == PlayerPosition.Second:
                    card.move_topleft((self.rect[0] + 0.45*self.rect[2] - card.rect[2]/2, self.rect[1] + self.rect[3]*0.4))
                elif card.space_history[-2].player_info.player_position == PlayerPosition.Third:
                    card.move_topleft((self.rect[0] + 0.55*self.rect[2] - card.rect[2]/2, self.rect[1] + self.rect[3]*0.3))
                card.back_up = False

    def clean(self):
        """If there are three cards on the table, clean game_space and set every player space to transfer_done=False status """
        self.cards = []
        self.full = False
        
class SpaceInterface:
    """Supports all space objects and renders them"""
    def __init__(self):
        self.space_list = []
        self.hand_cards = []
        self.card_moved = None

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

    def render(self, screen):
        for space in self.space_list:
            space.render(screen)
        for space in self.space_list:
            space.render_cards(screen)
    
    def update(self):
        """ Handles all moving cards"""
        for space in self.space_list:
            space.update()
            if space.cards_moving:
                for card, new_space in space.cards_moving.items():
                    if new_space.locked:
                        del space.cards_moving[card]
                        return
                    velocity = 20
                    current_pos = card.rect.topleft
                    dest = new_space.rect[0] + new_space.rect[2]/2, new_space.rect[1] + new_space.rect[3]/2
                    x_offset = dest[0] - current_pos[0]
                    y_offset = dest[1] - current_pos[1]
                    x_ratio = x_offset/(y_offset + 0.00001)
                    if (x_offset < velocity and y_offset < velocity) or card.space.mouse_from:
                        del space.cards_moving[card]
                        space.transfer(card, new_space)
                        new_space.adjust_card_position_in_space()
                        return
                    if x_offset > 0:
                        new_x = current_pos[0] + velocity*x_ratio
                    elif x_offset < 0:
                        new_x = current_pos[0] + velocity*x_ratio
                    else:
                        new_x = current_pos[0]

                    if y_offset > 0:
                        new_y = current_pos[1] + velocity
                    elif y_offset < 0:
                        new_y = current_pos[1] - velocity
                    else:
                        new_y = current_pos[1]

                    card.move_topleft((new_x, new_y))

    def adjust_all_space_card_position(self):
        for space in self.space_list:
            space.adjust_card_position_in_space()
                
    def check_input(self, mouse_keys, mouse_pos, mouse_rel, event, rule_validation_callback=None):
        for card in self.hand_cards:
            card.check_input(mouse_keys, mouse_pos, mouse_rel, event)
        # implement movement for one clicked card
        clicked_card = self.get_clicked_card()
        for space in self.space_list:
            if clicked_card:
                if clicked_card.space.mouse_from and event.type == pg.MOUSEMOTION:
                    clicked_card.move_topleft(mouse_pos)
                if clicked_card.check_rect_collision_with_space(space) and space.mouse_to:
                    self.card_moved = clicked_card
            else:
                if self.card_moved:
                    if space.mouse_to and event.type == pg.MOUSEBUTTONUP and space.rect.collidepoint(mouse_pos):
                        if rule_validation_callback:
                            if rule_validation_callback(self.card_moved):
                                self.card_moved.space.move_to_space(self.card_moved, space)
                        else:
                            self.card_moved.space.move_to_space(self.card_moved, space)
                        self.card_moved = None
                space.adjust_card_position_in_space()
                    
            
                
                
                    


    
