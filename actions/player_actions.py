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


def own_seen_cards_to_val(player: Player) -> int:
    num_cards_seen, special_cards_seen, special_cards = game_actions.calc_value_of_own_known_cards(player)
    total_value = 0
    total_seen = 0
    for card, value in num_cards_seen.items():
        if value > 0:
            total_value += card * value
            total_seen += 1
    for card, value in special_cards_seen.items():
        if value > 0:
            total_value += 5  # just assigning a plain expected value
            total_seen += 1
    not_seen = 4 - total_seen
    total_value += not_seen * 5
    return total_value


def chose_action(
    game: GameState,
    player: Player,
    checkpoint_decisions: CheckPointDecisions,
    check_point: str = "None",
) -> Any:
    play_options = checkpoint_decisions.check_point_decisions[check_point]

    if player.decision_policy == "random":
        decision = game.random_generator.choice(play_options)
        action_idx = None
    elif player.decision_policy == "epsilon-greedy":
        if check_point == "use_special_card.trade.opponent_decision":
            player.decider.checkpoint_bandits[check_point].actions = [p for p in game.players if p != player]
        decision, action_idx = player.decider.checkpoint_bandits[check_point].chose_action()
    else:
        raise ValueError("No compatible decision policy has been passed.")

    return decision, action_idx


def update_policy(game: GameState, player: Player, check_point: str, action_idx: Any) -> Tuple[GameState, Player]:
    if player.decision_policy == "random":
        pass
    elif player.decision_policy == "epsilon-greedy":
        own_cards_est_val = own_seen_cards_to_val(player)
        player.decider.checkpoint_bandits[check_point].update_bandit(action_idx, own_cards_est_val)
    else:
        raise ValueError("No compatible decision policy has been passed.")

    return game, player
