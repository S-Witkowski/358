import pygame as pg
from settings import WIDTH, HEIGHT
import functools 


class CardSpace:
    rect_color = (50, 50, 50)
    card_offset = 20

    def __init__(self, name: str, x: int, y: int, width: int, height: int, id_: str, mouse_from=False, mouse_to=False):
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
        self.labeled = False
    
    def __repr__(self) -> str:
        return self.name

    def add_label(self, gui_interface):
        if not self.labeled:
            gui_interface.show_label(
                    (self.x, self.y - HEIGHT*0.02), 
                    f"{self.name}", 
                    color=(245, 245, 245), 
                    timeout=0,
                    id_=f"CardSpaceLabel{self.name}"
                    )
            self.labeled = True
        
    def add(self, card):
        self.cards.append(card)
        # self.update()

    def remove(self, card):
        self.cards.remove(card)
        # self.update()
    
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

    def update(self):
        """
        Adjust position of cards
        width -> card_spacing
        height -> max_card_height
        
        """
        x_offset = self.x
        if self.cards:
            for card in self.cards:
                card.move((x_offset, self.y))
                x_offset += self.card_offset
                if self.mouse_from:
                    card.back_up = False  

    def render_cards(self, screen):
        for card in self.cards:
            card.render(screen)
    
    def render(self, screen):
        pg.draw.rect(screen, self.rect_color, self.rect)

class PlayerSpace(CardSpace):
    def __init__(self, name: str, x: int, y: int, width: int, height: int, id_: str, loot_box_space: CardSpace, mouse_from=False, mouse_to=False):
        super().__init__(name, x, y, width, height, id_, mouse_to=True, mouse_from=False)
        self.loot_box_space = loot_box_space
        self.choosen_game_mode_lst = []

    def add_loot_box_space(self, loot_box_space: CardSpace):
        self.loot_box_space = loot_box_space

class GameSpace(CardSpace):
    def __init__(self, name: str, x: int, y: int, width: int, height: int, id_: str):
        super().__init__(name, x, y, width, height, id_, mouse_to=True, mouse_from=False)
        self.cards = []
        self.full = False

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

    def update(self):
        super().update()
        if len(self.cards) == 3:
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
        if hasattr(space, "loot_box_space"):
            self.space_list.append(space.loot_box_space)

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
    
    def check_input(self, mouse_keys, mouse_pos, mouse_rel, event):
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
                    if space.mouse_to and event.type == pg.MOUSEBUTTONUP:
                        self.card_moved.space.transfer(self.card_moved, space)
                        self.card_moved = None
                space.update()

                
                    


    
