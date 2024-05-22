from AI.base import AbstractAI, TableInformation
from models.enums import GameMode, Suit
from models.card_models import CardsDict
from sprites import CardSprite
from space import PlayerSpace
from rules import Rules
import functools
from typing import List

class ClassicAI(AbstractAI):
    def __init__(self, table_info: TableInformation, rules: Rules) -> None:
        super().__init__(table_info, rules)

    def get_trump_suit(self) -> Suit|None:
        for suit in Suit:
            if suit.name == self.table_info.game_mode_selected.name:
                return suit

    def get_first_card_on_table_suit(self) -> Suit|None:
        if self.table_info.game_space_cards:
            if self.table_info.game_space_cards[0].space.first_card_on_table:
                return self.table_info.game_space_cards[0].space.first_card_on_table.suit
            
    def choose_game_mode(self, player: PlayerSpace) -> GameMode:
        card_dict = CardsDict(player.cards).card_dict
        available_game_mode_names = player.player_info.available_game_mode_names
        strongest_suit_name = available_game_mode_names[0]
        total_power = 0
        for suit_name, cl in card_dict.items():
            if suit_name in available_game_mode_names:
                total_power += cl.total_power_of_cards()
                if cl.total_power_of_cards() > card_dict[strongest_suit_name].total_power_of_cards():
                    strongest_suit_name = suit_name

        # check if NoTrump worth playing
        if GameMode.NoTrump.name in available_game_mode_names \
            and sum([self.check_if_card_can_win_from_starting_hand(card) for card in player.cards]) >= 2 \
            and total_power/len(player.cards) > 11:
            return GameMode.NoTrump
        # check if NoTricks worth playing
        if GameMode.NoTricks.name in available_game_mode_names and total_power/len(player.cards) < 7:
            return GameMode.NoTricks
        
        if strongest_suit_name == Suit.Clubs.name:
            return GameMode.Clubs
        elif strongest_suit_name == Suit.Diamonds.name:
            return GameMode.Diamonds
        elif strongest_suit_name == Suit.Hearts.name:
            return GameMode.Hearts
        elif strongest_suit_name == Suit.Spades.name:
            return GameMode.Spades
        else:
            raise ValueError(f"No gameMode selected for {player.name} which should not happen.")
        
    def choose_trash_cards(self, player: PlayerSpace) -> list[CardSprite]:
        if self.table_info.game_mode_selected.name == GameMode.NoTricks.name:
            trash_cards = []
            cards = player.cards.copy()
            while len(trash_cards) < 4:
                strongest_card = self.get_strongest_card(cards)
                cards.remove(strongest_card)
                trash_cards.append(strongest_card)
            return trash_cards

        winning_cards = [c for c in player.cards if self.check_if_card_can_win_from_starting_hand(c)]
        if self.table_info.game_mode_selected.name in GameMode.get_trumps():
            trump_cards = [c for c in player.cards if c.suit.name == self.get_trump_suit().name]
            trump_cards_not_in_winning = [c for c in trump_cards if c not in winning_cards]
        else:
            trump_cards = []
            trump_cards_not_in_winning = []
        best_cards = list(set(winning_cards).union(set(trump_cards)))
        trash_cards = list(set(player.cards).difference(set(best_cards)))

        if len(trash_cards) == 4:
            return trash_cards
        elif len(trash_cards) > 4:
            while len(trash_cards) > 4:
                strongest_card = self.get_strongest_card(trash_cards)
                trash_cards.remove(strongest_card)
            return trash_cards
        elif len(trash_cards) < 4:
            while len(trash_cards) < 4:
                if trump_cards_not_in_winning:
                    weakest_card = self.get_weakest_card(trump_cards_not_in_winning)
                else:
                    weakest_card = self.get_weakest_card(best_cards)
                trash_cards.append(weakest_card)
                best_cards.remove(weakest_card)
            return trash_cards
        else:
            raise ValueError("No trash cards found. That should not happen there.")

    def check_if_card_can_win_from_starting_hand(self, card: CardSprite) -> bool:
        opponent_cards = self.table_info.get_remaining_opponent_cards()
        for c in opponent_cards:
            if card != self.rules.compare(card, c, card.suit, GameMode.NoTrump):
                return False
        return True
    
    def get_strongest_card(self, cards: List[CardSprite]) -> CardSprite:
        """From card list gets the strongest card. Has to be in line with first_on_table card"""
        first_on_table_suit = self.get_first_card_on_table_suit()
        allowed_cards = self.rules.get_allowed_cards(cards, first_on_table_suit, self.table_info.game_mode_selected, cards)

        if allowed_cards:
            cards_dict = CardsDict(allowed_cards).card_dict
            strongest_card_number_of_cards = 0
            strongest_card = None
            strongest_card_power = 0

            # strongest card from allowed cards with the same suit
            if first_on_table_suit:
                strongest_card = cards_dict[first_on_table_suit.name].strongest_card()
                if strongest_card:
                    return strongest_card

            # strongest card from allowed cards without first_on_table_suit (there is no first_on_table_suit or no cards with the same suit)
            for _, inf in cards_dict.items():
                if inf.cards:
                    suit_strongest_card_ = inf.strongest_card()
                    suit_strongest_card_power_ = float(suit_strongest_card_)
                    if suit_strongest_card_power_ > strongest_card_power:
                        strongest_card = suit_strongest_card_
                        strongest_card_power = suit_strongest_card_power_
                        strongest_card_number_of_cards = inf.number_of_cards()
                    elif suit_strongest_card_power_ == strongest_card_power:
                        if strongest_card_number_of_cards > inf.number_of_cards():
                            strongest_card = suit_strongest_card_
                            strongest_card_power = suit_strongest_card_power_
                            strongest_card_number_of_cards = inf.number_of_cards()

            if strongest_card:
                return strongest_card
            else:
                raise ValueError("No strongest card found. That should not happen there.")

    def get_weakest_card(self, cards: List[CardSprite]) -> CardSprite:
        """From card list gets the weakest card. Has to be in line with first_on_table card"""
        first_on_table_suit = self.get_first_card_on_table_suit()
        trump_suit = self.get_trump_suit()
        allowed_cards = self.rules.get_allowed_cards(cards, first_on_table_suit, self.table_info.game_mode_selected, cards)
        if allowed_cards:
            cards_dict = CardsDict(allowed_cards).card_dict
            weakest_card_number_of_cards = 0
            weakest_card = None
            weakest_card_power = 20

            if first_on_table_suit:
                weakest_card = cards_dict[first_on_table_suit.name].weakest_card()
                if weakest_card:
                    return weakest_card

            for suit_name, inf in cards_dict.items():
                # choosing card without trump
                if inf.cards:
                    suit_weakest_card = inf.weakest_card()
                    suit_weakest_card_power = float(suit_weakest_card)
                    if not trump_suit or trump_suit.name != suit_name:
                        if suit_weakest_card_power < weakest_card_power:
                            weakest_card_number_of_cards = inf.number_of_cards()
                            weakest_card =  suit_weakest_card
                            weakest_card_power = suit_weakest_card_power
                        elif suit_weakest_card_power == weakest_card_power:
                            if inf.number_of_cards() >= weakest_card_number_of_cards:
                                weakest_card = inf.weakest_card()
                                weakest_card_power = suit_weakest_card_power
                                weakest_card_number_of_cards = inf.number_of_cards()

            if weakest_card:
                return weakest_card
            else:
                # only trump remains in hand
                weakest_card = cards_dict[trump_suit.name].weakest_card()
                if weakest_card:
                    return weakest_card
                else:
                    raise ValueError("No weakest card found. That should not happen there.")
        else:
            raise ValueError("No allowed card for weakest card function. That should not happen there.")

    def get_weakest_winning_card_from_hand(self) -> CardSprite:
        """ Case 2 cards on the table -> get weekest one if exists else weakest from hand"""
        first_on_table_suit = self.get_first_card_on_table_suit()
        winning_cards = []
        for card in self.table_info.hand_cards:
            if self.rules.validate_card(card, first_on_table_suit, self.table_info.game_mode_selected, self.table_info.hand_cards):
                strongest_card = functools.reduce(
                    lambda x, y: self.rules.compare(x, y, first_on_table_suit, self.table_info.game_mode_selected), 
                                self.table_info.game_space_cards + [card]) 
                if card == strongest_card:
                    winning_cards.append(card)
        if winning_cards:
            return self.get_weakest_card(winning_cards)
        else:
            return self.get_weakest_card(self.table_info.hand_cards)
    
    def get_strongest_losing_card_from_hand(self) -> CardSprite:
        """ NoTricks game"""
        first_on_table_suit = self.get_first_card_on_table_suit()
        allowed_cards = self.rules.get_allowed_cards(self.table_info.hand_cards, first_on_table_suit, self.table_info.game_mode_selected, self.table_info.hand_cards)
        strongest_losing_card = None
        for card in allowed_cards:
            game_space_weakest_cards = self.rules.get_game_space_weakest_cards(self.table_info.game_space_cards + [card], first_on_table_suit, self.table_info.game_mode_selected)
            if card in game_space_weakest_cards:
                if strongest_losing_card:
                    if card > strongest_losing_card:
                        strongest_losing_card = card
                else:
                    strongest_losing_card = card
        return strongest_losing_card
        
    def case_no_cards_in_game_space(self) -> CardSprite:
        for card in self.table_info.hand_cards:
            if self.check_if_card_can_win_from_starting_hand(card):
                return card
        return self.get_weakest_card(self.table_info.hand_cards)
    
    def case_one_card_in_game_space(self) -> CardSprite:
        first_on_table_suit = self.get_first_card_on_table_suit()
        for card in self.table_info.hand_cards:
            if self.rules.validate_card(card, first_on_table_suit, self.table_info.game_mode_selected):
                table_card = self.table_info.game_space_cards[0]
                better_card = self.rules.compare(card, table_card, table_card.suit, self.table_info.game_mode_selected)
                if card == better_card:
                    return card
        weakest_card = self.get_weakest_card(self.table_info.hand_cards)
        return weakest_card

    def case_two_cards_in_game_space(self) -> CardSprite:
        return self.get_weakest_winning_card_from_hand()

    def case_no_cards_in_game_space_no_tricks_game(self) -> CardSprite:
        return self.get_weakest_card(self.table_info.hand_cards)
    
    def case_one_card_in_game_space_no_tricks_game(self) -> CardSprite:
        stronges_losing_card = self.get_strongest_losing_card_from_hand()
        if stronges_losing_card:
            return stronges_losing_card
        else:
            strongest_card = self.get_strongest_card(self.table_info.hand_cards)
            if strongest_card:
                return strongest_card
            else:
                raise ValueError("No strongest card found. That should not happen there.")
            
    def case_two_cards_in_game_space_no_tricks_game(self) -> CardSprite:
        stronges_losing_card = self.get_strongest_losing_card_from_hand()
        if stronges_losing_card:
            return stronges_losing_card
        else:
            strongest_card = self.get_strongest_card(self.table_info.hand_cards)
            if strongest_card:
                return strongest_card
            else:
                raise ValueError("No strongest card found. That should not happen there.")

    def choose_best_card_trump_game(self) -> CardSprite:
        match len(self.table_info.game_space_cards):
            case 0:
                return self.case_no_cards_in_game_space()
            case 1:
                return self.case_one_card_in_game_space()
            case 2:
                return self.case_two_cards_in_game_space()
            case _:
                raise ValueError(f"No case for {len(self.table_info.game_space_cards)} cards in game_space. Error should not happened there.") 
            
    def choose_best_card_no_tricks_game(self) -> CardSprite:
        match len(self.table_info.game_space_cards):
            case 0:
                return self.case_no_cards_in_game_space_no_tricks_game()
            case 1:
                return self.case_one_card_in_game_space_no_tricks_game()
            case 2:
                return self.case_two_cards_in_game_space_no_tricks_game()
            case _:
                raise ValueError(f"No case for {len(self.table_info.game_space_cards)} cards in game_space. Error should not happened there.") 
    
    def choose_best_card(self) -> CardSprite:
        if self.table_info.game_mode_selected.name in GameMode.get_trumps() or self.table_info.game_mode_selected.name == GameMode.NoTrump.name:
            return self.choose_best_card_trump_game()
        else:
            return self.choose_best_card_no_tricks_game()

            

    

         