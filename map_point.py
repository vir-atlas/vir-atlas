# @author   Sophia Novo-Gradac
# 3/12/2021
# @brief    map_point object: holds respective stella_point, gps_point, and the various colors to display at coords x,y
#           Combines stella_point and gps_point into a point with a color and x,y coords for placing onto a canvas
# last updated: 4/12/2021 by Sophia Novo-Gradac
# @updates  made init_map_list(). Use this function to process all data
#           added detect_batch() which finds the correct batch based on gps data
# TODO:     build exception case for itnl dateline

import gps_point
import stella_point
import color as col
from math import tan
import numpy as np
import datetime

# visual wavelengths taken by STELLA are constant
vis_wl = [450, 500, 550, 570, 600, 650]
# near infared wavelengths taken by STELLA are constant
nir_wl = [610, 680, 730, 760, 810, 860]
black = "#000000"


class MapPoint:
    """map_point holds necessary info to put point on map.
    color = color to display
    x,y = pixel to display on"""

    def __init__(self, stella_point, gps_point, x, y):
        super(MapPoint, self).__init__()
        self.stella_point = stella_point        # added new stella_point attribute
        self.gps_point = gps_point
        self.vis_rgb = set_vis(stella_point)
        self.nir_rgb = set_nir(stella_point)
        self.temp_rgb = "None"
        self.x = x
        self.y = y
        # radius of data area. Aperature is +- 20 degrees (0.349 rads)
        self.confidence = gps_point.feet_since_takeoff * tan(0.349066)

    """print data to terminal. for debugging"""

    def print_point(self):
        # print(self.stella_point.timestamp, self.gps_point.time, self.color,
        # self.x, self.y)  # stella_point.timestamp may not print
        print(self.vis_rgb, self.nir_rgb, self.x, self.y)


""" Next 4 functions find max or min of latitude or longitude from all gps data points """


def find_min_lat(gps_list):
    num_points = len(gps_list)
    min = gps_list[0].latitude
    for i in range(num_points):
        if gps_list[i].latitude < min:
            min = gps_list[i].latitude
    return min


def find_min_lon(gps_list):
    num_points = len(gps_list)
    min = gps_list[0].longitude
    for i in range(num_points):
        if gps_list[i].longitude < min:
            min = gps_list[i].longitude
    return min


def find_max_lat(gps_list):
    num_points = len(gps_list)
    max = gps_list[0].latitude
    for i in range(num_points):
        if gps_list[i].latitude > max:
            max = gps_list[i].latitude
    return max


def find_max_lon(gps_list):
    num_points = len(gps_list)
    max = gps_list[0].longitude
    for i in range(num_points):
        if gps_list[i].longitude > max:
            max = gps_list[i].longitude
    return max


"""Scales to given canvas_size
returns list of map_list and the width and height of the canvas"""


def set_xy(gps_list, stella_list, canvas_size):

    min_lat = find_min_lat(gps_list)
    min_lon = find_min_lon(gps_list)
    max_lat = find_max_lat(gps_list)
    max_lon = find_max_lon(gps_list)

    map_list = []

    if (max_lat - min_lat) >= (max_lon - min_lon):
        delta = max_lat - min_lat
    else:
        delta = max_lon - min_lon

    scale = canvas_size / delta

    height = (max_lat - min_lat) * scale  # canvas height
    width = (max_lon - min_lon) * scale  # canvas width
    # one of the above will be equal to canvas_size depending on shape of data

    s_cur = 0
    g_cur = 0
    for gps in gps_list:

        # if count >= len(stella_list):     # stop adding points after exhausting stella_point List
        #     print("Not enough Stella Objects")
        #     break

        # skips over points that are recorded less than 1 foot off the ground
        if gps.feet_since_takeoff < 1:
            # s_cur += 1
            g_cur += 1
            continue

        y = (abs(max_lat - gps.latitude)) * scale
        x = (gps.longitude - min_lon) * scale

        if s_cur < len(stella_list):
            if g_cur == 0:
                cur_delta = abs(stella_list[s_cur].timestamp - gps.time)
                post_delta = abs(
                    stella_list[s_cur].timestamp - gps_list[g_cur + 1].time)
                if cur_delta < post_delta:
                    # create new MapPoint object with stella_point
                    map_list.append(MapPoint(stella_list[s_cur], gps, x, y))
                    s_cur += 1

            elif g_cur < len(gps_list):
                prev_delta = abs(
                    stella_list[s_cur].timestamp - gps_list[g_cur - 1].time)
                cur_delta = abs(stella_list[s_cur].timestamp - gps.time)
                if cur_delta < prev_delta:
                    # create new MapPoint object with stella_point
                    map_list.append(MapPoint(stella_list[s_cur], gps, x, y))
                    s_cur += 1

            else:
                prev_delta = abs(
                    stella_list[s_cur].timestamp - gps_list[g_cur - 1].time)
                cur_delta = abs(stella_list[s_cur].timestamp - gps.time)
                post_delta = abs(
                    stella_list[s_cur].timestamp - gps_list[g_cur + 1].time)

                if cur_delta < prev_delta and cur_delta < post_delta:
                    # create new MapPoint object with stella_point
                    map_list.append(MapPoint(stella_list[s_cur], gps, x, y))
                    s_cur += 1

        g_cur += 1
        # color = set_color(stella)                         # create RGB color (type str)
        # print(stella.timestamp, ', ', gps.time, ', ', gps.latitude, ', ',
        # gps.longitude, color)   # and associated color
    set_all_temps(map_list, stella_list)

    return map_list, width, height, max_lat - min_lat


"""functions below set the various colors for map_point. vis nir, and temp respectively.
    currently handles workaround where all values are 0"""
"""pull irradiance values from a stella_point object
    calls col.data_to_hex() to gather the RGB value (of type str) and return it to calling method."""


def set_vis(stella_point):
    max_i = max(stella_point.vis_pows)
    rgb = black
    if max_i > 0:
        rgb = col.data_to_hex(stella_point.vis_pows, vis_wl)

    return rgb


def set_nir(stella_point):
    max_i = max(stella_point.nir_pows)
    rgb = black
    if max_i > 0:
        rgb = col.data_to_hex(stella_point.nir_pows, nir_wl)

    return rgb


def get_min_temp(stella_list):
    min_temp = float(stella_list[0].surface_temp)
    for s in stella_list:
        if float(s.surface_temp) < min_temp:
            min_temp = float(s.surface_temp)
    return min_temp


def get_max_temp(stella_list):
    max_temp = float(stella_list[0].surface_temp)
    for s in stella_list:
        if float(s.surface_temp) > max_temp:
            max_temp = float(s.surface_temp)
    return max_temp


def set_temp(stella_point, min_temp, max_temp):
    # max_temp = 85.0
    # min_temp = -40.0 #max and min the sensor can see
    col.false_color(stella_point.surface_temp, min_temp, max_temp)


def set_all_temps(map_list, stella_list):
    max_temp = get_max_temp(stella_list)
    min_temp = get_min_temp(stella_list)
    for m in map_list:
        set_temp(m.stella_point, min_temp, max_temp)


"""test function"""


def print_mins(gps_list):
    min_lat = find_min_lat(gps_list)
    min_lon = find_min_lon(gps_list)
    print(min_lat, min_lon)


def detect_batch(gps_list, stella_list):
    time = gps_list[0].time
    batch = stella_list[0].batch
    prev_delta = abs((time - stella_list[0].timestamp).total_seconds())

    for s in stella_list:
        delta = abs((time - s.timestamp).total_seconds())
        if delta < prev_delta:
            delta = prev_delta
            batch = s.batch
    return batch


'''do all function for MapPoint.
use to process all data'''


def init_map_list(gps_file, stella_file, canvas_size):
    gps_list = gps_point.read_drone_csv(gps_file)
    stella_list = stella_point.make_stella_list(stella_file)

    batch = detect_batch(gps_list, stella_list)

    stella_list = stella_point.get_batch(stella_list, batch)

    map_list, width, height, delta_lat = set_xy(
        gps_list, stella_list, canvas_size)
    return map_list, width, height, delta_lat
