# @authors Tenise
# @date 04/14/2021
# @brief Handles Annotations
# @todo :(( everything

import tkinter as tk


class Annotation:
    def __init__(self, x_coordinate, y_coordinate, note):
        tk.Tk.__init__(self)
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.note = note

class AnnotationFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

class AnnotationEditor(notes):
    def __init__(self):
        self

