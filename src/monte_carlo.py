from node import Node
from random import random as random
import queue

def UCTSearch(initial_state, max_iters, update_frequency, simulate_game, simulation_metadata=None):
    first_pick = Node.determine_next_pick(initial_state)
    print(f"The {first_pick} team will pick next.")
    root = Node(state=initial_state, player=Node.players[first_pick])

    for i in range(max_iters + 1):
        selected_node = treePolicy(root)
        reward = simulate_game(selected_node.state, simulation_metadata) #default policy
        backpropagate(selected_node, reward)
        if i % update_frequency == 0:
            print("Iteration: ", i)
    return root.best_child(0)


def treePolicy(node):
    curr = node
    while not curr.is_terminal():
        if len(curr.possible_actions) > 0:
            return curr.expand()
        else:
            curr = curr.best_child()
    return curr


def backpropagate(node, reward):
    curr = node
    while curr is not None:
        curr.n += 1
        curr.q += reward
        reward = 1 - reward
        curr = curr.parent

