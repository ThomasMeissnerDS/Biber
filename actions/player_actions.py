from typing import Any, Tuple

from actions import game_actions
from base_classes.cards import Card
from base_classes.checkpoints import CheckPointDecisions
from base_classes.game_state import GameState
from base_classes.players import Player


def draw_card_from_deck(
    game_state: GameState, player: Player
) -> Tuple[GameState, Player]:
    drawn = game_state.card_deck.cards_in_deck[-1]
    game_state.card_deck.cards_in_deck = game_state.card_deck.cards_in_deck[:-1]
    player.card_in_hand = drawn
    return game_state, player


def draw_card_from_open_staple(
    game: GameState, player: Player
) -> Tuple[GameState, Player]:
    drawn = game.open_staple.cards_on_staple[-1]
    player.card_in_hand = drawn
    game.open_staple.cards_on_staple = game.open_staple.cards_on_staple[:-1]
    player.card_in_hand = drawn
    return game, player


def move_card_from_hand_to_open_staple(
    game_state: GameState, player: Player
) -> Tuple[GameState, Player]:
    game_state.open_staple.cards_on_staple.append(player.card_in_hand)
    player.card_in_hand = None
    return game_state, player


def pass_turn(game_state: GameState) -> GameState:
    game_state = game_actions.next_player_idx(game_state)
    return game_state


def knock_on_table(game: GameState) -> GameState:
    game.game_status = "finished"
    return game


def chose_action(
    game: GameState,
    player: Player,
    checkpoint_decisions: CheckPointDecisions,
    check_point: str = "None",
) -> Any:
    if check_point == "play_or_discard" and isinstance(player.card_in_hand, Card):
        play_options = checkpoint_decisions.check_point_decisions[check_point][
            player.card_in_hand.card_type
        ]
    else:
        play_options = checkpoint_decisions.check_point_decisions[check_point]

    if player.decision_policy == "random":
        decision = game.random_generator.choice(play_options)
    elif player.decision_policy == "epsilon-greedy":
        decision = player.decider.checkpoint_bandits[check_point].chose_action()
    else:
        raise ValueError("No compatible decision policy has been passed.")

    return decision
