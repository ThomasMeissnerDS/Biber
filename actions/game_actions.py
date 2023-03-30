from typing import Dict, List, Literal, Tuple

from actions import card_actions
from base_classes.cards import Card
from base_classes.game_state import GameState
from base_classes.players import Player


def create_game():
    new_game = GameState(random_seed=1, nb_players=4)
    return new_game


def calc_value_of_own_known_cards(
    player: Player,
) -> Tuple[Dict[int, int], Dict[str, int]]:
    num_cards_seen = {}
    for card in range(1, 9):
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

    return num_cards_seen, special_cards_seen


def calc_value_of_seen_cards(
    player: Player, game_state: GameState
) -> Tuple[Dict[int, int], Dict[str, int]]:
    num_cards_seen = {}
    for card in range(1, 9):
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
        if pl.name != player.name:  # type: ignore
            for the_card in pl.cards:  # type: ignore
                if the_card.card_type == "number" and pl.name in [  # type: ignore
                    pl.name for pl in the_card.seen_already_by  # type: ignore
                ]:
                    num_cards_seen[the_card.value] += 1  # type: ignore
                elif the_card.card_type in special_cards and pl.name in [  # type: ignore
                    pl.name for pl in the_card.seen_already_by  # type: ignore
                ]:
                    special_cards_seen[the_card.card_type] += 1  # type: ignore

    return num_cards_seen, special_cards_seen


def get_state_from_player_perspective(player: Player, game_state: GameState):
    num_cards_seen, special_cards_seen = calc_value_of_own_known_cards(player)
    num_cards_seen, special_cards_seen = calc_value_of_seen_cards(player, game_state)
    pass  # TODO: Add values from open staple and other players already seen cards


def next_player_idx(game_state: GameState) -> GameState:
    if game_state.player_in_action_idx + 1 > (game_state.nb_players - 1):
        game_state.player_in_action_idx = 0
    else:
        game_state.player_in_action_idx += 1
    return game_state


def move_card_from_deck_to_player(game_state: GameState, player: Player) -> GameState:
    sel_card = game_state.card_deck.cards_in_deck[-1]  # take top card
    game_state.card_deck.cards_in_deck = game_state.card_deck.cards_in_deck[:-1]
    player.cards.append(sel_card)
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
                game_state = move_card_from_deck_to_player(game_state, player)
            else:
                raise ValueError("Type of objects passed must be of GameState.")

    return game_state


def set_player_order(game: GameState) -> GameState:
    game.player_order = game.random_generator.choice(
        game.players, game.nb_players, replace=False
    ).tolist()
    return game


def prepare_game(game: GameState) -> GameState:
    game.fill_deck()
    game.create_players()
    game = set_player_order(game)
    game = fill_player_hands(game)
    game = move_top_card_from_deck_to_staple(game)
    return game


def make_turn(game_state: GameState) -> GameState:
    game_state.turn += 1
    if game_state.turn > game_state.max_turns:
        game_state.game_status = "finished"

    return game_state
