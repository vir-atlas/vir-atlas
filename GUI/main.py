# @authros Brynn and Tenise
# @date 3/26/21
# @breif Generates the main window for VIR - Atlas software.
# @todo Create functions for each GUI component

import tkinter as tk
import os

def main():
    # Create main window
    root = tk.Tk()
    root.configure(background='black')
    root.geometry("800x600")

    # Generate frames for each component
    menubar = tk.Frame(master=root, width=800, height=40, bg='grey')
    menubar.place(x=0,y=0)
    menubar.pack(fill=tk.X)

    irmap = tk.Frame(master=root, width=500, height=400, bg='grey')
    irmap.place(x=10, y=60)

    legend = tk.Frame(master=root, width=30, height=400, bg='grey')
    legend.place(x=520,y=60)

    satmap = tk.Frame(master=root, width=220, height=200, bg='grey')
    satmap.place(x=570,y=60)

    notes = tk.Frame(master=root, width=540, height=100, bg='grey')
    notes.place(x=10, y=480)

    annotations = tk.Frame(master=root, width=220, height=310, bg='grey')
    annotations.place(x=570,y=270)


    root.mainloop()


if __name__ == '__main__':
    main()
