from typing import Literal


class Card:
    def __init__(self,
                 card_type: Literal["number", "double_turn", "trade", "reveal"],
                 value: int = None,):
        self.card_type = card_type
        self.value = value
