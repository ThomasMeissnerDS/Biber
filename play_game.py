from actions.card_actions import exchange_card
from actions.game_actions import prepare_game, make_turn
from actions.player_actions import (
    draw_card_from_deck, draw_card_from_open_staple, move_card_from_hand_to_open_staple
)
from base_classes.game_state import GameState
from typing import Dict, List


PLAY_OPTIONS_MAPPING: Dict[str, List[str]] = {
    "number": ["move_to_open_staple", "exchange_with_own_card"],
    "other": ["move_to_open_staple", "use_special_card"],
}


def play_game():
    game = GameState(random_seed=1, nb_players=4)
    game = prepare_game(game)
    while game.game_status != "finished":
        game = make_turn(game)
        for player in game.player_order:
            # decide to draw from deck or open staple
            draw_options = ["deck", "open_staple"]
            decision = game.random_generator.choice(draw_options)

            if decision == "deck":
                game, player = draw_card_from_deck(game, player)
            elif decision == "open_staple":
                game, player = draw_card_from_open_staple(game, player)

            del draw_options
            del decision

            # card moved to player and player can decide how to proceed

            play_options = PLAY_OPTIONS_MAPPING[player.card_in_hand.card_type]
            decision = game.random_generator.choice(play_options)

            if decision == "move_to_open_staple":
                game, player = move_card_from_hand_to_open_staple(game, player)
            elif decision == "use_special_card" and player.card_in_hand.card_type == "number":
                idx_decision = game.random_generator.choice([i for i in range(4)])
                player, game = exchange_card(player, idx_decision, game)
            elif decision == "use_special_card" and player.card_in_hand.card_type == "double_turn":
                pass
            elif decision == "use_special_card" and player.card_in_hand.card_type == "trade":
                pass
            elif decision == "use_special_card" and player.card_in_hand.card_type == "trade":
                pass


            del play_options
            del decision

