from typing import Dict, List, Literal, Tuple, Union

from actions import card_actions
from base_classes.cards import Card
from base_classes.game_state import GameState
from base_classes.players import Player


def create_game():
    new_game = GameState(random_seed=1, nb_players=4)
    return new_game


def calc_value_of_own_known_cards(
    player: Player,
) -> Tuple[Dict[int, int], Dict[str, int], List[str]]:
    num_cards_seen = {}
    for card in range(0, 10):
        num_cards_seen[card] = 0

    special_cards = [
        "double_turn",
        "trade",
        "reveal",
    ]
    special_cards_seen = {
        "double_turn": 0,
        "trade": 0,
        "reveal": 0,
    }

    # calculate value of known card in front of player
    for idx, seen in enumerate(player.cards_seen):
        if isinstance(player.cards[idx], Card):
            the_card: Card = player.cards[idx]  # type: ignore
            if seen and the_card.card_type == "number":
                num_cards_seen[the_card.value] += 1
            elif seen and the_card.card_type in special_cards:
                special_cards_seen[the_card.card_type] += 1

    return num_cards_seen, special_cards_seen, special_cards


def calc_value_of_seen_cards(
    player: Player, game_state: GameState
) -> Tuple[
    Dict[int, int], Dict[str, int], List[Literal["double_turn", "trade", "reveal"]]
]:
    num_cards_seen = {}
    for card in range(0, 10):
        num_cards_seen[card] = 0

    special_cards: List[Literal["double_turn", "trade", "reveal"]] = [
        "double_turn",
        "trade",
        "reveal",
    ]
    special_cards_seen = {
        "double_turn": 0,
        "trade": 0,
        "reveal": 0,
    }

    for pl in game_state.players:
        if pl != player:  # type: ignore
            for the_card in pl.cards:  # type: ignore
                if (
                    the_card.card_type == "number"  # type: ignore
                    and player in the_card.seen_already_by  # type: ignore
                ):
                    num_cards_seen[the_card.value] += 1  # type: ignore
                elif (
                    the_card.card_type in special_cards  # type: ignore
                    and player in the_card.seen_already_by  # type: ignore
                ):
                    special_cards_seen[the_card.card_type] += 1  # type: ignore

    return num_cards_seen, special_cards_seen, special_cards


def get_state_from_player_perspective(
    player: Player, game_state: GameState
) -> Tuple[List[str], List[int]]:
    (
        own_cards_seen,
        own_special_cards_seen,
        special_cards_labels,
    ) = calc_value_of_own_known_cards(player)
    (
        num_cards_seen,
        special_cards_seen,
        other_special_cards_labels,
    ) = calc_value_of_seen_cards(player, game_state)

    game_state_labels = []
    game_state_values = []

    for key in range(0, 10):
        game_state_labels.append("own_seen_" + str(key))
        game_state_values.append(own_cards_seen[key])

    for ckey in special_cards_labels:
        game_state_labels.append("own_seen_special" + str(ckey))
        game_state_values.append(own_special_cards_seen[ckey])

    for key in range(0, 10):
        game_state_labels.append("others_seen_" + str(key))
        game_state_values.append(num_cards_seen[key])

    for okey in other_special_cards_labels:
        game_state_labels.append("other_seen_special" + str(okey))
        game_state_values.append(special_cards_seen[okey])

    # add info about which turn we have
    game_state_labels.append("turn")
    game_state_values.append(game_state.turn)

    return game_state_labels, game_state_values


def next_player_idx(game_state: GameState) -> GameState:
    if game_state.player_in_action_idx + 1 > (game_state.nb_players - 1):
        game_state.player_in_action_idx = 0
    else:
        game_state.player_in_action_idx += 1
    return game_state


def move_card_from_deck_to_player(
    game_state: GameState, player: Player, idx: int
) -> GameState:
    sel_card: Card = game_state.card_deck.cards_in_deck[-1]  # type: ignore  # take top card
    game_state.card_deck.cards_in_deck = game_state.card_deck.cards_in_deck[:-1]
    player.cards.append(sel_card)
    game_state.players[idx] = player
    return game_state


def move_top_card_from_deck_to_staple(game_state: GameState) -> GameState:
    card = game_state.card_deck.cards_in_deck[-1]  # take top card
    game_state.card_deck.cards_in_deck = game_state.card_deck.cards_in_deck[:-1]

    for player in game_state.players:
        card = card_actions.add_card_to_seen(player, card)  # type: ignore

    game_state.open_staple.cards_on_staple.append(card)
    return game_state


def fill_player_hands(game_state: GameState) -> GameState:
    # every player gets 4 cards
    for i in range(4):
        for idx in range(game_state.nb_players):
            player = game_state.players[idx]
            if isinstance(player, Player):
                game_state = move_card_from_deck_to_player(game_state, player, idx)
            else:
                raise ValueError("Type of objects passed must be of GameState.")
    return game_state


def players_see_outer_cards(game_state: GameState) -> GameState:
    for idx in range(game_state.nb_players):
        player = game_state.players[idx]
        if isinstance(player, Player):
            # see outer cards
            player.cards_seen[0] = True
            player.cards_seen[-1] = True
            player.cards[0] = card_actions.add_card_to_seen(  # type: ignore
                player, player.cards[0]  # type: ignore
            )
            player.cards[-1] = card_actions.add_card_to_seen(  # type: ignore
                player, player.cards[-1]  # type: ignore
            )
        else:
            raise ValueError("Type of objects passed must be of Player.")

        game_state.players[idx] = player
    return game_state


def set_player_order(game: GameState) -> GameState:
    ordered = game.random_generator.choice(
        game.players, game.nb_players, replace=False
    ).tolist()
    game.player_order = ordered
    game.players = ordered  # noqa
    return game


def prepare_game(game: GameState) -> GameState:
    game.fill_deck()
    game.create_players()
    game = set_player_order(game)
    game = fill_player_hands(game)
    game = players_see_outer_cards(game)
    game = move_top_card_from_deck_to_staple(game)
    return game


def make_turn(game_state: GameState) -> GameState:
    game_state.turn += 1
    if game_state.turn > game_state.max_turns:
        game_state.game_status = "finished"

    return game_state
