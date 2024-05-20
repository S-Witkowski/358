from sprites import Card, CardSprite
from models.enums import GameMode, Suit
from models.card_models import CardsDict
from typing import List
import functools

class Rules:

    def _compare_with_trump(self, one: Card, other: Card, first_on_table_suit: Suit, game_mode_selected: GameMode) -> Card:
        # same suit as first_on_table_suit, compare by value for any suit
        if one.suit == first_on_table_suit and other.suit == first_on_table_suit:
            return one if one > other else other
        
        # one suit match, other don't
        elif one.suit == first_on_table_suit and other.suit != first_on_table_suit:
            # other is trump 
            return other if other.suit.name == game_mode_selected.name else one
            
        # other suit match, one don't
        elif one.suit != first_on_table_suit and other.suit == first_on_table_suit:
            # one is trump 
            return one if one.suit.name == game_mode_selected.name else other
             
        # both suits don't match
        elif one.suit != first_on_table_suit and other.suit != first_on_table_suit:
            # both trumps
            if one.suit.name == game_mode_selected.name and other.suit.name == game_mode_selected.name:
                return one if one > other else other
            # one trump
            elif one.suit.name == game_mode_selected.name and other.suit.name != game_mode_selected.name:
                return one
            # other trump
            elif one.suit.name != game_mode_selected.name and other.suit.name == game_mode_selected.name:
                return other            
            else: # no trump
                return one if one > other else other
        else:
            raise ValueError(f"Case not implemented for: cards ->{one}|{other}, first_card ->{first_on_table_suit}")

    def _compare_without_trump(self, one: Card, other: Card, first_on_table_suit: Suit) -> Card:
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

    def compare(self, one: Card, other: Card, first_on_table_suit: Suit, game_mode_selected: GameMode) -> Card:
        if game_mode_selected.name in GameMode.get_trumps():
            return self._compare_with_trump(one, other, first_on_table_suit, game_mode_selected)
        elif game_mode_selected.name in GameMode.get_no_trumps():
            return self._compare_without_trump(one, other, first_on_table_suit)
        else:
            raise ValueError(f"GameMode {game_mode_selected} not detected which should not happen.")
        
    def get_game_space_strongest_card(self, cards: list[Card], first_on_table_suit: Suit, game_mode_selected: GameMode) -> Card:
        return functools.reduce(
            lambda x, y: self.compare(x, y, first_on_table_suit, game_mode_selected), cards)
    
    def get_game_space_weakest_cards(self, cards: list[Card], first_on_table_suit: Suit, game_mode_selected: GameMode) -> list[Card]:
        cards_copy = cards.copy()
        if len(cards_copy) == 3:
            strongest_card = functools.reduce(
                lambda x, y: self.compare(x, y, first_on_table_suit, game_mode_selected), cards_copy)
            cards_copy.remove(strongest_card)
            return cards_copy
        if len(cards_copy) == 2:
            strongest_card = functools.reduce(
                lambda x, y: self.compare(x, y, first_on_table_suit, game_mode_selected), cards_copy)
            cards_copy.remove(strongest_card)
            return cards_copy
    
    def validate_card(self, card: CardSprite, first_on_table_suit: Suit|None, game_mode_selected: GameMode, player_cards: List[Card]=None) -> bool:
        """Validates if card can be moved to gamespace"""
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
                if game_mode_selected.name == card.suit.name:
                    return True
                # check if trumps in hand
                elif [card for card in player_cards if game_mode_selected.name == card.suit.name]:
                    return False
                # trump not in hand
                elif not [card for card in player_cards if game_mode_selected.name == card.suit.name]:
                    return True
                else:
                    raise ValueError(f"No rules for validation {card} with ft {first_on_table_suit}")

    def get_allowed_cards(self, cards: List[Card], first_on_table_suit: Suit, game_mode_selected: GameMode, player_hand_cards: List[Card]=None) -> List[Card]:
        """From card list gets the allowed cards. Has to be in line with first_on_table card"""
        if cards:
            cards_dict = CardsDict(cards).card_dict
            # validate and extract only cards that are allowed
            allowed_cards = []
            for _, inf in cards_dict.items():
                if inf.cards:
                    if first_on_table_suit:
                        allowed_cards.extend(
                            [card for card in inf.cards if self.validate_card(card, first_on_table_suit, game_mode_selected, player_hand_cards)]
                            )
                    else:
                        allowed_cards.extend(inf.cards)
            allowed_cards = list(set(allowed_cards))
            return allowed_cards

