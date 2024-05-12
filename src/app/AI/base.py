from abc import ABC, abstractmethod

from sprites import Card
from models.enums import GameMode
from rules import Rules

from typing import List

class TableInformation:
    all_cards: List[Card]=[]
    trashed_cards: List[Card]=[]
    hand_cards: List[Card]=[]
    used_cards: List[Card]=[]
    game_space_cards: List[Card]=[]
    game_mode_salected: GameMode=None

    def __repr__(self):
        kws = [f"{key}={value!r}" for key, value in self.__dict__.items()]
        return "{}({})".format(type(self).__name__, ", ".join(kws))
    
    @classmethod
    def get_remaining_opponent_cards(cls):
        return list(set(cls.all_cards).difference(
            set(cls.trashed_cards), 
            set(cls.hand_cards), 
            set(cls.used_cards),
            set(cls.game_space_cards))
        )

class AbstractAI(ABC):
    def __init__(self, table_info: TableInformation, rules: Rules) -> None:
        self.table_info = table_info
        self.rules = rules

    @abstractmethod
    def choose_best_card(self):
        pass
