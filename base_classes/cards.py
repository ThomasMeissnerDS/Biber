from typing import Literal


class Card:
    def __init__(self,
                 card_type: Literal["number", "double_turn", "trade", "reveal"],
                 position_within_type: int,
                 current_position_type: Literal["deck", "player"] = "deck",
                 value: int = None,):
        self.card_type = card_type
        self.current_position_type = current_position_type
        self.position_within_type = position_within_type
        self.value = value
