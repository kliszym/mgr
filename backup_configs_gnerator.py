from copy import deepcopy

from topology import Topology


class BackupConfigsGenerator:
    def __init__(self, graph):
        self.topology = Topology()
        self.graph = graph
        self.graphs = []

    def generate_graphs(self):
        for i in range(1, self.graph.routers_count + 1):
            temp_graph = deepcopy(self.graph)
            temp_graph.delete_router(i)
            self.graphs.append(temp_graph)

    def compute_dijkstry(self):
        self.topology.clear_topology()
        for link in self.graph.links:
            link.dump_links(self.topology.topology)
        print(self.topology.topology)
        self.topology.clear_shortest_path_trees()
        self.topology.create_shortest_links()

    def compute_mrc(self):
        pass
