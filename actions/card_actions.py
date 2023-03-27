from base_classes.cards import Card
from base_classes.game_state import GameState
from base_classes.players import Player


def reveal_card(player: Player, card: Card, hand_idx) -> (Player, Card):
    player.cards_seen[hand_idx] = True

    if player not in card.seen_already_by:
        card.seen_already_by.append(player)

    return player, card


def exchange_card(player: Player, hand_idx, game_state: GameState) -> (Player, GameState):
    old_card: Card = player.cards[hand_idx]
    game_state.open_staple.cards_on_staple.append(old_card)
    player.cards[hand_idx] = player.card_in_hand
    player.card_in_hand = None
    return player, game_state
