# @author Sophia Novo-Gradac
# 3/12/2021
# @brief:   gps_point object: object that holds the decimal gps location of the drone and the timestamp at which it was taken.
#           __init__ parameters are the 1st, 2nd, and 3rd column (time, latitude, longitude) in the csv.
# functions outside the class process the csv vile into gps_points
from datetime import datetime
from statistics import median
import pandas as pd


class GpsPoint(object):
    """gps_point holds necessary time and GPS data from the drone to compute the gps for the map"""
    def __init__(self, time, latitude, longitude):
        super(GpsPoint, self).__init__()
        self.time = time
        self.latitude = float(latitude)
        self.longitude = float(longitude)

    """print data to terminal. for debugging"""
    def print_gps(self):
        print(self.time, self.latitude, self.longitude)


"""given a csv with the format:
    [milliseconds, time(utc), latitude, longitude, etc]
    read data into a list of gps_points"""
def read_drone_csv(drone_data):
    stream = open(drone_data, "r")
    line = stream.readline() # skip first line of csv

    gps_points = []

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

        gps_points.append(GpsPoint(time, words[2], words[3]))

        # debug print statement
        # gps_points[count].print_gps()

    stream.close()

    gps_points = median_points(gps_points)

    return gps_points


# this function finds the median value of all points in a GpsPoint List with matching timestamps and returns
# a new GpsPoint List that has been stripped of "duplicate" timestamp samples
def median_points(gps_points):

    # convert gps_points List into the data DataFrame so we can apply the median aggregation operation and remove
    # extra sample data
    variables = ["time", "latitude", "longitude"]
    data = pd.DataFrame([[getattr(i, j) for j in variables] for i in gps_points], columns=variables)
    df = data.groupby('time', as_index=False).agg({'latitude': median, 'longitude': median})

    # convert the dataframe back into a GpsPoint List
    count = 0
    final_points = []
    while count < len(df.index):
        final_points.append(GpsPoint(df.values[count][0], df.values[count][1], df.values[count][2]))
        count += 1

    return final_points


# datetime(GpsPoint([count][0]
# test read on Sophia's system
# read_drone_csv("/home/nova/cse326/Data Files_Feb-26th-2021-05-57PM-Flight-Airdata.csv")

# test read on Ty's system
# points = read_drone_csv("Data Files/Feb-26th-2021-05-57PM-Flight-Airdata.csv")
# points = median_points(points)
# for p in points:
#     print(p.time, ", ", p.latitude, ", ", p.longitude)
