

class World:
    def __init__(self, filename):
        print("Initializing World with {}".format(filename))
        with open(filename, "r") as f:
            data = f.read().split("\n")
            for i in range(len(data)):
                data[i] = data[i].split(" ")
                data[i] = list(filter(None, data[i]))

            data = [item for item in data if item != []]

            self.n_nodes = int(data.pop(0)[0])

            print("Number of nodes to place: {}".format(self.n_nodes))
if __name__  == "__main__":
    w = World("Uni50a.dat")