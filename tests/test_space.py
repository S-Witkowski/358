import pytest
from src.app.space import CardSpace
from src.app.models import Suit, CardValue
from app.game import Card

def test_space():
    deck_space = CardSpace("DeckSpace", 0, 0, 0, 0, True)
    for suit in Suit:
        for value in CardValue:
            deck_space.cards.append(
                Card(
                    suit, 
                    value, 
                    0,
                    0,
                    deck_space.width,
                    True
                    )
                )
    card_to_remove = deck_space.cards[0]
    deck_space.remove(card_to_remove)

    assert len(deck_space.cards) == 51
