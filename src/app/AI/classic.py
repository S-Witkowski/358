from AI.base import AbstractAI, TableInformation
from enums import GameMode, Suit
from models import CardsDict
from sprites import Card
from rules import Rules
from random import choice
import functools
from typing import List
import random

class ClassicAI(AbstractAI):
    def __init__(self, table_info: TableInformation, rules: Rules) -> None:
        super().__init__(table_info, rules)

    def get_trump_suit(self) -> Suit|None:
        for suit in Suit:
            if suit.name == self.table_info.game_mode_salected.name:
                return suit

    def get_first_card_on_table_suit(self) -> Suit|None:
        if self.table_info.game_space_cards:
            return self.table_info.game_space_cards[0].space.first_card_on_table.suit

    def check_if_card_can_win_from_starting_hand(self, card: Card) -> bool:
        opponent_cards = self.table_info.get_remaining_opponent_cards()
        for c in opponent_cards:
            if card != self.rules.compare(card, c, card.suit):
                return False
        return True
        
    def get_weakest_card(self, cards: List[Card]) -> Card:
        """From card list gets the weakest card. Has to be in line with first_on_table card"""
        cards_dict = CardsDict(cards).card_dict
        first_on_table_suit = self.get_first_card_on_table_suit()
        trump_suit = self.get_trump_suit()
        print(f"Getting weakest card... first_on_table_suit: {first_on_table_suit}, trump_suit: {trump_suit}")
        # validate and extract only cards that are allowed
        allowed_cards = []
        for suit, inf in cards_dict.items():
            if inf.cards:
                if first_on_table_suit:
                    allowed_cards.extend(
                        [card for card in inf.cards if self.rules.validate_card(card, first_on_table_suit)]
                        )
                else:
                    allowed_cards.extend(inf.cards)
        allowed_cards = list(set(allowed_cards))

        if allowed_cards:
            print(f"Allowed cards: {allowed_cards}")
            cards_dict = CardsDict(allowed_cards).card_dict
            number_of_cards = 0
            total_power_of_cards = 0
            weakest_card = None

            if first_on_table_suit:
                weakest_card = cards_dict[first_on_table_suit].weakest_card()
                if weakest_card:
                    print(f"Weakest card from same_suit rule {weakest_card}")
                    return weakest_card
            for suit, inf in cards_dict.items():
                # choosing card without trump
                if inf.cards:
                    if trump_suit != suit:
                        if inf.number_of_cards() > number_of_cards:
                            number_of_cards = inf.number_of_cards()
                            total_power_of_cards = inf.total_power_of_cards()
                            weakest_card =  inf.weakest_card()
                        elif inf.number_of_cards() == number_of_cards:
                            if inf.total_power_of_cards() >= total_power_of_cards:
                                weakest_card = inf.weakest_card()
            if weakest_card:
                print(f"Weakest card from len and power rule {weakest_card}")
                return weakest_card
            else:
                # only trump remains in hand
                weakest_card = cards_dict[trump_suit].weakest_card()
                if weakest_card:
                    print(f"Weakest trump card  {weakest_card}")
                    return weakest_card
                else:
                    raise ValueError("No weakest card found. That should not happen there.")
        else:
            raise ValueError("No allowed card for weakest card function. That should not happen there.")

    def get_weakest_winning_card_from_hand(self) -> Card:
        """ Case 2 cards on the table -> get weekest one if exists else weakest from hand"""
        first_on_table_suit = self.get_first_card_on_table_suit()
        winning_cards = []
        for card in self.table_info.hand_cards:
            if self.rules.validate_card(card, first_on_table_suit):
                strongest_card = functools.reduce(
                    lambda x, y: self.rules.compare(x, y, first_on_table_suit), 
                                self.table_info.game_space_cards + [card]) 
                if card == strongest_card:
                    winning_cards.append(card)
        if winning_cards:
            return self.get_weakest_card(winning_cards)
        else:
            return self.get_weakest_card(self.table_info.hand_cards)
            

    def case_no_cards_in_game_space(self) -> Card:
        for card in self.table_info.hand_cards:
            if self.check_if_card_can_win_from_starting_hand(card):
                return card
        return self.get_weakest_card(self.table_info.hand_cards)
    
    def case_one_card_in_game_space(self) -> Card:
        first_on_table_suit = self.get_first_card_on_table_suit()
        for card in self.table_info.hand_cards:
            if self.rules.validate_card(card, first_on_table_suit):
                table_card = self.table_info.game_space_cards[0]
                better_card = self.rules.compare(card, table_card, table_card.suit)
                if card == better_card:
                    return card
        weakest_card = self.get_weakest_card(self.table_info.hand_cards)
        print(f"on table {table_card} vs {weakest_card}. Choosed weakest card: {weakest_card}")
        return weakest_card

    def case_two_cards_in_game_space(self) -> Card:
        return self.get_weakest_winning_card_from_hand()

    def choose_best_card_trump_game(self) -> Card:
        match len(self.table_info.game_space_cards):
            case 0:
                return self.case_no_cards_in_game_space()
            case 1:
                return self.case_one_card_in_game_space()
            case 2:
                return self.case_two_cards_in_game_space()
            case _:
                raise ValueError(f"No case for {len(self.table_info.game_space_cards)} cards in game_space. Error should not happened there.") 
    
    def choose_best_card(self) -> Card:
        if self.table_info.game_mode_salected.name in GameMode.get_trumps():
            return self.choose_best_card_trump_game()
        else:
            raise NotImplementedError("Case for different game than trump not implemented yet.")





            

    

         