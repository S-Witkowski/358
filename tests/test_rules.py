from src.app.rules import Rules
from src.app.space.spaces import PlayerSpace
from src.app.card.base import Card
from src.app.models.scores_models import PlayerInfo
from src.app.models.enums import PlayerPosition, CardValue, Suit, GameMode

PLAYER_SPACE = PlayerSpace(
    "You", 
    0, 0, 0, 0,
    id_="PlayerSpace1", 
    player_info=PlayerInfo(player_position=PlayerPosition.First), 
    mouse_from=True, mouse_to=False
)


def test_compare_1():
    rules = Rules()
    card_1 = Card(Suit.Spades, CardValue.Ace)
    card_2 = Card(Suit.Spades, CardValue.Ten)
    assert rules.compare(card_1, card_2, Suit.Spades, GameMode.Spades) == card_1

def test_compare_2():
    rules = Rules()
    card_1 = Card(Suit.Spades, CardValue.Ace)
    card_2 = Card(Suit.Spades, CardValue.Ten)
    card_3 = Card(Suit.Hearts, CardValue.Three)
    game_mode_selected = GameMode.Hearts
    assert card_3 == rules.get_game_space_strongest_card([card_1, card_2, card_3], Suit.Spades, game_mode_selected)

def test_compare_3():
    rules = Rules()
    card_1 = Card(Suit.Spades, CardValue.Ace)
    card_2 = Card(Suit.Hearts, CardValue.Ten)
    card_3 = Card(Suit.Spades, CardValue.King)
    game_mode_selected = GameMode.Hearts
    assert card_2 == rules.get_game_space_strongest_card([card_1, card_2, card_3], Suit.Spades, game_mode_selected)

def test_compare_4():
    rules = Rules()
    card_1 = Card(Suit.Spades, CardValue.Five)
    card_2 = Card(Suit.Hearts, CardValue.Ace)
    card_3 = Card(Suit.Spades, CardValue.Three)
    game_mode_selected = GameMode.Clubs
    assert card_1 == rules.get_game_space_strongest_card([card_1, card_2, card_3], Suit.Spades, game_mode_selected)

def test_compare_5():
    rules = Rules()
    card_1 = Card(Suit.Hearts, CardValue.Queen)
    card_2 = Card(Suit.Spades, CardValue.Ace)
    card_3 = Card(Suit.Diamonds, CardValue.Nine)
    game_mode_selected = GameMode.Diamonds
    assert card_3 == rules.get_game_space_strongest_card([card_1, card_2, card_3], Suit.Hearts, game_mode_selected)

def test_compare_decide_turn_weakest_card_1():
    rules = Rules()
    card_1 = Card(Suit.Hearts, CardValue.Three)
    card_2 = Card(Suit.Spades, CardValue.Ace)
    card_3 = Card(Suit.Clubs, CardValue.Nine)
    game_mode_selected = GameMode.Diamonds
    assert card_3 in rules.get_game_space_weakest_cards([card_1, card_2, card_3], Suit.Hearts, game_mode_selected)
    assert card_2 in rules.get_game_space_weakest_cards([card_1, card_2, card_3], Suit.Hearts, game_mode_selected)


def test_compare_decide_turn_weakest_card_2():
    rules = Rules()
    card_1 = Card(Suit.Hearts, CardValue.Three)
    card_2 = Card(Suit.Spades, CardValue.Ace)
    game_mode_selected = GameMode.Diamonds
    assert card_2 in rules.get_game_space_weakest_cards([card_1, card_2], Suit.Hearts, game_mode_selected)