import play_game


def run_simulation():
    # total_results = {}
    total_infos = {}
    total_simulations = 40000
    for i in range(total_simulations):
        results, additional_infos = play_game.play_game(random_seed=i, nb_players=4)
        if i == 0:
            # total_results = results
            total_infos = additional_infos
        else:
            for decision_policy, pts in additional_infos.items():
                total_infos[decision_policy] += pts

        print(
            f"epsilon-greedy achieved an avg of {total_infos['epsilon-greedy'] / (i+1)}"
        )
        print(f"random achieved an avg of {total_infos['random'] / 3 / (i + 1)}")

    print("Final standings are.....")
    print(
        f"epsilon-greedy achieved an avg of {total_infos['epsilon-greedy'] / total_simulations}"
    )
    print(f"random achieved an avg of {total_infos['random'] / 3 / total_simulations}")


if __name__ == "__main__":
    run_simulation()
