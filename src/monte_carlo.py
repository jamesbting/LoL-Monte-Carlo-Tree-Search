from node import Node
from random import random as random

def UCTSearch(initial_state,possible_actions, max_iters):
    root = Node(state=initial_state, possible_actions=possible_actions)
    for i in range(max_iters + 1):
        selected_node = treePolicy(root)
        reward = defaultPolicy(selected_node.state)
        backpropagate(selected_node, reward)
        print(i)
    return root.bestChild(exploration_term=0)

def treePolicy(node):
    curr = node
    while not curr.isTerminal():        
        if not curr.isExpandable():
            print('here')
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
