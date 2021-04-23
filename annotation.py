# @authors Tenise
# @date 04/14/2021
# @brief Handles Annotations
# @todo add "Cancel" button to AnnotationEditor, correlate event coordinates with stella coordinates
import tkinter as tk
import sys
import map_point
import map_gen
global map_list
global scale


class Annotation(object):
    def __init__(self, x_coordinate, y_coordinate, note):
        tk.Tk.__init__(self)
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        for point in map_list:
            radius = map_gen.feet_to_pix(point.confidence, scale)
            if point.x == self.x_coordinate and point.y == self.y_coordinate:
                point.stella_point.annotation = note
            elif point.stella_point.x + radius > self.x_coordinate > point.stella_point.x - radius:
                if point.stella_point.y + radius > self.y_coordinate > point.stella_point.y - radius:
                    """Checks to see if user click a point within a stella point area"""
                    """If so, annotation coordinates are set to stella coordinates"""
                    point.stella_point.annotation = note
                    self.x_coordinate = point.stella_point.x
                    self.y_coordinate = point.stella_point.y
        self.note = note


# Responsible for the annotation_frame in main.py
class AnnotationFrame(tk.Frame):
    def __init__(self, master):
        # constructor for AnnotationFrame
        tk.Frame.__init__(self, master)

        self.width = 420
        self.height = 420

        # self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg="white")

        # set up the Listbox of all annotations
        self.listbox = tk.Listbox(self, bg="white")
        self.listbox.pack()

        # set up Scrollbar for Listbox
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack()

        # insert available annotations into listbox
        for point in map_list:
            # check if there's something in the annotation attribute
            if point.annotation != "":
                self.listbox.insert(point)

        # attaching listbox to scrollbar
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        # adding scrollbar's command parameter
        self.scrollbar.config(command=self.listbox.yview)


# Responsible for editing/adding Annotations
class AnnotationEditor(object):
    # constructor for AnnotationEditor
    def __init__(self, master):
        # call for popup window
        top = self.top = tk.Toplevel(master)

        # label for Annotation Editor
        self.label = tk.Label(top, text="VIR Atlas Annotations Editor")
        self.label.pack()

        # create attribute frame
        def get_attribute(x, y):
            for point in map_list:
                if point.stella_point.x == x & point.stella_point.y == y:
                    Annotation.x_coordinate = x
                    Annotation.y_coordinate = y

        # create entry
        self.note = tk.Entry(top)
        self.note_frame = tk.Fram(top).grid(row=1, column=1)
        self.note.pack()

        # create "Save" button that initiates save_note()
        self.save = tk.Button(top, text="Save", command=self.save_note)

        # create "Cancel" button that destroys the window
        # Do we need to make sure that this makes no changes to the Frame? I doubt it
        self.cancel = tk.Button(top, text="Cancel", command=self.top.destroy())

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


def set_map_list(map_points, map_scale):
    global map_list, scale
    map_list = map_points
    scale = map_scale
