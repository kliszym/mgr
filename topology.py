from copy import deepcopy
import sys


class Topology:
    def __init__(self):
        self.clear_topology()
        self.clear_shortest()
        self.unique_routers = []
        self.shortest_path_trees = {
            "trees": {

            }
        }

    def clear_topology(self):
        self.topology = {
            "a_router": [],
            "b_router": [],
            "length": []
        }

    def clear_shortest(self):
        self.shortest_template = {
            "a_router": [],
            "b_router": [],
            "length": []
        }

    def print_topology_shortest(self, shortest):
        for i in range(0, len(shortest["a_router"])):
            print(f"{shortest['a_router'][i]} -> {shortest['b_router'][i]} = {shortest['length'][i]}")

    def print_shortest_path_trees(self):
        for tree in self.shortest_path_trees["trees"]:
            print(f"Shortest path tree for router \"{tree}\":")
            self.print_topology_shortest(self.shortest_path_trees["trees"][tree])

    def get_unique_routers(self):
        for router in self.topology["a_router"]:
            if router not in self.unique_routers:
                self.unique_routers.append(router)
        for router in self.topology["b_router"]:
            if router not in self.unique_routers:
                self.unique_routers.append(router)

    def create_shortest_links(self):
        self.get_unique_routers()
        for unique_router in self.unique_routers:
            self.create_shortest_link(unique_router)
        self.print_shortest_path_trees()

    def create_shortest_link(self, router):
        self.shortest_path_trees["trees"][router] = deepcopy(self.shortest_template)
        visited = [False] * len(self.unique_routers)
        visited[router - 1] = True
        self.check_topology_for_router_links(self.shortest_path_trees["trees"][router], router)
        next_router, length = self.find_shortest_not_visited(self.shortest_path_trees["trees"][router], visited, router)
        while next_router != -1:
            visited[next_router - 1] = True
            self.check_shortest_for_router_links(self.shortest_path_trees["trees"][router], router, next_router, length)
            next_router, length = self.find_shortest_not_visited(self.shortest_path_trees["trees"][router], visited, router)

    def check_topology_for_router_links(self, shortest, router):
        for i in range(0, len(self.topology["a_router"])):
            if self.topology["a_router"][i] == router or self.topology["b_router"][i] == router:
                shortest_index = self.find_shortest_link_index(shortest, self.topology["a_router"][i], self.topology["b_router"][i])
                if shortest_index == -1:
                    shortest["a_router"].append(self.topology["a_router"][i])
                    shortest["b_router"].append(self.topology["b_router"][i])
                    shortest["length"].append(self.topology["length"][i])
                elif self.topology["length"][i] < shortest["length"][shortest_index]:
                    shortest["length"][shortest_index] = self.topology["length"][i]

    def check_shortest_for_router_links(self, shortest, base_router, router, base_len=0):
        for i in range(0, len(self.topology["a_router"])):
            if (self.topology["a_router"][i] == router and self.topology["b_router"][i] == base_router) \
                    or (self.topology["a_router"][i] == base_router and self.topology["b_router"][i] == router):
                continue
            if self.topology["a_router"][i] == router:
                shortest_index = self.find_shortest_link_index(shortest, base_router, self.topology["b_router"][i])
                if shortest_index == -1:
                    shortest["a_router"].append(base_router)
                    shortest["b_router"].append(self.topology["b_router"][i])
                    shortest["length"].append(self.topology["length"][i] + base_len)
                elif self.topology["length"][i] + base_len < shortest["length"][shortest_index]:
                    shortest["length"][shortest_index] = self.topology["length"][i] + base_len
            elif self.topology["b_router"][i] == router:
                shortest_index = self.find_shortest_link_index(shortest, base_router, self.topology["a_router"][i])
                if shortest_index == -1:
                    shortest["a_router"].append(base_router)
                    shortest["b_router"].append(self.topology["a_router"][i])
                    shortest["length"].append(self.topology["length"][i] + base_len)
                elif self.topology["length"][i] + base_len < shortest["length"][shortest_index]:
                    shortest["length"][shortest_index] = self.topology["length"][i] + base_len

    def find_shortest_link_index(self, shortest, a, b):
        for i in range(0, len(shortest["a_router"])):
            if (a == shortest["a_router"][i] and b == shortest["b_router"][i])\
                    or (a == shortest["b_router"][i] and b == shortest["a_router"][i]):
                return i
        return -1

    def find_shortest_not_visited(self, shortest_path_tree, visited, router):
        shortest = deepcopy(shortest_path_tree)
        i = 0
        while i != len(shortest["a_router"]):
            max_len = sys.maxsize
            min_len = min(shortest["length"])
            if min_len == max_len:
                return -1, -1
            if shortest["length"][i] == min_len:
                dest_router = shortest["a_router"][i] if shortest["a_router"][i] != router else shortest["b_router"][i]
                if visited[dest_router - 1]:
                    shortest["length"][i] = max_len
                    i = -1
                else:
                    return dest_router, shortest["length"][i]
            i += 1
        return -1, -1
