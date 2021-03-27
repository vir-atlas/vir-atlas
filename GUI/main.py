# @authros Brynn and Tenise
# @date 3/26/21
# @breif Generates the main window for VIR - Atlas software.
# @todo Create functions for each GUI component

import tkinter as tk
import os
import menubar as menu
import MapPoint
import StellaPoint

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
    #Call display point if a point is selected
    notes.place(x=10, y=480)

    annotations = tk.Frame(master=root, width=220, height=310, bg='grey')
    annotations.place(x=570,y=270)

    root.mainloop()

def test(frame):
    label = tk.Label(master=frame, text='fuck', bg='white').pack()
    return frame

"""Displays specific data on a point selected in to the notes canvas"""
def display_point_data(notes, point):
    nir_wavebands = ""
    vs_wavebands = ""
    for waveband in point.stella_point.nir_pows:
        nir_wavebands = nir_wavebands + " " + str(waveband)
    nir_label = tk.Label(master=notes, text="NIR Waveband Powers(nm):" + nir_wavebands, bg='white')
    nir_label.pack()
    for waveband in point.stella_point.vs_pows:
        vs_wavebands = vs_wavebands + " " + str(waveband)
    vs_label = tk.Label(master=notes, text="VS Waveband Powers(nm):" + vs_wavebands, bg='white')
    vs_label.pack()
    surface_temp_label = tk.Label(master=notes, text="Surface Temperature: " + str(point.stella_point.surface_temp), bg='white')
    surface_temp_label.pack()
    air_temp = tk.Label(master=notes, text="Air Temperature(C): " + str(point.stella_point.air_temp), bg='white')
    air_temp.pack()
    rel_humidity_label = tk.Label(master=notes, text="Relative Humidity(%): " + str(point.stella_point.rel_humid), bg='white')
    rel_humidity_label.pack()
    air_pressure_label = tk.Label(master=notes, text="Air Pressure(hPa): "+str(point.stella_point.air_pressure_hpa), bg='white')
    air_pressure_label.pack()
    altitude_label = tk.Label(master=notes, text="Altitude(m): " + str(point.stella_point.altitude_m_uncal), bg='white')
    altitude_label.pack()



if __name__ == '__main__':
    main()
