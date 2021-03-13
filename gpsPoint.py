# @author Sophia Novo-Gradac
# 3/12/2021
# @brief:   gps_point object: object that holds the decimal gps location of the drone and the timestamp at which it was taken.
#           __init__ parameters are the 1st, 2nd, and 3rd column (time, latitude, longitude) in the csv.
# functions outside the class process the csv vile into gps_points
from datetime import datetime
from statistics import median


class GpsPoint:
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

        time = datetime.strptime(words[1], "%Y-%m-%d %H:%M:%S")

        gps_points.append(GpsPoint(time, words[2], words[3]))
        gps_points[count].print_gps()

    stream.close()
    return gps_points


# Waiting discussion with Sophia to determine if this function is needed.
# Currently non-operational
def average_points(gps_points):
    length = 0
    point_list = list()
    latitude = []
    longitude = []

    while length <= len(gps_points):
        rep_point = gps_points[length]
        #iterate through list and collect similar points into a temporary list
        for point in gps_points:
            if point.time == rep_point.time:
                latitude.append(point.latitude)
                longitude.append(point.longitude)
                length += 1
            else:
                break

        time = rep_point.time
        med_lat = median(latitude)
        med_lon = median(longitude)
        point_list.append(GpsPoint(time, med_lat, med_lon))


        #avg lat & long values for same timestamp

    return point_list


# test read on Sophia's system
# read_drone_csv("/home/nova/cse326/Data Files_Feb-26th-2021-05-57PM-Flight-Airdata.csv")

# test read on Ty's system
# points = read_drone_csv("Data Files/Feb-26th-2021-05-57PM-Flight-Airdata.csv")
# points = average_points(points)
# for p in points:
#     print(p.time, ", ", p.latitude, ", ", p.longitude)
