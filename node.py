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

        parent.children.append(self)

    def is_fully_expanded(self):
        return len(self.state.get_legal_moves) == len(self.children)

    def best_child(self):
        return max(self.children, key=lambda x: x.ucb())

    def ucb(self):
        return self.wins / self.simulations + EXPLOR_PAR * math.sqrt(math.log(self.parent.simulations) / self.simulations)

    def add_children(self):
        legal_moves = self.state.get_legal_moves()
        if not legal_moves:
            raise ValueError("No legal moves")
        for move in legal_moves:
            new_state = self.state.clone()
            new_state.make_move(move)
            self.children[move] = Node(new_state, self, move)

    def update(self, result):
        pass

    def __repr__(self):
        return f"Node({self.state.board}, {self.wins}, {self.simulations})"
