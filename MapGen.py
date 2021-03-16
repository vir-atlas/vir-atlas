# @author Sophia Novo-Gradac
# 3/12/2021
# @brief:   places circles on canvas based on map_point objects and displays canvas.
# last updated: 3/16/2021 by Sophia Novo-Gradac
# @updates  added color and radius to create_circle
#           black is set as map background
# TODO:     Add maps for nir and vs
#           export canvas as jpg?

from tkinter import *
import MapPoint
import StellaPoint
import gpsPoint

canvas_size = 500 #test canvas size

"""tester for making drone path"""
def create_circle(map_point, radius, canvasName): #center coordinates, radius
    x = map_point.x
    y = map_point.y
    return canvasName.create_oval(x - radius, y - radius, x + radius, y + radius, fill = map_point.vs_rgb)

#test on sophia's pc
gps_points = gpsPoint.read_drone_csv("Data Files/Feb-26th-2021-05-57PM-Flight-Airdata.csv")
stella_points = StellaPoint.make_stella_points("Data Files/data.csv")
stella_points = StellaPoint.get_batch(stella_points, "1.X")
map_points = MapPoint.set_xy(gps_points, stella_points)


window = Tk()
map = Canvas(window,
             width=canvas_size,
             height=canvas_size,
             background = MapPoint.black)
map.pack()

for point in map_points:
    # point.print_point()
    create_circle(point, 10, map)

window.mainloop()
