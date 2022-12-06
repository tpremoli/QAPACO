from random import SystemRandom

class World:
    def __init__(self, filename, m=100, e=0.5):
        print("Initializing World with {}".format(filename))
        
        self.m = m
        self.e = e
        
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
            
            
    def generate_ant_paths(self, m=None):
        ants = []
        rng = SystemRandom()
        
        if not m:
            m = self.m

        # for each ant
        for _ in range(m):
            ant_path = []
            
            # Facility 0 is at location 0
            ant_path.append(0)
            
            facilities = [i for i in range(1,self.n_nodes)]
            
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
                
                # The pheromone corresponds to the fitness of putting facility i in location j
                next_facility = rng.choices(facilities,weights=final_pheromones,k=1)[0]
                ant_path.append(next_facility)
                facilities.remove(next_facility)
            
            ants.append(ant_path)
                
        return ants
    
    def column(self, matrix, i):
        return [row[i] for row in matrix]
        
    
    def calc_fitnesses(self, ant_paths):
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
        
        print("Best ant cost {}\n\t{}".format(min(costs), best_ant))
        
        return costs, best_ant
        
    def apply_pheromones(self, ant_paths, costs):
        for ant_index, ant_path in enumerate(ant_paths):
            for location, facility in enumerate(ant_path):
                applied_pheromone = 1 / costs[ant_index]
                self.pheromones[facility][location] += applied_pheromone
            
    
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

if __name__  == "__main__":
    w = World("Uni50a.dat", m=100, e=0.9)
    
    for x in range(1000):
        a = w.generate_ant_paths()
        c,ba = w.calc_fitnesses(a)
        w.apply_pheromones(a,c)
        w.evaporate_pheromones()
        
    