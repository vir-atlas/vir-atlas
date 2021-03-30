# @author Sophia Novo-Gradac
# 3/12/2021
# @brief:   draws entire map area based on stella data
#           this is accomplished with triangles
# last updated: 3/28/2021 by Sophia Novo-Gradac
# @updates  fills entire map. done with triangles
# TODO:     draw_data is computationally taxing, make a better algorithm
#           export canvas as jpg?
#           colors are consistently blended to the top right
#           add method to determine which color from map_point to use
#           canvas_size and resolution should be modifiable by user
#           streamline imports. Many extra are included for testing purposes

import tkinter as tk
import MapPoint
import StellaPoint
import gpsPoint
import Color
import math

canvas_size = 1000 #test canvas size
resolution = 10

'''triangle holds its corner coordinates, an id number, and a color'''
class Triangle:
    '''by default, a triangle has no color'''
    def __init__(self, id, x_coords, y_coords):
        self.id = id
        self.x_coords = x_coords
        self.y_coords = y_coords
        self.color = "None"

    '''must use set_color to change triangle's color'''
    def set_color(self, color):
        self.color = color

    '''draw on the given canvas'''
    def draw(self, canvasName):
        canvasName.create_polygon(  self.x_coords[0], self.y_coords[0], 
                                    self.x_coords[1], self.y_coords[1], 
                                    self.x_coords[2], self.y_coords[2], fill = self.color)

    '''based on id number, what are the 3 neighbors.
    if an edge triangle, chop values that are not in list'''    
    def neighbors(self, width, height, resolution):
        ids = []

        # evaluate neighbor's id numbers
        if self.id % 4 == 0: #left triangle in any given square
            ids = [self.id - 1, self.id + 1, self.id + 2]

        if self.id % 4 == 1: #top triangle in any given square
            ids = [self.id - 1, self.id - int(width*4/resolution) + 1, self.id + 1]

        if self.id % 4 == 2: #bottom triangle in any given square
            ids = [self.id - 1, self.id + int(width*4/resolution) - 1, self.id + 1]

        if self.id % 4 == 3: #right triangle in any given square
            ids = [self.id - 2, self.id - 1, self.id + 1]
        
        # going backwards through ids, remove incorrect values 
        for i in ids[::-1]:
            if int(i) < 0:
                ids.remove(i)
            if int(i) >= int(width/resolution * height/resolution * 4):
                ids.remove(i)

        return ids
    
    '''if the map_point is inside of the triangle, return true and set triangle's color
    otherwise return false'''
    def contains_point(self, map_point, mode):
        x_min = self.x_coords[0]
        y_min = self.y_coords[0]
        x_max = self.x_coords[0]
        y_max = self.y_coords[0]
        
        # find both x and y range
        for x in self.x_coords:
            if x < x_min:
                x_min = x
            if x > x_max:
                x_max = x
        for y in self.y_coords:
            if y < y_min:
                y_min = y
            if y > y_max:
                y_max = y
             
        # check if the map point is inside the range
        if map_point.x > x_min and map_point.x < x_max:
            if map_point.y > y_min and map_point.y < y_max:
                if mode == 'vis':
                    self.set_color(map_point.vs_rgb)
                if mode == 'nir':
                    self.set_color(map_point.nir_rgb)
                if mode == 'tmp':
                    self.set_color(map_point.temp_rgb)
                return True
        return False

"""fill entire canvas with triangles, but do not draw them"""
def get_poly(height, width):
    triangles = []

    count = 0
    for y in range(0, int(height / resolution)):
        for x in range(0, int(width / resolution)):
            #create 4 at time for each square, done in order of left, top, bottom, right
            triangles.append(Triangle(count, [resolution*x + resolution/2, resolution * x , resolution * x], 
                                            [resolution*y + resolution/2, resolution * y, resolution * (y + 1)]))
            triangles.append(Triangle(count + 1, [resolution*x + resolution/2, resolution * x , resolution * (x + 1)], 
                                            [resolution*y + resolution/2, resolution * y, resolution * y]))
            triangles.append(Triangle(count + 2, [resolution*x + resolution/2, resolution * (x + 1), resolution * x], 
                                            [resolution*y + resolution/2, resolution * (y + 1), resolution * (y + 1)]))
            triangles.append(Triangle(count + 3, [resolution*x + resolution/2, resolution * (x + 1), resolution * (x + 1)], 
                                            [resolution*y + resolution/2, resolution * y, resolution * (y + 1)]))
            
            count += 4
    
    return triangles

'''resets the color of all triangles'''
def clear_poly(poly_fill):
    for t in poly_fill:
        t.set_color("None")

'''find all triangles containing a map point and fill them
add to list of filled triangles (this is used later!)'''
def draw_data(map_points, poly_fill, mode):
    filled = []
    for mp in map_points: 
        for t in poly_fill:
            if t.contains_point(mp, mode):
                filled.append(t)
    return filled

'''fill all remaining triangles with "None" as their color
add to filled list, this causes for loop to eventually look at all triangles
colors are calculated based on the neighbor's color
if multiple neighbors are found, average their color
This accomplishes blending'''
def fill_all(filled, poly_fill, width, height, resolution):
    for t in filled:
        ids = t.neighbors(width, height, resolution)
        for i in ids:
            if poly_fill[i].color == "None":
                u_ids = poly_fill[i].neighbors(width, height, resolution)
                colors = []
                for j in u_ids:
                    if poly_fill[j].color != "None":
                        colors.append(poly_fill[j].color)
                if len(colors) > 0:
                    poly_fill[i].set_color(Color.average_color(colors))
                    filled.append(poly_fill[i])
                
def draw_flight_path(map_points, canvasName):
    for i in range(1, len(map_points)):
        canvasName.create_line(map_points[i - 1].x, map_points[i - 1].y, map_points[i].x, map_points[i].y)

"""tester for making drone path"""
def create_circle(map_point, radius, canvasName): #center coordinates, radius
    x = map_point.x
    y = map_point.y
    canvasName.create_oval(x - radius, y - radius, x + radius, y + radius, fill = map_point.nir_rgb)

#test on sophia's pc
#gps_points = gpsPoint.read_drone_csv(r'C:\Users\Sophia\Documents\Sophia\college\Spring2021 Textbooks\CSE326\vir-atlas-master\vir-atlas-master\Data Files\Feb-26th-2021-05-57PM-Flight-Airdata.csv')
#stella_points = StellaPoint.make_stella_points(r'C:\Users\Sophia\Documents\Sophia\college\Spring2021 Textbooks\CSE326\vir-atlas-master\vir-atlas-master\Data Files\data.csv')

# Test on Brynn's laptop. (I'll try and make this dynamic later where the user can enter the directory)
# gps_points reads in feb26th flight airdata
# stella_points reads data.csv
def main():
    gps_points = gpsPoint.read_drone_csv(r'Data Files/Feb-26th-2021-05-57PM-Flight-Airdata.csv')
    stella_points = StellaPoint.make_stella_points(r'Data Files/data.csv')

    stella_points = StellaPoint.get_batch(stella_points, "1.X")
    map_points,width,height = MapPoint.set_xy(gps_points, stella_points, canvas_size)

    height = round(height/10) * 10
    width = round(width/10) * 10

    window = tk.Tk()
    vis_map = tk.Canvas(window, width = width, height = height)
    nir_map = tk.Canvas(window, width = width, height = height)
    tmp_map = tk.Canvas(window, width = width, height = height)

    vis_map.pack()
    nir_map.pack()
    tmp_map.pack()

    poly_fill = get_poly(height, width)
    filled = draw_data(map_points, poly_fill, 'vis')
    fill_all(filled, poly_fill, width, height, resolution)
    for t in poly_fill:
        t.draw(vis_map)
    draw_flight_path(map_points, vis_map)

    clear_poly(poly_fill)
    filled = draw_data(map_points, poly_fill, 'nir')
    fill_all(filled, poly_fill, width, height, resolution)
    for t in poly_fill:
        t.draw(nir_map)
    draw_flight_path(map_points, nir_map)

    clear_poly(poly_fill)
    filled = draw_data(map_points, poly_fill, 'tmp')
    fill_all(filled, poly_fill, width, height, resolution)
    for t in poly_fill:
        t.draw(tmp_map)
    draw_flight_path(map_points, tmp_map)

    window.mainloop()

if __name__ == '__main__':
    main()
