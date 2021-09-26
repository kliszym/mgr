import tkinter as tk
from graph import *
from backup_configs_gnerator import BackupConfigsGenerator


class Application(tk.Frame):
    def __init__(self, master=None):
        self.row_ptr = 0
        self.canvas_size = (600, 600)
        self.textbox_size = (22, 20)
        self.textbox_path_size = (1, 1)
        self.drawing_radius = 200
        self.circle_radius = 20
        self.router_color = "blue"
        super().__init__(master)
        self.master = master
        self.pack()
        self.master.title("Networking Simulator")
        self.master.geometry("1000x600")
        self.create_buttons()
        self.create_path_gui()
        self.create_textbox()
        self.create_canvas()
        self.index = 0
        self.init_graph()

    def create_buttons(self):
        self.button_start = tk.Button(self, text="BASIC", command=self.draw_graph)
        self.button_start.grid(row=self.row_ptr, column=0, rowspan=1, columnspan=2, sticky="NESW")
        self.row_ptr += 1

        self.button_next = tk.Button(self, text="DEL NEXT", command=self.draw_next_graph)
        self.button_next.grid(row=self.row_ptr, column=0, rowspan=1, columnspan=2, sticky="NESW")
        self.row_ptr += 1

        self.button_load = tk.Button(self, text="LOAD", command=self.load_graph)
        self.button_load.grid(row=self.row_ptr, column=0, rowspan=1, columnspan=2, sticky="NESW")
        self.row_ptr += 1

        self.button_reset = tk.Button(self, text="RESET", command=self.reset_graph)
        self.button_reset.grid(row=self.row_ptr, column=0, rowspan=1, columnspan=2, sticky="NESW")
        self.row_ptr += 1

        self.button_quit = tk.Button(self, text="QUIT", command=self.master.destroy)
        self.button_quit.grid(row=self.row_ptr, column=0, rowspan=1, columnspan=2, sticky="NESW")
        self.row_ptr += 1

    def create_path_gui(self):
        self.button_path = tk.Button(self, text="PATH", command=self.compute_path)
        self.button_path.grid(row=self.row_ptr, column=0, rowspan=1, columnspan=1, sticky="NESW")
        textbox_w, textbox_h = self.textbox_path_size
        self.textbox_path = tk.Text(self, height=textbox_h, width=textbox_w)
        self.textbox_path.grid(row=self.row_ptr, column=1, rowspan=1, columnspan=1, sticky="NESW")
        self.row_ptr += 1


    def load_graph(self):
        text = self.textbox.get('0.0', tk.END)
        self.init_graph(text)
        self.draw_graph()

    def create_canvas(self):
        canvas_x, canvas_y = self.canvas_size
        self.canvas = tk.Canvas(self, width=canvas_x, height=canvas_y)
        self.canvas.grid(row=0, column=3, rowspan=20)

    def create_textbox(self):
        textbox_w, textbox_h = self.textbox_size
        self.textbox = tk.Text(self, height=textbox_h, width=textbox_w)
        self.label = tk.Label(self, text="Lengths:")
        self.label.config(font=("Courier", 14))
        self.label.grid(row=self.row_ptr, column=0, rowspan=1, sticky="SW")
        self.row_ptr += 1
        self.textbox.grid(row=self.row_ptr, column=0, rowspan=1, stick=tk.W)
        self.row_ptr += 1

    def init_graph(self, text=None):
        canvas_x, canvas_y = self.canvas_size
        center_x = canvas_x / 2
        center_y = canvas_y / 2
        center = (center_x, center_y)

        self.graph = Graph(center, self.drawing_radius, text)
        self.graphs = BackupConfigsGenerator(self.graph)
        self.graphs.generate_graphs()

    def draw_routers(self, graph):
        for router in graph.routers:
            point_x, point_y = router.point
            self.draw_circle(point_x, point_y, self.circle_radius, fill=self.router_color)
            self.canvas.create_text(point_x, point_y, text=str(router.id))

        self.canvas.create_rectangle(10, 10, self.canvas.winfo_width() - 10, self.canvas.winfo_height() - 10)

    def draw_links(self, graph):
        for link in graph.links:
            for router2 in link.links:
                router = next((router for router in graph.routers if router.id == link.router), None)
                if router is None:
                    continue
                point1_x, point1_y = router.point
                router = next((router for router in graph.routers if router.id == router2), None)
                if router is None:
                    continue
                point2_x, point2_y = router.point
                self.canvas.create_line(point1_x, point1_y, point2_x, point2_y)

    def draw_spt(self, graph, graphs, spt_router):
        leafs = graphs.topology.shortest_path_trees["trees"][spt_router]
        print(leafs)
        for index in range(0, len(leafs["a_router"])):
            for through in range(0, len(leafs["through"][index]) - 1):
                router1 = leafs["through"][index][through]
                router2 = leafs["through"][index][through + 1]
                print(f"router1: {router1}, router2: {router2}")
                router = next((router for router in graph.routers if router.id == router1), None)
                if router is None:
                    continue
                point1_x, point1_y = router.point
                router = next((router for router in graph.routers if router.id == router2), None)
                if router is None:
                    continue
                point2_x, point2_y = router.point
                self.canvas.create_line(point1_x, point1_y, point2_x, point2_y, fill="#FF0000")

    def draw_graph(self):
        graph = self.graph
        self.index = 0
        self.canvas.delete("all")
        self.draw_links(graph)
        self.draw_routers(graph)
        self.describe_graph(graph)

    def draw_next_graph(self):
        graph = self.graphs.graphs[self.index]
        self.canvas.delete("all")
        self.draw_links(graph)
        self.draw_routers(graph)
        self.describe_graph(graph)
        self.index += 1
        if self.index >= len(self.graphs.graphs):
            self.index = 0

    def draw_circle(self, x, y, r, **kwargs):
        self.canvas.create_oval(x - r, y - r, x + r, y + r, **kwargs)

    def describe_graph(self, graph):
        self.textbox.delete('0.0', tk.END)
        self.textbox.insert('0.0', str(graph))

    def compute_path(self):
        router = int(self.textbox_path.get('0.0', tk.END))
        self.graphs.compute_dijkstry()
        self.draw_spt(self.graph, self.graphs, router)
        self.draw_routers(self.graph)

    def reset_graph(self):
        self.init_graph()
        self.draw_graph()


def start_gui():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
