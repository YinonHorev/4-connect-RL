from state import GameState
from state import Players


def test_winner(player_one_winning_board):
    g = GameState(init_board=player_one_winning_board)
    assert g.is_terminal() == Players.green


def test_non_terminal_state(assignment_board):
    g = GameState(init_board=assignment_board)
    assert g.is_terminal() == False


def test_make_move(assignment_board):
    g = GameState(init_board=assignment_board)

    for i in range(3):
        g.make_move(4)

    assert g.is_terminal() == Players.green
