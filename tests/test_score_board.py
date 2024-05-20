from src.app.scores import ScoreBoard
from src.app.space import PlayerSpace
from src.app.models.scores_models import PlayerInfo
from src.app.models.enums import PlayerPosition, GameMode


PLAYERS =  [
            PlayerSpace(
                "You", 
                0, 0, 0, 0,
                id_="PlayerSpace1", 
                player_info=PlayerInfo(player_position=PlayerPosition.First), 
                mouse_from=True, mouse_to=False
                ),
            PlayerSpace(
                "Bot 1", 
                0, 0, 0, 0,
                id_="PlayerSpace2", 
                player_info=PlayerInfo(player_position=PlayerPosition.Second),
                  mouse_from=False, mouse_to=False
                ),
            PlayerSpace(
                "Bot 2", 
                0, 0, 0, 0,
                id_="PlayerSpace3", 
                player_info=PlayerInfo(player_position=PlayerPosition.Third), 
                mouse_from=False, mouse_to=False
                )
        ]

def test_update_current_game_mode_picking_player_space():
    score_board = ScoreBoard(players=PLAYERS)
    score_board.update_current_game_mode_picking_player_space()
    assert score_board.game_mode_picking_player_space == PLAYERS[0]
    score_board.update_current_game_mode_picking_player_space()
    assert score_board.game_mode_picking_player_space == PLAYERS[1]
    score_board.update_current_game_mode_picking_player_space()
    assert score_board.game_mode_picking_player_space == PLAYERS[2]
    score_board.update_current_game_mode_picking_player_space()
    assert score_board.game_mode_picking_player_space == PLAYERS[0]

def test_update_player_game_mode_picked_1():
    score_board = ScoreBoard(players=PLAYERS)
    score_board.update_current_game_mode_picking_player_space()
    score_board.update_player_game_mode_picked(GameMode.NoTricks)
    assert GameMode.NoTricks.name not in score_board.game_mode_picking_player_space.player_info.available_game_modes


def test_update_player_game_mode_picked_1():
    score_board = ScoreBoard(players=PLAYERS)

    score_board.update_current_game_mode_picking_player_space()
    print(f"Current player: {score_board.game_mode_picking_player_space}")
    score_board.update_player_game_mode_picked(GameMode.NoTricks)

    score_board.update_current_game_mode_picking_player_space()
    print(f"Current player: {score_board.game_mode_picking_player_space}")
    score_board.update_player_game_mode_picked(GameMode.Spades)

    print(score_board.first_player.player_info)
    
    assert GameMode.NoTricks.name not in score_board.first_player.player_info.available_game_mode_names
    assert GameMode.Spades.name in score_board.first_player.player_info.available_game_mode_names

    assert GameMode.NoTricks.name in score_board.second_player.player_info.available_game_mode_names
    assert GameMode.Spades.name not in score_board.second_player.player_info.available_game_mode_names
