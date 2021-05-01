# !/usr/bin/env python3
# -*-coding:utf-8 -*-
""" Run file for VIR-Atlas

Root Contains functions for swapping frames and updating information
Provides primary interactions with frames and the menubar
Uses Tkinter to create a window and show images
"""

import tkinter as tk
import menu_bar as menu
import map_gen
import legend
import satellite_image
from satellite_frame import SatelliteFrame
import annotation

__authors__ = ["Tyler Brynn Charity", "Franklin Keithley"]
__maintainer__ = "Tyler Brynn Charity"
__email__ = "tyler.charity@student.nmt.edu"

class Root(tk.Tk):
    """Main window constructor. Holds data files and a Map Object as well as Tk frames """
    def __init__(self):
        tk.Tk.__init__(self)

        self.geometry('1450x900')
        self.winfo_toplevel().title("VIR-Atlas")

        # Initialize data files
        self.stella_file = ''
        self.gps_file = ''
        self.map_file = ''
        self.satellite_image = ''
        self.satellite_coords = None
        # List of accepted types for user uploaded satellite images. Feel free to add.
        self.image_formats = [("image", ".jpeg"), ("image", ".png"), ("image", ".jpg")]

        self.map_data = map_gen.Map()
        self.resolution = 10  # default value. Might want to let user change this. The smaller, the more polygons in a map

        # Add default instructional canvas upon startup
        self.startup_message = tk.Canvas(width=840, height=840, bg="grey")
        self.startup_message.create_text(420, 420, font="Times 15", justify="center",
                                         text="Welcome to VIR - Atlas!\nTo get started,"
                                              " go to\nFiles -> Open New File")
        self.startup_message.place(y=20, x=20)

        # Initialize frames
        self.stella_frame = None
        self.legend_frame = None
        self.annotation_frame = None
        self.satellite_frame = None

        # Add the menu_bar to the main window
        menu_bar = menu.MenuBar(self)
        self.config(menu=menu_bar)

    def set_stella_data(self, file):
        """ Root's stella_file set to a STELLA csv file provided by the user """

        self.stella_file = file

    def set_gps_data(self, file):
        """ Root's gps_file set to a drone csv file provided by the user """

        self.gps_file = file

    def set_map_data(self, file):
        """ Root's map_file set to a .vmap file provided by the user """

        self.map_file = file

    def set_sat_file(self, file):
        """ If displaying an image, set the image to a file provided by the user """

        self.satellite_image = file

    def switch_frame(self, frame_class):
        """  If swapping Stella frames, set appropriate data and switch display

        Generates the new map based on the frame_class selected
        Swap legend_frame to the corresponding legend
        """

        new_frame = frame_class(self)
        self.map_data.gen_map(new_frame.mode, self.resolution, new_frame.canvas)

        if self.stella_frame is not None:
            self.stella_frame.destroy()
        self.stella_frame = new_frame
        self.stella_frame.place(x=20, y=20)

        # Switch legend to match current map
        new_legend = legend.Legend(self, self.stella_frame.mode)
        if self.legend_frame is not None:
            self.legend_frame.destroy()
        self.legend_frame = new_legend
        self.legend_frame.place(x=880, y=20)

    def get_annotation(self):
        """ Places and activates annotation frame """
        if self.annotation_frame is not None:
            self.annotation_frame.destroy()

        annotation.set_map_list(self.map_data.map_list, self.map_data.scale)
        self.annotation_frame = annotation.AnnotationFrame(self)
        self.annotation_frame.config(height=420, width=420, bg='#007BA7')
        self.annotation_frame.place(x=1010, y=460)

    def get_satellite(self):
        """ If generating a satellite image, get from gps coordinates and swap frame """

        self.satellite_coords = map_gen.get_pairs(self.map_data.map_list)
        self.satellite_image = satellite_image.get_satellite_image(self.satellite_coords)
        print(self.satellite_image)

        if self.satellite_frame is not None:
            self.satellite_frame.destroy()
        # self.satellite_frame = new_frame

        self.satellite_frame = tk.Frame(self)
        self.satellite_frame.config(height=420, width=420, bg='blue')
        print(self.satellite_image)
        SatelliteFrame(self.satellite_frame, self.satellite_image)
        self.satellite_frame.place(x=1010, y=20)

    def get_satellite_upload(self):
        """ If displaying an uploaded image, get image and swap frame to image """
        if self.satellite_frame is not None:
            self.satellite_frame.destroy()

        self.satellite_frame = tk.Frame(self)
        self.satellite_frame.config(height=420, width=420, bg='blue')
        SatelliteFrame(self.satellite_frame, self.satellite_image)
        self.satellite_frame.place(x=1010, y=20)

    def get_satellite_upload(self):
       # new_frame = SatelliteFrame(self, self.satellite_image)
        if self.satellite_frame is not None:
            self.satellite_frame.destroy()
        # self.satellite_frame = new_frame

        self.satellite_frame = tk.Frame(self)
        self.satellite_frame.config(height=420, width=420, bg='blue')
        print(self.satellite_image)
        SatelliteFrame(self.satellite_frame, self.satellite_image)
        self.satellite_frame.place(x=1010, y=20)

if __name__ == "__main__":
    root = Root()
    annotation.get_root(root)
    root.mainloop()
