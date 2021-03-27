# @author Tenise and Brynn
# @date 3/26/21
# @brief Menubar for the top of the screen / following Menubutton widget tutorial from Geeks4Geeks
# @todo positoning, and buttons relating to each initial menu button
from tkinter import *

root = Tk()

root.geometry("800x600")

root.title("VIR - Atlas")

def menubar():
    #create buttons
    filebutt = Menubutton(
        root,
        text="File",
        bg="black",
        activebg="blue",
        fg="white"
    )
    viewbutt = Menubutton(
        root,
        text="View",
        bg="black",
        activebg="blue",
        fg="white"
    )
    annotatebutt = Menubutton(
        root,
        text="Annotate",
        bg="black",
        active="blue",
        fg="white"
    )
    helpbutt = Menubutton(
        root,
        text="Help",
        bg="black",
        activebg="blue",
        fg="white"
    )

    filebutt.menu = Menu(filebutt)
    viewbutt.menu = Menu(viewbutt)
    annotatebutt.menu = Menu(annotatebutt)
    helpbutt.menu = Menu(helpbutt)







