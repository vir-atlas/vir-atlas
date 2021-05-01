# !/usr/bin/env python3
# -*-coding:utf-8 -*-
""" Houses all components and functions of the top menu

3 Dropdowns
File: Allows users to upload new data files, upload an old data file, save, or exit the program
View: Allows users to swap which map is being displayed (8 Options as of April 2021)
Satellite: Get generates an image from data if dataset is large enough. Upload allows user to upload an image.
"""

import tkinter as tk
from tkinter import filedialog
import sys
import stella_frame

__authors__ = ["Tyler Brynn Charity"]
__maintainer__ = "Tyler Brynn Charity"
__email__ = "tyler.charity@student.nmt.edu"

# currently disabled
def about():
    """ Creates a new window with helpful information """
    about_window = tk.Tk()
    about_window.title("About")
    about_window.geometry("400x300")

    tk.Label(about_window,
             text="Our team proposes to build an accurate visible and NIR (near-Infrared light) spectrum (or\n "
                  "Color-Infrared) mapping software specifically for STELLA (Science and Technology Education for\n "
                  "Land/Life Assessment), that will cartographically include and/or display STELLA’s other sensor\n "
                  "readings in a user friendly and visually appealing GUI (Graphical User Interface).\n "
             ).pack()


class MenuBar(tk.Menu):
    """MenuBar constructor"""
    def __init__(self, master):
        tk.Menu.__init__(self, master)
        # Dropdown menu of file options: open, save, exit
        file_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="File", underline=0, menu=file_menu)
        file_menu.add_command(label="Open New Files", underline=1, command=self.open_files)
        file_menu.add_command(label="Load Previous File", underline=1, command=self.open_prev_file)
        file_menu.add_command(label="Save File", underline=1, command=self.save_file)
        file_menu.add_command(label="Exit", underline=1, command=self.quit)

        # Dropdown menu of view options: vis, nir, temp, etc.
        view_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="View", underline=0, menu=view_menu)
        view_menu.add_command(label="Visual Map", underline=1,
                              command=lambda: master.switch_frame(stella_frame.VisFrame))
        view_menu.add_command(label="NIR Map", underline=1,
                              command=lambda: master.switch_frame(stella_frame.NirFrame))
        view_menu.add_command(label="Temp Map", underline=1,
                              command=lambda: master.switch_frame(stella_frame.TempFrame))
        view_menu.add_command(label="Surface vs Air Temp Map", underline=1,
                              command=lambda: master.switch_frame(stella_frame.SvaFrame))
        view_menu.add_command(label="NDVI Map", underline=1,
                              command=lambda: master.switch_frame(stella_frame.NdviFrame))
        view_menu.add_command(label="EVI Map", underline=1,
                              command=lambda: master.switch_frame(stella_frame.EviFrame))
        view_menu.add_command(label="SAVI Map", underline=1,
                              command=lambda: master.switch_frame(stella_frame.SaviFrame))
        view_menu.add_command(label="MSAVI Map", underline=1,
                              command=lambda: master.switch_frame(stella_frame.MsaviFrame))

        # # Dropdown menu of annotation options
        # annotate_menu = tk.Menu(self, tearoff=False)
        # self.add_cascade(label="Annotate", underline=0, menu=annotate_menu)
        # annotate_menu.add_command(label="New Annotation", underline=1, command=self.quit)
        # annotate_menu.add_command(label="Clear Annotations", underline=1, command=self.quit)

        # Dropdown menu of satellite frame options (uploading a new image or returning to the default)
        satellite_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Satellite", underline=0, menu=satellite_menu)
        satellite_menu.add_command(label="Get Satellite Image", underline=1, command=lambda: master.get_satellite())
        satellite_menu.add_command(label="Upload Aerial Image", underline=1, command=lambda: self.set_sat_image())

        # Help Menu
        help_menu = tk.Menu(self, tearoff=False)
        # self.add_cascade(label="Help", underline=0, menu=help_menu)
        help_menu.add_command(label="About", underline=1, command=about)

    def quit(self):
        """ closes the window """

        sys.exit(0)

    def open_files(self):
        """ Opens the stella and gps data files. """

        # @TODO We need to make sure the starting directory works on all machines
        self.master.set_stella_data(filedialog.askopenfilename(initialdir='/home/boxghost/Dropbox/SE',
                                                               title="Select STELLA data",
                                                               filetypes=(("Text Files", "*.txt"),)))
        self.master.set_gps_data(filedialog.askopenfilename(initialdir='/home/boxghost/Dropbox/SE/',
                                                            title="Select GPS data",
                                                            filetypes=(("CSV Files", "*.csv"),)))
        self.master.set_map_data('')

        if self.master.stella_file and self.master.gps_file:
            self.master.map_data.update_map(700, gps_file=self.master.gps_file,
                                            stella_file=self.master.stella_file,
                                            map_file=self.master.map_file)

            # Open the temperature map by default
            self.master.switch_frame(stella_frame.TempFrame)
            # Open the satellite image by default
            self.master.get_satellite()
            self.master.get_annotation()

    """Opens a map file""""
    def open_prev_file(self):
        """ Opens a .vmap file """

        self.master.set_map_data(filedialog.askopenfilename(initialdir='/home/boxghost/Dropbox/SE/',
                                                            title="Select Previous Map data",
                                                            filetypes=(("VIR-Atlas Files", "*.vmap"),)))
        self.master.set_gps_data(None)
        self.master.set_stella_data(None)

        if self.master.map_file:
            self.master.map_data.update_map(700, gps_file=self.master.gps_file,
                                            stella_file=self.master.stella_file,
                                            map_file=self.master.map_file)

            # Open the temperature map by default
            self.master.switch_frame(stella_frame.TempFrame)
            # Open the satellite image by default
            self.master.get_satellite()

    def save_file(self):
        """ Saves data into a .vmap file """

        file = filedialog.asksaveasfile(filetypes=[('VIR-Atlas map', '.vmap'), ('All files', '*')],
                                        defaultextension=".vmap", mode='wb')
        self.master.map_data.save_map(file)

    def set_sat_image(self):
        """ Opens an image file into the Satellite frame """
        file = filedialog.askopenfilename(initialdir='/home/boxghost/Dropbox/SE/',
                                          title="Select Previous Map data",
                                          filetypes=[("image", ".jpeg"), ("image", ".png"), ("image", ".jpg")])
        self.master.set_sat_file(file)
        if self.master.satellite_image != '':
            self.master.get_satellite_upload()


"""Window for testing purposes only. Shows how to create a MenuBar object."""
class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # menu_bar = MenuBar(parent/master/root)
        menu_bar = MenuBar(self)
        # I think the root window needs to do this to add the menu
        self.config(menu=menu_bar)


if __name__ == "__main__":
    app = App()
    app.mainloop()
