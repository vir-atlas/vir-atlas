# @authors Brynn and Tenise
# @date 3/26/21
# @brief Generates the main window for VIR - Atlas software.
# @todo Make window dynamically scaleable, create scrollable map/resize map properly, make open/save functions, create legend, display satmap... etc.

import tkinter as tk
import os
import MapPoint
import MapGen
import StellaPoint

def main():

    # Import canvas from MapGen
    map_choice=0
    display_map_canvas(map_choice, map_frame)
    map_frame.place(x=10, y=10)

    legend_frame = tk.Frame(master=root, width=30, height=260, bg='grey')
    legend_frame.place(x=1020, y=10)

    satmap_frame = tk.Frame(master=root, width=220, height=200, bg='grey')
    satmap_frame.place(x=1070, y=10)

    notes_frame = tk.Frame(master=root, width=1000, height=180, bg='grey')
    notes_frame.place(x=10, y=280)

    annotation_frame = tk.Frame(master=root, width=220, height=200, bg='grey')
    annotation_frame.place(x=1070, y=250)

"""
Displays a given map in the window. The map to display is specified by num. (0=visual map, 1=nir, 2=temp map) This should be 0 by defualt
"""
def display_map_canvas(keyword):
    map_frame = tk.Frame(master=root, bg='grey') 
    canvas_size = 1200
    resolution = 10
    gps_points = MapGen.gpsPoint.read_drone_csv(r'Data Files/Feb-26th-2021-05-57PM-Flight-Airdata.csv')
    stella_points = StellaPoint.make_stella_points(r'Data Files/data.csv')

    stella_points = StellaPoint.get_batch(stella_points, "1.X")
    map_points,width,height = MapPoint.set_xy(gps_points, stella_points, canvas_size)

    height = round(height/10) * 10
    width = round(width/10) * 10
    
    map_canvas = tk.Canvas(map_frame, width = width, height = height)
    map_canvas.pack()
    poly_fill = MapGen.get_poly(height, width)
    filled = MapGen.draw_data(map_points, poly_fill, keyword, resolution, width)
    MapGen.fill_all(filled, poly_fill, width, height, resolution)
    for t in poly_fill:
        t.draw(map_canvas)
    MapGen.draw_flight_path(map_points, map_canvas)
    map_canvas.pack()
    map_frame.place(x=10, y=10)

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
    surface_temp_label = tk.Label(master=notes, text="Surface Temperature: " + str(point.stella_point.surface_temp),
                                  bg='white')
    surface_temp_label.pack()
    air_temp = tk.Label(master=notes, text="Air Temperature(C): " + str(point.stella_point.air_temp), bg='white')
    air_temp.pack()
    rel_humidity_label = tk.Label(master=notes, text="Relative Humidity(%): " + str(point.stella_point.rel_humid),
                                  bg='white')
    rel_humidity_label.pack()
    air_pressure_label = tk.Label(master=notes, text="Air Pressure(hPa): " + str(point.stella_point.air_pressure_hpa),
                                  bg='white')
    air_pressure_label.pack()
    altitude_label = tk.Label(master=notes, text="Altitude(m): " + str(point.stella_point.altitude_m_uncal), bg='white')
    altitude_label.pack()

def menubar(root):
    menu = tk.Menu(root, background='black', foreground='white',
                activebackground='grey', activeforeground='white')

    # File
    filebutt = tk.Menu(menu, tearoff=0, background='black', foreground='white')
    filebutt.add_command(label="Open", command=open_file)
    filebutt.add_command(labe="Save", command=save_file)
    menu.add_cascade(label="File", menu=filebutt)

    # View
    viewbutt = tk.Menu(menu, tearoff=0, background='black', foreground='white')
    viewbutt.add_command(label="Visual Map", command=get_vis)
    viewbutt.add_command(label="NIR Map", command=get_nir)
    viewbutt.add_command(label="Temperature Map", command=get_tmp)
    viewbutt.add_separator()
    viewbutt.add_command(label="Zoom In", command=zoom)
    viewbutt.add_command(label="Zoom Out", command=zoom)
    menu.add_cascade(label="View", menu=viewbutt)

    # Annotate
    annotatebutt = tk.Menu(menu, tearoff=0, background='black', foreground='white')
    annotatebutt.add_command(label="New Annotation", command=new_annotate)
    menu.add_cascade(label="Annotate", menu=annotatebutt)

    # Help
    helpbutt = tk.Menu(menu, tearoff=0, background='black', foreground='white')
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


def get_vis():
    map_frame.destroy()
    display_map_canvas('vis')

def get_nir():
    map_frame.destroy()
    display_map_canvas('nir')

def get_tmp():
    map_frame.destroy()
    display_map_canvas('tmp')


# Create the main window
root = tk.Tk()
root.configure(background='black')
root.title('VIR - Atlas')
root.geometry("1300x500")
# Pass main window to menubar to create menu
root = menubar(root)

# Create frame for STELLA Map
map_frame = tk.Frame(master=root, bg='grey')
# Set default map value
map_type = 'vis'
# Get default map
display_map_canvas(map_type)

root.mainloop()
