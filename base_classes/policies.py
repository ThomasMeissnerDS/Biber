from typing import List


class Policy:
    def __init__(self):
        self.policy: List[str] = [
            "deck",
            "open_staple",
            "move_to_open_staple",
            "exchange_with_own_card",
            "use_special_card",
            0,
            1,
            2,
            3,
        ]
