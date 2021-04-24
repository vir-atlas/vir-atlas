# @authors  Timothy Goetsch
# 4/21/2021
# @brief    Legend object:  creates legends for the following modes: VIS, NIR, TEMP, SVA, NDVI, EVI, SAVI, MSAVI
# last updated: 4/23/2021 by Timothy Goetsch
# @updates  added mode-specific create_X sub-functions for Legend to call when initializing a new legend. TEMP and *VI
#           modes produce working legends, however sva is acting weird. Color saturation is tied to air_temp, so when
#           air_temp = median(scale) the legend is completely white. The issue lies in the interaction with false_two_color()
#           I think. Maybe I'm passing the wrong kind of values or something.
# TODO:

import tkinter as tk
from tkinter import Canvas, Frame, BOTH, W
import color as col
from math import floor
from statistics import median
import map_gen

DEBUG = 1


class Legend(Frame):
    def __init__(self, master, mode="vis"):
        # call constructor for tk.Frame
        Frame.__init__(self, master)

        self.pack(fill=BOTH, expand=1)

        # set display size
        self.width = 110
        self.height = 840

        # create canvas
        self.canvas = tk.Canvas(self, width=self.width, height=self.height)

        # set display mode
        self.mode = mode

        if DEBUG:
            self.min_temp = -40.0
            self.max_temp = 85.0
        else:
            self.min_temp = master.map_data.min_temp
            self.max_temp = master.map_data.max_temp

        # set scale
        self.scale = []
        self.set_scale()

        if mode == "temp":
            self.create_temp()
        elif mode == "ndvi" or mode == "evi" or mode == "savi" or mode == "msavi":
            self.create_vi()
        elif mode == "sva":
            self.create_sva()

        # collect color and scale lists
        # color, scale, delta = get_colors(self.mode, self.scale)
        #
        # # specify how much space to leave above/below legend and canvas top/bottom
        # start = 10
        # stop = self.height - start
        # step = 1
        #
        # # create colored rectangles
        # x_start = 10  # goes with window atm, may move to a method if both vertical and horizontal legends are produced
        # x_end = 60  # same as x_start
        # y = 10  # arbitrary y start value
        # # create rectangles, depends on x starting and ending values, y start value, and box_size, generalized for
        # # any mode
        # if color:
        #     # determine size of bounding box for each color depending on number of elements in the color List
        #     box_size = floor((stop - start) / len(color))
        #     legend_size = box_size * len(color) + start
        #
        #     # create vertical bar for tick marks, generalized for any mode
        #     x = 70
        #     self.canvas.create_line(x, start, x, legend_size)
        #
        #     for num, c in enumerate(color):
        #         self.canvas.create_rectangle(x_start, y, x_end, y + box_size, outline=c, fill=c)
        #         self.canvas.create_line(70, y, 75, y)
        #         if y == 0:
        #             self.canvas.create_text(80, y, anchor=W, font=("Arial", 10), text=scale[num])
        #         else:
        #             self.canvas.create_text(80, y + (box_size / 2), anchor=W, font=("Arial", 10), text=scale[num])
        #         y += box_size
        #         # print(y)
        #
        #     self.canvas.create_line(70, y, 75, y)

        # pack canvas
        self.canvas.pack(fill=BOTH, expand=1)

    def create_temp(self):
        if not self.scale:
            return
        color = []
        for i in self.scale:
            color.append(col.false_color(i, 0, 1))

        y_start = 10   # arbitrary y start value
        y_stop = self.height - y_start
        y = y_start  # y increment value
        x = 70

        rect_x1 = 10  # goes with window atm, may move to a method if both vertical and horizontal legends are produced
        rect_x2 = 60  # same as rect_x1
        rect_y1 = 10
        rect_y2 = 0

        if color:
            box_size = floor((y_stop - y_start) / len(color))
            legend_size = box_size * len(color) + y_start  # keeps the boxes and lines aligned at the bottom of the canvas

            self.canvas.create_line(x, y, x, legend_size)  # create vertical line for numbering

            for num, c in enumerate(color):
                rect_y2 = rect_y1 + box_size
                self.canvas.create_rectangle(rect_x1, rect_y1, rect_x2, rect_y2, outline=c, fill=c)
                self.canvas.create_line(x, y, x + 5, y)

                if y == 0:
                    self.canvas.create_text(x + 10, y, anchor=W, font=("Arial", 10), text=self.scale[num])
                else:
                    self.canvas.create_text(x + 10, y + (box_size / 2), anchor=W, font=("Arial", 10), text=self.scale[num])
                y += box_size
                rect_y1 += box_size
                # print(y)

            self.canvas.create_line(x, y, x + 5, y)

    def create_vi(self):
        if not self.scale:
            return
        color = []
        for i in self.scale:
            color.append(col.false_color_vi(i))

        y_start = 10   # arbitrary y start value
        y_stop = self.height - y_start
        y = y_start  # y increment value
        x = 70

        rect_x1 = 10  # goes with window atm, may move to a method if both vertical and horizontal legends are produced
        rect_x2 = 60  # same as rect_x1
        rect_y1 = 10
        rect_y2 = 0

        if color:
            box_size = floor((y_stop - y_start) / len(color))
            legend_size = box_size * len(color) + y_start  # keeps the boxes and lines aligned at the bottom of the canvas

            self.canvas.create_line(x, y, x, legend_size)  # create vertical line for numbering

            for num, c in enumerate(color):
                rect_y2 = rect_y1 + box_size
                self.canvas.create_rectangle(rect_x1, rect_y1, rect_x2, rect_y2, outline=c, fill=c)
                self.canvas.create_line(x, y, x + 5, y)

                if y == 0:
                    self.canvas.create_text(x + 10, y, anchor=W, font=("Arial", 10), text=self.scale[num])
                else:
                    self.canvas.create_text(x + 10, y + (box_size / 2), anchor=W, font=("Arial", 10), text=self.scale[num])
                y += box_size
                rect_y1 += box_size
                # print(y)

            self.canvas.create_line(x, y, x + 5, y)

    def create_sva(self):
        if not self.scale:
            return
        color = []

        temp_list = []  # list containing hex values for corresponding surface temps
        delta_list = []
        air_temp = median(self.scale)  # arbitrary air temperature value, however it needs to be inside the (min, max) range of scale
        # air_temp = 40
        print(air_temp)

        for num, s in enumerate(self.scale):
            temp, delta = set_temp(s, self.scale[-1], self.scale[0], air_temp)
            temp_list.append(temp)
            delta_list.append(delta)

        min_temp = min(self.scale)
        max_temp = max(self.scale)
        for num, s in enumerate(self.scale):
            color.append(col.false_two_color(air_temp, min_temp, max_temp, temp_list[-num], temp_list[num]))

        y_start = 10   # arbitrary y start value
        y_stop = self.height - y_start
        y = y_start  # y increment value
        x = 70

        rect_x1 = 10
        rect_x2 = 60
        rect_y1 = 10
        rect_y2 = 0

        if color:
            box_size = floor((y_stop - y_start) / len(color))
            legend_size = box_size * len(color) + y_start  # keeps the boxes and lines aligned at the bottom of the canvas

            self.canvas.create_line(x, y, x, legend_size)  # create vertical line for numbering

            for num, c in enumerate(color):
                rect_y2 = rect_y1 + box_size
                self.canvas.create_rectangle(rect_x1, rect_y1, rect_x2, rect_y2, outline=c, fill=c)
                self.canvas.create_line(x, y, x + 5, y)

                if y == 0:
                    self.canvas.create_text(x + 10, y, anchor=W, font=("Arial", 10), text=delta_list[num])
                else:
                    self.canvas.create_text(x + 10, y + (box_size / 2), anchor=W, font=("Arial", 10), text=delta_list[num])
                y += box_size
                rect_y1 += box_size
                # print(y)

            self.canvas.create_line(x, y, x + 5, y)

    def set_scale(self):
        if self.mode == "temp":
            self.scale = [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0]  # 11 values
        elif self.mode == "ndvi" or self.mode == "evi" or self.mode == "savi" or self.mode == "msavi":
            self.scale = [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0, -0.1, -0.2, -0.3, -0.4, -0.5, -0.6, -0.7, -0.8, -0.9, -1]  # 21 values
        elif self.mode == "sva":  # @todo: this wont work for maps with little difference between min and max temp values
            max_temp = int(self.max_temp)
            min_temp = int(self.min_temp)
            for _ in range(max_temp, min_temp, -5):
                self.scale.append(float(_))


# def get_colors(mode: str, scale: list):
#     """
#     8 maps (only need 3 unique legends)
#     VIS (VISUAL LIGHT) (data_to_hex)
#     NIR (NEAR INFRARED LIGHT) (data_to_hex)
#
#     TEMP (DISTRIBUTION FROM MIN_TEMP TO MAX_TEMP RECORDED)
#     SVA (SURFACE VS AIR TEMP, WHITE IS AIR TEMP, SUBTRACTS AIR TEMP FROM SURFACE TO OBTAIN DELTA)
#     VI There are (-1, 1) NEGATIVE NUMBER SYMBOLIZES DEAD
#     """
#     color = []
#     delta = []  # needed for the sva mode numbering on the legend
#
#     if mode == "vis":
#         # visible spectrum, will likely need a different legend type than a plain bar.
#         # scale = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]  # 11 values
#         # for i in scale:
#         #     color.append(col.false_color(i, 0, 1))
#         pass
#     elif mode == "nir":
#         # near infrared spectrum, will likely need a different legend type than a plain bar. (same as vis i think)
#         # scale = [-1, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]  # 21 values
#         # for i in scale:
#         #     color.append(col.false_color_vi(i))
#         pass
#     elif mode == "temp":
#         # temperatures, range(0, 1, 0.1) -> (d_blue, cyan, yellow, orange, red)
#         for i in scale:
#             color.append(col.false_color(i, 0, 1))
#     elif mode == "sva":
#         # surface vs air temp, range(?) -> (?)
#         temp = [0] * len(scale)  # list containing hex values for corresponding surface temps
#         delta = [0] * len(scale)
#         air_temp = scale[0] + scale[-1]  # arbitrary air temperature value, however it needs to be inside the (min, max) range of scale
#
#         for num, s in enumerate(scale):
#             temp[num] = set_temp(s, scale[0], scale[-1], air_temp)
#             color.append(col.false_two_color(air_temp, scale[0], scale[-1], temp[num], temp[-num]))
#         pass
#     elif mode == "ndvi" or mode == "evi" or mode == "savi" or mode == "msavi":
#         # vegetative indexes, range(-1, 1, 0.1) -> (d_blue, white, tan, green, d_green)
#         for i in scale:
#             color.append(col.false_color_vi(i))
#
#     return color, scale, delta


def set_temp(surface_temp, min_temp, max_temp, air_temp):
    """
    @todo: this likely needs to be placed in color.py and removed from here and stella_frame.py
    """
    # max_temp = 85.0
    # min_temp = -40.0 #max and min the sensor can see
    temp_rgb = col.false_color(surface_temp, min_temp, max_temp)

    temp_delta = surface_temp - air_temp
    min_delta = min_temp - air_temp
    max_delta = max_temp - air_temp
    red = '#ff0000'
    blue = '#0000ff'

    sva_rgb = col.false_two_color(temp_delta, min_delta, max_delta, blue, red)
    return sva_rgb, temp_delta

# def create_legend(mode: str, temp_max: str, temp_min: str):


def main():
    root = tk.Tk()
    frame = tk.Frame()
    cb = Legend(frame, "sva")
    # WIDTH X HEIGHT + Location on screen when opening (WIDTH + HEIGHT)
    frame.pack(fill=BOTH, expand=1)
    # root.geometry("110x840+1000+300")

    root.mainloop()


if __name__ == '__main__':
    main()
