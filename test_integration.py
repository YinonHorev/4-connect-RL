import pytest
import mcts
from state import GameState


def test_mcts_output(assignment_board) -> None:
    assert isinstance(mcts.mcts(GameState(assignment_board), 1000), GameState)
