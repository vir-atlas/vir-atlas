# @authors Tenise and Marisa 
# @date 04/14/2021
# @brief Handles Annotations
# @todo correlate event coordinates with stella coordinates
import tkinter
import tkinter as tk
import sys
import map_point
import map_gen

global map_list
global scale


class Annotation(object):
    def __init__(self, x, y, note):
        tk.Tk.__init__(self)
        self.x = x
        self.y = y
        for point in map_list:
            radius = map_gen.feet_to_pix(point.confidence, scale)
            if point.x == self.x and point.y == self.y:
                point.stella_point.annotation = note
            elif point.stella_point.x + radius > self.x > point.stella_point.x - radius:
                if point.stella_point.y + radius > self.y > point.stella_point.y - radius:
                    """Checks to see if user click a point within a stella point area"""
                    """If so, annotation coordinates are set to stella coordinates"""
                    point.stella_point.annotation = note
                    self.x = point.stella_point.x
                    self.y = point.stella_point.y
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
class AnnotationEditor(Annotation):
    # constructor for AnnotationEditor
    def __init__(self, new_annotation):
        # call for popup window
        self.top = tk.Toplevel()
        self.top.title("VIR Atlas Annotations Editor")
        self.top.geometry("400x400")

        # create attribute frame
        tk.Label(self.top, text="Attribute Frame").pack(side="top")
        # add attributes to frame
        self.get_attribute(new_annotation.x, new_annotation.y)

        # create entry
        self.note = tk.Entry(self.top)
        self.note.pack()

        # create "Save" button that initiates save_note()
        self.save = tk.Button(self.top, text="Save", command=self.save_note)
        self.save.place(x=50, y=200)

        # create "Cancel" button that destroys the window
        # Do we need to make sure that this makes no changes to the Frame? I doubt it
        self.cancel = tk.Button(self.top, text="Cancel", command=self.top.destroy())
        self.cancel.place(x=150, y=200)

    # gets and displays all attributes (if available)
    def get_attribute(self, x, y):
        for point in map_list:
            # check if given points are STELLA points or not
            if (point.x == float(x)) & (point.y == float(y)):
                # display correlating data
                surface_temp = "Surface Temperature (C): " + str(point.stella_point.surface_temp)
                air_temp = "Air Temperature (C): " + str(point.stella_point.air_temp)
                relative_humidity = "Relative Humidity (%): " + str(point.stella_point.relative_humidity)
                air_pressure_hpa = "Air Pressure(hPa): " + str(point.stella_point.air_pressure_hpa)
                altitude_m_uncal = "Altitude (m)" + str(point.stella_point.altitude_m_uncal)
                vis_pows = "Visual Light Spectrum(uW/cm^2): 450 nm-> " + str(
                    point.stella_point.vis_pows[0]) + " 500 nm-> " + str(
                    point.stella_point.vis_pows[1]) + " 550 nm-> " + str(
                    point.stella_point.vis_pows[2]) + " 570 nm-> " + str(
                    point.stella_point.vis_pows[3]) + " 600 nm->" + str(
                    point.stella_point.vis_pows[4]) + " 650 nm-> " + str(point.stella_point.vis_pows[5])
                nir_pows = "Near Infrared Light Spectrum(uW/cm^2): 610 nm-> " + str(
                    point.stella_point.nir_pows[0]) + " 680 nm-> " + str(
                    point.stella_point.nir_pows[1]) + " 730 nm-> " + str(
                    point.stella_point.nir_pows[2]) + " 760 nm-> " + str(
                    point.stella_point.vis_pows[3]) + " 810 nm->" + str(
                    point.stella_point.vis_pows[4]) + " 860 nm-> " + str(point.stella_point.vis_pows[5])

                tk.Label(self.top, text=surface_temp).pack(side="top")
                tk.Label(self.top, text=air_temp).pack(side="top")
                tk.Label(self.top, text=relative_humidity).pack(side="top")
                tk.Label(self.top, text=air_temp).pack(side="top")
                tk.Label(self.top, text=air_pressure_hpa).pack(side="top")
                tk.Label(self.top, text=altitude_m_uncal).pack(side="top")
                tk.Label(self.top, text=vis_pows).pack(side="top")
                tk.Label(self.top, text=nir_pows).pack(side="top")
            else:
                # display message if point doesn't have STELLA data attached to it
                tk.Label(self.attribute_frame, text="No data recorded for selected point!").pack(side="top")

    # saves notes made by user to the annotation attribute
    def save_note(self):
        Annotation.note = self.note.get()
        self.top.destroy()


def set_map_list(map_points, map_scale):
    global map_list, scale
    map_list = map_points
    scale = map_scale
