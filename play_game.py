from typing import Dict, List

from actions.card_actions import exchange_card, reveal_card, trade_card
from actions.game_actions import make_turn, prepare_game
from actions.player_actions import (
    draw_card_from_deck,
    draw_card_from_open_staple,
    move_card_from_hand_to_open_staple,
)
from base_classes.game_state import GameState

PLAY_OPTIONS_MAPPING: Dict[str, List[str]] = {
    "number": ["move_to_open_staple", "exchange_with_own_card"],
    "trade": ["move_to_open_staple", "use_special_card"],
    "reveal": ["move_to_open_staple", "use_special_card"],
    "double_turn": ["move_to_open_staple", "use_special_card"],
}


def play_game():
    game = GameState(random_seed=2, nb_players=4)
    game = prepare_game(game)
    while game.game_status != "finished":
        game = make_turn(game)
        for idx, player in enumerate(game.player_order):
            # decide to draw from deck or open staple
            draw_options = ["deck", "open_staple"]
            decision = game.random_generator.choice(draw_options)
            allowed_draws = 1

            if decision == "deck":
                game, player = draw_card_from_deck(game, player)
                if player.card_in_hand.card_type == "double_turn":
                    game, player = draw_card_from_deck(game, player)
                    allowed_draws += 1
            elif decision == "open_staple":
                game, player = draw_card_from_open_staple(game, player)

            del draw_options
            del decision

            # card moved to player and player can decide how to proceed

            play_options = PLAY_OPTIONS_MAPPING[player.card_in_hand.card_type]

            for draw in range(allowed_draws):
                decision = game.random_generator.choice(play_options)
                if decision == "move_to_open_staple":
                    game, player = move_card_from_hand_to_open_staple(game, player)
                elif (
                    decision == "exchange_with_own_card"
                    and player.card_in_hand.card_type == "number"
                ):
                    idx_decision = game.random_generator.choice([i for i in range(4)])
                    player, game = exchange_card(player, idx_decision, game)
                    del idx_decision
                    break
                elif (
                    decision == "use_special_card"
                    and player.card_in_hand.card_type == "trade"
                ):
                    idx_decision = game.random_generator.choice([i for i in range(4)])
                    target_idx_decision = game.random_generator.choice(
                        [i for i in range(4)]
                    )
                    opponent_decision = game.random_generator.choice(
                        [p for p in game.players if p.name != player.name]
                    )
                    player, target_player, game_state = trade_card(
                        player,
                        idx_decision,
                        opponent_decision,
                        target_idx_decision,
                        game,
                    )

                    del idx_decision
                    del target_idx_decision
                    del opponent_decision
                    break
                elif (
                    decision == "use_special_card"
                    and player.card_in_hand.card_type == "double_turn"
                ):
                    allowed_draws += 1
                    game, player = draw_card_from_deck(game, player)
                    game, player = move_card_from_hand_to_open_staple(game, player)
                elif (
                    decision == "use_special_card"
                    and player.card_in_hand.card_type == "reveal"
                ):
                    idx_decision = game.random_generator.choice([i for i in range(4)])
                    player, game = reveal_card(player, game, idx_decision)
                    del idx_decision
                    break

                del decision

            game.player_order[idx] = player

    # evaluation phase: exchange remaining non-numeric cards by random cards from staple until all are numerics
    print("Exchange remaining special cards with numeric cards.")
    for idx, player in enumerate(game.player_order):
        for card_idx, card in enumerate(player.cards):
            while card.card_type != "number":
                print()
                game, player = draw_card_from_deck(game, player)
                if player.card_in_hand == "number":
                    player, game = exchange_card(player, idx, game)
                    card = player.cards[card_idx]
                else:
                    game, player = move_card_from_hand_to_open_staple(game, player)

    # counting all players' points
    results = {}
    lowest_pts = 99
    best_player = ""
    for player in game.player_order:
        pts = player.calc_points_in_front()
        results[player.name] = pts
        if pts < lowest_pts:
            lowest_pts = pts
            best_player = player.name
        print(f"Player {player.name} achieved {pts} points.")

    print(f"Congratulations! Player {best_player} has won with {lowest_pts} points after {game.turn} turns.")


if __name__ == "__main__":
    play_game()

