# @author Sophia Novo-Gradac
# 3/12/2021
# @brief:   gps_point object: object that holds the decimal gps location of the drone and the timestamp at which it was taken.
#           __init__ parameters are the 1st, 2nd, and 3rd column (time, latitude, longitude) in the csv.
# functions outside the class process the csv vile into gps_points

class gps_point:
    """gps_point holds necessary time and GPS data from the drone to compute the gps for the map"""
    def __init__(self, time, latitude, longitude):
        super(gps_point, self).__init__()
        self.time = time
        self.latitude = float(latitude)
        self.longitude = float(longitude)

    """print data to terminal. for debugging"""
    def print_gps(self):
        print(self.time, self.latitude, self.longitude)

"""given a csv with the fromat:
    [milliseconds, time(utc), latitude, longitude, etc]
    read data into a list of gps_points"""
def read_drone_csv(drone_data):
    stream = open(drone_data, "r")
    line = stream.readline() #skip first line of csv

    gps_points = []

    count = -1
    while True:
        count += 1
        line = stream.readline()

        if not line:
            break

        words = line.split(',')
        gps_points.append(gps_point(words[1], words[2], words[3]))
        gps_points[count].print_gps()

    stream.close()
    return gps_points

# test read on Sophia's system
# read_drone_csv("/home/nova/cse326/Data Files_Feb-26th-2021-05-57PM-Flight-Airdata.csv")
