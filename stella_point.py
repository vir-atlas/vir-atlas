# @author Marisa Loraas, Sophia Novo-Gradac, Timothy Goetch
# 2/20/2021
# @brief:   StellaPoint object: creates an object for every point the STELLA records, so that you can access any attribute
#           that stella outputs for any point of record. Each attribute in the __init__ parameters are the attributes given out
#           by stella that can be seen in the stella_data_column_header.xlsx (besides the columns with "mark" in them because I
#           deemed them not important for these attributes, but they are commented out
# last updated: 4/15/2021 by Sophia Novo-Gradac
# @updates  nir values now adjusted to vis. (Paul's suggestion)
#           air temps taken in as floats
# TODO:     none

from datetime import datetime
# import csv
import numpy as np


class StellaPoint:
    def __init__(
            self,
            batch,
            day,
            timestamp,
            decimal_hour,
            milliseconds,
            surface_temp,
            surface_temp_error_bar,
            air_temp_units,
            air_temp,
            air_temp_error_bar,
            relative_humidity,
            relative_humidity_error_bar,
            air_pressure_hpa,
            air_pressure_error_bar,
            altitude_m_uncal,
            altitude_error_bar,
            visible_spectrum_error_bar,
            vis_pows,
            nir_spectrum_error_bar,
            nir_pows):
        self.batch = batch
        self.day = day
        self.timestamp = timestamp
    #   self.dhm = decimal_hours_mark
        self.dh = decimal_hour
        self.ms = milliseconds
    #   self.stm = surface_temp_mark
    #   self.surface_temp_units = surface_temp_units
        self.surface_temp = float(surface_temp)
        self.st_error_bar = float(surface_temp_error_bar)
    #   self.atm = air_temp_mark
    #   self.air_temp_units = air_temp_units
        self.air_temp = float(air_temp)
        self.at_error_bar = float(air_temp_error_bar)
    #   self.rhm = relative_humidity_mark
    #   self.rel_humid_units = relative_humidity_units
        self.rel_humid = relative_humidity
        self.rh_error_bar = relative_humidity_error_bar
    #   self.apm = air_pressure_mark
    #   self.air_pressure_units = air_pressure_units
        self.air_pressure_hpa = air_pressure_hpa
        self.ap_error_bar = air_pressure_error_bar
    #   self.altitude_mark = altitude_mark
    #   self.altitude_units = altitude_units
        self.altitude_m_uncal = altitude_m_uncal
        self.altitude_error_bar = altitude_error_bar
    #   self.vis_mark = visible_spectrum_mark
    #   self.vis_waveband_units = vis_waveband_units
    #   self.vis_power_units = vis_power_units
        self.vis_error_bar = visible_spectrum_error_bar
        # changed to an array of the powers. wavebands is constant and we dont
        # need to pull it.
        self.vis_pows = vis_pows
        self.nir_spectrum_error_bar = nir_spectrum_error_bar
        # changed to an array of the powers. wavebands is constant and we dont
        # need to pull it.
        self.nir_pows = nir_pows
        
        self.adjust_nir()

    """print data to terminal. for debugging"""

    def print_stella(self):
        print(
            self.batch,
            self.day,
            self.timestamp,
            self.dh,
            self.ms,
            self.surface_temp,
            self.st_error_bar,
            self.air_temp,
            self.at_error_bar,
            self.rel_humid,
            self.rh_error_bar,
            self.air_pressure_hpa,
            self.ap_error_bar,
            self.altitude_m_uncal,
            self.altitude_error_bar,
            self.vis_error_bar,
            self.vis_pows,
            self.nir_spectrum_error_bar,
            self.nir_pows)
    
    def adjust_nir(self):
        val_610 = self.vis_pows[4] + (self.vis_pows[5] - self.vis_pows[4])/5
        delta = abs(self.nir_pows[0] - val_610)

        if val_610 > self.nir_pows[0]:
            for i in range(6):
                self.nir_pows[i] += delta
        else:
            for i in range(6):
                self.vis_pows[i] += delta

"""find a way to pull out the batches so user can select which one"""


def make_stella_list(file):

    # Check that file can be read from
    try:
        # check that file can be opened
        stella_output = open(file, 'r')
    except FileNotFoundError as no_file:
        print("Error in reading stella input file", no_file)
        exit()

    stella_output.readline()  # rid header line

    # Read all contents from file into a List object, close file
    input_file = stella_output.readlines()
    stella_output.close()

    # Subdivide lines into check if the length of each list in points is
    # correct
    points = list()
    for line in input_file:
        points.append(str(line).rstrip().split(','))

    for point in list(points):

        if len(point) != 57:
            print("Error in Format of file, please check again")
            return

        for part in point:
            try:
                if isinstance(part, str):
                    if part.find('_') >= 0 or part.find('hh.hhhh') >= 0:
                        point.remove(part)
                        continue

                if isinstance(part, int):
                    point[point.index(part)] = int(part)

                if isinstance(part, float):
                    point[point.index(part)] = float(part)
            except ValueError:
                continue

    # stella_list: list of all StellaPoint objects in the order given by the
    # file
    stella_list = list()
    batches = []
    cur_batch = ""
    for point in list(points):

        arr = np.array([float(point[23]), float(point[25]), float(point[27]),
                    float(point[29]), float(point[31]), float(point[33]), 
                    float(point[38]), float(point[40]), float(point[42]),
                    float(point[44]), float(point[46]), float(point[48])])
        
        if cur_batch != point[0]: 
            if np.all((arr == 0)):
                continue
            cur_batch = point[0]
            start = float(point[3])
            batches.append(cur_batch)

        ms = (float(point[3]) - start) * 60 * 60 * 1000
        vis_pows = [float(point[23]), float(point[25]), float(point[27]),
                    float(point[29]), float(point[31]), float(point[33])]
        nir_pows = [float(point[38]), float(point[40]), float(point[42]),
                    float(point[44]), float(point[46]), float(point[48])]
        stella = StellaPoint(
            point[0],
            point[1],
            point[2],
            point[3],
            ms,
            point[5],
            point[6],
            point[7],
            point[8],
            point[9],
            point[11],
            point[12],
            point[14],
            point[15],
            point[17],
            point[18],
            point[21],
            vis_pows,
            point[36],
            nir_pows)

        stella.timestamp = datetime.strptime(
            stella.timestamp, "%Y%m%dT%H%M%SZ")  # Sample 20210225T203501Z
        stella_list.append(stella)

        # stella.print_stella() #for error checking

    # print(batches)
    return stella_list


"""returns a new list of stella_list based on their batch"""

def get_batch(stella_list, batch):
    points = []
    for stella in stella_list:
        if stella.batch == batch:
            points.append(stella)
    return points
