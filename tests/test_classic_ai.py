from src.app.rules import Rules
from src.app.space.spaces import PlayerSpace
from src.app.card.base import Card
from src.app.models.scores_models import PlayerInfo
from src.app.models.enums import PlayerPosition, CardValue, Suit, GameMode
from src.app.AI.classic import ClassicAI
from src.app.AI.base import TableInformation

import pytest
from unittest.mock import MagicMock, patch


PLAYER_SPACE = PlayerSpace(
    "You", 
    0, 0, 0, 0,
    id_="PlayerSpace1", 
    player_info=PlayerInfo(player_position=PlayerPosition.First), 
    mouse_from=True, mouse_to=False
)

DECK_CARDS = []
for suit in Suit:
    for value in CardValue:
        DECK_CARDS.append(
            Card(
                suit=suit, 
                value=value,
                )
            )

#################### TESTING CHOOSE GAME_MODE ####################

def test_ai_choose_game_mode_1():
    card_1 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Ace))][0] 
    card_2 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.King))][0]
    card_3 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Hearts, CardValue.Queen))][0]  
    card_4 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Hearts, CardValue.Three))][0]
    card_5 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Eight))][0]
    card_6 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Five))][0]

    PLAYER_SPACE.cards = [card_1, card_2, card_3, card_4, card_5, card_6]

    rules = Rules()
    table_info = TableInformation
    table_info.all_cards=DECK_CARDS
    table_info.hand_cards=PLAYER_SPACE.cards
    table_info.game_space_cards=[]
    ai = ClassicAI(table_info, rules)
    assert ai.choose_game_mode(PLAYER_SPACE).name == GameMode.Spades.name

def test_ai_choose_game_mode_2():
    card_1 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Ace))][0] 
    card_2 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.King))][0]
    card_3 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Hearts, CardValue.Jack))][0]  
    card_4 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Hearts, CardValue.King))][0]
    card_5 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Eight))][0]
    card_6 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Diamonds, CardValue.Ace))][0]

    PLAYER_SPACE.cards = [card_1, card_2, card_3, card_4, card_5, card_6]

    rules = Rules()
    table_info = TableInformation
    table_info.all_cards=DECK_CARDS
    table_info.hand_cards=PLAYER_SPACE.cards
    table_info.game_space_cards=[]
    ai = ClassicAI(table_info, rules)
    assert ai.choose_game_mode(PLAYER_SPACE).name == GameMode.NoTrump.name

def test_ai_choose_game_mode_3():
    card_1 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Ace))][0] 
    card_2 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Four))][0]
    card_3 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Hearts, CardValue.Seven))][0]  
    card_4 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Hearts, CardValue.Three))][0]
    card_5 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Deuce))][0]
    card_6 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Five))][0]

    PLAYER_SPACE.cards = [card_1, card_2, card_3, card_4, card_5, card_6]

    rules = Rules()
    table_info = TableInformation
    table_info.all_cards=DECK_CARDS
    table_info.hand_cards=PLAYER_SPACE.cards
    table_info.game_space_cards=[]
    ai = ClassicAI(table_info, rules)
    assert ai.choose_game_mode(PLAYER_SPACE).name == GameMode.NoTricks.name

def test_ai_choose_game_mode_last_choice():
    card_1 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Ace))][0] 
    card_2 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Four))][0]
    card_3 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Hearts, CardValue.Seven))][0]  
    card_4 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Hearts, CardValue.Three))][0]
    card_5 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Deuce))][0]
    card_6 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Five))][0]

    last_available_game_mode_name = GameMode.Spades.name

    player_space = PlayerSpace(
        "You", 
        0, 0, 0, 0,
        id_="PlayerSpace1", 
        player_info=PlayerInfo(
            player_position=PlayerPosition.First,
            available_game_mode_names=[last_available_game_mode_name]
            ), 
        mouse_from=True, mouse_to=False
    )
    player_space.cards = [card_1, card_2, card_3, card_4, card_5, card_6]

    rules = Rules()
    table_info = TableInformation
    table_info.all_cards=DECK_CARDS
    table_info.hand_cards=player_space.cards
    table_info.game_space_cards=[]
    ai = ClassicAI(table_info, rules)
    assert ai.choose_game_mode(player_space).name == last_available_game_mode_name

#################### TESTING CHOOSE TRASH_CARDS ####################

def test_ai_choose_trash_cards_1():
    """ Correct len of trash_cards choosen"""
    card_1 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Ace))][0] 
    card_2 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.King))][0]
    card_3 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Hearts, CardValue.Queen))][0]  # trash
    card_4 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Hearts, CardValue.King))][0]
    card_5 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Eight))][0]
    card_6 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Five))][0]
    card_7 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Clubs, CardValue.Five))][0] # trash
    card_8 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Clubs, CardValue.Three))][0] # trash
    card_9 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Diamonds, CardValue.Five))][0] # trash
    card_10 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Clubs, CardValue.Ace))][0]

    PLAYER_SPACE.cards = [card_1, card_2, card_3, card_4, card_5, card_6, card_7, card_8, card_9, card_10]

    rules = Rules()
    table_info = TableInformation
    table_info.all_cards=DECK_CARDS
    table_info.hand_cards=[card_1, card_2, card_3, card_4, card_5, card_6, card_7, card_8, card_9, card_10]
    table_info.game_space_cards=[]
    table_info.game_mode_selected=GameMode.Spades
    ai = ClassicAI(table_info, rules)
    assert len(ai.choose_trash_cards(PLAYER_SPACE)) == 4

def test_ai_choose_trash_cards_2():
    """ Choosen trash cards as expected -> weak cards on hand"""
    card_1 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Ace))][0] 
    card_2 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.King))][0]
    card_3 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Hearts, CardValue.Queen))][0]  # trash
    card_4 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Hearts, CardValue.King))][0]
    card_5 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Eight))][0]
    card_6 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Five))][0]
    card_7 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Clubs, CardValue.Five))][0] # trash
    card_8 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Clubs, CardValue.Three))][0] # trash
    card_9 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Diamonds, CardValue.Five))][0] # trash
    card_10 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Clubs, CardValue.Ace))][0]

    PLAYER_SPACE.cards = [card_1, card_2, card_3, card_4, card_5, card_6, card_7, card_8, card_9, card_10]

    rules = Rules()
    table_info = TableInformation
    table_info.all_cards=DECK_CARDS
    table_info.hand_cards=[card_1, card_2, card_3, card_4, card_5, card_6, card_7, card_8, card_9, card_10]
    table_info.game_space_cards=[]
    table_info.game_mode_selected=GameMode.Spades
    ai = ClassicAI(table_info, rules)
    trash_cards_choosen = ai.choose_trash_cards(PLAYER_SPACE) 
    assert len(trash_cards_choosen) == 4
    assert card_3 in trash_cards_choosen
    assert card_7 in trash_cards_choosen
    assert card_8 in trash_cards_choosen
    assert card_9 in trash_cards_choosen

def test_ai_choose_trash_cards_3():
    """ Choosen trash cards as expected -> good cards in hand"""
    card_1 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Ace))][0] 
    card_2 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.King))][0]
    card_3 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Hearts, CardValue.Queen))][0] # trash
    card_4 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Hearts, CardValue.King))][0] # trash
    card_5 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Eight))][0]
    card_6 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Five))][0] # trash
    card_7 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Clubs, CardValue.Five))][0] # trash
    card_8 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Clubs, CardValue.Queen))][0] 
    card_9 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Clubs, CardValue.King))][0] 
    card_10 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Clubs, CardValue.Ace))][0]

    PLAYER_SPACE.cards = [card_1, card_2, card_3, card_4, card_5, card_6, card_7, card_8, card_9, card_10]

    rules = Rules()
    table_info = TableInformation
    table_info.all_cards=DECK_CARDS
    table_info.hand_cards=[card_1, card_2, card_3, card_4, card_5, card_6, card_7, card_8, card_9, card_10]
    table_info.game_space_cards=[]
    table_info.game_mode_selected=GameMode.Spades
    ai = ClassicAI(table_info, rules)
    trash_cards_choosen = ai.choose_trash_cards(PLAYER_SPACE) 
    assert len(trash_cards_choosen) == 4
    assert card_3 in trash_cards_choosen
    assert card_4 in trash_cards_choosen
    assert card_6 in trash_cards_choosen
    assert card_7 in trash_cards_choosen

def test_ai_choose_trash_cards_4():
    """ Choosen trash cards as expected -> NoTricks game"""
    card_1 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Ace))][0] # trash
    card_2 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Four))][0]
    card_3 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Hearts, CardValue.Seven))][0] # trash
    card_4 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Hearts, CardValue.Three))][0]
    card_5 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Deuce))][0]
    card_6 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Five))][0]
    card_7 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Clubs, CardValue.Five))][0]
    card_8 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Clubs, CardValue.Three))][0] 
    card_9 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Clubs, CardValue.King))][0]  # trash
    card_10 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Clubs, CardValue.Queen))][0] # trash

    PLAYER_SPACE.cards = [card_1, card_2, card_3, card_4, card_5, card_6, card_7, card_8, card_9, card_10]

    rules = Rules()
    table_info = TableInformation
    table_info.all_cards=DECK_CARDS
    table_info.hand_cards=[card_1, card_2, card_3, card_4, card_5, card_6, card_7, card_8, card_9, card_10]
    table_info.game_space_cards=[]
    table_info.game_mode_selected=GameMode.NoTricks
    ai = ClassicAI(table_info, rules)
    trash_cards_choosen = ai.choose_trash_cards(PLAYER_SPACE) 
    assert len(trash_cards_choosen) == 4
    assert card_1 in trash_cards_choosen
    assert card_3 in trash_cards_choosen
    assert card_9 in trash_cards_choosen
    assert card_10 in trash_cards_choosen

def test_ai_choose_trash_cards_5():
    """ Choosen trash cards as expected -> NoTrump game"""
    card_1 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Ace))][0] 
    card_2 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.King))][0]
    card_3 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Hearts, CardValue.Jack))][0]  # trash
    card_4 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Hearts, CardValue.King))][0]
    card_5 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Eight))][0] # trash
    card_6 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Diamonds, CardValue.Ace))][0]
    card_7 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Clubs, CardValue.Five))][0] # trash
    card_8 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Clubs, CardValue.Three))][0] # trash
    card_9 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Diamonds, CardValue.King))][0]  
    card_10 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Clubs, CardValue.Queen))][0] 

    PLAYER_SPACE.cards = [card_1, card_2, card_3, card_4, card_5, card_6, card_7, card_8, card_9, card_10]

    rules = Rules()
    table_info = TableInformation
    table_info.all_cards=DECK_CARDS
    table_info.hand_cards=PLAYER_SPACE.cards
    table_info.game_space_cards=[]
    table_info.game_mode_selected=GameMode.NoTrump
    ai = ClassicAI(table_info, rules)
    trash_cards_choosen = ai.choose_trash_cards(PLAYER_SPACE) 
    assert len(trash_cards_choosen) == 4
    assert card_3 in trash_cards_choosen
    assert card_5 in trash_cards_choosen
    assert card_7 in trash_cards_choosen
    assert card_8 in trash_cards_choosen

def test_table_info_1():
    table_info = TableInformation
    table_info.all_cards=DECK_CARDS
    table_info.hand_cards=[c for c in DECK_CARDS if str(c) == str(Card(Suit.Clubs, CardValue.Deuce))]
    table_info.game_space_cards=[]
    table_info.game_mode_selected=GameMode.Spades

    print(Card(Suit.Spades, CardValue.Ace) in table_info.all_cards)
    assert len(table_info.get_remaining_opponent_cards()) == 51

#################### TESTING NO_TRICKS GAME_MODE ####################

def test_ai_choose_best_card_no_tricks_1():
    card_1 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Ace))][0] 
    card_2 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Ten))][0] 
    card_3 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Hearts, CardValue.Three))][0] 
    card_4 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Hearts, CardValue.King))][0] 

    rules = Rules()
    table_info = TableInformation
    table_info.all_cards=DECK_CARDS
    table_info.hand_cards=[card_1, card_2, card_3, card_4]
    table_info.game_space_cards=[]
    table_info.game_mode_selected=GameMode.NoTricks
    
    ai = ClassicAI(table_info, rules)
    assert ai.choose_best_card() == card_3

def test_ai_choose_best_card_no_tricks_2():
    card_1 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Ace))][0] 
    card_2 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Ten))][0] 
    card_3 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Hearts, CardValue.Three))][0] 
    card_4 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Hearts, CardValue.King))][0] 

    game_space_cards = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Eight))]

    rules = Rules()
    table_info = TableInformation
    table_info.all_cards=DECK_CARDS
    table_info.hand_cards=[card_1, card_2, card_3, card_4]
    table_info.game_space_cards=game_space_cards
    table_info.game_mode_selected=GameMode.NoTricks
    with patch('src.app.AI.classic.ClassicAI.get_first_card_on_table_suit', return_value=game_space_cards[0].suit):
        ai = ClassicAI(table_info, rules)
        assert ai.choose_best_card() == card_1

def test_ai_choose_best_card_no_tricks_3():
    card_1 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Ace))][0] 
    card_2 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Ten))][0] 
    card_3 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Hearts, CardValue.Three))][0] 
    card_4 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Hearts, CardValue.King))][0] 

    game_space_cards = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Eight))] + [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Queen))]

    rules = Rules()
    table_info = TableInformation
    table_info.all_cards=DECK_CARDS
    table_info.hand_cards=[card_1, card_2, card_3, card_4]
    table_info.game_space_cards=game_space_cards
    table_info.game_mode_selected=GameMode.NoTricks
    with patch('src.app.AI.classic.ClassicAI.get_first_card_on_table_suit', return_value=game_space_cards[0].suit):
        ai = ClassicAI(table_info, rules)
        assert ai.choose_best_card() == card_2


def test_ai_choose_best_card_no_tricks_4():
    card_1 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Ace))][0] 
    card_2 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Ten))][0] 
    card_3 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Hearts, CardValue.Three))][0] 
    card_4 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Hearts, CardValue.King))][0] 

    game_space_cards = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Eight))]

    rules = Rules()
    table_info = TableInformation
    table_info.all_cards=DECK_CARDS
    table_info.hand_cards=[card_1, card_2, card_3, card_4]
    table_info.game_space_cards=game_space_cards
    table_info.game_mode_selected=GameMode.NoTricks
    with patch('src.app.AI.classic.ClassicAI.get_first_card_on_table_suit', return_value=game_space_cards[0].suit):
        ai = ClassicAI(table_info, rules)
        assert ai.choose_best_card() == card_1

#################### TESTING OTHER GAME MODES ####################

def test_ai_choose_best_card_1():
    card_1 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Ace))][0] 
    card_2 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Ten))][0] 
    card_3 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Hearts, CardValue.Three))][0] 
    card_4 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Hearts, CardValue.King))][0] 

    rules = Rules()
    table_info = TableInformation
    table_info.all_cards=DECK_CARDS
    table_info.hand_cards=[card_1, card_2, card_3, card_4]
    table_info.game_space_cards=[]
    table_info.game_mode_selected=GameMode.Hearts
    
    ai = ClassicAI(table_info, rules)
    assert ai.choose_best_card() == card_1

def test_ai_choose_best_card_2():
    card_1 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Deuce))][0] 
    card_2 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Ten))][0] 
    card_3 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Hearts, CardValue.Three))][0] 
    card_4 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.King))][0] 

    game_space_cards = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Nine))]
    used_cards = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Ace))]

    rules = Rules()
    table_info = TableInformation
    table_info.all_cards = DECK_CARDS
    table_info.hand_cards = [card_1, card_2, card_3, card_4]
    table_info.game_space_cards = game_space_cards
    table_info.used_cards = used_cards
    table_info.game_mode_selected = GameMode.Hearts
    
    with patch('src.app.AI.classic.ClassicAI.get_first_card_on_table_suit', return_value=game_space_cards[0].suit):
        ai = ClassicAI(table_info, rules)
        assert ai.choose_best_card() == card_4

def test_ai_choose_best_card_3():
    card_1 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Deuce))][0] 
    card_2 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Ten))][0] 
    card_3 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Hearts, CardValue.Three))][0] 
    card_4 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Queen))][0] 

    game_space_cards = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Nine))] \
                    + [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.King))]
    used_cards = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Ace))]

    rules = Rules()
    table_info = TableInformation
    table_info.all_cards = DECK_CARDS
    table_info.hand_cards = [card_1, card_2, card_3, card_4]
    table_info.game_space_cards = game_space_cards
    table_info.used_cards = used_cards
    table_info.game_mode_selected = GameMode.Hearts
    
    with patch('src.app.AI.classic.ClassicAI.get_first_card_on_table_suit', return_value=game_space_cards[0].suit):
        ai = ClassicAI(table_info, rules)
        assert ai.choose_best_card() == card_1

def test_ai_choose_best_card_4():
    card_1 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Deuce))][0] 
    card_2 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Ten))][0] 
    card_3 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Hearts, CardValue.Three))][0] 
    card_4 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.King))][0] 

    game_space_cards = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Ace))]
    used_cards = []

    rules = Rules()
    table_info = TableInformation
    table_info.all_cards = DECK_CARDS
    table_info.hand_cards = [card_1, card_2, card_3, card_4]
    table_info.game_space_cards = game_space_cards
    table_info.used_cards = used_cards
    table_info.game_mode_selected = GameMode.Hearts
    
    with patch('src.app.AI.classic.ClassicAI.get_first_card_on_table_suit', return_value=game_space_cards[0].suit):
        ai = ClassicAI(table_info, rules)
        assert ai.choose_best_card() == card_1

def test_ai_choose_best_card_5():
    card_1 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Deuce))][0] 
    card_2 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Ten))][0] 
    card_3 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Hearts, CardValue.Three))][0] 
    card_4 = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Ace))][0] 

    game_space_cards = [c for c in DECK_CARDS if str(c) == str(Card(Suit.Spades, CardValue.Nine))]
    used_cards = []

    rules = Rules()
    table_info = TableInformation
    table_info.all_cards = DECK_CARDS
    table_info.hand_cards = [card_1, card_2, card_3, card_4]
    table_info.game_space_cards = game_space_cards
    table_info.used_cards = used_cards
    table_info.game_mode_selected = GameMode.Hearts
    
    with patch('src.app.AI.classic.ClassicAI.get_first_card_on_table_suit', return_value=game_space_cards[0].suit):
        ai = ClassicAI(table_info, rules)
        assert ai.choose_best_card() == card_4