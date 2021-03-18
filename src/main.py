import json
import time
import psutil
import queue
from random import random as random
from monte_carlo import UCTSearch as UCT

config = {
    'champions': {
        'fileName': "../../data/champions-cleaned.json"
    },
    'iterations': 1000,
    'defaultPolicy': 'random_winner', #options are: ['random_winner', 'nn', 'monte-carlo', 'similarity']
}


def main():
    champion_pool = json.load(open(config['champions']['fileName'], 'r'))
    initial_state = generate_initial_state(['121', '24', '18'], ['11', '26'], champion_pool)
   

    if config['defaultPolicy'] == 'random_winner':
        run_algorithm(initial_state, config['iterations'], random_winner)

def run_algorithm(initial_state, iterations, defaultPolicy):
    start_time = time.time()
    res = UCT(initial_state, config['iterations'], random_winner)
    finish_time = time.time()
    show_results(res, finish_time - start_time, psutil.Process().memory_info().peak_wset)


def random_winner(state):
    return 1 if random() > 0.5 else 0

def show_results(result, time, memory_usage):
    print('Result:', result)
    node_count = count_nodes(result.parent)
    print('Monte Carlo Tree Search created', node_count, 'tree nodes.')
    print('Took ',time , ' seconds to run.')
    print('Peak memory usage was: ', memory_usage/1000000, 'megabytes.')

def count_nodes(root):
    q = queue.Queue()
    count = 0
    q.put(root)
    while not q.empty():
        curr = q.get()
        count += 1
        for child in curr.children:
            q.put(child)
    return count

def generate_initial_state(blue_team, red_team, champion_pool):
    arr = [0] * len(champion_pool.keys())
    for blue in blue_team:
        arr[int(blue)] = 1
    for red in red_team:
        arr[int(red)] = -1
    return tuple(arr)

if __name__ == '__main__':
    main()
