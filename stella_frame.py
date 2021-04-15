# @authors Brynn and Frank
# @date 4/14/21
# @brief Everything within the STELLA map frame
# @TODO everything lol

import tkinter as tk
import map_gen


class StellaFrame(tk.Frame):
    # constructor for StellaFrame @TODO: This needs to be redone
    def __init__(self, master):
        # call constructor for tk.Frame
        tk.Frame.__init__(self, master)

        # I'm still unsure of these values. The width and height of the frame should both be 500
        # Set canvas size and resolution
        self.canvas_size = 500
        self.width = 500
        self.height = 500
        self.resolution = 100

        # initialize all three canvases
        self.nir_canvas = map_gen.get_map(master.gps_file, master.stella_file,
                                          self.canvas_size, self.resolution, 'nir')
        self.vis_canvas = map_gen.get_map(master.gps_file, master.stella_file,
                                          self.canvas_size, self.resolution, 'vis')
        self.temp_canvas = map_gen.get_map(master.gps_file, master.stella_file,
                                           self.canvas_size, self.resolution, 'temp')

        # set the default display mode
        self.mode = 'temp'

        # Create the default empty canvas
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, background='grey')

    # This needs to be called after a file is loaded to display the map
    def set_canvas(self):
        if self.mode == 'temp':
            self.canvas = self.temp_canvas
        if self.mode == 'vis':
            self.canvas = self.vis_canvas
        if self.mode == 'nir':
            self.canvas = self.nir_canvas

        # bound the scrolling region (needs work?)
        # @TODO: Need to figure out what to use in place of window_width
        self.canvas.configure(scrollregion=(0, 0, self.width, self.height))

        # place the canvas on the frame
        self.canvas.place()

        # This is what enables using the mouse:
        self.canvas.bind("<ButtonPress-1>", self.move_start)
        self.canvas.bind("<B1-Motion>", self.move_move)

        # linux scroll
        self.canvas.bind("<Button-4>", self.zoomer_p)
        self.canvas.bind("<Button-5>", self.zoomer_m)

        # windows scroll
        self.canvas.bind("<MouseWheel>", self.zoomer)

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

