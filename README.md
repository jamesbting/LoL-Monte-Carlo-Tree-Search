# Monte Carlo Tree Search for League of Legends Champion Recommendations

This repository is an implementation of a Monte Carlo Tree Search algorithm that will, given a team composition, run a Monte Carlo Tree Search and return the next best possible move. The return value is node with the following attributes:

- q: the number of times this node produced a favorable outcome
- n: the number of times this node was visited
- state: A tuple of length 154 (number of champions in League of Legends) where the i-th index represents whether a team selected the i-th champion. 1 means blue team selects the i-th champion, and -1 means the red team selects the i-th champion. A 0 means that neither team selected the champion. 
- depth: depth of the node in the Monte Carlo Tree. This will always be 1 for the node that is returned as a result.



## Pre-requisites

- Python 3.9.2
- pip 21.0.1

The following Python modules are required as well

- psutil 5.8.0
- numpy 1.20.1
- torch 1.7.1+cu110

You can install each module by running the command ```pip install <MODULE_NAME>```

This program has not been validated on any other versions of the perquisites. 

## Setting up the program 

After downloading the repository, and installing all the modules, ensure that the file locations in the config dictionary are correct. Select the number of iterations for the MCTS to run, and the default policy to use.

## Running the program

To run the program, navigate to the directory in which the repository is downloaded, and then run the following command: ```python src/main.py```

## Results

The results are stored in the results folder by default. Running the program once will generate one results.csv file, stamped with the date, time and default policy. Each row will represent one experiment, with 2 numbers. The first number is the time to run the experiment, and the second one is the peak memory usage in megabytes. 