from audioop import avg
from state import GameState
from state import Players
from node import Node
import numpy as np
import math
import random
from collections import defaultdict
import matplotlib.pyplot as plt

def play_a_lot():
    res = defaultdict(int)
    for i in range(1):
        print(i)
        res[play()] += 1
        print(res)



def play():
    """
    Play a game of Connect Four.
    Player green uses the MCTS algorithm to determine the best move.
    Player black chooses a random move.
    """
    state = GameState(assignment_board())
    # state = GameState()
    state.render()

    while not (winner := state.is_terminal()):
        if state.current_player == Players.green.value:
            move = mcts(state, 1000)
        else:
            move = random.choice(state.get_legal_moves())
        # print(f"Player {state.current_player} chooses column {move}")
        state.make_move(move)
        state.render()

    if winner == True:
        print("Draw!")
    print(f"Player {winner} wins!")
    print(state)

    return winner


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

def tipping_point():
    board = np.asarray(
        [
            [-1, -1, -1, 1, 0, 1, 0],
            [-1, 1, 1, 1, 0, -1, 0],
            [1, -1, -1, -1, 0, 1, 0],
            [-1, 1, 1, 1, 0, -1, 0],
            [1, 1, 1, -1, -1, -1, 0],
            [-1, -1, 1, -1, 1, 1, 0],
        ]
    )
    return board

def plot_win_ratios(win_ratio_per_move, legal_moves):
    _, num_simulations = win_ratio_per_move.shape
    
    plt.figure(figsize=(10, 6))
    for idx, move in enumerate(legal_moves):
        plt.plot(
            range(num_simulations), 
            win_ratio_per_move[idx], 
            label=f"Move {move}", 
            linestyle='-'
        )

    plt.title("Wins/Simulations Ratio per Move During MCTS")
    plt.xlabel("Number of Simulations")
    plt.ylabel("Wins/Simulations Ratio")
    plt.legend(loc="best", title="Moves")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()


def mcts(state: GameState, n_simulations: int):
    """Determine the best move using the Monte Carlo Tree Search algorithm."""
    root = Node(state, None, None)
    best_move = None
    prev_best_move = None
    win_ratio_per_move = np.zeros((len(state.get_legal_moves()), n_simulations))
    stable_count = 0
    for i in range(n_simulations):
        # Select nodes recursively until a leaf node is reached
        leaf = select(root)
        if winner := leaf.state.is_terminal():
            reward = get_reward(winner)
            backtrack(leaf, reward)
        else:
            # Expand the leaf node
            leaf.add_children()

            # Simulate a random game from the new node
            reward = simulate(leaf)

            # Backtrack the result of the simulation
            leaf = backtrack(leaf, reward)

        # Count the number of stable iterations
        prev_best_move = best_move
        best_move = -1
        for k, (move, child) in enumerate(root.children.items()):
            if child.simulations != 0:
                win_ratio_per_move[k, i] = child.wins / child.simulations
            if best_move == -1 or (child.simulations != 0 and root.children[best_move].wins / root.children[best_move].simulations < child.wins / child.simulations):
                best_move = move
        
        if prev_best_move == best_move:
            stable_count += 1
        else:
            stable_count = 0
        if stable_count == 30:
            break
    
    plot_win_ratios(win_ratio_per_move[:,0:i+1], state.get_legal_moves())

    # best_move, _ = root.best_child()
    best_move, best_move_child = max(root.children.items(), key=lambda c: c[1].wins / c[1].simulations)
    return best_move


def select(root: Node) -> Node:
    """Select the most promising leaf based on UCB formula."""
    curr_node = root
    while curr_node.children:
        _, curr_node = curr_node.best_child()
    return curr_node


def simulate(node: Node) -> int:
    """Simulate a random game from the current state."""
    temp_state = node.state.clone()
    while not (winner := temp_state.is_terminal()):
        move = random.choice(temp_state.get_legal_moves())
        temp_state.make_move(move)
    return get_reward(winner)


def backtrack(node: Node, reward: int) -> Node:
    """Update value and visits for states expanded in selection and expansion."""
    while node:
        node.update(reward)
        node = node.parent
    return node


def get_reward(winner: int) -> int:
    """Return the reward for the simulation."""
    if winner == True:
        return 0
    elif winner == Players.green:
        return 1
    else:
        return 0


if __name__ == "__main__":
    play_a_lot()
