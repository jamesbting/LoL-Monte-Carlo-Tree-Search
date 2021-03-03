from math import pow, sqrt, log
from random import random as random
#states will be a N-dimensional vector, where N is the number champions, and the following values:
# 1: Champion selected by blue team
# -1: Champion selected by red team
# 0: unselected
class Node(object):
    def __init__(self, parent = None, state = None, possible_actions = None):
        self.q = 0
        self.n = 0
        self.children = []
        self.parent = parent
        self.state = state
        self.possible_actions = possible_actions
        self.expanded = False

    def expand(self):
        self.expanded = True
        new_child = Node(parent=self, state=self.state)
        action = self.possible_actions[int(random() * len(self.possible_actions))]
        self.possible_actions.remove(action)
        self.children.append(new_child)
        return new_child

    def bestChild(self, exploration_term = pow(2, -0.5)):
        s = sorted(self.children, key = lambda c: c.q / c.n + (exploration_term * sqrt(2 * log(self.n)/c.n)))
        print(len(s))
        return s[len(s)-1]

    def isTerminal(self):
        blueTeamSelected = 0
        redTeamSelected = 0
        for selection in self.state:
            if selection == 1:
                blueTeamSelected += 1
            if selection == -1:
                redTeamSelected += 1
        return blueTeamSelected == 5 and redTeamSelected == 5

    def isExpandable(self):
        for child in self.children:
            if not child.expanded:
                return self.isTerminal()
        return False