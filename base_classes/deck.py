from base_classes.cards import Card
from typing import List, Optional


class CardDeck:
    def __init__(self):
        self.cards_in_deck: List[Optional[Card]] = []


class OpenStaple:
    def __init__(self):
        self.cards_on_staple: List[Optional[Card]] = []
