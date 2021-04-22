# @author   Sophia Novo-Gradac
# 3/12/2021
# @brief    map_point object: holds respective stella_point, gps_point, and the various colors to display at coords x,y
#           Combines stella_point and gps_point into a point with a color and x,y coords for placing onto a canvas
# last updated: 4/15/2021 by Sophia Novo-Gradac
# @updates  added 4 color functions/variables for vegetative index
#           added function/variable for surface vs air temperature
# TODO:     build exception case for itnl dateline

import gps_point
import stella_point
import color as col
import math
import numpy as np
import datetime
import pickle
import annotation

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
        self.sva_rgb = "None" #surface vs air temperature

        self.ndvi_rgb = set_ndvi(stella_point) # various vegetation index colors 
        self.evi_rgb = set_evi(stella_point)
        self.savi_rgb = set_savi(stella_point)
        self.msavi_rgb = set_msavi(stella_point)
        
        self.x = x
        self.y = y
        self.confidence = gps_point.feet_since_takeoff * math.tan(0.349066) # radius of data area. Aperature is +- 20 degrees (0.349 rads)

        self.annotation = ""

    """print data to terminal. for debugging"""

    def print_point(self):
        # print(self.stella_point.timestamp, self.gps_point.time, self.color,
        # self.x, self.y)  # stella_point.timestamp may not print
        # print(self.vis_rgb, self.nir_rgb, self.x, self.y)
        self.stella_point.print_stella()
        self.gps_point.print_gps()
        print(self.vis_rgb, self.nir_rgb, self.temp_rgb, self.sva_rgb, 
                self.ndvi_rgb, self.evi_rgb, self.savi_rgb, self.msavi_rgb, 
                self.x, self.y, self.confidence, self.annotation)

    def write_point(self, file):
        self.stella_point.write_stella(file)
        self.gps_point.write_gps(file)
        print(self.vis_rgb, self.nir_rgb, self.temp_rgb, self.sva_rgb, 
                self.ndvi_rgb, self.evi_rgb, self.savi_rgb, self.msavi_rgb, 
                self.x, self.y, self.confidence, self.annotation, file=file)
        # file.write(self.vis_rgb, self.nir_rgb, self.temp_rgb, self.sva_rgb, 
        #         self.ndvi_rgb, self.evi_rgb, self.savi_rgb, self.msavi_rgb, 
        #         self.x, self.y, self.confidence, self.annotation)

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
    annotation.set_map_list(map_list)

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

'''below 2 functions get min/max temperatures recorded'''
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

''' set the temp_rgb for 1 map_point'''
def set_temp(map_point, min_temp, max_temp):
    # max_temp = 85.0
    # min_temp = -40.0 #max and min the sensor can see
    map_point.temp_rgb = col.false_color(map_point.stella_point.surface_temp, min_temp, max_temp)

    temp_delta = map_point.stella_point.surface_temp - map_point.stella_point.air_temp
    min_delta = min_temp - map_point.stella_point.air_temp
    max_delta = max_temp - map_point.stella_point.air_temp
    red = '#ff0000'
    blue = '#0000ff'

    map_point.sva_rgb = col.false_two_color(temp_delta, min_delta, max_delta, blue, red)

''' For all map_points in list, set the temp_rgb '''
def set_all_temps(map_list, stella_list):
    max_temp = get_max_temp(stella_list)
    min_temp = get_min_temp(stella_list)
    for m in map_list:
        set_temp(m, min_temp, max_temp)


'''below are functions for calculating colors for various landsat maps
Follow Landsat 8 procedures.
Landsat 8 procedures: https://www.usgs.gov/core-science-systems/nli/landsat/landsat-surface-reflectance-derived-spectral-indices?qt-science_support_page_related_con=0#qt-science_support_page_related_con
Currently Included: NDVI, EVI, SAVI, MSAVI 
Unavailable due to Stella Data: NDMI, NBR, NBR2 '''

'''
Landsat 8 Bands: https://www.usgs.gov/faqs/what-are-best-landsat-spectral-bands-use-my-research?qt-news_science_products=0#qt-news_science_products
Band 1 - 0.43-0.45 - vis_pows[0]
Band 2 - 0.45-0.51 - vis_pows[0,1]
Band 3 - 0.53-0.59 - vis_pows[2,3]
Band 4 - 0.64-0.67 - vis_pows[5]
Band 5 - 0.85-0.88 - nir_pows[5]
Band 6 - 1.57-1.65 - n/a
Band 7 - 2.11-2.29 - n/a
Band 8 - 0.50-0.68 - vis_pows[1-5] nir_pows[0,1]
Band 9 - 1.36-1.38 - n/a
Band 10 - 10.60-11.19 - n/a
Band 11 - 1.50-12.51 - n/a
'''

def set_ndvi(stella_point):
    band4 = stella_point.vis_pows[5]
    band5 = stella_point.nir_pows[5]

    ndvi = (band5 - band4) / (band5 + band4) #range of 1 -> -1
    
    if ndvi > 1:
        print("ndvi > 1: ", ndvi)
        ndvi = 1
    if ndvi < -1:
        print("ndvi < -1: ", ndvi)
        ndvi = -1

    #1 = green, 0 = white?, -1 = blue
    return col.false_color_vi(ndvi)

def set_evi(stella_point):
    band2 = (stella_point.vis_pows[0] + stella_point.vis_pows[1]) / 2
    band4 = stella_point.vis_pows[5]
    band5 = stella_point.nir_pows[5]

    evi = 2.5 * ((band5 - band4) / (band5 + (6 * band4) - (7.5 * band2) + 1))

    if evi > 1:
        print("evi > 1: ", evi)
        # print(evi)
        # print(stella_point.vis_pows)
        # print(stella_point.nir_pows)
        evi = 1
    if evi < -1:
        print("evi < -1: ", evi)
        # print(evi)
        # print(stella_point.vis_pows)
        # print(stella_point.nir_pows)
        evi = -1

    return col.false_color_vi(evi)

def set_savi(stella_point):
    band4 = stella_point.vis_pows[5]
    band5 = stella_point.nir_pows[5]

    savi = ((band5 - band4) / (band5 + band4 + 0.5)) * (1.5)

    if savi > 1:
        print("savi > 1: ", savi)
        savi = 1
    if savi < -1:
        print("savi < -1: ", savi)
        savi = -1

    return col.false_color_vi(savi)

def set_msavi(stella_point):
    band4 = stella_point.vis_pows[5]
    band5 = stella_point.nir_pows[5]
    
    msavi = (2 * band5 + 1 - math.sqrt((2 * band5 + 1) ** 2 - 8 * (band5 - band4))) / 2

    if msavi > 1:
        print("msavi > 1: ", msavi)
        msavi = 1
    if msavi < -1:
        print("msavi > -1: ", msavi)
        msavi = -1

    return col.false_color_vi(msavi)

"""test function"""
def print_mins(gps_list):
    min_lat = find_min_lat(gps_list)
    min_lon = find_min_lon(gps_list)
    print(min_lat, min_lon)

'''Based on the gps data, return correct stella batch''' 
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

    map_list, width, height, delta_lat = set_xy(gps_list, stella_list, canvas_size)
    return map_list, width, height, delta_lat

def save_list(map_list, save_file):
    pickle.dump(map_list, open(save_file, "wb"))

def read_map_list(file):
    return pickle.load(open(file, 'rb'))
