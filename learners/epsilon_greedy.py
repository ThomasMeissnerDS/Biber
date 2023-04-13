from typing import Dict, List

import numpy as np

from base_classes import checkpoints


class EpsilonGreedy:
    """
    Single epsilon greedy multiarmed bandit.

    A single instace will take care of a single checkpoint in the game and estimate after each action for that checkpoint
    by how much the game state evaluation has been changed.
    """

    def __init__(self, actions, random_seed):
        self.epsilon = 0.20
        self.actions: List[str] = actions
        self.actions_indices: List[int] = [i for i in range(len(actions))]
        self.nb_actions_triggered: List[int] = [0 for _i in actions]
        self.total_impact_state_estimation: List[float] = [0.0 for _i in actions]
        self.avg_impact_state_estimation: List[float] = [0.0 for _i in actions]
        self.random_seed: int = random_seed
        self.random_generator = np.random.default_rng(self.random_seed)

    def update_random_generator(self):
        self.random_seed += 1
        if self.epsilon > 0.05:
            self.epsilon -= 0.001
        self.random_generator = np.random.default_rng(self.random_seed)

    def _get_best_arm(self) -> int:
        arm_index = np.argmax(np.asarray(self.avg_impact_state_estimation), axis=0)
        return arm_index

    def _get_random_arm(self) -> int:
        arm_index = self.random_generator.choice(self.actions_indices, 1)
        return arm_index[0]

    def _select_pull_mechanism(self) -> int:
        if self.random_generator.random() > self.epsilon:
            arm_index = self._get_best_arm()
        else:
            arm_index = self._get_random_arm()

        return arm_index

    def chose_action(self):
        action_idx: int = self._select_pull_mechanism()
        self.update_random_generator()
        return self.actions[action_idx], action_idx

    def update_bandit(self, action_idx: int, game_state_impact):
        self.nb_actions_triggered[action_idx] += 1
        self.total_impact_state_estimation[action_idx] += (
            game_state_impact * -1
        )  # we want to minimize the points
        self.avg_impact_state_estimation[action_idx] = (
            self.total_impact_state_estimation[action_idx]
            / self.nb_actions_triggered[action_idx]
        )


class EpsilonGreedyPlayer:
    """
    Wrapper class representing a player.

    This player contains a separate multiarmed bandit for each individual checkpoint.
    """

    def __init__(self, checkpts: checkpoints.CheckPointDecisions, random_seed: int = 1):
        self.checkpoints: checkpoints.CheckPointDecisions = checkpts
        self.checkpoint_bandits: Dict[str, EpsilonGreedy] = {}
        for checkpoint, actions in self.checkpoints.check_point_decisions.items():
            self.checkpoint_bandits[checkpoint] = EpsilonGreedy(
                actions=actions, random_seed=random_seed
            )
