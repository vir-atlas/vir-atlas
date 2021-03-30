# @author Tenise and Brynn
# @date 3/26/21
# @brief Menubar for the top of the screen / following Menubutton widget tutorial from Geeks4Geeks
# @todo commands
from tkinter import *


# this is the main function
def menubar(root):
    menu = Menu(root, background='black', foreground='white',
                activebackground='grey', activeforeground='white')

    # File
    filebutt = Menu(menu, tearoff=0, background='black', foreground='white')
    filebutt.add_command(label="Open", command=open_file)
    filebutt.add_command(labe="Save", command=save_file)
    menu.add_cascade(label="File", menu=filebutt)

    # View
    viewbutt = Menu(menu, tearoff=0, background='black', foreground='white')
    viewbutt.add_command(label="Infrared Map", command=change_map)
    viewbutt.add_command(label="Near Infrared Map", command=change_map)
    viewbutt.add_command(label="Other", command=change_map)
    viewbutt.add_separator()
    viewbutt.add_command(label="Zoom In", command=zoom)
    viewbutt.add_command(label="Zoom Out", command=zoom)
    menu.add_cascade(label="View", menu=viewbutt)

    # Annotate
    annotatebutt = Menu(menu, tearoff=0, background='black', foreground='white')
    annotatebutt.add_command(label="New Annotation", command=new_annotate)
    menu.add_cascade(label="Annotate", menu=annotatebutt)

    # Help
    helpbutt = Menu(menu, tearoff=0, background='black', foreground='white')
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
    aboutWindow = Tk()
    aboutWindow.title("About")
    aboutWindow.geometry("400x300")

    Label(aboutWindow,
          text="Our team proposes to build an accurate visible and NIR (near-Infrared light) spectrum (or\n "
               "Color-Infrared) mapping software specifically for STELLA (Science and Technology Education for\n "
               "Land/Life Assessment), that will cartographically include and/or display STELLA’s other sensor\n "
               "readings in a user friendly and visually appealing GUI (Graphical User Interface).\n "
          ).pack()


def change_map():
    x = 0


if __name__ == '__main__':
    menubar()
