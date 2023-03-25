from actions.game_actions import prepare_game
import pytest
from tests.general_fixtures import game


def test_prepare_game(game):
    game = prepare_game(game)
    for player in game.players:
        assert len(player.cards) == 4
