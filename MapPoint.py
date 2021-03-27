# @author   Sophia Novo-Gradac
# 3/12/2021
# @brief    map_point object: holds respective stella_point, gps_point, and the various colors to display at coords x,y
#           Combines stella_point and gps_point into a point with a color and x,y coords for placing onto a canvas
# last updated: 3/16/2021 by Sophia Novo-Gradac
# @updates  added colors for each type of map. (vs, nir, and temp)
#           link map_points based on delta ms timestamps calculated in both gps and stella points
#           colors are calculated on init in map_point object
#
# TODO:     consider chopping points from takeoff/landing
#           consider any other data points from the drone that shoul be kept
#           define canvas_size by data
#           build exception case for itnl dateline
#           fix temp_rgb function (only displaying red right now?)

import gpsPoint
import StellaPoint
import Color
from math import *

canvas_size = 500
black = "#000000"

class MapPoint:
    """map_point holds necessary info to put point on map.
    color = color to display
    x,y = pixel to display on"""
    def __init__(self, stella_point, gps_point, x, y):
        super(MapPoint, self).__init__()
        self.stella_point = stella_point        # added new stella_point attribute
        self.gps_point = gps_point
        self.vs_rgb = set_vs(stella_point)
        self.nir_rgb = set_nir(stella_point)
        self.temp_rgb = set_temp(stella_point)
        self.x = x
        self.y = y

    """print data to terminal. for debugging"""
    def print_point(self):
        # print(self.stella_point.timestamp, self.gps_point.time, self.color, self.x, self.y)  # stella_point.timestamp may not print
        print(self.vs_rgb, self.nir_rgb, self.x, self.y)

""" Next 4 functions find max or min of latitude or longitude from all gps data points """
def find_min_lat(gps_points):
    num_points = len(gps_points)
    min = gps_points[0].latitude
    for i in range(num_points):
        if gps_points[i].latitude < min:
            min = gps_points[i].latitude
    return min

def find_min_lon(gps_points):
    num_points = len(gps_points)
    min = gps_points[0].longitude
    for i in range(num_points):
        if gps_points[i].longitude < min:
            min = gps_points[i].longitude
    return min

def find_max_lat(gps_points):
    num_points = len(gps_points)
    max = gps_points[0].latitude
    for i in range(num_points):
        if gps_points[i].latitude > max:
            max = gps_points[i].latitude
    return max

def find_max_lon(gps_points):
    num_points = len(gps_points)
    max = gps_points[0].longitude
    for i in range(num_points):
        if gps_points[i].longitude > max:
            max = gps_points[i].longitude
    return max

"""assumes canvas size of 500 x 500 pixels and scales to it. Need to determine how we want to handle canvas size"""
def set_xy(gps_points, stella_points):

    min_lat = find_min_lat(gps_points)
    min_lon = find_min_lon(gps_points)
    max_lat = find_max_lat(gps_points)
    max_lon = find_max_lon(gps_points)

    map_points = []

    if (max_lat - min_lat) >=  (max_lon - min_lon):
        delta = max_lat - min_lat
    else:
        delta = max_lon - min_lon

    scale = canvas_size / delta

    s_cur = 0
    g_cur = 0
    for gps in gps_points:

        y = (abs(max_lat - gps.latitude)) * scale
        x = (gps.longitude - min_lon) * scale

        # if count >= len(stella_points):     # stop adding points after exhausting stella_point List
        #     print("Not enough Stella Objects")
        #     break

        if g_cur == 0 and stella_points[s_cur]:
            cur_delta = abs(stella_points[s_cur].timestamp - gps.time)
            post_delta = abs(stella_points[s_cur].timestamp - gps_points[g_cur + 1].time)
            if cur_delta < post_delta:
                map_points.append(MapPoint(stella_points[s_cur], gps, black, x, y))  # create new MapPoint object with stella_point
                s_cur += 1

        elif not (g_cur >= len(gps_points)) and stella_points[s_cur]:
            prev_delta = abs(stella_points[s_cur].timestamp - gps_points[g_cur - 1].time)
            cur_delta = abs(stella_points[s_cur].timestamp - gps.time)
            if cur_delta < prev_delta:
                map_points.append(MapPoint(stella_points[s_cur], gps, x, y))  # create new MapPoint object with stella_point
                s_cur += 1

        elif stella_points[s_cur]:
            prev_delta = abs(stella_points[s_cur].timestamp - gps_points[g_cur - 1].time)
            cur_delta = abs(stella_points[s_cur].timestamp - gps.time)
            post_delta = abs(stella_points[s_cur].timestamp - gps_points[g_cur + 1].time)

            if cur_delta < prev_delta and cur_delta < post_delta:
                map_points.append(MapPoint(stella_points[s_cur], gps, black, x, y))  # create new MapPoint object with stella_point
                s_cur += 1

        g_cur += 1
        # color = set_color(stella)                         # create RGB color (type str)
        # print(stella.timestamp, ', ', gps.time, ', ', gps.latitude, ', ', gps.longitude, color)   # and associated color

    return map_points


"""functions below set the various colors for map_point. Vs nir, and temp respectively.
    currently handles workaround where all values are 0"""
"""pull irradiance values from a stella_point object
    calls Color.data_to_hex() to gather the RGB value (of type str) and return it to calling method."""
def set_vs(stella_point):
    max_i = max(stella_point.vs_pows)
    rgb = black
    if max_i > 0:
        rgb = Color.data_to_hex(stella_point.vs_pows)

    return rgb

def set_nir(stella_point):
    max_i = max(stella_point.nir_pows)
    rgb = black
    if max_i > 0:
        rgb = Color.data_to_hex(stella_point.nir_pows)

    return rgb

def set_temp(stella_point):
    max_temp = 40.0
    min_temp = -30.0
    red = 0
    green = 0
    blue = 0

    # convert temp to a percentage scale of 0 to 100
    temp = (-1 * min_temp + float(stella_point.surface_temp))/(-1 * min_temp + max_temp)

    # OoR = out of range
    def OoR(color):
        if color < 0:
            color = 0

        if color > 255:
            color = 255

        return color

    # define the red value
    def rgb_red(temp):
        if temp <= 66:
            red = 255

        else:
            red = temp - 60
            red = 329.698727446 * (red ** -0.1332047592)
            red = OoR(red)

        return red

    # define the green value
    def rgb_green(temp):
        if temp <= 66:
            green = temp
            green = 99.4708025861 * log(green) - 161.1195681661

        else:
            green = temp - 60
            green = 288.1221695283 * (green ** -0.0755148492)

        green = OoR(green)

        return green

    # define the blue value
    def rgb_blue(temp):
        if temp >= 66:
            blue = 255

        else:
            if temp <= 19:
                blue = 0

            else:
                blue = temp - 10
                blue = 138.5177312231 * log(blue) - 305.0447927307
                blue = OoR(blue)

        return blue

    red = rgb_red(temp)
    green = rgb_green(temp)
    blue = rgb_blue(temp)
    return Color.rgb_to_hex([red, green, blue])


"""test function"""
def print_mins(gps_points):
    min_lat = find_min_lat(gps_points)
    min_lon = find_min_lon(gps_points)
    print(min_lat, min_lon)


# test for Sophia's computer
# gps_points = gpsPoint.read_drone_csv("Data Files/Feb-26th-2021-05-57PM-Flight-Airdata.csv")
# stella_points = StellaPoint.make_stella_points("Data Files/data.csv")
# stella_points = StellaPoint.get_batch(stella_points, "1.X")
# map_points = set_xy(gps_points, stella_points)
#
# for map in map_points:
#     map.print_point()

# # test for Ty's computer
# gps_points = gpsPoint.read_drone_csv("Data Files/Feb-26th-2021-05-57PM-Flight-Airdata.csv")
# set_xy(gps_points)
