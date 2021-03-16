# @author Sophia Novo-Gradac
# 2/26/2021
# @brief:   contains functions for translating various data into hex strings for color
#           most deal with the process of translating irradiance values to rgb
# last updated: 3/16/2021 by Sophia Novo-Gradac
# @updates  removed color class. Should not have had a class as color does not hold information
#           this file is only functional
#           tested need for altitude. Determined it was unecessary
# TODO:     debug resulting VS Colors
#           atm colors skew largely to yellow and are far too close to white
#           debug NIR colors. results in negative numbers?
#           develop RGB method for temperature readings

#!/usr/bin/env python3
import math

vis_wl = [450, 500, 550, 570, 600, 650]

'''Calculate and return the solid angle of the data from the altitude the data was taken at'''
def solid_ang(alt):
    rad = alt * math.sin(40)
    area = math.pi * (rad ** 2)
    return area / (alt ** 2)

'''take altitude and data in uW/cm^2 and convert to W/m^2 steridian'''
def data_to_spec(alt, data):
    for x in range(0,6):
        data[x] = data[x] / solid_ang(alt)
    return data

'''calculate and return gaussian function
S represents a heaviside function following S(x,y,z) = y(1-H(x)) + zH(x)'''
def gaussian(alpha, lam, beta, gamma, delta):
    S = gamma if lam-beta < 0 else delta
    return alpha * math.exp(-0.5 * (((lam-beta)*S) ** 2))

'''spectrum power data to xyz color system
input: spectrum data in uW/m^2 steridian and its wavelength
conversion based on 1931 CIE standards
gaussian conversion from http://jcgt.org/published/0002/02/01/paper.pdf'''
def spec_to_xyz(data):
    XYZ = [0,0,0]
    for x in range(0,6):
        XYZ[0] += data[x] * (gaussian(0.362, vis_wl[x], 442, 0.0624, 0.0375) + gaussian(1.056, vis_wl[x], 599.8, 0.0264, 0.0323) + gaussian(-0.065, vis_wl[x], 501.1, 0.0490, 0.0382))

        XYZ[1] += data[x] * (gaussian(0.821, vis_wl[x], 568.8, 0.0213, 0.0247) + gaussian(0.286, vis_wl[x], 530.9, 0.0613, 0.0322))

        XYZ[2] +=  data[x] * (gaussian(1.217, vis_wl[x], 437, 0.0845, 0.0278) + gaussian(0.681, vis_wl[x], 459, 0.0385, 0.0725))
        # print(XYZ)
    return XYZ

'''convert CIE 1931 XYZ values to RGB linearly.'''
def xyz_to_rgb(XYZ):
    RGB = [0,0,0]
    RGB[0] =  3.2404542*XYZ[0] - 1.5371385*XYZ[1] - 0.4985314*XYZ[2]
    RGB[1] = -0.9692660*XYZ[0] + 1.8760108*XYZ[1] + 0.0415560*XYZ[2]
    RGB[2] = 0.0556434*XYZ[0] - 0.2040259*XYZ[1] + 1.0572252*XYZ[2]
    return RGB

'''correct RGB values for larger range'''
def gamma_correction(RGB):
    for x in range(0,3):
        if RGB[x] <= 0.0031308:
            RGB[x] *= 12.92
        elif RGB[x] > 0.0031308:
            RGB[x] = 1.055 * (RGB[x] ** (1/2.4)) - 0.055
    # print(RGB)
    return RGB

'''scale brightness so readings in high or low exposure result in high contrast colors'''
def scale_brightness(RGB):
    scaled = [0,0,0]
    max = 0
    for x in RGB:
        if (x > max):
            max = x
    for i in range(0,3):
        scaled[i] = 255 * RGB[i] / max
    return scaled

def rgb_to_hex(RGB):
    RGB = scale_brightness(RGB)
    # print("#{:02x}{:02x}{:02x}".format(int(RGB[0]), int(RGB[1]), int(RGB[2])))
    return "#{:02x}{:02x}{:02x}".format(int(RGB[0]), int(RGB[1]), int(RGB[2]))

'''complete translation from data to RGB color
    currently does not consider altitude'''
# def data_to_hex(alt, data):
    # return rgb_to_hex(gamma_correction(xyz_to_rgb(spec_to_xyz(data_to_spec(alt, data)))))

def data_to_hex(data):
    return rgb_to_hex(gamma_correction(xyz_to_rgb(spec_to_xyz(data))))
