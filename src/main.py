import json
import time
import psutil
import queue
import simulation
from monte_carlo import UCTSearch as UCT

config = {
    'champions': {
        'fileName': "../../data/champions-cleaned.json"
    },
    'filtered_dataset': '../../data/filtered-dataset.csv',
    'win_rate_file': '../../data/win_rate.txt',
    'iterations': 1000,
    'defaultPolicy': 'mc', #options are: ['random_winner', 'nn', 'cosine', 'mc']
}


def main():
    champion_pool = json.load(open(config['champions']['fileName'], 'r'))
    initial_state = generate_initial_state(['121', '24', '18'], ['11', '26'], champion_pool)
    i = config['iterations']

    if config['defaultPolicy'] == 'random_winner':
        run_algorithm(initial_state, i, simulation.random_winner)
    if config['defaultPolicy'] == 'cosine':
        combinations = simulation.cosine_metadata(config['filtered_dataset'])
        run_algorithm(initial_state, i, simulation.cosine_similarity, combinations)
    if config['defaultPolicy'] == 'mc':
        win_rate = simulation.load_win_rate(config['win_rate_file'])
        run_algorithm(initial_state, i, simulation.majority_class, win_rate)
def run_algorithm(initial_state, iterations, defaultPolicy, simulation_metadata=None):
    start_time = time.time()
    res = UCT(initial_state, config['iterations'], defaultPolicy, simulation_metadata)
    finish_time = time.time()
    show_results(res, finish_time - start_time, psutil.Process().memory_info().peak_wset)


def show_results(result, time, memory_usage):
    print('Result:', result)
    node_count = count_nodes(result.parent)
    print('Monte Carlo Tree Search created', node_count, 'tree nodes.')
    print('Took ',time , ' seconds to run, and average iteration time of', time / config['iterations'], 'seconds.')
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
