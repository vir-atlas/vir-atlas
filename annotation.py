# @authors Tenise
# @date 04/14/2021
# @brief Handles Annotations
# @todo add "Cancel" button to AnnotationEditor, work on Annotation and AnnotationFrame

import tkinter as tk
import sys
import map_point

global map_list


class Annotation(object):
    def __init__(self, x_coordinate, y_coordinate, note):
        tk.Tk.__init__(self)
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        for point in map_list:
            if point.x == self.x_coordinate and point.y == self.y_coordinate:
                point.stella_point.annotation = note
        self.note = note


# Responsible for the annotation_frame in main.py
class AnnotationFrame(tk.Frame):
    def __init__(self, master):
        # constructor for AnnotationFrame
        tk.Frame.__init__(self, master)

        self.width = 420
        self.height = 420

        self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg="white")

        self.set_canvas()

    def notes(self, event):
        pass


# Responsible for editing/adding Annotations
class AnnotationEditor(object):
    # constructor for AnnotationEditor
    def __init__(self, master):
        # call for popup window
        top = self.top = tk.Toplevel(master)

        # label for Annotation Editor
        self.label = tk.Label(top, text="VIR Atlas Annotations Editor")
        self.label.pack()

        # create entry
        self.note = tk.Entry(top)
        self.note.pack()

        # create "Save" button that initiates save_note()
        self.save = tk.Button(top, text="Save", command=self.save_note)

    # saves notes made by user to the annotation attribute
    def save_note(self):
        Annotation.note = self.note.get()
        self.top.destroy()


def print_attributes(map_point):
    map_point.stella_point.surface_temp
    map_point.stella_point.air_temp
    map_point.stella_point.relative_humidity
    map_point.stella_point.air_pressure_hpa
    map_point.stella_point.altitude_m_uncal
    map_point.stella_point.vis_pows
    map_point.stella_point.nir_pows


def set_map_list(map_points):
    global map_list
    map_list = map_points
