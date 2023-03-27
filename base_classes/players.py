from base_classes.cards import Card
from typing import List, Optional


class Player:
    def __init__(self,
                 name: str = "player"):
        self.name = name
        self.cards: List[Optional[Card]] = []
        self.cards_seen: List[bool] = [False, False, False, False]
        self.card_in_hand: Optional[Card] = None

    def calc_points_in_front(self) -> int:
        total_value: int = 0
        for idx, c in enumerate(self.cards):
            if self.cards_seen[idx] and c.card_type == "number":
                total_value += c.value

        return total_value
