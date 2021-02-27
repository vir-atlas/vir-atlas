#!/usr/bin/env python3
import Tkinter as tk
import math
from color import Color
import colormath as cm


altitude = 0.14
irradiance = [7.2, 11.6, 5.9, 12.0, 11.3, 19.6] #red on pocky box indoor light
# irradiance = [62, 46.5, 20.2, 20.9, 19.5, 19.6] #cobalt fabric under phone light
# irradiance = [3500, 4000, 3500, 3000, 3000, 3000] #thin snow under direct sun

col = Color()
print(altitude)
print(irradiance)
RGB = col.data_to_hex(altitude,irradiance)
print("after data to hex")

window = tk.Tk()
label = tk.Label(text="Python rocks!", background=RGB)
label.pack()

window.mainloop()
