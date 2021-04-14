# @authors Brynn
# @date 4/13/21
# @brief The most recent main GUI file.
# @TODO Everything ;-;

import tkinter as tk
import menu_bar as menu


# Class creating the base window
class Root(tk.Tk):
    # Main window constructor
    def __init__(self):
        tk.Tk.__init__(self)

        # Add the menu_bar to the main window
        menu_bar = menu.MenuBar(self)
        self.config(menu=menu_bar)


if __name__ == "__main__":
    root = Root()
    root.mainloop()
