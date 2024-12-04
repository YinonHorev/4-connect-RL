from state import GameState
from state import Players
from node import Node
import numpy as np
import math
import random


def play():
    '''
    Play a game of Connect Four.
    Player green uses the MCTS algorithm to determine the best move.
    Player black chooses a random move.
    '''
    state = GameState()
    state.render()

    while not (winner := state.is_terminal()):
        if state.current_player == Players.green.value:
            move = mcts(state, 1000)
        else:
            move = random.choice(state.get_legal_moves())
        print(f"Player {state.current_player} chooses column {move}")
        state.make_move(move)
        state.render()
    
    if winner == True:
        print("Draw!")
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

def mcts(state: GameState, n_simulations: int):
    '''Determine the best move using the Monte Carlo Tree Search algorithm.'''
    root = Node(state, None, None)
    for _ in range(n_simulations):
        # Select nodes recursively until a leaf node is reached
        leaf = select(root)
        if winner := leaf.state.is_terminal():
            reward = get_reward(winner)
            backtrack(leaf, reward)
            continue

        # Expand the leaf node
        leaf.add_children()

        # Simulate a random game from the new node
        reward = simulate(leaf)

        # Backtrack the result of the simulation
        leaf = backtrack(leaf, reward)

    best_move, _ = root.best_child()
    return best_move

def select(root: Node) -> Node:
    '''Select the most promising leaf based on UCB formula.'''
    curr_node = root
    while curr_node.children:
        _, curr_node = curr_node.best_child()
    return curr_node

def simulate(node: Node) -> int:
    '''Simulate a random game from the current state.'''
    temp_state = node.state.clone()
    while not (winner := temp_state.is_terminal()):
        move = random.choice(temp_state.get_legal_moves())
        temp_state.make_move(move)
    return get_reward(winner)

def backtrack(node: Node, reward: int) -> Node:
    '''Update value and visits for states expanded in selection and expansion.'''
    while node:
        node.update(reward)
        node = node.parent
    return node

def get_reward(winner: int) -> int:
    '''Return the reward for the simulation.'''
    if winner == True:
        return 0
    elif winner == Players.green:
        return 1
    else:
        return -1

if __name__ == "__main__":
    play()
