from base_classes.cards import Card
from base_classes.game_state import GameState
from base_classes.players import Player


def create_game():
    new_game = GameState(random_seed=1, nb_players=4)
    return new_game


def next_player_idx(game_state: GameState) -> GameState:
    if game_state.player_in_action_idx + 1 > (game_state.nb_players - 1):
        game_state.player_in_action_idx = 0
    else:
        game_state.player_in_action_idx += 1
    return game_state


def move_card_from_deck_to_player(game_state: GameState, player: Player):
    sel_card = game_state.card_deck.cards_in_deck[-1]   # take top card
    game_state.card_deck.cards_in_deck = game_state.card_deck.cards_in_deck[:-1]
    player.cards.append(sel_card)
    return game_state


def fill_player_hands(game_state: GameState):
    # every player gets 4 cards
    for i in range(4):
        for idx in range(game_state.nb_players):
            game_state = move_card_from_deck_to_player(game_state, game_state.players[idx])

    return game_state


def prepare_game(game: GameState):
    game.fill_deck()
    game.create_players()
    game = fill_player_hands(game)
    return game


def make_turn(game_state: GameState):
    game_state.turn += 1
    if game_state.turn > game_state.max_turns:
        game_state.game_status = "finished"

    return game_state


