from actions.game_actions import prepare_game, next_player_idx
import pytest
from tests.general_fixtures import game


def test_prepare_game(game):
    game = prepare_game(game)
    for player in game.players:
        assert len(player.cards) == 4


def test_next_player_idx(game):
    game = prepare_game(game)
    assert game.player_in_action_idx == 0
    game = next_player_idx(game)
    assert game.player_in_action_idx == 1
    game = next_player_idx(game)
    assert game.player_in_action_idx == 2
    game = next_player_idx(game)
    assert game.player_in_action_idx == 3
    game = next_player_idx(game)
    assert game.player_in_action_idx == 0  # if not 0 then list index is exhausted and the game crashes
