import pygame as pg
import functools 

from models.scores_models import PlayerInfo
from settings import MARIGIN_PERC
from utils import sort_cards

class CardSpace:
    rect_color = (50, 50, 50)
    card_offset = 20

    def __init__(self, name: str, x: int, y: int, width: float, height: float, id_: str, mouse_from=False, mouse_to=False):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.id_ = id_
        self.mouse_from = mouse_from
        self.mouse_to = mouse_to

        self.pos = (x, y)
        self.rect = pg.Rect(x, y, width, height)
        self.cards = []
        self.clicked_card = None
        self.label = None
        self.cards_ordered = False
    
    def __str__(self) -> str:
        return self.name

    def add_label(self, gui_interface):
        if not self.label:
            self.label = gui_interface.show_label(
                    (self.x, self.y - self.height*0.1), 
                    f"{self.name}", 
                    color=(245, 245, 245), 
                    timeout=0,
                    id_=f"CardSpaceLabel{self.name}"
                    )
        
    def add(self, card):
        self.cards.append(card)
        self.adjust_card_position_in_space()

    def remove(self, card):
        self.cards.remove(card)
    
    def clean(self):
        self.cards = []

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
            x_offset = self.x
            for card in self.cards:
                card.move((x_offset, self.y))
                x_offset += self.card_offset
                if self.mouse_from:
                    card.back_up = False

    def update(self):
        pass

    def render_cards(self, screen):
        for card in self.cards:
            card.render(screen)
    
    def render(self, screen):
        pg.draw.rect(screen, self.rect_color, self.rect)

class PlayerSpace(CardSpace):
    def __init__(self, name: str, x: int, y: int, width: float, height: float, id_: str, player_info: PlayerInfo, mouse_from=False, mouse_to=False):
        super().__init__(name, x, y, width, height, id_, mouse_to=mouse_to, mouse_from=mouse_from)
        self.loot_box_space = None
        self.player_info = player_info

    def add_loot_box_space(self):
        self.loot_box_space = CardSpace(f"{self.name}Loot", self.x, self.y + self.height + self.height*MARIGIN_PERC, self.width, self.height, id_=f"{self.name}LootSpace")

    def sort_active_player_cards(self):
        """Update player cards"""
        if not self.clicked_card:
            if self.mouse_from:
                self.cards = sort_cards(self.cards)      

class GameSpace(CardSpace):
    def __init__(self, name: str, x: int, y: int, width: float, height: float, id_: str):
        super().__init__(name, x, y, width, height, id_, mouse_to=True, mouse_from=False)
        self.cards = []
        self.full = False
        self.first_card_on_table = None

    def transfer_all(self, new_space: CardSpace):
        print(f"transfer all {self.cards} from {self} to {new_space}")
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
        for card in self.cards:
            card.back_up = False

        if not self.first_card_on_table and len(self.cards) == 1:
            self.first_card_on_table = self.cards[0]
        elif self.first_card_on_table and len(self.cards) == 0:
            self.first_card_on_table = None

        if not self.full and len(self.cards) == 3:
            self.full = True
        elif len(self.cards) < 3:
            self.full = False
        else:
            raise ValueError(f"GameSpace should have 3 cards or less, found {len(self.cards)}")
    
    def clean(self):
        """If there are three cards on the table, clean game_space and set every player space to transfer_done=False status """
        self.cards = []
        self.full = False
        
class SpaceInterface:
    """Supports all space objects and renders them"""
    def __init__(self):
        self.space_list = []
        self.all_cards = []
        self.card_moved = None

    def load_all_cards(self):
        for space in self.space_list:
            self.all_cards.extend(space.cards)

    def get_clicked_card(self):
        """Gets the list of all clicked cards and evaluates which one is on the top, then return it as clicked_card """
        self.load_all_cards()
        clicked_cards = []
        for card in self.all_cards:
            if card.clicked and card not in clicked_cards:
                clicked_cards.append(card)
        if clicked_cards:
            return functools.reduce(lambda a, b: a if a.clicked_pos[0] - a.rect[0] < b.clicked_pos[0] - b.rect[0] else b, clicked_cards)

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
                gui_interface.hide_by_id(f"CardSpaceLabel{element.name}")
                self.space_list.remove(element)
                break
            
    def render(self, screen):
        for space in self.space_list:
            space.render(screen)
        for space in self.space_list:
            space.render_cards(screen)
    
    def update(self):
        for space in self.space_list:
            space.update()
    
    def check_input(self, mouse_keys, mouse_pos, mouse_rel, event, rules=None):
        for card in self.all_cards:
            card.check_input(mouse_keys, mouse_pos, mouse_rel, event)
        # implement movement for one clicked card
        clicked_card = self.get_clicked_card()
        for space in self.space_list:
            if clicked_card:
                if clicked_card.space.mouse_from and event.type == pg.MOUSEMOTION:
                    clicked_card.move(mouse_pos)
                if clicked_card.check_rect_collision_with_space(space) and space.mouse_to:
                    self.card_moved = clicked_card
            else:
                if self.card_moved:
                    if space.mouse_to and event.type == pg.MOUSEBUTTONUP and space.rect.collidepoint(mouse_pos):
                        if rules and self.get_by_id("GameSpace").first_card_on_table:
                            if rules.validate_card(
                                self.card_moved, 
                                self.get_by_id("GameSpace").first_card_on_table.suit
                                ):
                                self.card_moved.space.transfer(self.card_moved, space)
                            else:
                                print(f"{self.card_moved} can't be moved to {space}!")
                        else:
                            self.card_moved.space.transfer(self.card_moved, space)

                        print(f"{self.card_moved} moved to {space.name}")
                        self.card_moved = None
                space.adjust_card_position_in_space()

                
                    


    
