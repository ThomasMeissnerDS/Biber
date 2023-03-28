from actions.player_actions import move_card_from_hand_to_open_staple
from base_classes.cards import Card
from base_classes.game_state import GameState
from base_classes.players import Player


def reveal_card(player: Player, game: GameState, hand_idx) -> (Player, GameState):
    player.cards_seen[hand_idx] = True

    if player not in player.cards[hand_idx].seen_already_by:
        player.cards[hand_idx].seen_already_by.append(player)

    game, player = move_card_from_hand_to_open_staple(game, player)

    return player, game


def exchange_card(player: Player, hand_idx, game_state: GameState) -> (Player, GameState):
    old_card: Card = player.cards[hand_idx]
    game_state.open_staple.cards_on_staple.append(old_card)
    player.cards[hand_idx] = player.card_in_hand
    game_state, player = move_card_from_hand_to_open_staple(game_state, player)
    return player, game_state


def trade_card(player: Player, hand_idx, target_player: Player, target_idx):
    pass
