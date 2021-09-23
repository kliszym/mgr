from data import data
import math


class Router:
    def __init__(self, r_id, point):
        self.id = r_id
        self.point = point


class Link:
    def __init__(self, router, links, lengths):
        self.router = router
        self.links = links
        self.lengths = lengths

    def __str__(self):
        return f"{self.router}->{self.links} ({self.lengths})"

    def delete_router(self, router):
        index = 0
        for link in self.links:
            if router == link:
                self.links.pop(index)
                self.lengths.pop(index)
                break
            index += 1

    def dump_links(self, topology):
        for link, length in zip(self.links, self.lengths):
            topology["a_router"].append(self.router)
            topology["b_router"].append(link)
            topology["length"].append(length)


class Graph:
    def __init__(self, center, radius, text = None):
        if text is None:
            self.routers_count = data["routers_count"]
            self.routers = []
            points = self._routers_points(center, radius)
            self._create_routers(points)
            self.links = []
            for key in data["routers"]:
                self.links.append(Link(key, data["routers"][key]["links"], data["routers"][key]["lengths"]))
        else:
            data_text = self.process_text(text)
            self.routers_count = data_text["routers_count"]
            self.routers = []
            points = self._routers_points(center, radius)
            self._create_routers(points)
            self.links = []
            for key in data_text["routers"]:
                self.links.append(Link(key, data_text["routers"][key]["links"], data_text["routers"][key]["lengths"]))

    def __str__(self):
        str = ""
        for link in self.links:
            str += f"{link}\n"
        return str

    def _routers_points(self, center, radius):
        x_center, y_center = center
        points = []
        count_list = range(0, self.routers_count)
        angles = [(2 * math.pi/self.routers_count) * i for i in count_list]
        for angle in angles:
            x = x_center + radius * math.cos(angle)
            y = y_center + radius * math.sin(angle)
            points.append((x, y))
        return points

    def _create_routers(self, points):
        i = 1
        for point in points:
            self.routers.append(Router(i, point))
            i += 1

    def delete_router(self, router_id):
        to_delete = None
        for router in self.routers:
            if router.id == router_id:
                to_delete = router
                self.routers_count -= 1
                break

        if to_delete is not None:
            self.routers.remove(to_delete)

        to_delete = None
        for link in self.links:
            if link.router == router_id:
                to_delete = link
            link.delete_router(router_id)

        if to_delete is not None:
            self.links.remove(to_delete)

    def process_text(self, text):
        data_text = {
            "routers_count": 0,
            "routers": {

            }
        }
        text_lines = text.split("\n")
        max_router = 0
        for line in text_lines:
            if not line:
                continue
            print(data_text["routers_count"])
            routers_and_rest = line.split("->")
            router = int(routers_and_rest[0])
            if router > max_router:
                max_router = router
            data_text["routers"][router] = {
                "links": [],
                "lengths": []
            }
            print(routers_and_rest)
            routers_and_rest[1] = routers_and_rest[1].replace("[", "")
            routers_and_rest[1] = routers_and_rest[1].replace("]", "")
            routers_and_rest[1] = routers_and_rest[1].replace(")", "")
            routers_and_rest[1] = routers_and_rest[1].replace(" ", "")
            links_and_lengths = routers_and_rest[1].split("(")
            print(links_and_lengths)
            print("\n")
            links = links_and_lengths[0].split(",")
            links = list(map(int, links))
            lengths = links_and_lengths[1].split(",")
            lengths = list(map(int, lengths))
            data_text["routers"][router]["links"] = links
            data_text["routers"][router]["lengths"] = lengths
            temp_max_router = max(links)
            if temp_max_router > max_router:
                max_router = temp_max_router
        data_text["routers_count"] = max_router
        print(data_text)
        return data_text

