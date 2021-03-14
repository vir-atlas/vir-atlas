# @author Sophia Novo-Gradac
# 3/12/2021
# @brief:   places circles on canvas based on map_point objects and displays canvas.

from tkinter import *
import MapPoint
import gpsPoint

canvas_size = 500 #test canvas size

"""tester for making drone path"""
def create_circle(map_point, canvasName): #center coordinates, radius
    x = map_point.x
    y = map_point.y
    return canvasName.create_oval(x - 1, y - 1, x + 1, y + 1)

#test on sophia's pc
# gps_points = gpsPoint.read_drone_csv("/home/nova/cse326/Data Files_Feb-26th-2021-05-57PM-Flight-Airdata.csv")
gps_points = gpsPoint.read_drone_csv("Data Files/Feb-26th-2021-05-57PM-Flight-Airdata.csv")
map_points = MapPoint.set_xy(gps_points)


window = Tk()
map = Canvas(window,
             width=canvas_size,
             height=canvas_size)
map.pack()

for point in map_points:
    create_circle(point, map)

# count = -1
# while True:
#     count += 1
#
#     if count >= len(map_points):
#         break
#
#     create_circle(map_points[count], map)

window.mainloop()
