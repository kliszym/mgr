from copy import deepcopy

from topology import Topology


class BackupConfigsGenerator:
    def __init__(self, graph):
        self.topology = Topology()
        self.graph = graph
        self.topologies = []
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
        self.topologies = []
        for graph_index in range(1, self.graph.routers_count + 1):
            self.topologies.append(Topology())
            graph = deepcopy(self.graph)
            graph.maximize_weights(graph_index)
            print(f"Start for node {graph_index} failure:")
            for link in graph.links:
                link.dump_links(self.topologies[len(self.topologies) - 1].topology)
            self.topologies[len(self.topologies) - 1].clear_shortest_path_trees()
            self.topologies[len(self.topologies) - 1].create_shortest_links()
            print(self.topologies[len(self.topologies) - 1].dump_routing_tables())

        similar_indexes = []
        similar_indexes_index = -1
        for topology1_index in range(0, len(self.topologies)):
            first = True
            if self.check_indexes_contain(similar_indexes, topology1_index):
                continue
            for topology2_index in range(0, len(self.topologies)):
                if topology1_index == topology2_index:
                    continue
                routing_table1 = self.topologies[topology1_index].dump_routing_tables()
                routing_table2 = self.topologies[topology2_index].dump_routing_tables()

                if self.check_routing_tables_equality(routing_table1, routing_table2):
                    if first:
                        first = False
                        similar_indexes_index += 1
                        similar_indexes.append([topology1_index, topology2_index])
                    else:
                        similar_indexes[similar_indexes_index].append(topology2_index)

        print(similar_indexes)
            # print(f"{self.topologies[len(self.topologies) - 1].shortest_path_trees}")

    def compute_author(self):
        self.topologies = []
        for graph_index in range(1, self.graph.routers_count + 1):
            self.topologies.append(Topology())
            links = self.topology.dump_shortest_links(graph_index)
            for link in links:
                graph = deepcopy(self.graph)
                graph_router_a, graph_router_b = link
                graph.maximize_weights(graph_router_a, graph_router_b)
                print(f"Start for link {graph_router_a} -> {graph_router_b} failure:")
                for link in graph.links:
                    link.dump_links(self.topologies[len(self.topologies) - 1].topology)
                self.topologies[len(self.topologies) - 1].clear_shortest_path_trees()
                self.topologies[len(self.topologies) - 1].create_shortest_links()
                print(f"{self.topologies[len(self.topologies) - 1].shortest_path_trees}")

    def check_indexes_contain(self, indexes, element):
        contains = False
        for indexes_arrays in indexes:
            for array_element in indexes_arrays:
                if element == array_element:
                    contains = True
        return contains

    def check_routing_tables_equality(self, routing_table_1, routing_table_2):
        for entry in routing_table_1:
            if entry not in routing_table_2:
                print(f"In routing table {routing_table_2} is no entry {entry}.")
                return False
        for entry in routing_table_2:
            if entry not in routing_table_1:
                print(f"In routing table {routing_table_1} is no entry {entry}.")
                return False
        return True
