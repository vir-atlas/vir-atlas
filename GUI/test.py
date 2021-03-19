# @author Brynn and Tenise
# @date 3/19/21
# @brief Creates the main window for VIR - Atlas software.
# @todo Many things...

from tkinter import *
from PIL import ImageTk, Image
import os

def main():
    # Main window object named root
    root = Tk()

    # Give it a title
    root.title("GUI Test")
    # Set window size

    # Place top buttons
    frame = Frame().grid(row = 0, column = 0, rowspan = 10, columnspan = 10)
    filebutt = Button(frame, text = "File").grid(row = 0, column = 0, sticky = W)
    editbutt = Button(frame, text = "Edit").grid(row = 0, column = 1, sticky = W)
    viewbutt = Button(frame, text = "View").grid(row = 0, column = 2, sticky = W)
    helpbutt = Button(frame, text = "Help").grid(row = 0, column = 3, sticky = W)

    # Space buffer in top menu
    padding = Label(frame, width = 10).grid(row = 0, column = 4)


    # Place ir map (image) in grid
    # This needs to be replaced with a canvas instead of an image.
    irmap = ImageTk.PhotoImage(Image.open("irmap.png"))
    Label(root, image = irmap).grid(row = 1, column = 0, columnspan = 5)


    # Place image
    actmap = ImageTk.PhotoImage(Image.open("map.jpg"))
    Label(root, text = "Infrared Map", image = actmap, height = 400, width = 400).grid(row = 1, column = 6, rowspan = 4, columnspan = 4)


    # Actually display window
    root.mainloop()


if __name__ == "__main__":
    main()
