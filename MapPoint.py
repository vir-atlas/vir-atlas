"""TODO:    -find a way to define canvas_size
            -give map points correct color (black for testing)
            -build exception case for international dateline"""
import gpsPoint

canvas_size = 500
black = "000000"

class map_point:
    """map_point holds necessary info to put point on map.
    color = color to display
    x,y = pixel to display on"""
    def __init__(self, color, x, y):
        super(map_point, self).__init__()
        self.color = color
        self.x = x
        self.y = y

    """print data to terminal. for debugging"""
    def print_point(self):
        print(self.color, self.x, self.y)

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
def set_xy(gps_points):
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

    count = -1
    while True:
        count += 1

        if count >= len(gps_points):
            break

        y = (abs(max_lat - gps_points[count].latitude)) * scale
        x = (gps_points[count].longitude - min_lon) * scale
        map_points.append(map_point(black, x, y))
        map_points[count].print_point()

    return map_points

"""test function"""
def print_mins(gps_points):
    min_lat = find_min_lat(gps_points)
    min_lon = find_min_lon(gps_points)
    print(min_lat, min_lon)

# test for Sophia's computer
# gps_points = gpsPoint.read_drone_csv("/home/nova/cse326/Data Files_Feb-26th-2021-05-57PM-Flight-Airdata.csv")
# set_xy(gps_points)
