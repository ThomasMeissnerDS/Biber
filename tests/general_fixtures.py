import pytest

from base_classes.game_state import GameState


@pytest.fixture
def game():
    new_game = GameState(random_seed=1, nb_players=4)
    return new_game
