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


# Class creating the base window
class Root(tk.Tk):
    # Main window constructor
    def __init__(self):
        tk.Tk.__init__(self)

        self.geometry('1450x900')
        self.winfo_toplevel().title("VIR-Atlas")

        # Initialize data files
        self.stella_file = 0
        self.gps_file = 0
        self.map_file = 0
        self.satellite_image = 0
        self.satellite_coords = None
        # List of accepted types for user uploaded satellite images. Feel free to add.
        self.image_formats = [("image", ".jpeg"), ("image", ".png"), ("image", ".jpg")]

        self.map_data = map_gen.Map()
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

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
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

    # Displays the generated satellite image
    def get_satellite(self):
        print("We got here at least")
        self.satellite_coords = map_gen.get_pairs(self.map_data.map_list)
        self.satellite_image = satellite_image.get_satellite_image(self.satellite_coords)

        # new_frame = SatelliteFrame(self, self.satellite_image)
        if self.satellite_frame is not None:
            self.satellite_frame.destroy()

        test_frame = tk.Frame(self)
        test_frame.config(height=420, width=420, bg='blue')
        SatelliteFrame(test_frame, self.satellite_image)
        test_frame.place(x=1010, y=20)


        """            
        satellite_image = filedialog.askopenfilename(initialdir='/home/boxghost/Dropbox/SE/vir-atlas',
                                                         title="Select an image", filetypes=self.image_formats)"""


if __name__ == "__main__":
    root = Root()
    root.mainloop()
