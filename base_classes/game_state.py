from base_classes.players import Player
from base_classes.deck import CardDeck, OpenStaple
from typing import List, Optional


class GameState:
    def __init__(self):
        self.turn = 0
        self.player_in_action: Optional[Player] = None
        self.player_order: Optional[List[Player]] = None
        self.card_deck: Optional[CardDeck] = None
        self.open_staple: Optional[OpenStaple] = None

    def init_game(self):
        pass

    def execute_turn(self):
        pass

    def evaluate_game(self):
        pass

