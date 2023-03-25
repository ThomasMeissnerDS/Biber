from base_classes.cards import Card
from base_classes.game_state import GameState
from base_classes.players import Player


def create_game():
    new_game = GameState(random_seed=1, nb_players=4)
    return new_game


def move_card_from_deck_to_player(game_state: GameState, player: Player):
    sel_card = game_state.card_deck.cards_in_deck[-1]   # take top card
    game_state.card_deck.cards_in_deck = game_state.card_deck.cards_in_deck[:-1]
    player.cards.append(sel_card)
    player.cards[-1].current_position_type = "player"
    player.cards[-1].position_within_type = len(player.cards) - 1


def fill_player_hands(game: GameState):
    # every player gets 4 cards
    for i in range(4):
        for idx in range(game.nb_players):
            move_card_from_deck_to_player(game, game.players[idx])

    return game


def prepare_game(game: GameState):
    game.fill_deck()
    game.create_players()
    game = fill_player_hands(game)
    return game


