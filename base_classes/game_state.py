import random
from typing import List, Literal, Optional

import numpy as np

from base_classes.cards import Card
from base_classes.deck import CardDeck, OpenStaple
from base_classes.players import Player


class GameState:
    def __init__(self, random_seed: int, nb_players: int, max_turns: int = 10):
        self.turn = 0
        self.max_turns = max_turns
        self.nb_players: int = nb_players
        self.players: List[Optional[Player]] = []
        self.player_in_action_idx: int = 0
        self.player_order: Optional[List[Player]] = None
        self.card_deck: CardDeck = CardDeck()
        self.open_staple: OpenStaple = OpenStaple()
        self.random_seed: int = random_seed
        self.random_generator = np.random.default_rng(self.random_seed)
        self.game_status: Literal["ongoing", "finished"] = "ongoing"

    def fill_deck(self):
        # fill number cards into deck
        [
            self.card_deck.cards_in_deck.append(Card(card_type="number", value=val))
            for val in range(9)
            for _i in range(4)
        ]
        [
            self.card_deck.cards_in_deck.append(Card(card_type="number", value=9))
            for _i in range(9)
        ]
        # fill in special cards
        [
            self.card_deck.cards_in_deck.append(Card(card_type="double_turn", value=0))
            for _i in range(5)
        ]
        [
            self.card_deck.cards_in_deck.append(Card(card_type="trade", value=0))
            for _i in range(9)
        ]
        [
            self.card_deck.cards_in_deck.append(Card(card_type="reveal", value=0))
            for _i in range(7)
        ]

        self.card_deck.cards_in_deck = self.random_generator.choice(self.card_deck.cards_in_deck, len(self.card_deck.cards_in_deck), replace=False).tolist()

    def create_players(self):
        [
            self.players.append(Player(name=f"player_{player}"))
            for player in range(self.nb_players)
        ]

    def evaluate_game(self):
        pass
