# @authors Brynn
# @date 4/13/21
# @brief Everything within the STELLA map frame
# @TODO everything lol

import tkinter as tk
import stella_point
import map_gen
import map_point
import gps_point


class StellaFrame(tk.Frame):
    # constructor for StellaFrame
    def __init__(self, master):
        # call constructor for tk.Frame
        tk.Frame.__init__(self, master)

        # initialize the grid system
        self.grid()

        # set the default display mode
        self.mode = 'tmp'

        # set up the rows and columns for the grid system
        for row in range(2):
            self.master.rowconfigure(row, weight=1)

        for col in range(2):
            self.master.columnconfigure(col, weight=1)

        self.update()

        # place the frames in the grid system
        # self.menuFrame.place(x=0, y=0)
        self.irFrame.grid(
            row=0,
            column=0,
            rowspan=1,
            columnspan=1,
            sticky=tk.W + tk.E + tk.N + tk.S)
        self.satFrame.grid(
            row=0, column=1,
            rowspan=1,
            columnspan=1,
            sticky=tk.W + tk.E + tk.N + tk.S)
        self.notesFrame.grid(
            row=1,
            column=0,
            rowspan=1,
            columnspan=2,
            sticky=tk.W + tk.E + tk.N + tk.S)

        # fixes the frame in place so the canvas doesn't forcefully expand it
        self.irFrame.grid_propagate(0)
        # self.menuFrame.grid_propagate(0)

        self.setCanvas(self.irFrame, self.stellaCanvas)

    def stellaCanvas(self, canvas):
        # pull data from files
        self.gps_points = gps_point.read_drone_csv(r'Data Files/Feb-26th-2021-05-57PM-Flight-Airdata.csv')
        self.stella_points = stella_point.make_stella_list(r'Data Files/data.txt')

        # parse data, get width and height
        self.stella_points = stella_point.get_batch(self.stella_points, "1.X")
        self.map_points, self.mapWidth, self.map_height = \
            map_point.set_xy(self.gps_points, self.stella_points, 1200)

        # preprocess width and height
        self.map_width = round(self.mapWidth / 10) * 10
        self.map_height = round(self.map_height / 10) * 10

        # create image based on data
        self.poly_fill = map_gen.get_poly(self.map_height, self.mapWidth)
        self.filled = map_gen.draw_data(self.map_points,
                                       self.poly_fill,
                                       self.mode,
                                       10,
                                       self.mapWidth)
        map_gen.fill_all(self.filled,
                        self.poly_fill,
                        self.map_width,
                        self.map_height,
                        10)

        # attach map imaging to the canvas
        for t in self.poly_fill:
            t.draw(self.canvas)

        # draw the drone's flight path
        map_gen.draw_flight_path(self.map_points, self.canvas)

    def setCanvas(self, base_frame, canvas_mode):
        # tk.update() will allow retrieval of width and height
        self.update()
        self.window_width = base_frame.winfo_width()
        self.window_height = base_frame.winfo_height()

        # set up the canvas
        self.canvas = tk.Canvas(base_frame,
                                width=self.windowWidth * 0.5,
                                height=self.windowHeight * 0.5,
                                background='grey')

        # set up the scrollbars (unnecessary imo)
        self.xsb = tk.Scrollbar(base_frame,
                                orient="horizontal",
                                command=self.canvas.xview)
        self.ysb = tk.Scrollbar(base_frame,
                                orient="vertical",
                                command=self.canvas.yview)

        # bound the scrolling region (needs work?)
        self.canvas.configure(scrollregion=(0, 0,
                                            self.windowWidth * 0.5,
                                            self.windowHeight * 0.5))

        # set up the grid for the canvas
        self.xsb.grid(row=1, column=0, sticky="ew")
        self.ysb.grid(row=0, column=1, sticky="ns")

        # place the canvas on the frame
        self.canvas.grid(row=0, column=0, sticky="nsew")
        base_frame.grid_rowconfigure(0, weight=1)
        base_frame.grid_columnconfigure(0, weight=1)

        # set up the type of canvas you want
        canvas_mode(self.canvas)

        # This is what enables using the mouse:
        self.canvas.bind("<ButtonPress-1>", self.move_start)
        self.canvas.bind("<B1-Motion>", self.move_move)

        # linux scroll
        self.canvas.bind("<Button-4>", self.zoomer_p)
        self.canvas.bind("<Button-5>", self.zoomer_m)

        # windows scroll
        self.canvas.bind("<MouseWheel>", self.zoomer)

    # move
    def move_start(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def move_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    # windows zoom
    def zoomer(self, event):
        if event.delta > 0:
            self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        elif event.delta < 0:
            self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # linux zoom
    def zoomer_p(self, event):
        self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def zoomer_m(self, event):
        self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

# Window for testing purposes only.
if __name__ == '__main__':
    master = tk.Tk()
    master.geometry('1600x900')
    StellaFrame(master)
    master.mainloop()
