# QAPACO - Ant Colony Optimization for the Quadratic Assignment Problem

Github link: https://github.com/tpremoli/QAPACO

## Introduction

This program is an exploration into ant-colony optimization (ACO) for the quadratic assignment problem (QAP). 

Read more about the problem [here](https://en.wikipedia.org/wiki/Quadratic_assignment_problem)

The results of the program are found in report.pdf

## Implementation

This implementation consists of two files: world.py and main.py. 

In world.py, a World class is defined, which holds all the information for a particular ACO run (i.e distance, flow, and pheromone matrices), along with methods to generate ant paths, apply pheromones, calculate fitness, and plotting results. No heuristics are used (Due to problem specification)

main.py contains methods for running the program, which enable running multiple attempts concurrently, so we can compare multiple attempts faster. For each run, the program also saves plots under plots/, stats under stats/, and final saved World objects under worlds/ (These are useful if we want to do analysis without having to rerun experiments). There is also a method to run ACO scripts with randomized ant paths, which allow us to compare the ACO approach to a completely random approach


## Prerequisites:
In the root directory run:

    pip install -r requirements.txt

To run the program run

    python main.py

in the root directory.

## Usage

To run experiments with custom parameters, add your desired parameters in the main file with the following convention

    run_process(no_attempts, m, e, max_iter=10_000, print_data=False, filename="Uni50a.dat")

where

    no_attempts = The number of ACO attempts that will be ran for these parameters
    m = The number of ants in the ACO runs
    e = The evaporation rate in the ACO
    max_iter = The maximum number of iterations in the ACO run. Defaults to 10_000
    print_data = Whether or not to print verbose information. Defaults to False
    filename = The QAP problem file. Defaults to Uni50a.dat

Although this analysis focused on the "Uni50a.dat" problem, this program works for many QAP problems in the correct format.

To run a single attempt with random ants, use the method

    run_random(m, e, max_iter, print_data)

Where the parameters mean the same thing.

Plots generated will be saved in `plots/`, final stats in `stats/`, and pickles in `plots/`. To load a pickle, use the `load_pickle(filename)` method provided in main.py. Filenames correspond to the run paremeters and attempt.