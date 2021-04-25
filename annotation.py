# @authors Tenise and Marisa 
# @date 04/14/2021
# @brief Handles Annotations
# @todo correlate event coordinates with stella coordinates
import tkinter
import tkinter as tk
import PIL
from tkinter.ttk import *
import sys
import map_point
import map_gen

global map_list
global scale
global root
global selected


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

    def edit_annotation_button(self):
        annotation = AnnotationEditor(self)
        annotation.note.insert('1.0', self.note)


# Responsible for the annotation_frame in main.py
class AnnotationFrame(tk.Frame):
    def __init__(self, master):
        # constructor for AnnotationFrame
        tk.Frame.__init__(self, master)
        self.master = master
        root.annotation_frame = self
        self.width = 420
        self.height = 420
        self.recent = None
        #for annotations that are not in a map point
        self.annotations = list()
        self.pins = {}
        # edit and save buttons
        self.edit_btn = tk.Button(self, text="Edit", bg="white", fg="#007BA7")
        self.delete_btn = tk.Button(self, text="Delete", bg="white", fg="#007BA7")
        root.annotation_frame.edit_btn = tk.Button(root.annotation_frame, text="Edit", bg="white", fg="#007BA7")
        root.annotation_frame.delete_btn = tk.Button(root.annotation_frame, text="Delete", bg="white", fg="#007BA7")

        # self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg="white")
        # set up the Listbox of all annotations
        self.listbox = tk.Listbox(self, width=70, height=10, bg="white", selectmode="single", listvariable=self.annotations)
        tk.Label(self, text="Annotations", bg="#007BA7", fg="white", font=("Courier", "16", "bold")).pack()
        self.listbox.pack()
        self.listbox.bind('<<ListboxSelect>>', root.annotation_frame.selection)


        # set up Scrollbar for Listbox
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side="right")

        # attaching listbox to scrollbar
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        # adding scrollbar's command parameter
        self.scrollbar.config(command=self.listbox.yview)

    def add_annotation(self, annotation):
        self.listbox.delete(0, 'end')
        root.annotation_frame.annotations.append(annotation)
        for item in root.annotation_frame.annotations:
            # check if there's something in the annotation attribute
            if item.note != "":
                self.listbox.insert("end", item)
        root.annotation_frame.listbox = self.listbox
        self.listbox.pack()

        pin = PIL.ImageTk.PhotoImage(PIL.Image.open("pin.jpg"))
        annotate_btn = tk.Button(root.stella_frame.canvas, image=pin, bg="white", command=annotation.edit_annotation_button)
        annotate_btn.image = pin
        annotate_btn.place(x=annotation.x, y=annotation.y)
        annotate_btn.bind("<Button-1>", annotation.edit_annotation_button)
        root.stella_frame.canvas.pack()
        self.pins[str(annotation)] = annotate_btn


    def edit_annotation(self):
        for item in root.annotation_frame.annotations:
            if selected == str(item):
                annotation = AnnotationEditor(item)
                annotation.note.insert('1.0', item.note)

    def delete_annotation(self):
        temp = 0
        for item in root.annotation_frame.annotations:
            if selected == str(item):
                root.annotation_frame.annotations.remove(item)
                root.annotation_frame.listbox.delete(temp)
                root.annotation_frame.listbox.pack()
                btn = self.pins[str(item)]
                btn.destroy()
                del self.pins[str(item)]
                root.stella_frame.canvas.pack()
            temp += 1



    def selection(self, evt):
        event = evt.widget
        cur = event.curselection()
        if len(cur) > 0:
            select = event.curselection()
            annotation = event.get(select)
            get_selection(annotation)
            root.stella_frame.canvas.pack()
            root.annotation_frame.edit_btn.configure(command=root.annotation_frame.edit_annotation, font=("Courier", "12", "bold italic"))
            root.annotation_frame.edit_btn.pack(side="left", ipadx=10)
            root.annotation_frame.delete_btn.configure(command=root.annotation_frame.delete_annotation, font=("Courier", "12", "bold italic"))
            root.annotation_frame.delete_btn.pack(side='right', ipadx=10)


# Responsible for editing/adding Annotations
class AnnotationEditor(Annotation):
    # constructor for AnnotationEditor
    def __init__(self, new_annotation):
        # call for popup window
        self.annotation = new_annotation
        self.top = tk.Toplevel()
        self.top.title("VIR Atlas Annotations Editor")
        self.top.geometry("400x620")
        # create attribute frame
        title = "Point attributes at x: " + str(new_annotation.x) + " y: " + str(new_annotation.y)
        tk.Label(self.top, text=title, bg="#007BA7", fg="white", font=("Courier", "12", "bold")).pack(side="top")
        # add attributes to frame
        self.get_attribute(new_annotation.x, new_annotation.y)

        # create entry box for input
        self.note = tk.Text(self.top, width=40, height=10, font=("Courier", "10", "bold italic"), bg="white", fg="#007BA7")
        self.note.pack()

        # create "Save" button that initiates save_note()
        self.save = tk.Button(self.top, text="Save", bg="white", fg="#007BA7", font=("Courier", "10", "bold italic"), command=self.save_note)
        self.save.pack()

        # create "Cancel" button that destroys the window
        # Do we need to make sure that this makes no changes to the Frame? I doubt it
        self.cancel = tk.Button(self.top, text="Cancel", bg="white", fg="#007BA7", font=("Courier", "10", "bold italic"), command=self.cancel)
        self.cancel.pack()

        self.top.configure(bg="#007BA7")

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
                tk.Label(self.top, text=surface_temp, bg="#007BA7", fg="white", font=("Courier", "9", "bold")).pack(side="top")
                tk.Label(self.top, text=air_temp, bg="#007BA7", fg="white", font=("Courier", "9", "bold")).pack(side="top")
                tk.Label(self.top, text=relative_humidity, bg="#007BA7", fg="white", font=("Courier", "9", "bold")).pack(side="top")
                tk.Label(self.top, text=air_temp,bg="#007BA7", fg="white", font=("Courier", "9", "bold")).pack(side="top")
                tk.Label(self.top, text=air_pressure_hpa, bg="#007BA7", fg="white", font=("Courier", "9", "bold")).pack(side="top")
                tk.Label(self.top, text=altitude_m_uncal, bg="#007BA7", fg="white", font=("Courier", "9", "bold")).pack(side="top")
                tk.Label(self.top, text=vis_pows,bg="#007BA7", fg="white", font=("Courier", "9", "bold")).pack(side="top")
                tk.Label(self.top, text=nir_pows,bg="#007BA7", fg="white", font=("Courier", "9", "bold")).pack(side="top")
                flag = 1
                break
            else:
                # display message if point doesn't have STELLA data attached to it
                continue
        if flag == 0:
            tk.Label(self.top, text="No data recorded for selected point!").pack(side="top")

    # saves notes made by user to the annotation attribute
    def save_note(self):
        temp = 0
        for item in root.annotation_frame.annotations:
            temp += 1
            if item is self.annotation:
                root.annotation_frame.annotations.remove(item)
                root.annotation_frame.listbox.delete(temp)
                btn = root.annotation_frame.pins[str(item)]
                btn.destroy()
                del root.annotation_frame.pins[str(item)]
                root.stella_frame.canvas.pack()

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


def get_selection(annotation):
    global selected
    selected = annotation
