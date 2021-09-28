from copy import deepcopy
import sys


class Topology:
    def __init__(self):
        self.clear_topology()
        self.clear_shortest()
        self.unique_routers = []
        self.clear_shortest_path_trees()

    def clear_shortest_path_trees(self):
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
            "length": [],
            "through": []
        }

    def dump_shortest_links(self, node):
        ret = []
        for tree in self.shortest_path_trees["trees"]:
            if tree == node:
                spt = self.shortest_path_trees["trees"][tree]
                for links in spt['through']:
                    for link_index in range(0, len(links) - 1):
                        if ((links[link_index], links[link_index + 1]) not in ret) \
                                and ((links[link_index + 1], links[link_index]) not in ret):
                            ret.append((links[link_index], links[link_index + 1]))
        return ret

    def print_topology_shortest(self, shortest):
        for i in range(0, len(shortest["a_router"])):
            print(
                f"{shortest['a_router'][i]} -> {shortest['b_router'][i]} = {shortest['length'][i]}\t{shortest['through'][i]}")

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

    #        self.print_shortest_path_trees()

    def create_shortest_link(self, router):
        self.shortest_path_trees["trees"][router] = deepcopy(self.shortest_template)
        visited = [False] * len(self.unique_routers)
        visited[router - 1] = True
        self.check_topology_for_router_links(self.shortest_path_trees["trees"][router], router)
        next_router, length, through = self.find_shortest_not_visited(self.shortest_path_trees["trees"][router],
                                                                      visited, router)
        while next_router != -1:
            visited[next_router - 1] = True
            self.check_shortest_for_router_links(self.shortest_path_trees["trees"][router], router, next_router, length,
                                                 through)
            next_router, length, through = self.find_shortest_not_visited(self.shortest_path_trees["trees"][router],
                                                                          visited, router)

    def check_topology_for_router_links(self, shortest, router):
        for i in range(0, len(self.topology["a_router"])):
            if self.topology["length"][i] == sys.maxsize:
                continue
            if self.topology["a_router"][i] == router or self.topology["b_router"][i] == router:
                shortest_index = self.find_shortest_link_index(shortest, self.topology["a_router"][i],
                                                               self.topology["b_router"][i])
                if shortest_index == -1:
                    shortest["a_router"].append(self.topology["a_router"][i])
                    shortest["b_router"].append(self.topology["b_router"][i])
                    shortest["length"].append(self.topology["length"][i])
                    if self.topology["a_router"][i] == router:
                        shortest["through"].append([self.topology["a_router"][i], self.topology["b_router"][i]])
                    else:
                        shortest["through"].append([self.topology["b_router"][i], self.topology["a_router"][i]])
                elif self.topology["length"][i] < shortest["length"][shortest_index]:
                    shortest["length"][shortest_index] = self.topology["length"][i]
                    if self.topology["a_router"][i] == router:
                        shortest["through"][shortest_index].append(self.topology["b_router"][i])
                    else:
                        shortest["through"][shortest_index].append(self.topology["a_router"][i])

    def check_shortest_for_router_links(self, shortest, base_router, router, base_len=0, through=[]):
        for i in range(0, len(self.topology["a_router"])):
            if self.topology["length"][i] == sys.maxsize:
                continue
            if (self.topology["a_router"][i] == router and self.topology["b_router"][i] == base_router) \
                    or (self.topology["a_router"][i] == base_router and self.topology["b_router"][i] == router):
                continue
            if self.topology["a_router"][i] == router:
                shortest_index = self.find_shortest_link_index(shortest, base_router, self.topology["b_router"][i])
                if shortest_index == -1:
                    shortest["a_router"].append(base_router)
                    shortest["b_router"].append(self.topology["b_router"][i])
                    shortest["length"].append(self.topology["length"][i] + base_len)
                    shortest["through"].append(through + [self.topology["b_router"][i]])
                elif self.topology["length"][i] + base_len < shortest["length"][shortest_index]:
                    shortest["length"][shortest_index] = self.topology["length"][i] + base_len
                    shortest["through"][shortest_index] = through + [self.topology["b_router"][i]]

            elif self.topology["b_router"][i] == router:
                shortest_index = self.find_shortest_link_index(shortest, base_router, self.topology["a_router"][i])
                if shortest_index == -1:
                    shortest["a_router"].append(base_router)
                    shortest["b_router"].append(self.topology["a_router"][i])
                    shortest["length"].append(self.topology["length"][i] + base_len)
                    shortest["through"].append(through + [self.topology["a_router"][i]])
                elif self.topology["length"][i] + base_len < shortest["length"][shortest_index]:
                    shortest["length"][shortest_index] = self.topology["length"][i] + base_len
                    shortest["through"][shortest_index] = through + [self.topology["a_router"][i]]

    def find_shortest_link_index(self, shortest, a, b):
        for i in range(0, len(shortest["a_router"])):
            if (a == shortest["a_router"][i] and b == shortest["b_router"][i]) \
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
                return -1, -1, []
            if shortest["length"][i] == min_len:
                dest_router = shortest["a_router"][i] if shortest["a_router"][i] != router else shortest["b_router"][i]
                if visited[dest_router - 1]:
                    shortest["length"][i] = max_len
                    i = -1
                else:
                    return dest_router, shortest["length"][i], shortest["through"][i]
            i += 1
        return -1, -1, []

    def dump_routing_tables(self):
        routing_tables = []
        for tree_id in self.shortest_path_trees["trees"]:
            tree = self.shortest_path_trees["trees"][tree_id]
            for path in tree["through"]:
                # destionation, managment router, next-hop
                routing_tables.append([path[len(path) - 1], path[0], path[1]])
        return routing_tables

    def dump_costs(self, failed_node=None):
        costs_tables = []
        for tree_id in self.shortest_path_trees["trees"]:
            if failed_node == tree_id:
                continue
            tree = self.shortest_path_trees["trees"][tree_id]
            for links in tree["through"]:
                if links[len(links) - 1] == failed_node or links[0] == failed_node:
                    continue
                # destionation, managment router, next-hop
                sum = 0
                for link_index in range(0, len(links) - 1):
                    sum += self.find_cost(links[link_index], links[link_index + 1])
                costs_tables.append({
                    "router_a": links[0],
                    "router_b": links[len(links) - 1],
                    "cost": sum})

        return costs_tables

    def find_cost(self, router_a, router_b):
        spt_a = self.shortest_path_trees["trees"][router_a]
        print(spt_a)

        for index in range(0, len(spt_a["a_router"])):
            if (spt_a["a_router"][index] == router_a and spt_a["b_router"][index] == router_b) \
                    or (spt_a["a_router"][index] == router_b and spt_a["b_router"][index] == router_a):
                return spt_a["length"][index]
        return sys.maxsize
