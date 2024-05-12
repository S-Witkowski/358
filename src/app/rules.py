from sprites import Card
from models.enums import GameMode, Suit
from typing import List

class Rules:
    def __init__(self, game_mode_selected: GameMode) -> None:
        self.game_mode_selected = game_mode_selected

    def compare_with_trump(self, one: Card, other: Card, first_on_table_suit: Suit) -> Card:
        # same suit as first_on_table_suit, compare by value for any suit
        if one.suit == first_on_table_suit and other.suit == first_on_table_suit:
            return one if one > other else other
        
        # one suit match, other don't
        elif one.suit == first_on_table_suit and other.suit != first_on_table_suit:
            # other is trump 
            return other if other.suit.name == self.game_mode_selected.name else one
            
        # other suit match, one don't
        elif one.suit != first_on_table_suit and other.suit == first_on_table_suit:
            # one is trump 
            return one if one.suit.name == self.game_mode_selected.name else other
             
        # both suits don't match
        elif one.suit != first_on_table_suit and other.suit != first_on_table_suit:
            # both trumps
            if one.suit.name == self.game_mode_selected.name and other.suit.name == self.game_mode_selected.name:
                return one if one > other else other
            # one trump
            elif one.suit.name == self.game_mode_selected.name and other.suit.name != self.game_mode_selected.name:
                return one
            # other trump
            elif one.suit.name != self.game_mode_selected.name and other.suit.name == self.game_mode_selected.name:
                return other            
            else: # no trump
                return one if one > other else other
        else:
            raise ValueError(f"Case not implemented for: cards ->{one}|{other}, first_card ->{first_on_table_suit}")

    def compare_without_trump(self, one: Card, other: Card, first_on_table_suit: Suit) -> Card:
        # same suit compare by value
        if one.suit == first_on_table_suit and other.suit == first_on_table_suit:
            return one if one > other else other
        # different suits, no trump
        elif one.suit == first_on_table_suit and other.suit != first_on_table_suit:
            return one
        elif one.suit != first_on_table_suit and other.suit == first_on_table_suit:
            return other
        elif one.suit != first_on_table_suit and other.suit == first_on_table_suit:
            return one if one > other else other
        else:
            raise ValueError(f"Case not implemented for: cards ->{one}|{other}, first_card ->{first_on_table_suit}")

    def compare(self, one: Card, other: Card, first_on_table_suit: Suit) -> Card:
        if self.game_mode_selected.name in GameMode.get_trumps():
            return self.compare_with_trump(one, other, first_on_table_suit)
        elif self.game_mode_selected.name in GameMode.get_no_trumps():
            return self.compare_without_trump(one, other, first_on_table_suit)
        else:
            raise ValueError(f"GameMode {self.game_mode_selected} not detected which should not happen.")

    def validate_card(self, card: Card, first_on_table_suit: Suit, player_cards: List[Card]=None) -> bool:
        """Validates if card can be moved to gamespace"""
        if not isinstance(card, Card):
            raise TypeError(f"card should be {Card} type, got {type(card)}")
        if not isinstance(first_on_table_suit, Suit):
            raise TypeError(f"first_on_table_suit should be {Suit} type, got {type(first_on_table_suit)}")
        if not player_cards:
            player_cards = card.space.cards
        # no first_on_table_suit so zero cards on game_space
        if not first_on_table_suit:
            return True
        # same suit card allowed
        if first_on_table_suit == card.suit:
            return True
        # if player throws card with different suit and doesn't have any card with same suit
        else:
            # cards in player hand with same suit as first_card
            if [card for card in player_cards if first_on_table_suit == card.suit]:
                return False
            else: # player doesn't have card with same suit -> have to throw trump if has any
                if self.game_mode_selected.name == card.suit.name:
                    return True
                # check if trumps in hand
                elif [card for card in player_cards if self.game_mode_selected.name == card.suit.name]:
                    return False
                # trump not in hand
                elif not [card for card in player_cards if self.game_mode_selected.name == card.suit.name]:
                    return True
                else:
                    raise ValueError(f"No rules for validation {card} with ft {first_on_table_suit}")
                    

