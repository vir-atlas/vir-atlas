# @author Timothy Goetsch
# @date 03/7/2021
# @brief Displays a tiled window of black, blue, red, and yellow colors using the tkinter
# module and matrix manipulation.
# @todo import StellaPoint information to start displaying colors based on Stella's data.

import tkinter as tk
import read_stella as rs
# import numpy as np


class Grid:
    def __init__(self, name, grid_height, grid_width):
        self.name = name
        self.height = grid_height
        self.width = grid_width
        self.tiles = maketiles(grid_height, grid_width)

    class Tile:
        def __init__(self, tile_x, tile_y, tile_type, tile_color):
            self.x = tile_x
            self.y = tile_y
            self.type = tile_type
            self.color = tile_color


def makegrid(name, grid_height, grid_width):
    grid = Grid(name, grid_height, grid_width)
    return grid


def maketiles(grid_height, grid_width):
    tiles = [[Grid.Tile(tile_x, tile_y, "Surface", "red") for tile_x in range(grid_width)]
             for tile_y in range(grid_height)]
    return tiles


def main():

    test1 = makegrid("test", 10, 10)
    for x in range(10):
        for y in range(10):
            if x % 2 == 0 and y % 2 == 0:
                test1.tiles[x][y].color = "black"
            elif x % 2 == 0:
                test1.tiles[x][y].color = "blue"
            elif x % 2 == 0:
                test1.tiles[x][y].color = "yellow"

    color_matrix = [[0 for _ in range(10)] for _ in range(10)]

    for x in range(10):
        for y in range(10):
            color_matrix[x][y] = test1.tiles[x][y].color

    width, height = 400, 400

    root = tk.Tk()
    root.title("color_matrix")

    frame = tk.Frame()
    frame.pack()

    canvas = tk.Canvas(frame, width=width, height=height, bd=0, highlightthickness=0)
    rows, cols = len(color_matrix), len(color_matrix[0])

    rect_width, rect_height = width // rows, height // cols
    for y, row in enumerate(color_matrix):
        for x, color in enumerate(row):
            x0, y0 = x * rect_width, y * rect_height
            x1, y1 = x0 + rect_width - 1, y0 + rect_height - 1
            canvas.create_rectangle(x0, y0, x1, y1, fill=color, width=0)

    canvas.pack()
    root.mainloop()


if __name__ == '__main__':
    main()
