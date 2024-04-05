import pytest
from src.app.models.card import Card, Suit, CardValue

def test_card():
    card = Card(Suit.Clubs, CardValue.Ace)
    assert card.suit == Suit.Clubs
    assert card.value == CardValue.Ace
    assert repr(card) == "Ace of Clubs"
    assert Card(Suit.Clubs, CardValue.Ace) > Card(Suit.Clubs, CardValue.King)
