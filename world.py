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
            
            
    def generate_ant_paths(self, m=1):
        ants = []
        rng = SystemRandom()
        
        # for each ant
        for _ in range(m):
            # Facilities lists the facilities that haven't yet been visited
            facilities = [i for i in range(self.n_nodes)]
            # random placement
            ant_path = []
            ant_path.append(rng.randint(0,self.n_nodes-1))
            facilities.remove(ant_path[0])
            
            current_node = ant_path[0]
            
            # for each facility
            for _ in range(self.n_nodes-1):
                # getting the weights of each path
                weights = []
                for f in facilities:
                    weights.append(self.distances[current_node][f])

                # Picking next node to visit from facilities using weights
                next_node = rng.choices(facilities, weights=weights, k=1)[0]          
                
                ant_path.append(next_node)               
                current_node = next_node
                
            ants.append(ant_path)
        
        return ants
        
if __name__  == "__main__":
    w = World("Uni50a.dat")
    a = w.generate_ant_paths()