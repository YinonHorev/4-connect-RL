import numpy as np
from enum import Enum


class Players(Enum):
    green = 1
    black = -1


class GameState:
    """A class to represent a 4 connect"""

    def __init__(self, init_board: np.ndarray | None = None):
        self.board: np.ndarray = (
            init_board if isinstance(init_board, np.ndarray) else np.zeros((6, 7), dtype=int)
        )
        self.current_player: int = 1

    def get_legal_moves(self) -> list[int]:
        return [col for col in range(7) if self.board[0, col] == 0]

    def check_legal_move(self, col: int) -> bool:
        return col >= 0 and col < 7 and self.board[0, col] == 0

    def make_move(self, col: int):
        """Play a turn and switch player.

        Players are denoated as [1, -1]
        """
        for row in reversed(range(6)):
            if self.board[row, col] == 0:
                self.board[row, col] = self.current_player
                self.current_player *= -1
                break

    def is_terminal(self) -> Players | bool:
        """Check if game is over.

        Returns: False if game is ongoing, True for Draw, or a winning player.
        """
        return self._check_winner() or len(self.get_legal_moves()) == 0

    def _check_winner(self) -> Players | None:
        """Checks if the given player has won the game."""

        # horizontal
        for player in Players:
            for i in range(6):
                for j in range(3):
                    if (
                        self.board[i][j] == player.value
                        and self.board[i][j + 1] == player.value
                        and self.board[i][j + 2] == player.value
                        and self.board[i][j + 3] == player.value
                    ):
                        return player

            # vertical
            for i in range(3):
                for j in range(6):
                    if (
                        self.board[i][j] == player.value
                        and self.board[i + 1][j] == player.value
                        and self.board[i + 2][j] == player.value
                        and self.board[i + 3][j] == player.value
                    ):
                        return player

            # diagonal
            for i in range(3):
                for j in range(3):
                    if (
                        self.board[i][j] == player.value
                        and self.board[i + 1][j + 1] == player.value
                        and self.board[i + 2][j + 2] == player.value
                        and self.board[i + 3][j + 3] == player.value
                    ):
                        return player

            for i in range(3):
                for j in range(3, 6):
                    if (
                        self.board[i][j] == player.value
                        and self.board[i + 1][j - 1] == player.value
                        and self.board[i + 2][j - 2] == player.value
                        and self.board[i + 3][j - 3] == player.value
                    ):
                        return player

        return None

    def clone(self):
        new_state = GameState()
        new_state.board = self.board.copy()
        new_state.current_player = self.current_player
        return new_state

    def render(self):
        print(self)

    def __str__(self):
        return str(self.board)
