import tkinter as tk
import math
from graph import *
from backup_configs_gnerator import BackupConfigsGenerator


class Application(tk.Frame):
    def __init__(self, master=None):
        self.canvas_size = (600, 600)
        self.textbox_size = (22, 30)
        self.drawing_radius = 200
        self.circle_radius = 20
        self.router_color = "blue"
        super().__init__(master)
        self.master = master
        self.pack()
        self.master.title("Networking Simulator")
        self.master.geometry("1000x600")
        self.create_buttons()
        self.create_textbox()
        self.create_canvas()
        self.index = 0
        self.init_graph()

    def create_buttons(self):
        self.button_start = tk.Button(self, text="BASIC", command=self.draw_graph)
        self.button_start.grid(row=0, column=0, rowspan=1, sticky="NESW")

        self.button_next = tk.Button(self, text="NEXT", command=self.draw_next_graph)
        self.button_next.grid(row=1, column=0, rowspan=1, sticky="NESW")

        self.button_quit = tk.Button(self, text="QUIT", command=self.master.destroy)
        self.button_quit.grid(row=2, column=0, rowspan=1, sticky="NESW")

    def create_canvas(self):
        canvas_x, canvas_y = self.canvas_size
        self.canvas = tk.Canvas(self, width=canvas_x, height=canvas_y)
        self.canvas.grid(row=0, column=1, rowspan=20)

    def create_textbox(self):
        textbox_w, textbox_h = self.textbox_size
        self.textbox = tk.Text(self, height=textbox_h, width=textbox_w)
        self.label = tk.Label(self, text="Lengths:")
        self.label.config(font=("Courier", 14))
        self.label.grid(row=3, column=0, rowspan=1, sticky="SW")
        self.textbox.grid(row=4, column=0, rowspan=1, stick=tk.W)
        self.textbox.insert(tk.END, "Example text:")

    def init_graph(self):
        canvas_x, canvas_y = self.canvas_size
        center_x = canvas_x / 2
        center_y = canvas_y / 2
        center = (center_x, center_y)

        self.graph = Graph(center, self.drawing_radius)
        self.graphs = BackupConfigsGenerator(self.graph)
        self.graphs.generate_graphs()

    def draw_routers(self, graph):
        for router in graph.routers:
            point_x, point_y = router.point
            self.draw_circle(point_x, point_y, self.circle_radius, fill=self.router_color)

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

    def draw_graph(self):
        self.index = 0
        self.canvas.delete("all")
        self.draw_links(self.graph)
        self.draw_routers(self.graph)

    def draw_next_graph(self):
        self.canvas.delete("all")
        self.draw_links(self.graphs.graphs[self.index])
        self.draw_routers(self.graphs.graphs[self.index])
        self.index += 1
        if self.index >= len(self.graphs.graphs):
            self.index = 0

    def draw_circle(self, x, y, r, **kwargs):
        self.canvas.create_oval(x - r, y - r, x + r, y + r, **kwargs)


def start_gui():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
