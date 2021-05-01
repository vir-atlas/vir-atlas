# !/usr/bin/env python3
# -*-coding:utf-8 -*-
""" Handles Map details, user interactions, and map mode

StellaFrame Subclasses are for each type of map and switch the map mode.
Class functions handle zooming and scrolling
"""

import tkinter as tk
import annotation
import map_gen

RESOLUTION = 10

__authors__ = ["Tyler Brynn Charity", "Franklin Keithley"]
__maintainer__ = "Tyler Brynn Charity"
__email__ = "tyler.charity@student.nmt.edu"


class StellaFrame(tk.Frame):
    """ constructor for StellaFrame """
    def __init__(self, master):
        # call constructor for tk.Frame
        tk.Frame.__init__(self, master)

        # I'm still unsure of these values. The width and height of the frame should both be 500
        # Set canvas size
        self.canvas_size = 2000
        self.width = 840
        self.height = 840

        self.map_data = map_gen.Map()

        # set the default display mode
        self.mode = 'vis'

        # Create and display the default canvas with start message
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, background='grey')
        self.canvas.pack()
        self.set_canvas()

    def load_canvases(self):
        """ Initialize the data for the map """
        self.master.stella_frame.map_data.update_map(self.master.stella_frame.canvas_size,
                                                     gps_file=self.master.gps_file,
                                                     stella_file=self.master.stella_file,
                                                     map_file=self.master.map_file)

    def set_canvas(self):
        """ Sets canvas to frame and events such as scrolling and zooming """

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

    def create_annotation(self, event):
        """ handles annotation additions to the map """
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


class VisFrame(StellaFrame):
    """ Frame for Visual Light Spectrum """
    def __init__(self, master):
        super().__init__(master)
        self.mode = "vis"


class NirFrame(StellaFrame):
    """ Frame for Near-Infrared Light spectrum """
    def __init__(self, master):
        super().__init__(master)
        self.mode = "nir"


class TempFrame(StellaFrame):
    """ Frame for Surface Temperature """
    def __init__(self, master):
        super().__init__(master)
        self.mode = "temp"

class SvaFrame(StellaFrame):
    """ Frame for Surface vs Air Temperature """
    def __init__(self, master):
        super().__init__(master)
        self.mode = "sva"


class NdviFrame(StellaFrame):
    """ Normalized Difference Vegetation Index Frame """
    def __init__(self, master):
        super().__init__(master)
        self.mode = "ndvi"


class EviFrame(StellaFrame):
    """ Enhanced Vegetation Index Frame """
    def __init__(self, master):
        super().__init__(master)
        self.mode = 'evi'


class SaviFrame(StellaFrame):
    """ Soil Adjusted Vegetation Index Frame """
    def __init__(self, master):
        super().__init__(master)
        self.mode = "savi"


class MsaviFrame(StellaFrame):
    """ Modified Soil Adjusted Vegetation Index Frame """
    def __init__(self, master):
        super().__init__(master)
        self.mode = "msavi"
