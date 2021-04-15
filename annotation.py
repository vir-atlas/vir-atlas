# @authors Tenise
# @date 04/14/2021
# @brief Handles Annotations
# @todo add "Cancel" button to AnnotationEditor, work on Annotation and AnnotationFrame

import tkinter as tk
import sys


class Annotation(object):
    def __init__(self, x_coordinate, y_coordinate, note):
        tk.Tk.__init__(self)
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.note = note


# Responsible for the annotation_frame in main.py
class AnnotationFrame:
    def __init__(self, master):
        pass
        # annotations = self.annotations =

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

    def save_note(self):
        self.save = self.note.get()
        self.top.destroy()
