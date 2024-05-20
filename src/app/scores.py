from space import PlayerSpace
from models.enums import PlayerPosition, GameMode

class ScoreBoard:
    """Keeping track of scores. Should be inited in new_game"""
    def __init__(self, players: list[PlayerSpace]):
        self.players = players
        self.game_mode_picking_player_space = None
        self.game_mode = None
        self.first_player = self._get_player_with_position(PlayerPosition.First)
        self.second_player = self._get_player_with_position(PlayerPosition.Second)
        self.third_player = self._get_player_with_position(PlayerPosition.Third)
        self.rounds_played = 0

    def __str__(self) -> str:
        return "\n".join([f"{p}: total_score-> {p.player_info.total_score}" for p in (self.players)])

    def update_player_game_mode_picked(self, game_mode_picked: GameMode) -> bool:
        if game_mode_picked.name in self.game_mode_picking_player_space.player_info.available_game_mode_names:
            self.game_mode_picking_player_space.player_info.update_available_game_mode_names(game_mode_picked)
            self.game_mode = game_mode_picked
            return True
        else:
            return False

    def update_current_game_mode_picking_player_space(self) -> None:
        """Updates game_mode_picking_player_space inside score_board. Should be called only once per round inside prepare_game."""
        if not self.game_mode_picking_player_space:
            self.game_mode_picking_player_space = self.first_player
        else:
            if self.game_mode_picking_player_space == self.first_player:
                self.game_mode_picking_player_space = self.second_player
            elif self.game_mode_picking_player_space == self.second_player:
                self.game_mode_picking_player_space = self.third_player 
            elif self.game_mode_picking_player_space == self.third_player:
                self.game_mode_picking_player_space = self.first_player
            else:
                raise ValueError(f"Cannot update game_mode_picking_player_space player to: {self.game_mode_picking_player_space.name}")
    
    def change_starting_current_score(self, game_mode_selected: GameMode) -> None:
        """Called after update_current_game_mode_picking_player_space in prepare_game phase"""
        if game_mode_selected.name == game_mode_selected.NoTricks.name:
            if self.game_mode_picking_player_space == self.first_player:
                self.first_player.player_info.current_score = 3
                self.second_player.player_info.current_score = 5
                self.third_player.player_info.current_score = 8
            elif self.game_mode_picking_player_space == self.second_player:
                self.first_player.player_info.current_score = 8
                self.second_player.player_info.current_score = 3
                self.third_player.player_info.current_score = 5
            elif self.game_mode_picking_player_space == self.third_player:
                self.first_player.player_info.current_score = 5
                self.second_player.player_info.current_score = 8
                self.third_player.player_info.current_score = 3
        else:
            if self.game_mode_picking_player_space == self.first_player:
                self.first_player.player_info.current_score = -8
                self.second_player.player_info.current_score = -5
                self.third_player.player_info.current_score = -3
            elif self.game_mode_picking_player_space == self.second_player:
                self.first_player.player_info.current_score = -3
                self.second_player.player_info.current_score = -8
                self.third_player.player_info.current_score = -5
            elif self.game_mode_picking_player_space == self.third_player:
                self.first_player.player_info.current_score = -5
                self.second_player.player_info.current_score = -3
                self.third_player.player_info.current_score = -8

    def update_current_score(self, player_space: PlayerSpace, game_mode_selected: GameMode) -> None:
        """Increments current score of player_space by 1"""
        if game_mode_selected.name == game_mode_selected.NoTricks.name:
            player_space.player_info.current_score -= 1
        else:
            player_space.player_info.current_score += 1

    def update_score_board_for_next_round(self) -> None:
        """Increments total score of player_space by current score"""
        self.game_mode = None
        self.rounds_played += 1
        for p in self.players:
            p.player_info.total_score += p.player_info.current_score
            p.player_info.current_score = 0

    def get_turn_order(self, taking_player: PlayerSpace) -> list[PlayerSpace]:
        if taking_player.player_info.player_position == PlayerPosition.First:
            order = [taking_player, self.second_player, self.third_player]
        elif taking_player.player_info.player_position == PlayerPosition.Second:
            order = [taking_player, self.third_player, self.first_player]
        elif taking_player.player_info.player_position == PlayerPosition.Third:
            order = [taking_player, self.first_player, self.second_player]
        else:
            raise ValueError("Starting order isn't correctly specified.")

        return order
    
    def get_winner(self) -> PlayerSpace:
        return max(self.players, key=lambda p: p.player_info.total_score)

    def get_player_by_id(self, id_: str) -> PlayerSpace:
        for p in self.players:
            if p.id_ == id_:
                return p
        raise ValueError(f"No player with this id_: {id_}")
    
    def _get_player_with_position(self, player_position: PlayerPosition) -> PlayerSpace:
        for p in self.players:
            if p.player_info.player_position.name == player_position.name:
                return p
        raise ValueError(f"No player with this position: {player_position}")
    

            
            
    


        

    

    

