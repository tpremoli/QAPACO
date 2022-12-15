from random import SystemRandom
import matplotlib.pyplot as plt
import numpy.random as npr

class World:
    def __init__(self, filename, m=100, e=0.5, print_data=True):
        """Initializes a world using an m (ant count) and e (evaporation coefficient)
        A world in this case is a matrix of distances, a matrix of flow values between facilities, 
        and a node count. A pheromone matrix is also created, where pheromone[i][j] is the bias of
        placing facility i in location j.

        Args:
            filename (str): Distance and Flow filename to open
            m (int, optional): ant count. Defaults to 100.
            e (float, optional): evaporation rate. Defaults to 0.5.
            print_data (bool, optional): whether to print current state. Defautls to true
        """
        if print_data:
            print("Initializing World with {}".format(filename))
        
        # This keeps track of costs for plotting
        self.all_costs = []
        
        self.m = m
        self.e = e
        
        if print_data:
            print("Ant count: {}; Evaporation rate: {}".format(m,e))
        with open(filename, "r") as f:
            # Splitting data by  line
            data = f.read().split("\n")
            for i in range(len(data)):
                data[i] = data[i].split(" ")
                data[i] = list(filter(None, data[i]))

            # gets rid of empty entries
            data = [item for item in data if item != []]

            # n nodes is straighforward
            self.n_nodes = int(data.pop(0)[0])
            
            if print_data:
                print("Number of nodes: {}".format(self.n_nodes))
            
            self.distances = []
            
            # moving thru array and parsing values
            for i in range(self.n_nodes):
                self.distances.append([int(val) for val in data.pop(0)])
             
            if print_data:
                print("Distance matrix loaded")
            
            self.flow = []
            
            for i in range(self.n_nodes):
                self.flow.append([int(val) for val in data.pop(0)])
            
            if print_data:
                print("Flow matrix loaded")
            
            self.pheromones = []
            rng = SystemRandom()
            
            # Setting random pheromone values per row
            for i in range(self.n_nodes):
                self.pheromones.append([rng.random() for _ in range(self.n_nodes)])
            
            if print_data:
                print("Pheromone table created")
            
            
    def generate_ant_paths(self, m=None):
        """Generates and returns m ants. if m not passed, uses world m.

        Args:
            m (int, optional): Ant count. Defaults to self.m.

        Returns:
            list(int): a list of int values. In this list, list[location] = facility
        """
        ants = []
        rng = SystemRandom()
        
        if not m:
            m = self.m

        # for each ant
        for _ in range(m):
            ant_path = []
            
            first = rng.randint(0,49)
            # Facility 0 is at location 0
            ant_path.append(first)
            
            facilities = [i for i in range(0,self.n_nodes)]
            
            facilities.remove(first)
            
            # the index in an ant path is the location (0-49)
            # We want to place a random facility at each location according to pheromone
            for loc in range(1, self.n_nodes):
                # This is the  pheromones of each facility for being in the current location
                all_facility_pheromones = self.column(self.pheromones, loc)
                final_pheromones = []
                
                # We get remove the facilities that have already been placed at a location
                for facility, pheromone in enumerate(all_facility_pheromones):
                    if facility in facilities:
                        final_pheromones.append(pheromone)
                
                max = sum(final_pheromones)
                selection_probs = [x/max for x in final_pheromones]
                
            
                # The pheromone corresponds to the fitness of putting facility i in location j
                next_facility = facilities[npr.choice(len(final_pheromones), p=selection_probs)]
                ant_path.append(next_facility)
                facilities.remove(next_facility)
            
            ants.append(ant_path)
                
        return ants
    
    def column(self, matrix, i):
        """Returns a matrix column as a 1d list

        Args:
            matrix (2d list): matrix to extract
            i (int): column to use

        Returns:
            list: a 1d list of the column chosen
        """
        return [row[i] for row in matrix]
        
    
    def calc_fitnesses(self, ant_paths, iter_no=0, print_data=True):
        """Calculates the fitness of the ant paths passed.

        Args:
            ant_paths (list): 2d list of previously generated ant paths
            iter_no (int, optional): Itereation we are on. Used for printing state. Defaults to 0.

        Returns:
            list(int): a list of the fitnesses of the ant paths.
        """
        costs = []
        
        for antpath in ant_paths:
            cost = 0
            
            # This is exactly the math equation
            for i in range(self.n_nodes):
                for j in range(self.n_nodes):
                    # Distance between locations i and j
                    D = self.distances[i][j]
                    
                    # flow between the facilities at locations i and j
                    F = self.flow[antpath[i]][antpath[j]]
                    
                    cost += D*F
            
            costs.append(cost)

        min_index = min(range(len(costs)), key=costs.__getitem__)
        best_ant = ant_paths[min_index]
        
        max_index = max(range(len(costs)), key=costs.__getitem__)
        worst_ant = ant_paths[max_index]

        if print_data:
            print("iter: {}\n\tBest ant cost {}\n\tWorst ant cost {}".format(iter_no, min(costs), max(costs)))
        
        self.all_costs.append(costs)
        
        return costs, best_ant, costs[min_index]
        
    def apply_pheromones(self, ant_paths, costs):
        """Applies ant path pheromone based on the cost list

        Args:
            ant_paths (2d list): Previously generated ant paths
            costs (list(int)): list of costs of the previously passed ant paths
        """
        for ant_index, ant_path in enumerate(ant_paths):
            for location, facility in enumerate(ant_path):
                applied_pheromone = 1 / costs[ant_index]
                self.pheromones[facility][location] += applied_pheromone

    def convert_to_avgs(self, list):
        avgs_list = []
        for sublist in list:
            avgs_list.append(sum(sublist) / len(sublist))
        return avgs_list
    
    def plt_fitnesses(self, num, all_costs=None):
        """Plots best and average ants for each iteration

        Args:
            num (int): id of figure
            all_costs (list, optional): 2d array containing all cost calcs. defaults to this world's instance 
        """
        if not all_costs:
            all_costs = self.all_costs
            
        plt.figure(figsize = (20, 10), num=num)
        x = [i for i in range(len(all_costs))]
        y1 = self.convert_to_avgs(all_costs)
        plt.plot(x, y1, label="Average solution cost")
        y2 = [min(i) for i in all_costs]
        plt.plot(x, y2, label="Best solution cost")
        
        plt.title("ACO fitness over time. m:{} e:{} attempt {}".format(self.m,self.e,num), size=26)
        plt.ylabel("Cost (lower is better)", size = 20)
        plt.xlabel("Iteration", size = 20)
        plt.legend(prop={'size': 20})
        plt.grid(color = 'gray', axis = 'y', alpha = 0.6, zorder = 0)

    
    def evaporate_pheromones(self, e=None):
        """Evaporates pheromones according to evaporation rate

        Args:
            e (float, optional): Evaporation rate. Defaults to 0.5.
        """
        # Just quickly applying map function to the 2d array of pheromone vals
        if e:
            mult_e = lambda x: x*e
        else:
            mult_e = lambda x: x*self.e
        self.pheromones =  [list(map(mult_e, sublist)) for sublist in self.pheromones]

    def get_total_avg(self):
        """Gets the average ant cost across all iterations

        Returns:
            int: average cost of all ants across all iterations
        """
        avg_list = self.convert_to_avgs(self.all_costs)
        return sum(avg_list) / len(avg_list)

def runtest(w):
    """This runs a quick test to ensure the pheromone placing works

    Args:
        w (world): the world to run the test on
    """
    a = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49]]
    c, ba = w.calc_fitnesses(a)
    for _ in range(500):
        w.apply_pheromones(a,c)
        w.evaporate_pheromones()
    
    a = w.generate_ant_paths()
    c,ba = w.calc_fitnesses(a)
    
    # If the pheromone has been applied so many times, then the only real path should be the same one that was input
    assert a[0] == ba
    assert c[0] == 5941988
    

    
    