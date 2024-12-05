from state import GameState
import math


EXPLOR_PAR = math.sqrt(2)


class Node:
    def __init__(self, state: GameState, parent: "Node", move: int):
        self.state = state
        self.parent = parent
        self.children = {}
        self.wins = 0
        self.simulations = 0

        if parent is not None:
            parent.children[move] = self

    def best_child(self) -> tuple[int, "Node"]:
        """Return the move and corresponding child node with the highest UCB value."""
        for move, child in self.children.items():
            if child.simulations == 0:
                return move, child
        max_move, max_child = max(
            self.children.items(), key=lambda item: item[1]._ucb()
        )
        return max_move, max_child

    def add_children(self):
        """Add all legal next moves as children to the node."""
        legal_moves = self.state.get_legal_moves()
        if not legal_moves:
            raise ValueError("No legal moves")
        for move in legal_moves:
            new_state = self.state.clone()
            new_state.make_move(move)
            self.children[move] = Node(new_state, self, move)

    def update(self, result):
        """Update the win and simulation count of the node, based on the result of the simulation."""
        self.simulations += 1
        self.wins += result

    def _ucb(self) -> float:
        """Calculate the Upper Confidence Bound of the node."""
        return self._exploitation() + self._exploration()

    def _exploitation(self) -> float:
        return self.wins / self.simulations if self.simulations != 0 else 0.0

    def _exploration(self) -> float:
        return (
            EXPLOR_PAR * math.sqrt(math.log(self.parent.simulations) / self.simulations)
            if self.simulations != 0
            else 0.0
        )

    def __repr__(self):
        return f"Node({self.state.board}, {self.wins}, {self.simulations})"
