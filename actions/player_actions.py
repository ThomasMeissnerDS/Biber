from base_classes.game_state import GameState

def draw_card_from_deck():
    pass


def exchange_card():
    pass


def draw_card_from_open_staple():
    pass


def pass_turn():
    pass


def knock_on_table(game: GameState):
    game.game_status = "finished"
    return game