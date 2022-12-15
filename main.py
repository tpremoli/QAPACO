""" This is the main file for the program. It has 2 methods, run_process and single_aco.
run_process runs n attempts of an ACO with determined parameters concurrently, and single_aco
actually executes this.

Running this file will run all 4 experiments described in the markscheme and save outputs to out folder
"""
import matplotlib.pyplot as plt
from multiprocessing import Pool
from world import World

def single_aco(i, m, e, max_iter, print_data):
    """This method runs the ACO with the specified parameters and plots them. This will usually be ran as a subprocess (do multiple attempts @once)

    Args:
        e (float): e val for world, evaporation rate
        m (int): m val for world, ant count
        max_iter (int, optional): Max interations of the process. Defaults to 1000.
        print_data (bool, optional): Whether to print each step's data. Defaults to False.
    """
    print("Launching attempt {}".format(i+1))
    w = World("Uni50a.dat", m=m, e=e, print_data=print_data)
    bestant_cost = 10000000000000000000000000000000000000000000000
    bestant = []
    for x in range(max_iter):
        a = w.generate_ant_paths()
        c, new_bestant, new_bestant_cost = w.calc_fitnesses(a, x+1, print_data=print_data)
        w.apply_pheromones(a,c)
        w.evaporate_pheromones()
        if new_bestant_cost < bestant_cost:
            bestant = new_bestant
            bestant_cost = new_bestant_cost

    avgant_cost = w.get_total_avg()
    w.plt_fitnesses(num=i+1)
    print("\tattempt {} best ant cost: {}\n\tavg ant cost: {}\n\tant:{}".format(i+1,bestant_cost,avgant_cost,bestant))
    plt.show()
    
def run_process(no_attempts, m, e, max_iter=10_000, print_data=False):
    """Creates multiprocesses ACO according to no_attempts
    
    Args:
        no_attempts (int): how many times to run the ACO with the parameters
        e (float): e val for world, evaporation rate
        m (int): m val for world, ant count
        max_iter (int, optional): Max interations of the process. Defaults to 1000.
        print_data (bool, optional): Whether to print each step's data. Defaults to False.
    """
    
    print("m: {}, e: {}".format(m,e))
    
    # We create pools with processes as no attempts (10,000 iterations is a lot, so better to run experiments concurrently)
    pool = Pool(processes=no_attempts)
    inputs = []
    for i in range(no_attempts):
        inputs.append((i,m,e,max_iter,print_data))
    
    # We use tuples for arguments
    pool.starmap(single_aco,inputs)
    
if __name__  == "__main__":
    
