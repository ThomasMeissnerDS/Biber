import random
from typing import List, Literal, Optional

import numpy as np

from base_classes.cards import Card
from base_classes.checkpoints import CheckPointDecisions
from base_classes.deck import CardDeck, OpenStaple
from base_classes.players import Player
from learners.epsilon_greedy import EpsilonGreedyPlayer
from learners.learner_utils import load_model


class GameState:
    def __init__(
        self,
        random_seed: int,
        nb_players: int,
        max_turns: int = 10,
        player_configs: Optional[List[str]] = None,
        player_decision_logic: Optional[List[str]] = None,
    ):
        self.turn = 0
        self.max_turns = max_turns
        self.nb_players: int = nb_players
        self.players: List[Optional[Player]] = []
        self.player_in_action_idx: int = 0
        self.player_order: Optional[List[Player]] = None

        if not isinstance(player_configs, list):
            self.player_configs: List[str] = ["None" for _p in range(self.nb_players)]
        else:
            self.player_configs = player_configs

        if not isinstance(player_decision_logic, list):
            self.player_decision_logic: List[str] = [
                "random" for _p in range(self.nb_players)
            ]
        else:
            self.player_decision_logic = player_decision_logic

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

        self.card_deck.cards_in_deck = self.random_generator.choice(
            self.card_deck.cards_in_deck,
            len(self.card_deck.cards_in_deck),
            replace=False,
        ).tolist()

    def create_players(self):
        check_pts = CheckPointDecisions()

        for player_nb, conf in enumerate(self.player_configs):
            player = Player(
                name=f"player_{player_nb}",
                decision_policy=self.player_decision_logic[player_nb],
            )
            if self.player_configs[player_nb] == "None" or self.player_configs[player_nb] is None:
                if player.decision_policy == "random":
                    pass
                elif player.decision_policy == "epsilon-greedy":
                    player.decider = EpsilonGreedyPlayer(
                        checkpts=check_pts, random_seed=self.random_seed
                    )
                self.players.append(player)
            else:
                print(self.player_configs)
                try:
                    loaded_player = load_model(conf)
                    loaded_player.name = f"player_{player_nb}"
                    self.players.append(loaded_player)
                    del loaded_player
                except FileNotFoundError:
                    print(f"No config has been found. Creating player {player_nb} from scratch.")
                    if player.decision_policy == "epsilon-greedy":
                        player.decider = EpsilonGreedyPlayer(
                            checkpts=check_pts, random_seed=self.random_seed
                        )
                    self.players.append(player)
