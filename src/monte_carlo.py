from node import Node
from random import random as random
import queue

def UCTSearch(initial_state, max_iters):
    first_pick = list(Node.players.keys())[1 if random() > 0.5 else 0]
    print(f"The {first_pick} team will pick first.")
    root = Node(state=initial_state, player=Node.players[first_pick])

    for i in range(max_iters + 1):
        selected_node = treePolicy(root)
        reward = defaultPolicy(selected_node.state)
        backpropagate(selected_node, reward)
        print("iteration: ", i)

    print(root.player)
    return root.best_child(0)
    #return get_result(root, 0)


def treePolicy(node):
    curr = node
    while not curr.is_terminal():
        if len(curr.possible_actions) > 0:
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

def bfs(root):
    q = queue.Queue()
    q.put(root)
    while(not q.empty()):
        curr = q.get()
        for child in curr.children:
            q.put(child)
        print(curr.depth)
