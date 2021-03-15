from node import Node
from random import random as random


def UCTSearch(initial_state, max_iters):
    first_pick = list(Node.players.keys())[1 if random() > 0.5 else 0]
    print(f"The {first_pick} team will pick first.")
    root = Node(state=initial_state, player=Node.players[first_pick])

    for i in range(max_iters + 1):
        selected_node = treePolicy(root)
        reward = defaultPolicy(selected_node.state)
        backpropagate(selected_node, reward)
        print(f"iteration: {i}")
    return get_result(root, 0)


def treePolicy(node):
    curr = node
    while not curr.is_terminal():
        if curr.is_expandable():
            return curr.expand()
        else:
            curr = curr.best_child()
    return curr


# simulation of the game
def defaultPolicy(state):
    return 1 if random() > 0.5 else 0


def backpropagate(node, reward):
    curr = node
    while curr is not None:
        curr.n += 1
        curr.q += reward
        reward = 1 - reward
        curr = curr.parent


def get_result(root, depth):
    print(f"depth: {depth}")
    if len(root.children) == 0:
        return root
    return get_result(root.best_child(exploration_term=0), depth + 1)
