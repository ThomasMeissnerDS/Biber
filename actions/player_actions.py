from base_classes.game_state import GameState
from base_classes.players import Player
from actions.game_actions import next_player_idx


def draw_card_from_deck(game_state: GameState, player: Player) -> (GameState, Player):
    drawn = game_state.open_staple.cards_on_staple[-1]
    game_state.open_staple.cards_on_staple = game_state.open_staple.cards_on_staple[:-1]
    player.card_in_hand = drawn
    return game_state, player


def draw_card_from_open_staple(game: GameState, player: Player) -> (GameState, Player):
    drawn = game.card_deck.cards_in_deck[-1]
    player.card_in_hand = drawn
    game.card_deck.cards_in_deck = game.card_deck.cards_in_deck[:-1]
    player.card_in_hand = drawn
    return game, player


def move_card_from_hand_to_open_staple(game_state: GameState, player: Player) -> (GameState, Player):
    game_state.open_staple.cards_on_staple.append(player.card_in_hand)
    player.card_in_hand = None
    return game_state, player


def pass_turn(game_state: GameState) -> GameState:
    game_state = next_player_idx(game_state)
    return game_state


def knock_on_table(game: GameState) -> GameState:
    game.game_status = "finished"
    return game