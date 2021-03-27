import json
import time
import psutil
import queue
import simulation
from monte_carlo import UCTSearch as UCT
from datetime import date
import csv

config = {
    'champions': {
        'fileName': "../data/champions-cleaned.json"
    },
    'filtered_dataset': '../data/filtered-dataset-no-header.csv',
    'win_rate_file': '../data/win_rate.txt',
    'iterations': 1000,
    'update_frequency': 100,
    'default_policy': 'nn', #options are: ['random_winner', 'nn', 'cosine', 'mc']
    'nn': 
    {
        'location': "../nn-reward-function/models/champion-model-1616800920/model.pickle"
    },
    'num_experiments': 100,
    'results_location': 'results'
}


def main():
    champion_pool = json.load(open(config['champions']['fileName'], 'r'))
    initial_state = generate_initial_state(['121', '24', '18'], ['11', '26'], champion_pool)
    run_experiment(config['default_policy'], config['num_experiments'], initial_state, location = config['results_location'])




def run_experiment(default_policy, iterations, initial_state, location=None):
    results = []
    for i in range(iterations):
        print(f'iter: {i}')
        if default_policy == 'random':
            results.append(run_algorithm(initial_state, simulation.random_winner))

        if default_policy == 'cosine':
            combinations = simulation.cosine_metadata(config['filtered_dataset'])
            results.append(run_algorithm(initial_state, simulation.cosine_similarity, combinations))

        if default_policy == 'mc':
            win_rate = simulation.load_win_rate(config['win_rate_file'])
            results.append(run_algorithm(initial_state, simulation.majority_class, win_rate))
        
        if default_policy == 'nn':
            network = simulation.load_nn(config['nn']['location'])
            results.append(run_algorithm(initial_state, simulation.forward_pass, network))

    if location is not None:
        save_results(results, default_policy, location)


def run_algorithm(initial_state, defaultPolicy, simulation_metadata=None):
    start_time = time.time()
    res = UCT(initial_state, config['iterations'], config['update_frequency'], defaultPolicy, simulation_metadata)
    finish_time = time.time()
    memory = psutil.Process().memory_info().peak_wset
    show_results(res, finish_time - start_time, memory)
    return [finish_time - start_time, psutil.Process().memory_info().peak_wset]

def show_results(result, time, memory_usage):
    print('Result:', result)
    node_count = count_nodes(result.parent)
    print('Monte Carlo Tree Search created', node_count, 'tree nodes.')
    print('Took',time , 'seconds to run, and average iteration time of', time / config['iterations'], 'seconds.')
    print('Peak memory usage was:', memory_usage/1000000, 'megabytes.')

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

def save_results(results, policy, location):
    today = date.today().strftime('%d-%m-%Y')
    curr_time = int(time.time())
    average_time = 0
    with open(f'{location}/results-{policy}-{today}-{curr_time}.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for row in results:
            writer.writerow(row)
            average_time += row[0]
    f.close()
    average_time /= len(results)
    print(f'Average time: {average_time}')


if __name__ == '__main__':
    main()
