# @author Sophia Novo-Gradac
# 2/26/2021
# @brief:   contains functions for translating various data into hex strings for color
#           most deal with the process of translating irradiance values to rgb
# last updated: 4/15/2021 by Sophia Novo-Gradac
# @updates  added 2 new false color functions
# TODO:     infared works, but it might be desirable to define differently

#!/usr/bin/env python3
import math
import numpy as np

'''calculate and return piecewise gaussian function
S represents a heaviside function following S(x,y,z) = y(1-H(x)) + zH(x)'''
def gaussian(alpha, lam, beta, gamma, delta):
    S = gamma if lam-beta < 0 else delta
    return alpha * math.exp(-0.5 * (((lam-beta)*S) ** 2))

'''Following 3 functions handle the piecewise gaussian fit for x, y, and z
constants are from http://jcgt.org/published/0002/02/01/paper.pdf 1931 CIE standards'''
def x_fit_31(wave):
    return (gaussian(0.362, wave, 442, 0.0624, 0.0375) + gaussian(1.056, wave, 599.8, 0.0264, 0.0323) + gaussian(-0.065, wave, 501.1, 0.0490, 0.0382))

def y_fit_31(wave):
    return (gaussian(0.821, wave, 568.8, 0.0213, 0.0247) + gaussian(0.286, wave, 530.9, 0.0613, 0.0322))

def z_fit_31(wave):
    return (gaussian(1.217, wave, 437, 0.0845, 0.0278) + gaussian(0.681, wave, 459, 0.0385, 0.0725))


'''Given spectral power data, return XYZ tristimulus values
Where X = sum(P(lam)*x(lam)*lam) and Y,Z also follow this equation
Calculate X,Y,Z
returned linearized X,Y,Z (each is in range 0-1)'''
def spec_to_xyz(data, wl):
    X, Y, Z = 0, 0, 0

    for i in range(0,6):
        X += data[i] * x_fit_31(wl[i]) * wl[i]
        Y += data[i] * y_fit_31(wl[i]) * wl[i]
        Z += data[i] * z_fit_31(wl[i]) * wl[i]

    sum = X + Y + Z
    return X/sum, Y/sum, Z/sum

'''convert CIE 1931 XYZ values to linear RGB 
uses sRGB M values, which is based on D50 white
Pulled from http://www.brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html'''
def xyz_to_rgb(XYZ):
    M = np.array([  [3.24096994, -1.53738318, -0.49861076], 
                    [-0.96924364, 1.8759675, 0.04155506],
                    [0.05563008, -0.20397696, 1.05697151]])
    
    RGB = np.matmul(M, XYZ)
    return RGB

'''correct RGB values for larger range
handles outside case exceptions'''
def gamma_correction(RGB):
    for x in range(0,3):
        if RGB[x] <= 0.0031308:
            RGB[x] *= 12.92
        else:
            RGB[x] = 1.055 * (RGB[x] ** (1/2.4)) - 0.055

    RGB = scale_brightness(RGB)
    return RGB

# OoR = out of range
def OoR(RGB):
    col_min = min(RGB)
    if col_min < 0:
        for i in range(3):
            RGB[i] -= col_min
    
    scale = 255 / max(RGB)
    if scale < 1:
        for i in range(3):
            RGB[i] *= scale
        
    return RGB
    
'''scale from sRGB to 32 bit color
    RGB values should be in range 0-1'''
def scale_brightness(RGB):
    for x in range(3):
        RGB[x] *= 255

    OoR(RGB)
    return RGB

'''convert RGB given in list format to hex string'''
def rgb_to_hex(RGB):
    return "#{:02x}{:02x}{:02x}".format(int(RGB[0]), int(RGB[1]), int(RGB[2]))

'''convert hex string to RGB given in list'''
def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    return list(int(hex[i:i+2], 16) for i in (0, 2, 4))

'''given a list of hex color strings,
return the average color in a hex string'''
def average_color(colors):
    sum = [0,0,0]
    
    for c in colors:
        RGB = hex_to_rgb(c)
        sum[0] += RGB[0]
        sum[1] += RGB[1]
        sum[2] += RGB[2]

    sum[0] = sum[0] / len(colors)
    sum[1] = sum[1] / len(colors)
    sum[2] = sum[2] / len(colors)

    return rgb_to_hex(sum)

'''complete translation from data to RGB color'''
def data_to_hex(data, wl):
    return rgb_to_hex(gamma_correction(xyz_to_rgb(spec_to_xyz(data, wl))))

'''takes 3 floats and returns a false color RGB string
value should be between min and max. Min and max are the bounds used for calculating the color'''
def false_color(value, min, max):
    d_blue = np.array([0, 0, 128])    # 0
    cyan = np.array([0, 255, 255])    # 0.25
    yellow = np.array([255, 255, 0])  # 0.5
    orange = np.array([255, 128, 0])  # 0.75
    red = np.array([255, 0, 0])       # 1

    color = []
    # convert temp to a percentage scale of 0 to 100
    p = (value - min)/(max - min)

    if p < 0.25:
        color = (1 - p / 0.25) * d_blue + (p / 0.25) * cyan
    elif p < 0.5:
        p = p - 0.25
        color = (1 - p / 0.25) * cyan + (p / 0.25) * yellow
    elif p < 0.75:
        p = p - 0.5
        color = (1 - p / 0.25) * yellow + (p / 0.25) * orange
    else:
        p = p - 0.75
        color = (1 - p / 0.25) * orange + (p / 0.25) * red

    return rgb_to_hex(color)

'''false color for vegetative index
takes value from -1 to 1'''
def false_color_vi(value):
    # print(value)
    d_blue = np.array([0, 0, 128])      # -1  -> 0
    white = np.array([255, 255, 255])   # 0   -> 0.5
    tan = np.array([210, 180, 140])     # 0.1 -> 0.55
    green = np.array([0, 255, 0])       # 0.5 -> 0.75
    d_green = np.array([0, 128, 0])     # 1   -> 1

    color = []
    # convert temp to a percentage scale of 0 to 100
    p = (value + 1)/(2)

    if p < 0.5:
        color = (1 - p / 0.5) * d_blue + (p / 0.5) * white
    elif p < 0.55:
        p = p - 0.5
        color = (1 - p / 0.05) * white + (p / 0.05) * tan
    elif p < 0.75:
        p = p - 0.55
        color = (1 - p / 0.2) * tan + (p / 0.2) * green
    else:
        p = p - 0.75
        color = (1 - p / 0.25) * green + (p / 0.25) * d_green

    # print(color)
    # print(rgb_to_hex(color))
    return rgb_to_hex(color)

''' returns associated color between hex color 1 and color 2
color1 to min, color2 to max, white to 0
false color between 2 colors '''
def false_two_color(value, min, max, color1, color2):
    c1 = np.array(hex_to_rgb(color1))
    c2 = np.array(hex_to_rgb(color2))
    white = np.array([255,255,255])

    p = (value - min)/(max - min)

    if p < 0.5:
        color = (1 - p / 0.5) * c1 + (p / 0.5) * white
    else:
        p = p - 0.5
        color = (1 - p / 0.5) * white + (p / 0.5) * c2
    return rgb_to_hex(color)

