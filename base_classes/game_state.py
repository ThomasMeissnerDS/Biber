from base_classes.players import Player
from base_classes.cards import Card
from base_classes.deck import CardDeck, OpenStaple
import numpy as np
from typing import List, Optional


class GameState:
    def __init__(self, random_seed: int, nb_players: int):
        self.turn = 0
        self.nb_players: int = nb_players
        self.players: List[Optional[Player]] = []
        self.player_in_action: Optional[Player] = None
        self.player_order: Optional[List[Player]] = None
        self.card_deck: CardDeck = CardDeck()
        self.open_staple: Optional[OpenStaple] = None
        self.random_seed: int = random_seed
        self.random_generator = np.random.default_rng(self.random_seed)

    def fill_deck(self):
        poss_in_deck = [pos for pos in range(45)]

        # fill number cards into deck
        [self.card_deck.cards_in_deck.append(Card(card_type="number", position_within_type=self.random_generator.choice(poss_in_deck, 1, replace=False), value=val)) for val in range(9) for _i in range(4)]
        [self.card_deck.cards_in_deck.append(Card(card_type="number", position_within_type=self.random_generator.choice(poss_in_deck, 1, replace=False), value=9)) for _i in range(9)]
        # fill in special cards
        [self.card_deck.cards_in_deck.append(Card(card_type="double_turn", position_within_type=self.random_generator.choice(poss_in_deck, 1, replace=False), value=0)) for _i in range(5)]
        [self.card_deck.cards_in_deck.append(Card(card_type="trade", position_within_type=self.random_generator.choice(poss_in_deck, 1, replace=False), value=0)) for _i in range(9)]
        [self.card_deck.cards_in_deck.append(Card(card_type="reveal", position_within_type=self.random_generator.choice(poss_in_deck, 1, replace=False), value=0)) for _i in range(7)]

    def create_players(self):
        [self.players.append(Player(name=f"player_{player}")) for player in range(self.nb_players)]

    def execute_turn(self):
        pass

    def evaluate_game(self):
        pass
