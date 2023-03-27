from base_classes.players import Player
from typing import Literal, Optional, List


class Card:
    def __init__(self,
                 card_type: Literal["number", "double_turn", "trade", "reveal"],
                 value: int = None,):
        self.card_type = card_type
        self.value = value
        self.seen_already_by: List[Optional[Player]] = []
