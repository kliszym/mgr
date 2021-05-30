from copy import deepcopy


class BackupConfigsGenerator:
    def __init__(self, graph):
        self.graph = graph
        self.graphs = []

    def generate_graphs(self):
        for i in range(1, self.graph.routers_count + 1):
            temp_graph = deepcopy(self.graph)
            temp_graph.delete_router(i)
            self.graphs.append(temp_graph)
