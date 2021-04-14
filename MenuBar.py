# @authors Brynn
# @date 4/13/21
# @brief Houses all components and functions of the top menu
# @todo fill in functions

import tkinter as tk
import sys

class MenuBar(tk.Menu):
    # MenuBar constructor
    def __init__(self, master):
        tk.Menu.__init__(self, master)

        # Dropdown menu of file options: open, save, exit
        fileMenu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="File", underline=0, menu=fileMenu)
        fileMenu.add_command(label="Open File", underline=1, command=self.quit)
        fileMenu.add_command(label="Save File", underline=1, command=self.quit)
        fileMenu.add_command(label="Exit", underline=1, command=self.quit)

        # Dropdown menu of view options: vis, nir, temp
        viewMenu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="View", underline=0, menu=viewMenu)
        viewMenu.add_command(label="Visual Map", underline=1, command=self.quit)
        viewMenu.add_command(label="NIR Map", underline=1, command=self.quit)
        viewMenu.add_command(label="Temp Map", underline=1, command=self.quit)

        # Dropdown menu of annotation options
        annotateMenu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Annotate", underline=0, menu=annotateMenu)
        annotateMenu.add_command(label="New Annotation", underline=1, command=self.quit)
        annotateMenu.add_command(label="Clear Annotations", underline=1, command=self.quit)

        # Help Menu
        helpMenu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Help", underline=0, menu=helpMenu)
        helpMenu.add_command(label="About", underline=1, command=self.about)

    # Creates a new window with helpful information
    def about(self):        
        aboutWindow = tk.Tk()
        aboutWindow.title("About")
        aboutWindow.geometry("400x300")

        tk.Label(aboutWindow,
              text="Our team proposes to build an accurate visible and NIR (near-Infrared light) spectrum (or\n "
                   "Color-Infrared) mapping software specifically for STELLA (Science and Technology Education for\n "
                   "Land/Life Assessment), that will cartographically include and/or display STELLA’s other sensor\n "
                   "readings in a user friendly and visually appealing GUI (Graphical User Interface).\n "
              ).pack()


    # Closes the window
    def quit(self):
        sys.exit(0)




#Window for testing purposes only. Shows how to create a menubar object.
class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # menubar = MenuBar(parent/master/root)
        menubar = MenuBar(self)
        # I think the root window needs to do this to add the menu
        self.config(menu=menubar)

if __name__ == "__main__":
    app=App()
    app.mainloop()
        
