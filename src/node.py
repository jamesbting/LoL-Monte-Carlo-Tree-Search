from math import pow, sqrt, log
from random import random as random
class Node(object):
    def __init__(self, parent = None, state = None, possible_actions = None):
        self.q = 0
        self.n = 0
        self.children = []
        self.parent = parent
        self.state = state
        self.possible_actions = possible_actions

    def expand(self):
        new_child = Node(parent=self, state=self.state)
        action = self.possible_actions[random() * len(self.possible_actions)]
        self.possible_actions.remove(action)
        self.children.append(new_child)
        return new_child

    def bestChild(self, exploration_term = pow(2, -0.5)):
        s = sorted(self.children, key = lambda c: c.q / c.n + (exploration_term * sqrt(2 * log(self.n)/c.n)))
        return s[-1]

    def isTerminal(self):
        return len(self.state) == 10