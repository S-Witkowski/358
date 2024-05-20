from models.enums import PlayerPosition, GameMode
from dataclasses import dataclass, field

@dataclass
class PlayerInfo:
    """Keeping track of player info"""
    player_position: PlayerPosition
    total_score: int = 0
    current_score: int = 0
    available_game_mode_names: list[str] = field(default_factory=lambda: [gm.name for gm in GameMode])

    def update_available_game_mode_names(self, game_mode: GameMode):
        self.available_game_mode_names.remove(game_mode.name)
        print(f"game mode {game_mode} removed from {self.available_game_mode_names} from {self}")