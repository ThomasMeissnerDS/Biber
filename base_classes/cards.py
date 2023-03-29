from typing import Callable, List, Literal, Optional

from base_classes import players  # noqa: F403


class Card:
    def __init__(
        self,
        card_type: Literal["number", "double_turn", "trade", "reveal"],
        value: int = 0,
    ):
        self.card_type = card_type
        self.value = value
        self.seen_already_by: List[Optional[players.Player]] = []  # noqa: F403, F405
