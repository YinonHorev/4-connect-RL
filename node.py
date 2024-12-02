from state import GameState
import math
from typing import Self

EXPLOR_PAR = math.sqrt(2)


class Node:
    def __init__(self, state: GameState, parent: Self | None):
        self.state = state
        self.parent = parent
        self.children = {}
        self.wins = 0
        self.simulations = 0

    def best_child(self) -> Self:
        return max(self.children.values(), key=lambda x: x.ucb())

    def ucb(self) -> float:
        return self._exploitation() + self._exploration()

    def _exploitation(self) -> float:
        return self.wins / self.simulations if self.simulations != 0 else 0.0

    def _exploration(self) -> float:
        return (
            EXPLOR_PAR * math.sqrt(math.log(self.parent.simulations) / self.simulations)
            if self.simulations != 0
            else 0.0
        )

    def add_children(self):
        legal_moves = self.state.get_legal_moves()
        if not legal_moves:
            raise ValueError("No legal moves")
        for move in legal_moves:
            new_state = self.state.clone()
            new_state.make_move(move)
            self.children[move] = Node(new_state, self)

    def update(self, result):
        pass

    def __repr__(self):
        return f"Node({self.state.board}, {self.wins}, {self.simulations})"
