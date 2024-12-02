import pytest
import numpy as np


@pytest.fixture
def player_one_winning_board() -> np.ndarray:
    board = np.asarray(
        [
            [-1, -1, -1, 1, 0, 0, 0],
            [-1, 1, 1, 1, 0, 0, 0],
            [1, -1, -1, -1, 0, 0, 0],
            [-1, 1, 1, 1, 1, 0, 0],
            [1, 1, 1, -1, -1, 0, 0],
            [-1, -1, 1, -1, 1, 0, 0],
        ]
    )
    yield board


@pytest.fixture
def assignment_board() -> np.ndarray:
    board = np.asarray(
        [
            [-1, -1, -1, 1, 0, 1, 0],
            [-1, 1, 1, 1, 0, -1, 0],
            [1, -1, -1, -1, 0, 1, 0],
            [-1, 1, 1, 1, 0, -1, 0],
            [1, 1, 1, -1, 0, -1, 0],
            [-1, -1, 1, -1, 0, 1, 0],
        ]
    )
    return board
