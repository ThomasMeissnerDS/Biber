from typing import Any, List, Optional

from base_classes import cards  # noqa: F403


class Player:
    def __init__(self, name: str = "player", decision_policy: str = "random"):
        self.name = name
        self.cards: List[Optional[cards.Card]] = []  # noqa: F403, F405
        self.cards_seen: List[bool] = [False, False, False, False]
        self.card_in_hand: Optional[cards.Card] = None  # noqa: F403, F405
        self.decision_policy: str = decision_policy
        self.decider: Any = None

    def calc_points_in_front(self) -> int:
        total_value: int = 0
        for idx, c in enumerate(self.cards):
            if isinstance(c, cards.Card):
                if self.cards_seen[idx] and c.card_type == "number":
                    total_value += c.value
            else:
                raise ValueError("Passed object is not of type Card.")

        return total_value

    def calc_final_points(self) -> int:
        total_value: int = 0
        for idx, c in enumerate(self.cards):
            if isinstance(c, cards.Card):
                if c.card_type == "number":
                    total_value += c.value
            else:
                raise ValueError("Passed object is not of type Card.")

        return total_value
