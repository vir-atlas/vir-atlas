# @author Tenise and Brynn
# @date 3/26/21
# @brief Menubar for the top of the screen / following Menubutton widget tutorial from Geeks4Geeks
# @todo positoning, and buttons relating to each initial menu button
from tkinter import *


# this is the main function
def menubar(root):

    menu = Menu(root)

    filebutt = Menu(menu, tearoff=0)
    filebutt.add_command(label="Open", command=open_file)
    filebutt.add_command(labe="Save", command=save_file)
    filebutt.add_separator()
    menu.add_cascade(label="File", menu=filebutt)

    viewbutt = Menu(menu,tearoff=0)
    viewbutt.add_command(label="Zoom In", command=zoom)
    viewbutt.add_command(label="Zoom Out", command=zoom)
    menu.add_cascade(label="View", menu=viewbutt)

    annotatebutt = Menu(menu, tearoff=0)
    annotatebutt.add_command(label="New Annotation", command=new_annotate)
    menu.add_cascade(label="Annotate", menu=annotatebutt)

    helpbutt = Menu(menu, tearoff=0)
    helpbutt.add_command(label="About", command=about)
    menu.add_cascade(label="Help", menu=helpbutt)

    root.config(menu=menu)
    return root


# these can be filled in later, but this is where the commands will be executed
def open_file():
    x = 0

def save_file():
    x = 0

def zoom():
    x = 0

def new_annotate():
    x = 0

def about():
    x = 0

if __name__ == '__main__':
    menubar()
