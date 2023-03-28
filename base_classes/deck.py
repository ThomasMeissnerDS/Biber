from typing import List, Optional

from base_classes.cards import Card


class CardDeck:
    def __init__(self):
        self.cards_in_deck: List[Optional[Card]] = []


class OpenStaple:
    def __init__(self):
        self.cards_on_staple: List[Optional[Card]] = []
