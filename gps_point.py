# !/usr/bin/env python3
# -*-coding:utf-8 -*-
""" Provides functions for converting a data file from a drone into point objects

GpsPoint object: creates an object for every point that the drone records
                __init__ parameters are the 1st, 2nd, 3rd, and 4th column (time, latitude, longitude, altitude)
Tested with a Phantom 4. Data files from this drone by default are encrypted.
Use https://airdata.com/ to translate into CSV format. File must be in proper formatting and refer to a single flight.
Currently built for airdata's csv output from April 2021
"""

from datetime import datetime

__authors__ = ["Marisa Loraas", "Sophia Novo-Gradac", "Timothy Goetch"]
__maintainer__ = "Marisa Loraas"
__email__ = "marisa.loraas@student.nmt.edu"


class GpsPoint(object):
    def __init__(
            self,
            milliseconds,
            time,
            latitude,
            longitude,
            feet_since_takeoff):
        super(GpsPoint, self).__init__()
        self.milliseconds = milliseconds    # milliseconds since takeoff
        self.time = time                    # datetime at which data was taken
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.feet_since_takeoff = float(feet_since_takeoff)


    def print_gps(self):
        """ print all data to terminal."""

        print(
            self.milliseconds,
            self.time,
            self.latitude,
            self.longitude,
            self.feet_since_takeoff)

def read_drone_csv(drone_data):
    """ read drone_data file and return a list of GpsPoint objects

    file must correspond to a single flight
    file must have the format:
        [milliseconds, time(utc), latitude, longitude, feet_since_takeoff, etc.]
    return the list
    """

    # Check that file can be read from
    try:
        # check that file can be opened
        stream = open(drone_data, 'r')
    except FileNotFoundError as no_file:
        print("Error in reading drone data file", no_file)
        exit()

    line = stream.readline()  # skip first line of csv

    gps_list = []

    count = -1
    while True:
        count += 1
        line = stream.readline()

        if not line:
            break

        words = line.split(',')

        # converting timestamp from csv file into a datetime object so that
        # we can compare it against others
        time = datetime.strptime(words[1], "%Y-%m-%d %H:%M:%S")

        # skips over points that are recorded less than 1 foot off the ground
        if float(words[4]) < 1 and len(gps_list) == 0:
            continue

        # calculate milliseconds since takeoff
        if len(gps_list) == 0:
            start = int(words[0])

        gps_list.append(
            GpsPoint(int(words[0]) - start, time, words[2], words[3], words[4]))

    stream.close()

    return gps_list