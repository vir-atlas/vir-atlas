# @authors Brynn, Frank
# @date 4/13/21
# @brief All things for the Satellite image frame
# @TODO Everything lol

import tkinter as tk
from datetime import date
from satsearch import Search


class SatelliteFrame(tk.Frame):
    # constructor for SatelliteFrame
    def __init__(self, master, coords):
        # call constructor for tk.Frame
        tk.Frame.__init__(self, master)

        self.coords = coords

        self.canvas_size = 300
        self.width = 300
        self.height = 300

        self.start_date = ''
        self.end_date = ''
        self.items = []
        self.keys = []
        # satsearch.Search object
        self.search = 0
        self.satellite_filename = ''
        # tk.PhotoImage object
        self.satellite_image = 0

        self.canvas = tk.Canvas(self, width=self.width, height=self.height, background='white')

        self.set_canvas()

    def get_satellite_image(self):
        # set the date parameters for searching
        self.start_date = '2021-04-07T00:00:00Z'
        self.end_date = date.today().strftime('%Y-%m-%dT00:00:00Z')

        # search for a satellite image match
        self.search = Search(
            bbox=self.coords,
            datetime=self.start_date + '/' + self.end_date,
            url='https://earth-search.aws.element84.com/v0')

        # only record the latest one
        self.items = self.search.items(limit=1)

        # try to find a better way to do this
        self.keys = [k for i in self.items for k in i.assets]

        # download the latest one
        self.satellite_filename = self.items[0].download(
            self.keys[0],
            filename_template='satellite_images/image')

    def set_canvas(self):
        self.canvas.configure(scrollregion=(0, 0, self.width, self.height))

        self.satellite_image = tk.PhotoImage(file=self.satellite_filename)

        self.canvas.create_image(image=self.satellite_image)

        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
