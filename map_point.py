# !/usr/bin/env python3
# -*-coding:utf-8 -*-
""" Provides functions for pairing Gps and Stella data to a single point. Also generates proper colors.

A list of StellaPoints and a list of GpsPoints are paired based on time to create a list of MapPoints
Stella's batch is automatically detected.
"""

import gps_point
import stella_point
import color as col
import math
import pickle

__authors__ = ["Sophia Novo-Gradac"]
__maintainer__ = "Sophia Novo-Gradac"
__email__ = "sophia.novo-gradac@student.nmt.edu"

# visual wavelengths taken by STELLA are constant
vis_wl = [450, 500, 550, 570, 600, 650]
# near infared wavelengths taken by STELLA are constant
nir_wl = [610, 680, 730, 760, 810, 860]
black = "#000000"


class MapPoint:
    """ holds respective stella_point, gps_point, and the various colors to display at coords x,y """

    def __init__(self, stella_point, gps_point, x, y):
        super(MapPoint, self).__init__()
        self.stella_point = stella_point  # added new stella_point attribute
        self.gps_point = gps_point

        self.vis_rgb = self.set_vis()
        self.nir_rgb = self.set_nir()
        self.temp_rgb = "None"
        self.sva_rgb = "None"  # surface vs air temperature

        # various vegetation index colors
        self.ndvi_rgb = self.set_ndvi()
        self.evi_rgb = self.set_evi()
        self.savi_rgb = self.set_savi()
        self.msavi_rgb = self.set_msavi()

        self.x = x
        self.y = y
        self.confidence = gps_point.feet_since_takeoff * math.tan(0.349066)
        # radius of data area. Aperature is +- 20 degrees (0.349 rads)

        self.annotation = ""  # default is empty. User adds info here

    def print_point(self):
        """ print all data to terminal."""

        self.stella_point.print_stella()
        self.gps_point.print_gps()
        print(self.vis_rgb, self.nir_rgb, self.temp_rgb, self.sva_rgb,
              self.ndvi_rgb, self.evi_rgb, self.savi_rgb, self.msavi_rgb,
              self.x, self.y, self.confidence, self.annotation)

    def set_vis(self):
        """ Sets color for Visual spectrum data using CIE 1931 standards. Defined in color.py """

        max_i = max(self.stella_point.vis_pows)
        rgb = black
        if max_i > 0:
            rgb = col.data_to_hex(self.stella_point.vis_pows, vis_wl)

        return rgb

    def set_nir(self):
        """ Sets color for NIR data using CIE 1931 standards. Defined in color.py

        If left adjusted, no variation in data can be observed through color.
        Uses NIR power values set with the minimum as 0.
        """

        max_i = max(self.stella_point.nir_pows)
        rgb = black
        m = min(self.stella_point.nir_pows)
        un_adjust = list()
        for n in self.stella_point.nir_pows:
            un_adjust.append(n - m)

        if max_i > 0:
            rgb = col.data_to_hex(un_adjust, nir_wl)

        return rgb

    def set_temp(self, min_temp, max_temp):
        """ sets both raw temp and surface vs air temperature color """

        # max_temp = 85.0
        # min_temp = -40.0 #max and min the sensor can see
        self.temp_rgb = col.false_color(self.stella_point.surface_temp, min_temp, max_temp)

        # temp_delta = self.stella_point.surface_temp - self.stella_point.air_temp
        # min_delta = min_temp - self.stella_point.air_temp
        # max_delta = max_temp - self.stella_point.air_temp
        red = '#ff0000'  # used for "hotter than air"
        blue = '#0000ff'  # used for "colder than air"

        self.sva_rgb = col.false_two_color(self.stella_point.surface_temp, min_temp,
                                           self.stella_point.air_temp, max_temp, blue, red)

    """
    below are functions for calculating colors for various landsat maps
    Follow Landsat 8 procedures.
    Landsat 8 procedures: https://www.usgs.gov/core-science-systems/nli/landsat/landsat-surface-reflectance-derived-spectral-indices?qt-science_support_page_related_con=0#qt-science_support_page_related_con
    Currently Included: NDVI, EVI, SAVI, MSAVI 
    Unavailable due to Stella Data: NDMI, NBR, NBR2 
    """

    """
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
    """

    def set_ndvi(self):
        """ calculates standard VI and sets appropriate color. Equation and band information in links above."""

        band4 = self.stella_point.vis_pows[5]
        band5 = self.stella_point.nir_pows[5]

        band4 = band4 / 10000
        band5 = band5 / 10000

        ndvi = (band5 - band4) / (band5 + band4)  # range of 1 -> -1

        # out of bounds handling
        if ndvi > 1:
            # print("ndvi > 1: ", ndvi)
            ndvi = 1
        if ndvi < -1:
            # print("ndvi < -1: ", ndvi)
            ndvi = -1

        # 1 = green, 0 = white?, -1 = blue
        return col.false_color_vi(ndvi)

    def set_evi(self):
        """ corrects ndvi for atmospheric conditions. sets color. Equation and band information in links above."""

        band2 = (self.stella_point.vis_pows[0] + self.stella_point.vis_pows[1]) / 2
        band4 = self.stella_point.vis_pows[5]
        band5 = self.stella_point.nir_pows[5]

        band2 = band2 / 10000
        band4 = band4 / 10000
        band5 = band5 / 10000

        evi = 2.5 * ((band5 - band4) / (band5 + (6 * band4) - (7.5 * band2) + 1))

        # out of bounds handling
        if evi > 1:
            # print("evi > 1: ", evi)
            evi = 1
        if evi < -1:
            # print("evi < -1: ", evi)
            evi = -1

        return col.false_color_vi(evi)

    def set_savi(self):
        """ corrects ndvi for soil reflectance. sets color. Equation and band information in links above."""

        band4 = self.stella_point.vis_pows[5]
        band5 = self.stella_point.nir_pows[5]

        band4 = band4 / 10000
        band5 = band5 / 10000

        savi = ((band5 - band4) / (band5 + band4 + 0.5)) * (1.5)

        # out of bounds handling
        if savi > 1:
            # print("savi > 1: ", savi)
            savi = 1
        if savi < -1:
            # print("savi < -1: ", savi)
            savi = -1

        return col.false_color_vi(savi)

    def set_msavi(self):
        """ corrects ndvi for bare soil reflectance. sets color. Equation and band information in links above."""

        band4 = self.stella_point.vis_pows[5]
        band5 = self.stella_point.nir_pows[5]

        band4 = band4 / 10000
        band5 = band5 / 10000

        # out of bounds handling
        msavi = (2 * band5 + 1 - math.sqrt((2 * band5 + 1) ** 2 - 8 * (band5 - band4))) / 2

        if msavi > 1:
            # print("msavi > 1: ", msavi)
            msavi = 1
        if msavi < -1:
            # print("msavi > -1: ", msavi)
            msavi = -1

        return col.false_color_vi(msavi)


def find_min_lat(gps_list):
    """ return minimum latitude value recorded by drone """

    num_points = len(gps_list)
    min = gps_list[0].latitude
    for i in range(num_points):
        if gps_list[i].latitude < min:
            min = gps_list[i].latitude
    return min


def find_min_lon(gps_list):
    """ return minimum longitude value recorded by drone """

    num_points = len(gps_list)
    min = gps_list[0].longitude
    for i in range(num_points):
        if gps_list[i].longitude < min:
            min = gps_list[i].longitude
    return min


def find_max_lat(gps_list):
    """ return maximum latitude value recorded by drone """

    num_points = len(gps_list)
    max = gps_list[0].latitude
    for i in range(num_points):
        if gps_list[i].latitude > max:
            max = gps_list[i].latitude
    return max


def find_max_lon(gps_list):
    """ return maximum longitude value recorded by drone"""

    num_points = len(gps_list)
    max = gps_list[0].longitude
    for i in range(num_points):
        if gps_list[i].longitude > max:
            max = gps_list[i].longitude
    return max


def set_xy(gps_list, stella_list, canvas_size):
    """ pair gps and stella points from a list, return list of map_points and defining map features

    x,y coords are generated by scaling longitude and latitude to the canvas size
    See color.py for details on color generation
    returns tuple: map_list, width, height, max_lat - min_lat, min_t, max_t
    width and height refer to new canvas dimensions
    """

    min_lat = find_min_lat(gps_list)
    min_lon = find_min_lon(gps_list)
    max_lat = find_max_lat(gps_list)
    max_lon = find_max_lon(gps_list)

    border = canvas_size * 0.1  # 10% boundary around data

    map_list = []

    if (max_lat - min_lat) >= (max_lon - min_lon):
        delta = max_lat - min_lat
    else:
        delta = max_lon - min_lon

    scale = (canvas_size - 2 * border) / delta

    height = (max_lat - min_lat) * canvas_size / delta + border  # canvas height
    width = (max_lon - min_lon) * canvas_size / delta + border  # canvas width
    # one of the above will be equal to canvas_size depending on shape of data

    chop_takeoff(gps_list, stella_list)

    s_cur = 0
    g_cur = 0
    for gps in gps_list:

        # if count >= len(stella_list):     # stop adding points after exhausting stella_point List
        #     print("Not enough Stella Objects")
        #     break

        y = (abs(max_lat - gps.latitude)) * scale + border
        x = (gps.longitude - min_lon) * scale + border

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

    min_t, max_t = set_all_temps(map_list, stella_list)

    return map_list, width, height, max_lat - min_lat, min_t, max_t


def chop_takeoff(gps_list, stella_list):
    """ removes list values that are not part of the data set because they were during takeoff

    function is performed as data collected during takeoff results in all black and is inconsistent with dataset
    currently done based on time.
    Data taken during landing is chopped through list generation. not included here.
    """

    stella_time_delta = (stella_list[-1].ms - stella_list[0].ms) / len(stella_list)
    gps_time_delta = (gps_list[-1].milliseconds - gps_list[0].milliseconds) / len(gps_list)

    ratio = stella_time_delta / gps_time_delta
    longer_flag = 's'
    num_extra = len(stella_list) - len(gps_list) / ratio
    # print(len(stella_list), len(gps_list), stella_time_delta, gps_time_delta, ratio, num_extra)

    if ratio < 1:
        ratio = 1 / ratio
        longer_flag = 'g'
        num_extra = len(gps_list) - len(stella_list) / ratio

    # only chop half of the extra.
    # assume other half are at the end and will be chopped by pairing
    shift = num_extra / 2.1
    if int(shift) > 0:
        if longer_flag == 's':
            for i in range(int(shift), -1, -1):
                stella_list.pop(i)
            start = stella_list[0].ms
            for s in stella_list:
                s.ms -= start
        if longer_flag == 'g':
            for i in range(int(shift), -1, -1):
                gps_list.pop(i)
            start = gps_list[0].milliseconds
            for g in gps_list:
                g.milliseconds -= start


def get_min_temp(stella_list):
    """ return minimum surface temperature recorded by STELLA """

    min_temp = float(stella_list[0].surface_temp)
    for s in stella_list:
        if float(s.surface_temp) < min_temp:
            min_temp = float(s.surface_temp)
    return min_temp


def get_max_temp(stella_list):
    """ return maximum surface temperature recorded by STELLA """

    max_temp = float(stella_list[0].surface_temp)
    for s in stella_list:
        if float(s.surface_temp) > max_temp:
            max_temp = float(s.surface_temp)
    return max_temp


def set_all_temps(map_list, stella_list):
    """ For all map_points in list, set the temperature related colors """

    max_temp = get_max_temp(stella_list)
    min_temp = get_min_temp(stella_list)
    for m in map_list:
        m.set_temp(min_temp, max_temp)
    return min_temp, max_temp

def print_mins(gps_list):
    """ print the minimum latitude and maximum longitude found in a list of GpsPoints """

    min_lat = find_min_lat(gps_list)
    min_lon = find_min_lon(gps_list)
    print(min_lat, min_lon)


def detect_batch(gps_list, stella_list):
    """ Based on the gps data, return correct stella batch """

    time = gps_list[0].time
    batch = stella_list[0].batch
    prev_delta = abs((time - stella_list[0].timestamp).total_seconds())

    for s in stella_list:
        delta = abs((time - s.timestamp).total_seconds())
        if delta < prev_delta:
            delta = prev_delta
            batch = s.batch
    return batch

def init_map_list(gps_file, stella_file, canvas_size):
    """ completes all necessary tasks to generate the list of MapPoints for the given dataset """

    gps_list = gps_point.read_drone_csv(gps_file)
    stella_list = stella_point.make_stella_list(stella_file)

    batch = detect_batch(gps_list, stella_list)

    stella_list = stella_point.get_batch(stella_list, batch)

    map_list, width, height, delta_lat, min_t, max_t = set_xy(gps_list, stella_list, canvas_size)
    return map_list, width, height, delta_lat, min_t, max_t


def save_list(map_list, save_file):
    """ saves all data to a byte file """
    pickle.dump(map_list, save_file)


def read_map_list(file):
    """ reads in a file created by VIR-Atlas into a map_list """
    return pickle.load(open(file, 'rb'))
