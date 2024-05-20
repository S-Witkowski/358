from abc import ABC, abstractmethod
from space import PlayerSpace
from sprites import CardSprite
from models.enums import GameMode
from rules import Rules

class TableInformation:
    all_cards: list[CardSprite]=[]
    trashed_cards: list[CardSprite]=[]
    hand_cards: list[CardSprite]=[]
    used_cards: list[CardSprite]=[]
    game_space_cards: list[CardSprite]=[]
    game_mode_selected: GameMode=None

    def reset(cls):
        cls.trashed_cards = []
        cls.hand_cards = []
        cls.used_cards = []
        cls.game_space_cards = []
        cls.game_mode_selected = None
    
    @classmethod
    def get_remaining_opponent_cards(cls) -> list:
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

    @abstractmethod
    def choose_game_mode(self, player: PlayerSpace) -> GameMode:
        pass

    @abstractmethod
    def choose_trash_cards(self, player: PlayerSpace) -> list[CardSprite]:
        pass