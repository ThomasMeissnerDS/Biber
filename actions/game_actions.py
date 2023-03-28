from actions.card_actions import add_card_to_seen

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


def move_card_from_deck_to_player(game_state: GameState, player: Player) -> GameState:
    sel_card = game_state.card_deck.cards_in_deck[-1]  # take top card
    game_state.card_deck.cards_in_deck = game_state.card_deck.cards_in_deck[:-1]
    player.cards.append(sel_card)
    return game_state


def move_top_card_from_deck_to_staple(game_state: GameState) -> GameState:
    card = game_state.card_deck.cards_in_deck[-1]  # take top card
    game_state.card_deck.cards_in_deck = game_state.card_deck.cards_in_deck[:-1]

    game_state.open_staple.cards_on_staple.append(card)
    for player in game_state.players:
        player, card = add_card_to_seen(player, card)
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
    game.player_order = game.random_generator.choice(game.players, 4).tolist()
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
