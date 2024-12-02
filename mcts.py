from state import GameState
from state import Players
from node import Node
import numpy as np
import math
import random


def play():
    state = GameState()
    state.render()

    while not (winner := state.is_terminal()):
        # move = int(input(f"Player {state.current_player}, enter a move: "))
        if state.current_player == Players.green.value:
            state = mcts(state, 100)
            if winner := state.is_terminal():
                break
        else:
            move = random.choice(state.get_legal_moves())
            state.make_move(move)
        state.render()
    print(f"Player {winner} wins!")


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


def mcts(state: GameState, n_simulations: int) -> GameState:
    """
    Monte Carlo Tree Search algorithm
    """
    root = Node(state, None)
    for i in range(n_simulations):
        # Select nodes recursively until a leaf node is reached
        leaf = select(root)
        if winner := leaf.state.is_terminal():
            reward = get_reward(winner)
            leaf = backtrack(leaf, reward)
            continue

        # Expand the leaf node
        leaf.add_children()

        # Simulate a random game from the new node
        reward = simulate(leaf)

        # Backtrack the result of the simulation
        leaf = backtrack(leaf, reward)
    return root.best_child().state


def select(root: Node):
    """
    Select the most promising leaf based on UCB formula
    """
    curr_node = root
    while curr_node.children:
        curr_node = curr_node.best_child()
    return curr_node


def simulate(node: Node):
    temp_state = node.state.clone()
    while not (winner := temp_state.is_terminal()):
        move = random.choice(temp_state.get_legal_moves())
        temp_state.make_move(move)
    return get_reward(winner)


def backtrack(node: Node, reward: int):
    """
    Update value and visits for states expanded in selection and expansion
    """
    while node := node.parent:
        node.simulations += 1
        node.wins += reward
    return node


def get_reward(winner: Players | bool) -> int:
    if winner == True:
        return 0
    elif winner == Players.green:
        return 1
    else:
        return -1


if __name__ == "__main__":
    play()
