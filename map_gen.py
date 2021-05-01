# !/usr/bin/env python3
# -*-coding:utf-8 -*-
""" Functions for generating a map in tkinter from a data set stored in a list of MapPoints

Voronoi polygons are used to fill the map.
MapPoints are used as seeds to generate the polygons
To fill the entire map, quasi-random points are also generated as seeds. Their spacing depends on resolution.
To consider altitude, if the seed is outside of the field of view of stella (kept as "confidence" in a MapPoint)
the color is scaled to gray appropriately.
Within double the radius, the color is halfway between the proper data and grey.
Outside double the radius, the color fades to gray.
This is meant to represent the possible area that the data refers to.
The lower the altitude, the more accurate the data, but the less area it applies to.
"""

import tkinter as tk
import map_point
import color as col
import math
from scipy.spatial import Voronoi
import numpy as np
import annotation

__authors__ = ["Sophia Novo-Gradac"]
__maintainer__ = "Sophia Novo-Gradac"
__email__ = "sophia.novo-gradac@student.nmt.edu"


def create_circle(map_point, ftpix, mode, canvasName):
    """ draws a circle on a map given a map point. Used for testing color and altitude. """

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


def feet_to_pix(delta_lat, height):
    """ return the multiplier that translates feet on the ground to pixels on the map """

    delta_ft = delta_lat * 60 * 6076.12
    return height / delta_ft


def get_pairs(map_list):
    """ returns minimum and maximum Gps Coordinate recorded as array"""

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
    """ Holds a list of map points, list of polygons, and defining dataset characteristics """

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
        """ initializes map with new data files """

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
            self.map_list, self.width, self.height, self.delta_lat, self.min_temp, self.max_temp = map_point.init_map_list(
                gps_file, stella_file,
                canvas_size)
            self.scale = feet_to_pix(self.delta_lat, self.height)

        annotation.set_map_list(self.map_list, self.scale)

        self.width = int(math.ceil(self.width))
        self.height = int(math.ceil(self.height))

    def clear_map(self):
        """ clears map data such that lists are empty and constants are set to 0 """

        self.map_list.clear()
        self.poly_list.clear()
        self.width = 0
        self.height = 0
        self.delta_lat = 0
        self.scale = 0
        self.max_temp = 0
        self.min_temp = 0
        self.air_temp = 0

    def gen_map_simple(self, mode, canvas):
        """ sets map data on canvas using circles. Some data will overlap. Mode chooses which colorset to use. """

        # canvas.config(width = self.width, height = self.height)

        for m in self.map_list:
            create_circle(m, self.scale, mode, canvas)

        self.draw_flight_path(self.map_list, canvas)
        return canvas

    def gen_map(self, mode, resolution, canvas):
        """ sets map data on canvas using generated Voronoi polygons. Mode chooses which colorset to use. """

        # check to see if polygons were already created. If not, generate them
        if len(self.poly_list) == 0:
            vor, points = self.get_Voronoi(resolution)
            self.poly_list = self.get_poly_list(vor, points)

        for p in self.poly_list:
            p.draw(mode, self.scale, canvas)

        self.draw_flight_path(canvas)
        return canvas

    def save_map(self, file):
        """ caller for saving a map_list to a file """

        map_point.save_list(self.map_list, file)

    def draw_flight_path(self, canvasName):
        """ draws the flight path as arrows on map. Points of arrows correspond to a point of data """

        for i in range(1, len(self.map_list)):
            canvasName.create_line(self.map_list[i - 1].x, self.map_list[i - 1].y, self.map_list[i].x,
                                   self.map_list[i].y,
                                   arrow=tk.LAST, dash=(6, 2), fill='black', width=2)

    def get_Voronoi(self, resolution):
        """ generate seeds to generate polygons, then return Voronoi object and the list of seeds as tuple

        Voronoi import: https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.Voronoi.html
        Uses fortune's algorithm and list of seeds to generate
        """

        # get quasi-random filling seeds
        points = np.empty((0, 2), int)
        for a in range(resolution, self.height, resolution):
            for b in range(resolution, self.width, resolution):
                bound = int(resolution / 1.5)
                x = b + np.random.randint(low=-bound, high=bound)
                y = a + np.random.randint(low=-bound, high=bound)

                points = np.append(points, np.array([[x, y]]), axis=0)

        # add data points to list of seeds
        for m in self.map_list:
            points = np.append(points, np.array([[m.x, m.y]]), axis=0)

        vor = Voronoi(points)
        return vor, points

    def get_poly_list(self, vor, points):
        """ Return a list of polygons generated from data held in Voronoi object

        Voronoi holds number of lists
        point_region -> index in regions of corresponding seed
        regions -> indexes of the vertices that form the region
        vertices -> coordinates of each polygon vertex as "x, y"
        Looping through this list, pair each set of vertices with their corresponding seed.
        Then pair their closest MapPoint and repair any vertices outside the canvas bounds
        """

        poly_list = list()
        vertices = list()

        count = 0
        for v in vor.point_region:
            for i in vor.regions[v]:
                if i != -1:
                    vertices.append(vor.vertices[i][0])
                    vertices.append(vor.vertices[i][1])
            if len(vertices) != 0:
                poly_list.append(VorPoly(vertices, points[count]))
                vertices.clear()
            count += 1

        for p in poly_list:
            p.get_map_point(self.map_list)
            p.repair(self.width, self.height)

        return poly_list


class VorPoly:
    """ Holds relevant polygon information for drawing """

    def __init__(self, vertices, seed):
        self.vertices = vertices.copy()  # Points required to draw
        self.seed = seed  # Used for radius comparison
        self.map_point = None  # Gives color
        self.dist = 0  # distance from MapPoint held

    def draw(self, mode, scale, canvas):
        """ sets color based on the mode selected, map point held, and distance from data, then draws on canvas """

        # set color
        color = '#7d7d7d'
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

        # mute to gray if outside of field of view
        if self.dist > 0:
            ratio = self.map_point.confidence * scale / self.dist
            if ratio < 1:
                ratio -= 0.25
                color = col.fade(ratio, color)
                if ratio < 0:
                    color = '#7d7d7d'

        if self.vertices:
            canvas.create_polygon(self.vertices, fill=color)

    def get_map_point(self, map_list):
        """ Find and set each polygon's nearest point of data """

        self.map_point = map_list[0]
        self.dist = math.dist(self.seed, [self.map_point.x, self.map_point.y])

        for m in map_list:
            if math.dist(self.seed, [m.x, m.y]) < self.dist:
                self.map_point = m
                self.dist = math.dist(self.seed, [self.map_point.x, self.map_point.y])

    def repair(self, width, height):
        """ If a vertex is outside of the canvas range, delete it """

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
