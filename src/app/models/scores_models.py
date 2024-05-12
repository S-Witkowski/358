from models.enums import GameMode, PlayerPosition
from dataclasses import dataclass

@dataclass
class GameModePicked:
    """Keeping track of game mode picked"""
    Clubs: bool = False
    Diamonds: bool = False
    Hearts: bool = False
    Spades: bool = False
    NoTrump: bool = False
    NoTricks: bool = False

    @classmethod
    def get_available_game_modes(cls) -> list[GameMode]:
        available_game_modes = []
        if not cls.Clubs:
            available_game_modes.append(GameMode.Clubs)
        if not cls.Diamonds:
            available_game_modes.append(GameMode.Diamonds)
        if not cls.Hearts:
            available_game_modes.append(GameMode.Hearts)
        if not cls.Spades:
            available_game_modes.append(GameMode.Spades)
        if not cls.NoTrump:
            available_game_modes.append(GameMode.NoTrump)
        if not cls.NoTricks:
            available_game_modes.append(GameMode.NoTricks)
        return available_game_modes
    
    @classmethod
    def update_game_mode_picked(cls, game_mode: GameMode) -> None:
        if game_mode == GameMode.Clubs:
            cls.Clubs = True
        if game_mode == GameMode.Diamonds:
            cls.Diamonds = True
        if game_mode == GameMode.Hearts:
            cls.Hearts = True
        if game_mode == GameMode.Spades:
            cls.Spades = True
        if game_mode == GameMode.NoTrump:
            cls.NoTrump = True
        if game_mode == GameMode.NoTricks:
            cls.NoTricks = True

@dataclass
class PlayerInfo:
    """Keeping track of player info"""
    player_position: PlayerPosition
    total_score: int = 0
    current_score: int = 0
    game_mode_picked: GameModePicked = GameModePicked