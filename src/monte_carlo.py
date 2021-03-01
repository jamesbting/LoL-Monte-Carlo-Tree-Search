from node import Node
from random import random as random

def UCTSearch(initial_state, max_iters):
    root = Node(state=initial_state)
    for i in range(max_iters + 1):
        selected_node = treePolicy(root)
        reward = defaultPolicy(selected_node.state)
        backpropagate(selected_node, reward)
    return root.bestChild(exploration_term=0)

def treePolicy(node):
    curr = node
    while not curr.isTerminal():        
        if not curr.isExpanded():
            return curr.expand()
        else:
            curr = curr.bestChild()
    return curr

#simulation of the game
def defaultPolicy(state):
    return 1 if random() > 0.5 else 0

def backpropagate(node, reward):
    curr = node
    while curr is not None:
        curr.n += 1
        curr.q += reward
        curr = curr.parent
