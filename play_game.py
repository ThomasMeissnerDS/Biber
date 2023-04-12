from typing import Dict, List

from actions.card_actions import exchange_card, reveal_card, trade_card
from actions.game_actions import (
    get_state_from_player_perspective,
    make_turn,
    prepare_game,
)
from actions.player_actions import (
    chose_action,
    draw_card_from_deck,
    draw_card_from_open_staple,
    move_card_from_hand_to_open_staple,
)
from base_classes.checkpoints import CheckPointDecisions
from base_classes.game_state import GameState
from general_utils import config_loader
from learners.learner_utils import save_model


def play_game():
    print("Start a new game")
    checkpoint_decisions = CheckPointDecisions()
    game_config = config_loader.load_conf_file("game_settings.yaml")

    game = GameState(
        random_seed=7,
        nb_players=4,
        player_configs=game_config["player_settings"]["save_states"],
    )
    game = prepare_game(game)
    while game.game_status != "finished":
        game = make_turn(game)
        for idx, player in enumerate(game.player_order):
            print("---------------------------")
            print([(c.card_type, c.value) for c in player.cards])
            # decide to draw from deck or open staple -> checkpoint: "draw_card"
            game_state_labels, game_state_values = get_state_from_player_perspective(
                player, game
            )
            decision = chose_action(game, player, checkpoint_decisions, "draw_card")
            allowed_draws = 1

            if decision == "deck":
                game, player = draw_card_from_deck(game, player)
                if player.card_in_hand.card_type == "double_turn":
                    game, player = draw_card_from_deck(game, player)
            elif decision == "open_staple":
                game, player = draw_card_from_open_staple(game, player)

            del decision
            del game_state_labels
            del game_state_values

            # card moved to player and player can decide how to proceed

            while allowed_draws >= 1:
                decision = chose_action(
                    game, player, checkpoint_decisions, "play_or_discard"
                )

                if decision == "move_to_open_staple":
                    game, player = move_card_from_hand_to_open_staple(game, player)
                    allowed_draws -= 1
                elif (
                    decision == "exchange_with_own_card"
                    and player.card_in_hand.card_type == "number"
                ):
                    idx_decision = chose_action(
                        game,
                        player,
                        checkpoint_decisions,
                        "exchange_with_own_card.number.idx_decision",
                    )
                    player, game = exchange_card(player, idx_decision, game)
                    del idx_decision
                    allowed_draws -= 2
                elif (
                    decision == "use_special_card"
                    and player.card_in_hand.card_type == "trade"
                ):
                    idx_decision = chose_action(
                        game,
                        player,
                        checkpoint_decisions,
                        "use_special_card.trade.idx_decision",
                    )
                    target_idx_decision = chose_action(
                        game,
                        player,
                        checkpoint_decisions,
                        "use_special_card.trade.target_idx_decision",
                    )

                    checkpoint_decisions.check_point_decisions[
                        "use_special_card.trade.opponent_decision"
                    ] = [p for p in game.players if p != player]
                    opponent_decision = chose_action(
                        game,
                        player,
                        checkpoint_decisions,
                        "use_special_card.trade.opponent_decision",
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
                    allowed_draws -= 2
                elif (
                    decision == "use_special_card"
                    and player.card_in_hand.card_type == "double_turn"
                ):
                    game, player = draw_card_from_deck(game, player)
                    game, player = move_card_from_hand_to_open_staple(game, player)
                elif (
                    decision == "use_special_card"
                    and player.card_in_hand.card_type == "reveal"
                ):
                    idx_decision = chose_action(
                        game,
                        player,
                        checkpoint_decisions,
                        "use_special_card.reveal.idx_decision",
                    )
                    player, game = reveal_card(player, game, idx_decision)
                    del idx_decision
                    allowed_draws -= 2

                del decision

            if game.player_configs[idx] == "None":
                pass
            else:
                save_model(game.player_configs[idx], player)

    # evaluation phase: exchange remaining non-numeric cards by random cards from staple until all are numerics
    print("Exchange remaining special cards with numeric cards.")
    for idx, player in enumerate(game.player_order):
        for card_idx, card in enumerate(player.cards):
            while card.card_type != "number":
                game, player = draw_card_from_deck(game, player)
                if player.card_in_hand.card_type == "number":
                    player, game = exchange_card(player, card_idx, game)
                    card = player.cards[card_idx]
                else:
                    game, player = move_card_from_hand_to_open_staple(game, player)

    # counting all players' points
    results = {}
    lowest_pts = 99
    best_player = []
    for player in game.player_order:
        pts = player.calc_final_points()
        results[player.name] = pts
        if pts < lowest_pts:
            lowest_pts = pts
            best_player = [player.name]
        elif pts == lowest_pts:
            best_player.append(player.name)
        print(f"Player {player.name} achieved {pts} points.")

    if len(best_player) == 1:
        print(
            f"Congratulations! Player {best_player[0]} has won with {lowest_pts} points after {game.turn - 1} turns."
        )
    else:
        print(
            f"Congratulations! The following players have won with {lowest_pts} points after {game.turn - 1} turns:"
        )
        for player in best_player:
            print(f"{player}")


if __name__ == "__main__":
    play_game()
