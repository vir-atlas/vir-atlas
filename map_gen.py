# @author Sophia Novo-Gradac
# 3/12/2021
# @brief:   draws entire map area based on stella data
#           this is accomplished with triangles
# last updated: 4/15/2021 by Sophia Novo-Gradac
# @updates  added ifs for VI and SVA map
#           canvas size reconfiged based on calculations in get_map_alt

import tkinter as tk
import map_point
import color as col
import math
from scipy.spatial import Voronoi
import numpy as np
import annotation


"""tester for making drone path"""

def create_circle(map_point, ftpix, mode, canvasName):  # center coordinates, radius
    x = map_point.x
    y = map_point.y
    radius = map_point.confidence * ftpix
    color = '#000000'
    if mode == 'vis':
        color = map_point.vis_rgb
    if mode == 'nir':
        color = map_point.nir_rgb
    if mode == 'temp':
        color = map_point.temp_rgb
    if mode == 'ndvi':
        color = map_point.ndvi_rgb  # various vegetation index colors
    if mode == 'evi':
        color = map_point.evi_rgb
    if mode == 'savi':
        color = map_point.savi_rgb
    if mode == 'msavi':
        color = map_point.msavi_rgb
    if mode == 'sva':
        color = map_point.sva_rgb

    canvasName.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color, outline='')


'''return multiplier that translates feet to pixels
height in pixels '''


def feet_to_pix(delta_lat, height):
    delta_ft = delta_lat * 60 * 6076.12
    return height / delta_ft


def get_pairs(map_list):
    min_lon = map_list[0].gps_point.longitude
    min_lat = map_list[0].gps_point.latitude
    max_lon = map_list[0].gps_point.longitude
    max_lat = map_list[0].gps_point.latitude

    for point in map_list:
        if point.gps_point.longitude < min_lon:
            min_lon = point.gps_point.longitude

        if point.gps_point.latitude < min_lat:
            min_lat = point.gps_point.latitude

        if point.gps_point.longitude > max_lon:
            max_lon = point.gps_point.longitude

        if point.gps_point.latitude > max_lat:
            max_lat = point.gps_point.latitude

    return [min_lon, min_lat, max_lon, max_lat]


class Map:
    def __init__(self):
        self.map_list = list()
        self.poly_list = list()
        self.width = 0
        self.height = 0
        self.delta_lat = 0
        self.scale = 0
        self.max_temp = 0
        self.min_temp = 0
        self.air_temp = 0


    def update_map(self, canvas_size, gps_file=0, stella_file=0, map_file=0):
        self.clear_map()
        if map_file != '':
            self.map_list = map_point.read_map_list(map_file)

            min_lat = self.map_list[0].gps_point.latitude
            max_lat = self.map_list[0].gps_point.latitude
            self.max_temp = self.map_list[0].stella_point.surface_temp
            self.min_temp = self.map_list[0].stella_point.surface_temp
            self.air_temp = self.map_list[0].stella_point.air_temp

            for m in self.map_list:
                if m.x > self.width:
                    self.width = m.x
                if m.y > self.height:
                    self.height = m.y
                if m.gps_point.latitude > max_lat:
                    max_lat = m.gps_point.latitude
                elif m.gps_point.latitude < min_lat:
                    min_lat = m.gps_point.latitude
                if m.stella_point.surface_temp > self.max_temp:
                    self.max_temp = m.stella_point.surface_temp
                elif m.stella_point.surface_temp < self.min_temp:
                    self.min_temp = m.stella_point.surface_temp
                self.air_temp += self.map_list[0].stella_point.air_temp

            self.air_temp = self.air_temp / len(self.map_list)

            self.width = self.width / 0.9
            self.height = self.height / 0.9

            self.delta_lat = max_lat - min_lat
            self.scale = feet_to_pix(self.delta_lat, self.height)

        elif gps_file != '' and stella_file != '':
            self.map_list, self.width, self.height, self.delta_lat, self.min_temp, self.max_temp = map_point.init_map_list(gps_file, stella_file,
                                                                                             canvas_size)
            self.scale = feet_to_pix(self.delta_lat, self.height)
        
        annotation.set_map_list(self.map_list, self.scale)

        self.width = int(math.ceil(self.width))
        self.height = int(math.ceil(self.height))

        # annotation.set_map_list(self.map_list, self.scale)


    def clear_map(self):
        self.map_list.clear()
        self.width = 0
        self.height = 0
        self.delta_lat = 0
        self.scale = 0
        self.poly_list.clear()

    def gen_map_alt(self, mode, canvas):

        # canvas.config(width = self.width, height = self.height)

        for m in self.map_list:
            create_circle(m, self.scale, mode, canvas)

        self.draw_flight_path(self.map_list, canvas)
        return canvas

    def gen_map(self, mode, resolution, canvas):
        if len(self.poly_list) == 0:
            vor, points = self.get_Voronoi(resolution)
            self.poly_list = self.get_poly_list(vor, points)

        for p in self.poly_list:
            p.draw(mode, self.scale, canvas)

        self.draw_flight_path(canvas)
        return canvas

    def save_map(self, file):
        map_point.save_list(self.map_list, file)


    '''draws drone flight path with a black line'''

    def draw_flight_path(self, canvasName):
        for i in range(1, len(self.map_list)):
            canvasName.create_line(self.map_list[i - 1].x, self.map_list[i - 1].y, self.map_list[i].x, self.map_list[i].y,
                                   arrow=tk.LAST, dash=(6, 2), fill='black', width=2)

    def get_Voronoi(self, resolution):
        points = np.empty((0, 2), int)
        for a in range(resolution, self.height, resolution):
            for b in range(resolution, self.width, resolution):
                bound = int(resolution / 1.5)
                x = b + np.random.randint(low=-bound, high=bound)
                y = a + np.random.randint(low=-bound, high=bound)

                points = np.append(points, np.array([[x, y]]), axis=0)

        # for m in self.map_list:
        #     points = np.append(points, np.array([[m.x, m.y]]), axis=0)

        vor = Voronoi(points)
        return vor, points

    def get_poly_list(self, vor, points):
        poly_list = list()
        vertices = list()

        count = 0
        complete = True
        for v in vor.point_region:
            for i in vor.regions[v]:
                if i != -1:
                    vertices.append(vor.vertices[i][0])
                    vertices.append(vor.vertices[i][1])
                elif i == -1:
                    # print("in i == -1")
                    # vertices.clear()
                    complete = False
                    # break
            if len(vertices) != 0:
                poly_list.append(VorPoly(vertices, points[count], complete))
                vertices.clear()
            complete = True
            count += 1

        for p in poly_list:
            p.get_map_point(self.map_list)
            p.repair(self.width, self.height)

        return poly_list


class VorPoly:
    def __init__(self, vertices, seed, complete):
        self.vertices = vertices.copy()
        self.seed = seed
        self.map_point = None
        self.dist = 0
        self.complete = complete

    def draw(self, mode, scale, canvas):
        if mode == 'vis':
            color = self.map_point.vis_rgb
        if mode == 'nir':
            color = self.map_point.nir_rgb
        if mode == 'temp':
            color = self.map_point.temp_rgb
        if mode == 'ndvi':
            color = self.map_point.ndvi_rgb  # various vegetation index colors
        if mode == 'evi':
            color = self.map_point.evi_rgb
        if mode == 'savi':
            color = self.map_point.savi_rgb
        if mode == 'msavi':
            color = self.map_point.msavi_rgb
        if mode == 'sva':
            color = self.map_point.sva_rgb


        if self.dist > 0:
            ratio = self.map_point.confidence * scale / self.dist
            if ratio < 1:
                ratio -= 0.25
                color = col.fade(ratio, color)
                if ratio < 0:
                    color = '#7d7d7d'

        # print(self.vertices, color)
        if self.vertices:
            canvas.create_polygon(self.vertices, fill=color)


    def get_map_point(self, map_list):
        self.map_point = map_list[0]
        self.dist = math.dist(self.seed, [self.map_point.x, self.map_point.y])

        for m in map_list:
            if math.dist(self.seed, [m.x, m.y]) < self.dist:
                self.map_point = m
                self.dist = math.dist(self.seed, [self.map_point.x, self.map_point.y])

    def repair(self, width, height):
        i = len(self.vertices) - 1
        while i > -1:
            if i % 2 == 0:
                if self.vertices[i] < 0 or self.vertices[i] > width:
                    self.vertices.pop(i)
                    self.vertices.pop(i)
                    i -= 1
            else:
                if self.vertices[i] < 0 or self.vertices[i] > height:
                    self.vertices.pop(i - 1)
                    self.vertices.pop(i - 1)
                    i -= 1
            i -= 1


