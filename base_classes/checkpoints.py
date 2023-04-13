class CheckPointDecisions:
    def __init__(self):
        self.check_point_decisions = {
            "draw_card": ["deck", "open_staple"],
            "play_or_discard.number": [
                "move_to_open_staple",
                "exchange_with_own_card",
            ],
            "play_or_discard.special_card": [
                "move_to_open_staple",
                "use_special_card",
            ],
            "exchange_with_own_card.number.idx_decision": [0, 1, 2, 3],
            "use_special_card.trade.idx_decision": [0, 1, 2, 3],
            "use_special_card.trade.target_idx_decision": [0, 1, 2, 3],
            "use_special_card.trade.opponent_decision": [0, 1, 2],  # cannot choose yourself, so nb players -1
            "use_special_card.reveal.idx_decision": [0, 1, 2, 3],
        }
