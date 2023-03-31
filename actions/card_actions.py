from typing import Tuple

from actions.player_actions import move_card_from_hand_to_open_staple
from base_classes.cards import Card
from base_classes.game_state import GameState
from base_classes.players import Player


def add_card_to_seen(player: Player, card: Card) -> Card:
    if player not in card.seen_already_by:
        if isinstance(player, Player):
            card.seen_already_by.append(player)  # TODO: Add player name instead
        else:
            raise ValueError("Expected object to be of type Player.")

    return card


def reveal_card(player: Player, game: GameState, hand_idx) -> Tuple[Player, GameState]:
    player.cards_seen[hand_idx] = True
    player.cards[hand_idx] = add_card_to_seen(player, player.cards[hand_idx])
    game, player = move_card_from_hand_to_open_staple(game, player)
    return player, game


def exchange_card(
    player: Player, hand_idx, game_state: GameState
) -> Tuple[Player, GameState]:
    player.cards[hand_idx], player.card_in_hand = (
        player.card_in_hand,
        player.cards[hand_idx],
    )
    game_state, player = move_card_from_hand_to_open_staple(game_state, player)
    # everyone has seen that card now
    for pl in game_state.players:
        if pl not in game_state.open_staple.cards_on_staple[-1].seen_already_by:  # type: ignore
            game_state.open_staple.cards_on_staple[-1] = add_card_to_seen(
                pl, game_state.open_staple.cards_on_staple[-1]  # type: ignore
            )
    player.cards[hand_idx] = add_card_to_seen(player, player.cards[hand_idx])
    return player, game_state


def trade_card(
    player: Player, hand_idx, target_player: Player, target_idx, game_state: GameState
) -> Tuple[Player, Player, GameState]:
    player.cards[hand_idx], target_player.cards[target_idx] = (
        target_player.cards[target_idx],
        player.cards[hand_idx],
    )
    game_state, player = move_card_from_hand_to_open_staple(game_state, player)

    # update if players have seen the cards
    if player in player.cards[hand_idx].seen_already_by:
        player.cards_seen[hand_idx] = True
    else:
        player.cards_seen[hand_idx] = False

    if target_player in target_player.cards[target_idx].seen_already_by:
        target_player.cards_seen[target_idx] = True
    else:
        target_player.cards_seen[target_idx] = False
    return player, target_player, game_state
