# @author Marisa Loraas
# 2/20/2021
# @brief: StellaPoint object: creates an object for every point the STELLA records, so that you can access any attribute
# that stella outputs for any point of record. Each attribute in the __init__ parameters are the attributes given out
# by stella that can be seen in the stella_data_column_header.xlsx (besides the columns with "mark" in them because I
# deemed them not important for these attributes, but they are commented out
from datetime import datetime


class StellaPoint:
    def __init__(self, batch, day, timestamp, decimal_hour,  surface_temp_units, surface_temp, surface_temp_error_bar,
                 air_temp_units, air_temp, air_temp_error_bar, relative_humidity_units, relative_humidity,
                 relative_humidity_error_bar, air_pressure_units, air_pressure_hpa, air_pressure_error_bar,
                 altitude_units, altitude_m_uncal, altitude_error_bar,  vs_waveband_units, vs_power_units,
                 visible_spectrum_error_bar, vs_waveband_450, vs_power_450, vs_waveband_500, vs_power_500,
                 vs_waveband_550, vs_power_550, vs_waveband_570, vs_power_570, vs_waveband_600, vs_power_600,
                 vs_waveband_650, vs_power_650, nir_waveband_units, nir_power_units, nir_spectrum_error_bar,
                 nir_waveband_610, nir_power_610, nir_waveband_680, nir_power_680, nir_waveband_730, nir_power_730,
                 nir_waveband_760, nir_power_760, nir_waveband_810,
                 nir_power_810, nir_waveband_860, nir_power_860):
        self.batch = batch
        self.day = day
        self.timestamp = timestamp
    #   self.dhm = decimal_hours_mark
        self.dh = decimal_hour
    #   self.stm = surface_temp_mark
        self.surface_temp_units = surface_temp_units
        self.surface_temp = surface_temp
        self.st_error_bar = surface_temp_error_bar
    #   self.atm = air_temp_mark
        self.air_temp_units = air_temp_units
        self.air_temp = air_temp
        self.at_error_bar = air_temp_error_bar
    #   self.rhm = relative_humidity_mark
        self.rel_humid_units = relative_humidity_units
        self.rel_humid = relative_humidity
        self.rh_error_bar = relative_humidity_error_bar
    #   self.apm = air_pressure_mark
        self.air_pressure_units = air_pressure_units
        self.air_pressure_hpa = air_pressure_hpa
        self.ap_error_bar = air_pressure_error_bar
    #   self.altitude_mark = altitude_mark
        self.altitude_units = altitude_units
        self.altitude_m_uncal = altitude_m_uncal
        self.altitude_error_bar = altitude_error_bar
    #   self.vs_mark = visible_spectrum_mark
        self.vs_waveband_units = vs_waveband_units
        self.vs_power_units = vs_power_units
        self.vs_error_bar = visible_spectrum_error_bar
        self.vs_waveband_450 = vs_waveband_450  # <-- check
        self.vs_power_450 = vs_power_450
        self.vs_waveband_500 = vs_waveband_500  # <-- check
        self.vs_power_500 = vs_power_500
        self.vs_waveband_550 = vs_waveband_550  # <-- check
        self.vs_power_550 = vs_power_550
        self.vs_waveband_570 = vs_waveband_570
        self.vs_power_570 = vs_power_570
        self.vs_waveband_600 = vs_waveband_600  # <-- check
        self.vs_power_600 = vs_power_600
        self.vs_waveband_650 = vs_waveband_650
        self.vs_power_650 = vs_power_650
    #   self.nir_spectrum_mark = nir_spectrum_mark
        self.nir_waveband_units = nir_waveband_units
        self.nir_power_units = nir_power_units
        self.nir_spectrum_error_bar = nir_spectrum_error_bar
        self.nir_waveband_610 = nir_waveband_610  # <--Check
        self.nir_power_610 = nir_power_610
        self.nir_waveband_680 = nir_waveband_680  # <--Check
        self.nir_power_680 = nir_power_680
        self.nir_waveband_730 = nir_waveband_730  # <-- Check
        self.nir_power_730 = nir_power_730
        self.nir_waveband_760 = nir_waveband_760  # <--Check
        self.nir_power_760 = nir_power_760
        self.nir_waveband_810 = nir_waveband_810  # <--Check
        self.nir_power_810 = nir_power_810
        self.nir_waveband_860 = nir_waveband_860  # <-- check
        self.nir_power_860 = nir_power_860


def make_stella_points(file):

    # Check that file can be read from
    try:
        # check that file can be opened
        stella_output = open(file, 'r')
    except FileNotFoundError as no_file:
        print("Error in reading stella input file", no_file)

    # Read all contents from file into a List object, close file
    input_file = stella_output.readlines()
    stella_output.close()

    # Subdivide lines into check if the length of each list in points is correct
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

    #  stella_points: list of all StellaPoint objects in the order given by the file
    stella_points = list()
    for point in list(points):
        stella = StellaPoint(point[0], point[1], point[2], point[3], point[4], point[5], point[6], point[7],
                             point[8], point[9], point[10], point[11], point[12], point[13], point[14], point[15],
                             point[16], point[17], point[18], point[19], point[20], point[21], point[22], point[23],
                             point[24], point[25], point[26], point[27], point[28], point[29], point[30], point[31],
                             point[32], point[33], point[34], point[35], point[36], point[37], point[38], point[39],
                             point[40], point[41], point[42], point[43], point[44], point[45], point[46], point[47],
                             point[48])

        stella.timestamp = datetime.strptime(stella.timestamp, "%Y%m%dT%H%M%SZ") # Sample 20210225T203501Z
        stella_points.append(stella)

    return stella_points


# Test StellaPoint -- Ty
# file = "Data Files/data.csv"
# stella_point = make_stella_points(file)
# print('Size of Stella Point Object: ', len(stella_point))
