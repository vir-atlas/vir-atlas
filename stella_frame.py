# @authors Brynn and Frank
# @date 4/14/21
# @brief Everything within the STELLA map frame

import tkinter as tk

import annotation
import map_gen

RESOLUTION = 10

class StellaFrame(tk.Frame):
    """constructor for StellaFrame"""
    def __init__(self, master):
        # call constructor for tk.Frame
        tk.Frame.__init__(self, master)

        # I'm still unsure of these values. The width and height of the frame should both be 500
        # Set canvas size and resolution
        self.canvas_size = 2000
        self.width = 840
        self.height = 840
        self.resolution = 100

        self.map_data = map_gen.Map()

        # set the default display mode
        self.mode = 'vis'

        # Create and display the default canvas with start message
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, background='grey')
        self.canvas.pack()
        self.set_canvas()

    """This needs to be called after a file is loaded!"""
    def load_canvases(self):
        # initialize all three canvases
        self.master.stella_frame.map_data.update_map(self.master.stella_frame.canvas_size,
                                                     gps_file=self.master.gps_file,
                                                     stella_file=self.master.stella_file,
                                                     map_file=self.master.map_file)

    """ This needs to be called to add the canvas to the frame"""
    def set_canvas(self):

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

        # bound right clicking to Annotations
        self.canvas.bind("<Button-3>", self.create_annotation)

    """create a new annotation"""
    def create_annotation(self, event):
        # create new Annotation object
        new_annotation = annotation.Annotation(event.x, event.y, "")
        # pass object to AnnotationEditor
        annotation.AnnotationEditor(new_annotation)

    """move"""
    def move_start(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def move_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    """windows zoom"""
    def zoomer(self, event):
        if event.delta > 0:
            self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        elif event.delta < 0:
            self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    """linux zoom"""
    def zoomer_p(self, event):
        self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def zoomer_m(self, event):
        self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    """ Functions for setting a mode (called from menu_bar)"""
    def vis_mode(self):
        self.mode = 'vis'
        self.set_canvas()

    def nir_mode(self):
        self.mode = 'nir'
        self.set_canvas()

    def temp_mode(self):
        self.mode = 'temp'
        self.set_canvas()


class VisFrame(StellaFrame):
    def __init__(self, master):
        super().__init__(master)
        self.mode = "vis"


class NirFrame(StellaFrame):
    def __init__(self, master):
        super().__init__(master)
        self.mode = "nir"
        # master.map_data.gen_map(self.mode, RESOLUTION, self.canvas)


class TempFrame(StellaFrame):
    def __init__(self, master):
        super().__init__(master)
        self.mode = "temp"
        # master.map_data.gen_map(self.mode, RESOLUTION, self.canvas)


class SvaFrame(StellaFrame):
    def __init__(self, master):
        super().__init__(master)
        self.mode = "sva"
        # master.map_data.gen_map(self.mode, RESOLUTION, self.canvas)


class NdviFrame(StellaFrame):
    def __init__(self, master):
        super().__init__(master)
        self.mode = "ndvi"
        # master.map_data.gen_map(self.mode, RESOLUTION, self.canvas)


class EviFrame(StellaFrame):
    def __init__(self, master):
        super().__init__(master)
        self.mode = 'evi'
        # master.map_data.gen_map(self.mode, RESOLUTION, self.canvas)


class SaviFrame(StellaFrame):
    def __init__(self, master):
        super().__init__(master)
        self.mode = "savi"
        # master.map_data.gen_map(self.mode, RESOLUTION, self.canvas)


class MsaviFrame(StellaFrame):
    def __init__(self, master):
        super().__init__(master)
        self.mode = "msavi"
        # master.map_data.gen_map(self.mode, RESOLUTION, self.canvas)
