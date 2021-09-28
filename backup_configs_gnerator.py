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
        topologies = []
        for graph_index in range(1, self.graph.routers_count + 1):
            topologies.append(Topology())
            graph = deepcopy(self.graph)
            graph.maximize_weights(graph_index)
            for link in graph.links:
                link.dump_links(topologies[len(topologies) - 1].topology)
            topologies[len(topologies) - 1].clear_shortest_path_trees()
            topologies[len(topologies) - 1].create_shortest_links()
        return topologies

    def compute_author(self):
        topologies = []
        for graph_index in range(1, self.graph.routers_count + 1):
            topologies.append(Topology())
            links = self.topology.dump_shortest_links(graph_index)
            for link in links:
                graph = deepcopy(self.graph)
                graph_router_a, graph_router_b = link
                graph.maximize_weights(graph_router_a, graph_router_b)
                for link in graph.links:
                    link.dump_links(topologies[len(topologies) - 1].topology)
                topologies[len(topologies) - 1].clear_shortest_path_trees()
                topologies[len(topologies) - 1].create_shortest_links()
        return topologies

    def find_all_costs(self, topologies):
        costs = []
        for topology_index in range(0, len(topologies)):
            costs += (topologies[topology_index].dump_costs(topology_index + 1))
        return costs

    def find_unique_costs(self, costs_a, costs_b):
        index_a = 0
        while index_a < len(costs_a):
            entry = costs_a[index_a]
            alternate_entry = {
                "router_a": entry["router_b"],
                "router_b": entry["router_a"],
                "cost": entry["cost"]
            }
            index_b = 0
            while index_b < len(costs_b):
                if costs_b[index_b] == entry or costs_b[index_b] == alternate_entry:
                    del(costs_a[index_a])
                    del(costs_b[index_b])
                    index_a -= 1
                    break
                index_b += 1
            index_a += 1

    def find_max_cost(self, costs_a, costs_b):
        max_cost = 0
        max_node_a = dict()
        max_node_b = dict()
        index_a = 0
        while index_a < len(costs_a):
            index_b = 0
            entry_a = costs_a[index_a]
            while index_b < len(costs_b):
                entry_b = costs_b[index_b]
                if entry_a["router_a"] == entry_b["router_a"] and entry_a["router_b"] == entry_b["router_b"] \
                        or entry_a["router_a"] == entry_b["router_b"] and entry_a["router_b"] == entry_b["router_a"]:
                    if abs(entry_a["cost"] - entry_b["cost"]) > max_cost:
                        max_cost = entry_a["cost"] - entry_b["cost"]
                        max_node_a = entry_a
                        max_node_b = entry_b
                index_b += 1
            index_a += 1
        return max_cost, max_node_a, max_node_b

    def costs_dict_to_array(self, costs_dict):
        ret = []
        for entry in costs_dict:
            ret.append(entry["cost"])
        return ret

    def find_unique_routing_table_options(self, topologies):
        uniques = dict()
        uniques_count = dict()
        for router1 in range(1, self.graph.routers_count + 1):
            for router2 in range(1, self.graph.routers_count + 1):
                if router1 == router2:
                    continue
                key = str(router1) + "->" + str(router2)
                uniques[key] = []
                uniques_count[key] = 0
                for topology_index in range(0, len(topologies)):
                    routing_table = topologies[topology_index].dump_routing_tables()
                    for entry in routing_table:
                        if entry[1] == router1 and entry[0] == router2:
                            if entry not in uniques[key]:
                                uniques[key].append(entry)
                                uniques_count[key] += 1
        sum = 0
        for count in uniques_count.keys():
            sum += uniques_count[count]
        print(sum)

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
                print(f"In routing table {routing_table_2} has no entry {entry}.")
                return False
        for entry in routing_table_2:
            if entry not in routing_table_1:
                print(f"In routing table {routing_table_1} has no entry {entry}.")
                return False
        print(f"Routing table {routing_table_1} is equal to {routing_table_2}.")
        return True
