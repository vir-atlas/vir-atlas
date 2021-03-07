# @author Timothy Goetsch
# @date 03/7/2021
# @brief Displays a tiled window of black, blue, red, and yellow colors using the tkinter module and matrix manipulation.
# @todo import StellaPoint information to start displaying colors based on Stella's data.

import tkinter as tk
import read_stella as rs
#import numpy as np

class Grid:
    def __init__(self, name, height, width):
        self.name = name
        self.height = height
        self.width = width
        self.tiles = makeTiles(height, width)

    class Tile:
        def __init__(self, x, y, type, color):
            self.x = x
            self.y = y
            self.type = type
            self.color = color

def makeGrid(name, height, width):
        grid = Grid(name, height, width)
        return grid

def makeTiles(height, width):
    tiles = [[Grid.Tile(x, y, "Surface", "red") for x in range(width)] for y in range(height)]
    return tiles

test1 = makeGrid("test", 10, 10)
for x in range(10):
    for y in range(10):
        if x % 2 == 0 and y % 2 == 0:
            test1.tiles[x][y].color = "black"
        elif x % 2 == 0:
            test1.tiles[x][y].color = "blue"
        elif x % 2 == 0:
            test1.tiles[x][y].color = "yellow"

colorMatrix = [[0 for x in range(10)] for y in range(10)]
for x in range(10):
    for y in range(10):
        colorMatrix[x][y] = test1.tiles[x][y].color

width, height = 400, 400

root = tk.Tk()
root.title("colorMatrix")

frame = tk.Frame()
frame.pack()

canvas = tk.Canvas(frame, width=width, height=height, bd=0, highlightthickness=0)
rows, cols = len(colorMatrix), len(colorMatrix[0])

rect_width, rect_height = width // rows, height // cols
for y, row in enumerate(colorMatrix):
    for x, color in enumerate(row):
        x0, y0 = x * rect_width, y * rect_height
        x1, y1 = x0 + rect_width-1, y0 + rect_height-1
        canvas.create_rectangle(x0, y0, x1, y1, fill=color, width=0)

canvas.pack()

root.mainloop()


