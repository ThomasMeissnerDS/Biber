from base_classes.cards import Card
from typing import List, Optional

class Player:
    def __init__(self,
                 name: str = "player"):
        self.name = name
        self.cards: List[Optional[Card]] = []
