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
    'iterations': 15,
    'update_frequency': 15,
    'default_policy': 'cosine',  # options are: ['random', 'nn', 'cosine', 'mc']
    'nn':
        {
            'location': "../nn-reward-function/models/champion-model-06-04-2021-1617757457-ls256-lr0.0005-l20.05/model.pickle"
        },
    'num_experiments': 10,
    'results_location': 'results/real'
}


def main():
    initial_state = generate_initial_state(['121', '24', '18'], ['11', '26'])
    default_policy = config['default_policy']
    i = config['num_experiments']
    save_location = config['results_location']

    if default_policy == 'random':
        run_experiment(default_policy, i, initial_state, simulation.random_winner, location=save_location)
    elif default_policy == 'cosine':
        combinations = simulation.cosine_metadata(config['filtered_dataset'])
        run_experiment(default_policy, i, initial_state, simulation.cosine_similarity, metadata=combinations,
                       location=save_location)
    elif default_policy == 'mc':
        win_rate = simulation.load_win_rate(config['win_rate_file'])
        run_experiment(default_policy, i, initial_state, simulation.majority_class, metadata=win_rate,
                       location=save_location)
    elif default_policy == 'nn':
        network = simulation.load_nn(config['nn']['location'])
        run_experiment(default_policy, i, initial_state, simulation.forward_pass, metadata=network,
                       location=save_location)
    else:
        print(f'Reward function {default_policy} not defined.')

def run_experiment(default_policy, iterations, initial_state, simulation_function, metadata=None, location=None):
    results = []
    recs = []
    for i in range(iterations):
        time_and_mem, rec = run_algorithm(initial_state, simulation_function, simulation_metadata=metadata)
        results.append(time_and_mem)
        recs.append(rec)
    if location is not None:
        save_results(results, recs, default_policy, location)


def run_algorithm(initial_state, defaultPolicy, simulation_metadata=None):
    start_time = time.time()
    res = UCT(initial_state, config['iterations'], config['update_frequency'], defaultPolicy, simulation_metadata)
    finish_time = time.time()
    memory = psutil.Process().memory_info().peak_wset / 1000000
    node_count = count_nodes(res.parent)
    show_results(res, node_count, finish_time - start_time, memory)
    return [finish_time - start_time, memory, node_count], list(res.state)


def show_results(result, node_count, time, memory_usage):
    print('Result:', result)
    print('Monte Carlo Tree Search created', node_count, 'tree nodes.')
    print('Took', time, 'seconds to run, and average iteration time of', time / config['iterations'], 'seconds.')
    print('Peak memory usage was:', memory_usage, 'megabytes.')


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


def generate_initial_state(blue_team, red_team):
    arr = []
    for i in range(5):
        arr.append(0 if i >= len(blue_team) else int(blue_team[i]))

    for i in range(5, 10):
        arr.append(0 if i - 5 >= len(red_team) else int(red_team[i - 5]))
    return tuple(arr)


def save_results(results, recs, policy, location):
    today = date.today().strftime('%d-%m-%Y')
    curr_time = int(time.time())
    average_time = 0
    average_mem = 0
    average_nodes = 0
    with open(f'{location}/results-{policy}-{today}-{curr_time}.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for row in results:
            writer.writerow(row)
            average_time += row[0]
            average_mem += row[1]
            average_nodes += row[2]
    f.close()

    with open(f'{location}/recs-{policy}-{today}-{curr_time}.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for row in recs:
            writer.writerow(row)
    f.close()

    average_time /= len(results)
    average_mem /= len(results)
    average_nodes /= len(results)
    print(f'Average time: {average_time}')
    print(f'Average peak memory usage: {average_mem}')
    print(f'Average nodes: {average_nodes}')


if __name__ == '__main__':
    main()
