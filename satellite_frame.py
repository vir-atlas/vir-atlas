# @authors Brynn, Frank
# @date 4/13/21
# @brief All things for the Satellite image frame
# @TODO Everything lol

import tkinter as tk
from tkinter import ttk
from datetime import date
from satsearch import Search
from PIL import ImageTk, Image


class SatelliteFrame(tk.Frame):
    def __init__(self, root, file_path):
        tk.Frame.__init__(self, root)

        self.canvas = tk.Canvas(root, width=420, height=420, bg='grey')

        self.canvas.grid(row=0, column=0, sticky='nswe')
        self.canvas.update()

        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        # self.master.geometry("420x420")

        self.canvas.bind('<Configure>', self.update_image)
        self.canvas.bind('<ButtonPress-1>', self.move_from)
        self.canvas.bind('<B1-Motion>', self.move_to)
        self.canvas.bind('<MouseWheel>', self.zoom)
        self.canvas.bind('<Button-5>', self.zoom)
        self.canvas.bind('<Button-4>', self.zoom)

        self.image = Image.open(file_path)

        self.imageWidth, self.imageHeight = self.image.size

        self.scale = 1.0
        self.magnitude = 1.3

        self.container = self.canvas.create_rectangle(0, 0, self.imageWidth, self.imageHeight, width=0)
        self.update_image()

    def move_from(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def move_to(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        self.update_image()

    def zoom(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        scale = 1.0

        if event.num == 5 or event.delta == -120:
            i = min(self.imageWidth, self.imageHeight)
            if int(i * self.scale) < 30:
                return  # image is less than 30 pixels
            self.scale /= self.magnitude
            scale /= self.magnitude

        if event.num == 4 or event.delta == 120:
            i = min(self.canvas.winfo_width(), self.canvas.winfo_height())
            if i < self.scale:
                return  # 1 pixel is bigger than the visible area
            self.scale *= self.magnitude
            scale *= self.magnitude

        self.canvas.scale("all", x, y, scale, scale)
        self.update_image()

    def update_image(self, event=None):
        ''' Show image on the Canvas '''
        bbox1 = self.canvas.bbox(self.container)  # get image area
        # Remove 1 pixel shift at the sides of the bbox1
        bbox1 = (bbox1[0] + 1, bbox1[1] + 1, bbox1[2] - 1, bbox1[3] - 1)
        bbox2 = (self.canvas.canvasx(0),  # get visible area of the canvas
                 self.canvas.canvasy(0),
                 self.canvas.canvasx(self.canvas.winfo_width()),
                 self.canvas.canvasy(self.canvas.winfo_height()))
        bbox = [min(bbox1[0], bbox2[0]), min(bbox1[1], bbox2[1]),  # get scroll region box
                max(bbox1[2], bbox2[2]), max(bbox1[3], bbox2[3])]
        if bbox[0] == bbox2[0] and bbox[2] == bbox2[2]:  # whole image in the visible area
            bbox[0] = bbox1[0]
            bbox[2] = bbox1[2]
        if bbox[1] == bbox2[1] and bbox[3] == bbox2[3]:  # whole image in the visible area
            bbox[1] = bbox1[1]
            bbox[3] = bbox1[3]
        self.canvas.configure(scrollregion=bbox)  # set scroll region
        x1 = max(bbox2[0] - bbox1[0], 0)  # get coordinates (x1,y1,x2,y2) of the image tile
        y1 = max(bbox2[1] - bbox1[1], 0)
        x2 = min(bbox2[2], bbox1[2]) - bbox1[0]
        y2 = min(bbox2[3], bbox1[3]) - bbox1[1]
        if int(x2 - x1) > 0 and int(y2 - y1) > 0:  # show image if it in the visible area
            x = min(int(x2 / self.scale), self.imageWidth)  # sometimes it is larger on 1 pixel...
            y = min(int(y2 / self.scale), self.imageHeight)  # ...and sometimes not
            image = self.image.crop((int(x1 / self.scale), int(y1 / self.scale), x, y))
            imagetk = ImageTk.PhotoImage(image.resize((int(x2 - x1), int(y2 - y1))))
            imageid = self.canvas.create_image(max(bbox2[0], bbox1[0]), max(bbox2[1], bbox1[1]),
                                               anchor='nw', image=imagetk)
            self.canvas.lower(imageid)  # set image into background
            self.canvas.imagetk = imagetk  # keep an extra reference to prevent garbage-collection


if __name__ == '__main__':
    master = tk.Tk()
    master.geometry("1600x900")
    test_frame = tk.Frame(master)
    test_frame.config(height=420, width=420, bg='blue')
    SatelliteFrame(test_frame, "satellite_images/image_thumbnail.jpg")
    test_frame.place(x=400, y=400)
    master.mainloop()
