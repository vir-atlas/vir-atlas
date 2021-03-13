"""TODO:    -find a way to define canvas_size
            -give map points correct color (black for testing)
            -build exception case for international dateline"""
import gpsPoint
import StellaPoint as SP
from color import Color

canvas_size = 500
black = "000000"

class MapPoint:
    """map_point holds necessary info to put point on map.
    color = color to display
    x,y = pixel to display on"""
    def __init__(self, stella_point, color, x, y):
        super(MapPoint, self).__init__()
        self.stella_point = stella_point
        self.color = color
        self.x = x
        self.y = y

    """print data to terminal. for debugging"""
    def print_point(self):
        print(self.stella_point.timestamp, self.color, self.x, self.y)

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

        stella_points = SP.make_stella_points("Data Files/data.csv")
        color = set_color(stella_points[count])

        map_points.append(MapPoint(stella_points[count], color, x, y))
        map_points[count].print_point()

    return map_points


"""set_color pulls altitude and irradiance values (of type str) from a stella_point object, casts them to floats,
    calls Color.data_to_hex() to gather the RGB value (of type str) and return it to calling method."""
def set_color(stella_point):

    # There's likely a better way to initialize the irradiance list. Do we want this to be general so it will work with
    # either the visual OR infrared bands?
    irradiance = list()
    irradiance += [stella_point.vs_power_450, stella_point.vs_power_500, stella_point.vs_power_550,
                  stella_point.vs_power_570, stella_point.vs_power_600, stella_point.vs_power_650]

    irradiance = [float(i) for i in irradiance]
    altitude = float(stella_point.altitude_m_uncal)

    # right now this is a hack to workaround stella_point objects with NO values in the vs_power range.
    color = Color()
    max_i = max(irradiance)
    rgb = str
    if max_i > 0:
        rgb = color.data_to_hex(altitude, irradiance)

    return rgb


"""test function"""
def print_mins(gps_points):
    min_lat = find_min_lat(gps_points)
    min_lon = find_min_lon(gps_points)
    print(min_lat, min_lon)


# test for Sophia's computer
# gps_points = gpsPoint.read_drone_csv("/home/nova/cse326/Data Files_Feb-26th-2021-05-57PM-Flight-Airdata.csv")
# set_xy(gps_points)

# test for Ty's computer
# gps_points = gpsPoint.read_drone_csv("Data Files/Feb-26th-2021-05-57PM-Flight-Airdata.csv")
# set_xy(gps_points)
