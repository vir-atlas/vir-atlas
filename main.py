# @authors Brynn
# @date 4/22/21
# @brief The most recent main GUI file.
# @TODO Add the legend, annotations, and satellite frames to the main window

import tkinter as tk
import menu_bar as menu
import map_gen
import legend
import satellite_image
from satellite_frame import SatelliteFrame
import annotation


# Class creating the base window
class Root(tk.Tk):
    # Main window constructor
    def __init__(self):
        tk.Tk.__init__(self)

        self.geometry('1450x900')
        self.winfo_toplevel().title("VIR-Atlas")

        # Initialize data files
        self.stella_file = ''
        self.gps_file = ''
        self.map_file = ''
        self.satellite_image = ''
        self.satellite_coords = None
        # List of accepted types for user uploaded satellite images. Feel free to add.
        self.image_formats = [("image", ".jpeg"), ("image", ".png"), ("image", ".jpg")]

        self.map_data = map_gen.Map()
        self.resolution = 10    #default value. Might want to let user change this. The smaller, the more polygons in a map
        """
        self.map_data.update_map(1000,
                                 "Data Files/Apr-17th-2021-04-55PM-Flight-Airdata.csv",
                                 "Data Files/data.txt")

        # self.satellite_coords = map_gen.get_pairs(self.map_data.map_list)
        """

        # Add default instructional canvas upon startup
        self.startup_message = tk.Canvas(width=840, height=840, bg="grey")
        self.startup_message.create_text(420, 420, font="Times 15", justify="center",
                                         text="Welcome to VIR - Atlas!\nTo get started,"
                                              " go to\nFiles -> Open New File")
        self.startup_message.place(y=20, x=20)

        # Initialize frames
        self.stella_frame = None
        self.legend_frame = None
        self.annotation_frame = None
        self.satellite_frame = None

        # Add the menu_bar to the main window
        menu_bar = menu.MenuBar(self)
        self.config(menu=menu_bar)

    def set_stella_data(self, file):
        self.stella_file = file

    def set_gps_data(self, file):
        self.gps_file = file

    def set_map_data(self, file):
        self.map_file = file

    def set_sat_file(self, file):
        self.satellite_image = file

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        self.map_data.gen_map(new_frame.mode, self.resolution, new_frame.canvas)

        if self.stella_frame is not None:
            self.stella_frame.destroy()
        self.stella_frame = new_frame
        self.stella_frame.place(x=20, y=20)

        # Switch legend to match current map
        new_legend = legend.Legend(self, self.stella_frame.mode)
        if self.legend_frame is not None:
            self.legend_frame.destroy()
        self.legend_frame = new_legend
        self.legend_frame.place(x=880, y=20)

    def get_annotation(self):
        if self.annotation_frame is not None:
            self.annotation_frame.destroy()

        annotation.set_map_list(self.map_data.map_list, self.map_data.scale)
        self.annotation_frame = annotation.AnnotationFrame(self)
        self.annotation_frame.config(height=420, width=420, bg='#007BA7')
        self.annotation_frame.place(x=1010, y=460)

    # Displays the generated satellite image
    def get_satellite(self):
        self.satellite_coords = map_gen.get_pairs(self.map_data.map_list)
        self.satellite_image = satellite_image.get_satellite_image(self.satellite_coords)
        print(self.satellite_image)

        # new_frame = SatelliteFrame(self, self.satellite_image)
        if self.satellite_frame is not None:
            self.satellite_frame.destroy()
        # self.satellite_frame = new_frame

        self.satellite_frame = tk.Frame(self)
        self.satellite_frame.config(height=420, width=420, bg='blue')
        print(self.satellite_image)
        SatelliteFrame(self.satellite_frame, self.satellite_image)
        self.satellite_frame.place(x=1010, y=20)


        """            
        satellite_image = filedialog.askopenfilename(initialdir='/home/boxghost/Dropbox/SE/vir-atlas',
                                                         title="Select an image", filetypes=self.image_formats)"""

    def get_satellite_upload(self):
       # new_frame = SatelliteFrame(self, self.satellite_image)
        if self.satellite_frame is not None:
            self.satellite_frame.destroy()
        # self.satellite_frame = new_frame

        self.satellite_frame = tk.Frame(self)
        self.satellite_frame.config(height=420, width=420, bg='blue')
        print(self.satellite_image)
        SatelliteFrame(self.satellite_frame, self.satellite_image)
        self.satellite_frame.place(x=1010, y=20)

if __name__ == "__main__":
    root = Root()
    annotation.get_root(root)
    root.mainloop()
