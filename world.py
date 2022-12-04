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
            
if __name__  == "__main__":
    w = World("Uni50a.dat")