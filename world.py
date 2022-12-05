from random import SystemRandom


class World:
    def __init__(self, filename):
        print("Initializing World with {}".format(filename))
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

            print("Number of nodes: {}".format(self.n_nodes))
            
            self.distances = []
            
            # moving thru array and parsing values
            for i in range(self.n_nodes):
                self.distances.append([int(val) for val in data.pop(0)])
                
            print("Distance matrix loaded")
            
            self.flow = []
            
            for i in range(self.n_nodes):
                self.flow.append([int(val) for val in data.pop(0)])
            
            print("Flow matrix loaded")
            
            self.pheromones = []
            rng = SystemRandom()
            
            # Setting random pheromone values per row
            for i in range(self.n_nodes):
                self.pheromones.append([rng.random() for _ in range(self.n_nodes)])
                
            print("Pheromone table created")
            
            
    def generate_ant_paths(self, m=5):
        ants = []
        rng = SystemRandom()
        
        # for each ant
        for _ in range(m):
            # Facilities lists the facilities that haven't yet been visited
            facilities = [i for i in range(self.n_nodes)]
            # random placement
            current_node = rng.randint(0,self.n_nodes-1)
            
            facilities.remove(current_node)
            
            ant_path = []            
            ant_path.append(current_node)
            
            # for each facility
            for _ in range(self.n_nodes-1):
                # getting the weights of each path
                weights = []
                for f in facilities:
                    weights.append(self.distances[current_node][f])
                if len(weights)  == 1:
                    weights = [1]
                # Picking next node to visit from facilities using weights
                next_node = rng.choices(facilities, weights=weights, k=1)[0]          
                
                ant_path.append(next_node)
                
                facilities.remove(next_node)
                current_node = next_node
                
            ants.append(ant_path)
        
        return ants
    
    def calc_fitnesses(self, ant_paths):
        costs = []
        
        for antpath in ant_paths:
            # We get current node and following node and calc fitness of that edge edge
            path = antpath.copy()
            
            current_node = path.pop(0)
            current_cost = 0            
            for _ in range(self.n_nodes-1):
                # This equation might not be correct. Asking Ayah
                next_node = path.pop(0)

                # Getting distance and flow from current node to next node                
                D = self.distances[current_node][next_node]
                F = 100 - self.flow[current_node][next_node]
                
                current_cost += D*F
                
                current_node = next_node
            
            costs.append(current_cost)

        min_index = min(range(len(costs)), key=costs.__getitem__)
        best_ant = ant_paths[min_index]
        
        print("Best ant cost {}\n\t{}".format(min(costs), best_ant))
        
        return costs, best_ant
        
    def apply_pheromones(self, ant_paths, costs):
        for i, antpath in enumerate(ant_paths):
            # We get current node and following node and apply pheromone on that edge
            path = antpath.copy()
            
            current_node = path.pop(0)
            for _ in range(self.n_nodes-1):
                # This equation might not be correct. Asking Ayah
                next_node = path.pop(0)
                
                # Inversely proportional costs (lower cost = better)
                pheromone = 1 / costs[i]

                # Getting distance and flow from current node to next node                
                self.pheromones[current_node][next_node] += pheromone
                
                current_node = next_node
    
    def evaporate_pheromones(self, e=0.5):
        """Evaporates pheromones according to evaporation rate

        Args:
            e (float, optional): Evaporation rate. Defaults to 0.5.
        """
        # Just quickly applying map function to the 2d array of pheromone vals
        mult_e = lambda x: x*e
        self.pheromones =  [list(map(mult_e, sublist)) for sublist in self.pheromones]

if __name__  == "__main__":
    w = World("Uni50a.dat")
    for x in range(100):
        a = w.generate_ant_paths(100)
        c,ba = w.calc_fitnesses(a)
        w.apply_pheromones(a,c)
        w.evaporate_pheromones(e=0.9)
        
    
    