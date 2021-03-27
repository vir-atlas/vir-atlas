# @authros Brynn and Tenise
# @date 3/26/21
# @breif Generates the main window for VIR - Atlas software.
# @todo Create functions for each GUI component

import tkinter as tk
import os
import menubar as menu

def main():
    # Create main window
    root = tk.Tk()
    root.configure(background='black')
    root.title('VIR - Atlas')
    root.geometry("800x600")

    # Generate and place frames for each component
    # Generate menu and buttons
    root = menu.menubar(root)

    irmap = tk.Frame(master=root, width=500, height=400, bg='grey')
    irmap = test(irmap)
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

def test(frame):
    label = tk.Label(master=frame, text='fuck', bg='white').pack()
    return frame

if __name__ == '__main__':
    main()
