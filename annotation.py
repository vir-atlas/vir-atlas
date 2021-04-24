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
global root


class Annotation(object):
    def __init__(self, x, y, note):
        # tk.Tk.__init__(self)
        self.x = x
        self.y = y
        for point in map_list:
            radius = point.confidence * scale
            if int(point.x) == self.x and int(point.y) == self.y:
                point.annotation = note
            elif (point.x + radius) > self.x > (point.x - radius):
                if (point.y + radius) > self.y > (point.y - radius):
                    """Checks to see if user click a point within a stella point area"""
                    """If so, annotation coordinates are set to stella coordinates"""
                    point.annotation = note
                    self.x = int(point.x)
                    self.y = int(point.y)
                    break

        self.note = note


# Responsible for the annotation_frame in main.py
class AnnotationFrame(tk.Frame):
    def __init__(self, master):
        # constructor for AnnotationFrame
        tk.Frame.__init__(self, master)
        self.master = master
        self.width = 420
        self.height = 500
        #for annotations that are not in a map point
        self.annotations = list()

        # self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg="white")

        # set up the Listbox of all annotations
        self.listbox = tk.Listbox(self, bg="white")
        tk.Label(self, text="Annotations").pack()
        self.listbox.pack()

        # set up Scrollbar for Listbox
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack()

        # insert available annotations into listbox
        for point in map_list:
            # check if there's something in the annotation attribute
            if point.annotation != "":
                self.listbox.insert("end", point)

        # attaching listbox to scrollbar
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        # adding scrollbar's command parameter
        self.scrollbar.config(command=self.listbox.yview)


    def add_annotation(self, annotation):
        self.listbox.delete(0, 'end')
        root.annotation_frame.annotations.append(annotation)
        for point in map_list:
            # check if there's something in the annotation attribute
            if point.annotation != "":
                self.listbox.insert("end", point.annotation)
            if point.annotation == annotation.note:
                root.annotation_frame.annotations.remove(annotation)
        for annotation in root.annotation_frame.annotations:
            self.listbox.insert('end', annotation.note)

# Responsible for editing/adding Annotations
class AnnotationEditor(Annotation):
    # constructor for AnnotationEditor
    def __init__(self, new_annotation):
        # call for popup window
        self.annotation = new_annotation
        self.top = tk.Toplevel()
        self.top.title("VIR Atlas Annotations Editor")
        self.top.geometry("400x600")
        # create attribute frame
        tk.Label(self.top, text="Point Attributes").pack(side="top")
        # add attributes to frame
        self.get_attribute(new_annotation.x, new_annotation.y)

        # create entry box for input
        self.note = tk.Text(self.top, width=40, height=10)
        self.note.pack()

        # create "Save" button that initiates save_note()
        self.save = tk.Button(self.top, text="Save", command=self.save_note)
        self.save.pack()

        # create "Cancel" button that destroys the window
        # Do we need to make sure that this makes no changes to the Frame? I doubt it
        self.cancel = tk.Button(self.top, text="Cancel", command=self.cancel)
        self.cancel.pack()

    # gets and displays all attributes (if available)
    def get_attribute(self, x, y):
        flag = 0
        for point in map_list:
            # check if given points are STELLA points or not

            if (int(point.x) == x) and (int(point.y) == y):
                # display correlating data
                surface_temp = "Surface Temperature (C): " + str(point.stella_point.surface_temp)
                air_temp = "Air Temperature (C): " + str(point.stella_point.air_temp)
                relative_humidity = "Relative Humidity (%): " + str(point.stella_point.rel_humid)
                air_pressure_hpa = "Air Pressure(hPa): " + str(point.stella_point.air_pressure_hpa)
                altitude_m_uncal = "Altitude (m): " + str(point.stella_point.altitude_m_uncal)
                vis_pows = "Visual Light Spectrum(uW/cm^2):\n 450 nm-> " + str(
                    point.stella_point.vis_pows[0]) + "\n 500 nm-> " + str(
                    point.stella_point.vis_pows[1]) + "\n 550 nm-> " + str(
                    point.stella_point.vis_pows[2]) + "\n 570 nm-> " + str(
                    point.stella_point.vis_pows[3]) + "\n 600 nm->" + str(
                    point.stella_point.vis_pows[4]) + "\n 650 nm-> " + str(point.stella_point.vis_pows[5])
                nir_pows = "Near Infrared Light Spectrum(uW/cm^2):\n 610 nm-> " + str(
                    point.stella_point.nir_pows[0]) + "\n 680 nm-> " + str(
                    point.stella_point.nir_pows[1]) + "\n 730 nm-> " + str(
                    point.stella_point.nir_pows[2]) + "\n 760 nm-> " + str(
                    point.stella_point.vis_pows[3]) + "\n 810 nm->" + str(
                    point.stella_point.vis_pows[4]) + "\n 860 nm-> " + str(point.stella_point.vis_pows[5])
                tk.Label(self.top, text=surface_temp).pack(side="top")
                tk.Label(self.top, text=air_temp).pack(side="top")
                tk.Label(self.top, text=relative_humidity).pack(side="top")
                tk.Label(self.top, text=air_temp).pack(side="top")
                tk.Label(self.top, text=air_pressure_hpa).pack(side="top")
                tk.Label(self.top, text=altitude_m_uncal).pack(side="top")
                tk.Label(self.top, text=vis_pows).pack(side="top")
                tk.Label(self.top, text=nir_pows).pack(side="top")
                flag = 1
                break
            else:
                # display message if point doesn't have STELLA data attached to it
                continue
        if flag == 0:
            tk.Label(self.top, text="No data recorded for selected point!").pack(side="top")

    # saves notes made by user to the annotation attribute
    def save_note(self):
        self.annotation = Annotation(self.annotation.x, self.annotation.y, self.note.get('1.0', 'end-1c'))
        root.annotation_frame.add_annotation(self.annotation)
        self.top.destroy()

    def cancel(self):
        self.top.destroy()


def set_map_list(map_points, map_scale):
    global map_list, scale
    map_list = map_points
    scale = map_scale


def get_root(main_root):
    global root
    root = main_root
