import pytest

from actions import game_actions
from tests.general_fixtures import game


def test_prepare_game(game):
    game = game_actions.prepare_game(game)
    for player in game.players:
        assert len(player.cards) == 4


def test_fll_deck(game):
    game.fill_deck()
    assert len(game.card_deck.cards_in_deck) == 66


def test_next_player_idx(game):
    game = game_actions.prepare_game(game)
    assert game.player_in_action_idx == 0
    game = game_actions.next_player_idx(game)
    assert game.player_in_action_idx == 1
    game = game_actions.next_player_idx(game)
    assert game.player_in_action_idx == 2
    game = game_actions.next_player_idx(game)
    assert game.player_in_action_idx == 3
    game = game_actions.next_player_idx(game)
    assert (
        game.player_in_action_idx == 0
    )  # if not 0 then list index is exhausted and the game crashes
