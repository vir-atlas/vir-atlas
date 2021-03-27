# @author Sophia Novo-Gradac
# 2/26/2021
# @brief:   contains functions for translating various data into hex strings for color
#           most deal with the process of translating irradiance values to rgb
# last updated: 3/16/2021 by Sophia Novo-Gradac
# @updates  debugged, colors are now more accurate and the correct scale
#           negative or greater tha 255 RGB values are handled
# TODO:     atm colors skew largely to yellow and are far too close to white

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

def x_fit_31(wave):
    return (gaussian(0.362, wave, 442, 0.0624, 0.0375) + gaussian(1.056, wave, 599.8, 0.0264, 0.0323) + gaussian(-0.065, wave, 501.1, 0.0490, 0.0382))

def y_fit_31(wave):
    return (gaussian(0.821, wave, 568.8, 0.0213, 0.0247) + gaussian(0.286, wave, 530.9, 0.0613, 0.0322))

def z_fit_31(wave):
    return (gaussian(1.217, wave, 437, 0.0845, 0.0278) + gaussian(0.681, wave, 459, 0.0385, 0.0725))

'''spectrum power data to xyz color system
input: spectrum data in uW/m^2 steridian and its wavelength
conversion based on 1931 CIE standards
gaussian conversion from http://jcgt.org/published/0002/02/01/paper.pdf'''
def spec_to_xyz(data):
    
    X = 0
    Y = 0
    Z = 0

    for i in range(0,6):
        X += data[i] * x_fit_31(vis_wl[i]) * vis_wl[i]
        Y += data[i] * y_fit_31(vis_wl[i]) * vis_wl[i]
        Z += data[i] * z_fit_31(vis_wl[i]) * vis_wl[i]
        # print(X, Y, Z)

    sum = X + Y + Z

    XYZ = [X / sum, Y / sum, Z / sum]
    
    print("spec_to_xyz: ",XYZ)
    return XYZ

'''convert CIE 1931 XYZ values to RGB linearly.'''
def xyz_to_rgb(XYZ):
    RGB = [0,0,0]
     
    RGB[0] = 3.24096994*XYZ[0] - 1.53738318*XYZ[1] - 0.49861076*XYZ[2]
    RGB[1] = -0.96924364*XYZ[0] + 1.8759675*XYZ[1] + 0.04155506*XYZ[2]
    RGB[2] = 0.05563008*XYZ[0] - 0.20397696*XYZ[1] + 1.05697151*XYZ[2]

    print("xyz_to_rgb: ",RGB)
    return RGB

'''correct RGB values for larger range'''
def gamma_correction(RGB):
    for x in range(0,3):
        if RGB[x] <= 0.0031308:
            RGB[x] *= 12.92
        else:
            RGB[x] = 1.055 * (RGB[x] ** (1/2.4)) - 0.055
        if RGB[x] < 0:
            RGB[x] = 0
        if RGB[x] > 1:
            RGB[x] = 1

    RGB = scale_brightness(RGB)
    return RGB

'''scale from sRGB to 32 bit color
    RGB values should be in range 0-100'''
def scale_brightness(RGB):
    for x in range(3):
        RGB[x] *= 255
    return RGB

def rgb_to_hex(RGB):
    return "#{:02x}{:02x}{:02x}".format(int(RGB[0]), int(RGB[1]), int(RGB[2]))

'''complete translation from data to RGB color
    currently does not consider altitude'''
# def data_to_hex(alt, data):
    # return rgb_to_hex(gamma_correction(xyz_to_rgb(spec_to_xyz(data_to_spec(alt, data)))))

def data_to_hex(data):
    return rgb_to_hex(gamma_correction(xyz_to_rgb(spec_to_xyz(data))))
