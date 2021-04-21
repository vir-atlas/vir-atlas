# @authors Brynn
# @date 4/13/21
# @brief Houses all components and functions of the top menu
# @todo fill in functions

import tkinter as tk
from tkinter import filedialog
import sys

# Creates a new window with helpful information
def about():
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
    # MenuBar constructor
    def __init__(self, master):
        tk.Menu.__init__(self, master)

        # Dropdown menu of file options: open, save, exit
        file_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="File", underline=0, menu=file_menu)
        file_menu.add_command(label="Open New Files", underline=1, command=self.open_files)
        file_menu.add_command(label="Load Previous File", underline=1, command=self.open_prev_file)
        file_menu.add_command(label="Save File", underline=1, command=self.save_file)
        file_menu.add_command(label="Exit", underline=1, command=self.quit)

        # Dropdown menu of view options: vis, nir, temp
        view_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="View", underline=0, menu=view_menu)
        view_menu.add_command(label="Visual Map", underline=1, command=self.master.stella_frame.vis_mode)
        view_menu.add_command(label="NIR Map", underline=1, command=self.master.stella_frame.nir_mode)
        view_menu.add_command(label="Temp Map", underline=1, command=self.master.stella_frame.temp_mode)

        # Dropdown menu of annotation options
        annotate_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Annotate", underline=0, menu=annotate_menu)
        annotate_menu.add_command(label="New Annotation", underline=1, command=self.quit)
        annotate_menu.add_command(label="Clear Annotations", underline=1, command=self.quit)

        # Help Menu
        help_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Help", underline=0, menu=help_menu)
        help_menu.add_command(label="About", underline=1, command=about)

    # Closes the window
    def quit(self):
        sys.exit(0)

    # Opens the stella and gps data files.
    def open_files(self):
        # @TODO We need to make sure the starting directory works on all machines
        self.master.set_stella_data(filedialog.askopenfilename(initialdir='/home/boxghost/Dropbox/SE',
                                                               title="Select STELLA data",
                                                               filetypes=(("Text Files", "*.txt"),)))
        self.master.set_gps_data(filedialog.askopenfilename(initialdir='/home/boxghost/Dropbox/SE/',
                                                            title="Select GPS data",
                                                            filetypes=(("CSV Files", "*.csv"),)))
                                               
        self.master.update()
        self.master.stella_frame.load_canvases()
        self.master.stella_frame.set_canvas()
        self.master.mainloop()

    def open_prev_file(self):
        self.master.set_map_data(filedialog.askopenfilename(initialdir='/home/boxghost/Dropbox/SE/',
                                                            title="Select Previous Map data",
                                                            filetypes=(("VIR-Atlas Files", "*.vmap"),)))

        self.master.update()
        self.master.stella_frame.load_canvases()
        self.master.stella_frame.set_canvas()
        self.master.mainloop()

    def save_file(self):
        file = filedialog.asksaveasfile(defaultextension=".vmap")
        self.master.map_data.save_list(file)


# Window for testing purposes only. Shows how to create a MenuBar object.
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
