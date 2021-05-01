#!/usr/bin/env python3
# -*-coding:utf:8 -*-
"""Provides Legend, class for generating the various legends used in vir-atlas

Legend creates a Canvas on which the specified type of legend is drawn and packs
it into the master Frame of vir-atlas. Possible color legend types are TEMP, SVA,
and one legend for all of the following four map types: NDVI, EVI, SAVI, MSAVI.
"""

import tkinter as tk
from tkinter import Frame, BOTH, W
import color as col
from math import floor
import numpy as np

__authors__ = "Timothy Goetsch"
__maintainer__ = "Timothy Goetsch"
__email__ = "timothy.goetsch@student.nmt.edu"


class Legend(Frame):
    """Legend class for legend generation in vir-atlas"""
    def __init__(self, master, mode="vis"):
        """create a new Legend object"""

        Frame.__init__(self, master)

        self.pack(fill=BOTH, expand=1)

        self.width = 110         # set the legend frame width
        self.height = 840        # set the legend frame height

        self.canvas = tk.Canvas(self, width=self.width, height=self.height)

        self.mode = mode        # set the mode type to one of VIR, NIR, TEMP, SVA, NDVI, EVI, SAVI, MSAVI

        if __name__ == '__main__':
            self.min_temp = -40.0
            self.max_temp = 85.0
            self.air_temp = 22.5
        else:
            self.min_temp = master.map_data.min_temp
            self.max_temp = master.map_data.max_temp
            self.air_temp = master.map_data.air_temp

        self.scale = []
        self.set_scale()        # set the scale of legend

        if mode == "temp":
            self.create_temp()
        elif mode == "ndvi" or mode == "evi" or mode == "savi" or mode == "msavi":
            self.create_vi()
        elif mode == "sva":
            self.create_sva()

        self.canvas.pack(fill=BOTH, expand=1)

    def create_temp(self):
        """Create the temperature legend for the TEMP mode"""
        if len(self.scale) == 0:    # if scale is empty return an empty canvas
            return
        color = []
        for i in self.scale:        # try to create the color range with respect to the size of scale
            try:
                color.append(col.false_color(i, self.min_temp, self.max_temp))
            except ValueError:
                print("LEGEND, create_temp: Could not generate color list")
                return

        legend_top = 10
        legend_bottom = self.height - legend_top

        box_top = legend_top
        box_left = 10
        box_right = 50

        box_size = floor((legend_bottom - legend_top) / len(color))
        legend_size = box_size * len(color) + box_top  # keeps the boxes and lines aligned at the bottom of the canvas

        line_x = box_right + 10
        line_y = legend_top

        self.canvas.create_line(line_x, line_y, line_x, legend_size)  # create vertical line for numbering

        for num, c in enumerate(color):
            box_bottom = box_top + box_size
            self.canvas.create_rectangle(box_left, box_top, box_right, box_bottom,
                                         outline=c,
                                         fill=c)
            self.canvas.create_line(line_x, line_y, line_x + 5, line_y)  # draw horizontal component of number line

            if line_y == 0:  # create first box at top of legend
                self.canvas.create_text(line_x + 10, line_y,
                                        anchor=W,
                                        font=("Arial", 10),
                                        text='{:.2f}'.format(self.scale[num]))
            else:  # add box_size to subsequent boxes
                self.canvas.create_text(line_x + 10, line_y + (box_size / 2),
                                        anchor=W,
                                        font=("Arial", 10),
                                        text='{:.2f}'.format(self.scale[num]))
            line_y += box_size
            box_top += box_size
            # print(line_y)

        self.canvas.create_line(line_x, line_y, line_x + 5, line_y)  # create final horizontal component of number line

    def create_vi(self):
        """Create the VI legend for the following modes: NDVI, EVI, SAVI, MSAVI"""
        if len(self.scale) == 0:  # if scale is empty return an empty canvas
            return
        color = []
        for i in self.scale:  # try to create the color range with respect to the size of scale
            try:
                color.append(col.false_color_vi(i))
            except ValueError:
                print("LEGEND, create_vi: Could not generate color list")
                return

        legend_top = 10
        legend_bottom = self.height - legend_top

        box_top = legend_top
        box_left = 10
        box_right = 50

        box_size = floor((legend_bottom - legend_top) / len(color))
        legend_size = box_size * len(color) + box_top  # keeps the boxes and lines aligned at the bottom of the canvas

        line_x = box_right + 10
        line_y = legend_top

        self.canvas.create_line(line_x, line_y, line_x, legend_size)  # create vertical line for numbering

        for num, c in enumerate(color):
            box_bottom = box_top + box_size
            self.canvas.create_rectangle(box_left, box_top, box_right, box_bottom,
                                         outline=c,
                                         fill=c)
            self.canvas.create_line(line_x, line_y, line_x + 5, line_y)  # draw horizontal component of number line

            if line_y == 0:  # create first box at top of legend
                self.canvas.create_text(line_x + 10, line_y,
                                        anchor=W,
                                        font=("Arial", 10),
                                        text='{:.2f}'.format(self.scale[num]))
            else:  # add box_size to subsequent boxes
                self.canvas.create_text(line_x + 10, line_y + (box_size / 2),
                                        anchor=W,
                                        font=("Arial", 10),
                                        text='{:.2f}'.format(self.scale[num]))
            line_y += box_size
            box_top += box_size
            # print(line_y)

        self.canvas.create_line(line_x, line_y, line_x + 5, line_y)  # create final horizontal component of number line

    def create_sva(self):
        """Create the surface temperature vs air temperature legend for the SVA mode"""
        if len(self.scale) == 0:  # if scale is empty return an empty canvas
            return
        color = []

        red = '#ff0000'
        blue = '#0000ff'

        for i in self.scale:  # try to create the color range with respect to the size of scale
            try:
                color.append(col.false_two_color(i, self.min_temp, self.air_temp,
                                                 self.max_temp, blue, red))
            except ValueError:
                print("LEGEND, create_sva: Could not generate color list")
                return

        legend_top = 10
        legend_bottom = self.height - legend_top

        box_top = legend_top
        box_left = 10
        box_right = 50

        box_size = floor((legend_bottom - legend_top) / len(color))
        legend_size = box_size * len(color) + box_top  # keeps the boxes and lines aligned at the bottom of the canvas

        line_x = box_right + 10
        line_y = legend_top

        self.canvas.create_line(line_x, line_y, line_x, legend_size)  # create vertical line for numbering

        for num, c in enumerate(color):
            box_bottom = box_top + box_size
            self.canvas.create_rectangle(box_left, box_top, box_right, box_bottom,
                                         outline=c,
                                         fill=c)
            self.canvas.create_line(line_x, line_y, line_x + 5, line_y)  # draw horizontal component of number line

            if line_y == 0:  # create first box at top of legend
                self.canvas.create_text(line_x + 10, line_y,
                                        anchor=W,
                                        font=("Arial", 10),
                                        text='{:.2f}'.format(self.scale[num]))
            else:  # add box_size to subsequent boxes
                self.canvas.create_text(line_x + 10, line_y + (box_size / 2),
                                        anchor=W,
                                        font=("Arial", 10),
                                        text='{:.2f}'.format(self.scale[num]))
            line_y += box_size
            box_top += box_size
            # print(line_y)

        self.canvas.create_line(line_x, line_y, line_x + 5, line_y)  # create final horizontal component of number line

    def set_scale(self):
        """set the scale for each mode. """
        delta = (self.min_temp - self.max_temp) / 40
        if self.mode == "temp":
            self.scale = np.arange(self.max_temp, self.min_temp, delta)  # 30 values
        elif self.mode == "ndvi" or self.mode == "evi" or self.mode == "savi" or self.mode == "msavi":
            self.scale = np.arange(1, -1.05, -0.05)  # 41 values
        elif self.mode == "sva":
            self.scale = np.arange(self.max_temp, self.min_temp, delta)


def main():
    """creates a standalone frame containing the specified legend type for debugging purposes"""
    legend_type = "ndvi"
    root = tk.Tk()
    frame = tk.Frame()
    cb = Legend(frame, legend_type)
    frame.pack(fill=BOTH, expand=1)
    # root.geometry("110x840+1000+300")  # WIDTH X HEIGHT + Location on screen when opening (WIDTH + HEIGHT)
    root.mainloop()


if __name__ == '__main__':  # run main if called from command-line
    main()
