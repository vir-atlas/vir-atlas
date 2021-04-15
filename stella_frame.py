# @authors Brynn and Frank
# @date 4/14/21
# @brief Everything within the STELLA map frame
# @TODO ake the generated canvases replace the previous. (Need to use teh destroy function)

import tkinter as tk
import map_gen


class StellaFrame(tk.Frame):
    # constructor for StellaFrame @TODO: This needs to be redone
    def __init__(self, master):
        # call constructor for tk.Frame
        tk.Frame.__init__(self, master)

        # I'm still unsure of these values. The width and height of the frame should both be 500
        # Set canvas size and resolution
        self.canvas_size = 700
        self.width = 500
        self.height = 500
        self.resolution = 10

        # set the default display mode
        self.mode = 'vis'

        # Create and display the default empty canvas
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, background='black')
        self.canvas.pack()

        # initialize all three canvases
        self.nir_canvas = self.canvas
        self.vis_canvas = self.canvas
        self.temp_canvas = self.canvas

    # Testing purposes only, actual code commented below
    def load_canvases(self):
        # initialize all three canvases
        self.nir_canvas = tk.Canvas(width=500, height=500, bg="blue")
        self.vis_canvas = tk.Canvas(width=500, height=500, bg="green")
        self.temp_canvas = tk.Canvas(width=500, height=500, bg="red")

    """
    # This needs to be called after a file is loaded!
    def load_canvases(self):
        # initialize all three canvases
        self.nir_canvas = map_gen.get_map_alt(self.master.gps_file, self.master.stella_file,
                                              self.canvas_size, self.resolution, 'nir', self.canvas)
        self.vis_canvas = map_gen.get_map_alt(self.master.gps_file, self.master.stella_file,
                                              self.canvas_size, self.resolution, 'vis', self.canvas)
        # Currently commented out due to color errors (Tries to use "None" color in get_map_alt)
        # self.temp_canvas = map_gen.get_map_alt(self.master.gps_file, self.master.stella_file,
        # self.canvas_size, self.resolution, 'temp', self.canvas)
    """

    # This needs to be called to add the canvas to the frame
    def set_canvas(self):
        # Create and display the default empty canvas
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, background='black')
        self.update()
        self.canvas.destroy()

        # Set the appropriate map
        if self.mode == 'temp':
            self.canvas = self.temp_canvas
        if self.mode == 'vis':
            self.canvas = self.vis_canvas
        if self.mode == 'nir':
            self.canvas = self.nir_canvas

        # bound the scrolling region (needs work?)
        self.canvas.configure(scrollregion=(0, 0, self.width, self.height))

        # This is what enables using the mouse:
        self.canvas.bind("<ButtonPress-1>", self.move_start)
        self.canvas.bind("<B1-Motion>", self.move_move)

        # linux scroll
        self.canvas.bind("<Button-4>", self.zoomer_p)
        self.canvas.bind("<Button-5>", self.zoomer_m)

        # windows scroll
        self.canvas.bind("<MouseWheel>", self.zoomer)

        # place the canvas on the frame
        self.canvas.pack()
        self.canvas.place()

    # move
    def move_start(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def move_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    # windows zoom
    def zoomer(self, event):
        if event.delta > 0:
            self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        elif event.delta < 0:
            self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # linux zoom
    def zoomer_p(self, event):
        self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def zoomer_m(self, event):
        self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # Functions for setting a mode (called from menu_bar)
    def vis_mode(self):
        self.mode = 'vis'
        self.set_canvas()

    def nir_mode(self):
        self.mode = 'nir'
        self.set_canvas()

    def temp_mode(self):
        self.mode = 'temp'
        self.set_canvas()
