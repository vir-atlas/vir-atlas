# @authors Brynn
# @date 4/13/21
# @brief The most recent main GUI file.
# @TODO Everything ;-;

import tkinter as tk
import menu_bar as menu
import stella_frame


# Class creating the base window
class Root(tk.Tk):
    # Main window constructor
    def __init__(self):
        tk.Tk.__init__(self)

        self.geometry('810x560')

        # Initialize data files
        self.stella_file = 0
        self.gps_file = 0

        # Add the stella_frame to the main window
        self.stella_frame = stella_frame.StellaFrame(self)
        self.stella_frame.set_canvas()
        self.stella_frame.place(x=20, y=20)

        # Add the menu_bar to the main window
        menu_bar = menu.MenuBar(self)
        self.config(menu=menu_bar)

    def set_stella_data(self, file):
        self.stella_file = file

    def set_gps_data(self, file):
        self.gps_file = file


if __name__ == "__main__":
    root = Root()
    root.mainloop()
