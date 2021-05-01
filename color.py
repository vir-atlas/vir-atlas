# !/usr/bin/env python3
# -*-coding:utf-8 -*-
""" Provides functions for translating various data to a hex color string

All functions are global.
Some utility functions such as averaging, and string/array conversion are included
functions pertaining to data_to_hex take spectral power data in uW/cm^2, their associated wavelength for conversion
Temperature and VI data used false color to generate the associated string
Sources for constants used in the code are in function comments.
"""

import math
import numpy as np

__authors__ = ["Sophia Novo-Gradac"]
__maintainer__ = "Sophia Novo-Gradac"
__email__ = "sophia.novo-gradac@student.nmt.edu"


def gaussian(alpha, lam, beta, gamma, delta):
    """ Calculate gaussian function and return result

     = α * exp(−1/2 * [(λ−β) * S(λ−β,γ,δ)] ^ 2)
     S is a pair heaviside functions
     S(x,y,z) = y(1 - H(x)) + z * (H(x))
    """

    S = gamma if lam - beta < 0 else delta
    return alpha * math.exp(-0.5 * (((lam - beta) * S) ** 2))


def x_fit_31(wave):
    """ Calculate x gaussian fit and return

    fits are piecewise gaussian functions from CIE 1931 standards.
    alpha, beta, gamma and delta are constants from http://jcgt.org/published/0002/02/01/paper.pdf page 4
    """

    return (gaussian(0.362, wave, 442, 0.0624, 0.0375) + gaussian(1.056, wave, 599.8, 0.0264, 0.0323) +
            gaussian(-0.065, wave, 501.1, 0.0490, 0.0382))


def y_fit_31(wave):
    """ See x_fit_31 """

    return (gaussian(0.821, wave, 568.8, 0.0213, 0.0247) + gaussian(0.286, wave, 530.9, 0.0613, 0.0322))


def z_fit_31(wave):
    """ See x_fit_31 """

    return (gaussian(1.217, wave, 437, 0.0845, 0.0278) + gaussian(0.681, wave, 459, 0.0385, 0.0725))


def spec_to_xyz(data, wl):
    """ Given spectral power data, return XYZ tristimulus values in tuple

    X = ∑ x * P * Δλ where x is the fit, P is the power, and Δλ is the current wavelength
    Y and Z also follow this equation
    returned linearized X,Y,Z (each is in range 0-1)
    """

    X, Y, Z = 0, 0, 0
    wl_mult = [1.25, 1.1, 0.98, 0.98, 1, 1]  # values from calibrating to D50 White

    for i in range(0, 6):
        X += data[i] * x_fit_31(wl[i]) * wl[i] * wl_mult[i]
        Y += data[i] * y_fit_31(wl[i]) * wl[i] * wl_mult[i]
        Z += data[i] * z_fit_31(wl[i]) * wl[i] * wl_mult[i]

    sum = X + Y + Z

    if sum == 0:
        return 0, 0, 0

    return X / sum, Y / sum, Z / sum


def xyz_to_rgb(XYZ):
    """ convert CIE 1931 XYZ values to linear RGB (each in range 0->1), return as array

    Conversion done by multiplying matrices.
    M is matrix of constants for sRGB using D50 whitepoint
    from http://www.brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html
    """

    M = np.array([[3.1338561, -1.6168667, -0.4906146],
                  [-0.9787684, 1.9161415, 0.0334540],
                  [0.0719453, -0.2289914, 1.4052427]])

    RGB = np.matmul(M, XYZ)
    return RGB


def gamma_correction(RGB):
    """ correct RGB values for larger range and set to 0->255 range, return as array

    gamma correction "stretches" color values to be more useful to the human eye
    gamma correction found on https://www.oceanopticsbook.info/view/photometry-and-visibility/from-xyz-to-rgb
    scale_brightness handles out of range exceptions and sets values to 0->255
    """

    for x in range(0, 3):
        if RGB[x] <= 0.0031308:
            RGB[x] *= 12.92
        else:
            RGB[x] = 1.055 * (RGB[x] ** (1 / 2.4)) - 0.055

    RGB = scale_brightness(RGB)
    return RGB


def OoR(RGB):
    """ recorrect any RGB values outside of the range by moving min value to 0 and scaling to max value """

    col_min = min(RGB)
    if col_min < 0:
        for i in range(3):
            RGB[i] -= col_min

    if max(RGB) > 1:
        scale = 255 / max(RGB)
        if scale < 1:
            for i in range(3):
                RGB[i] *= scale

    return RGB


def scale_brightness(RGB):
    """ scale from linear sRGB to 32 bit color (0->255). Handles out of range values. """

    for x in range(3):
        RGB[x] *= 255

    OoR(RGB)
    return RGB


def rgb_to_hex(RGB):
    """ convert RGB given in list format to hex string and return"""

    return "#{:02x}{:02x}{:02x}".format(int(RGB[0]), int(RGB[1]), int(RGB[2]))


def hex_to_rgb(hex):
    """ convert hex string to RGB array and return """

    hex = hex.lstrip('#')
    return list(int(hex[i:i + 2], 16) for i in (0, 2, 4))


def average_color(colors):
    """ given a list of hex color strings, return the average color in a hex string """

    avg = [0, 0, 0]

    for c in colors:
        RGB = hex_to_rgb(c)
        avg[0] += RGB[0]
        avg[1] += RGB[1]
        avg[2] += RGB[2]

    avg[0] = avg[0] / len(colors)
    avg[1] = avg[1] / len(colors)
    avg[2] = avg[2] / len(colors)

    return rgb_to_hex(avg)


def data_to_hex(data, wl):
    """ given spectral power data and the corresponding wavelengths, return """

    return rgb_to_hex(gamma_correction(xyz_to_rgb(spec_to_xyz(data, wl))))


def false_color(value, min, max):
    """ take 3 floats, where value is between min and max, and return a hex false color for that value

    color gradient from dark blue, cyan, yellow, orange, and red over even distribution
    done based on value percentage in range min -> max
    """

    d_blue = np.array([0, 0, 128])  # 0
    cyan = np.array([0, 255, 255])  # 0.25
    yellow = np.array([255, 255, 0])  # 0.5
    orange = np.array([255, 128, 0])  # 0.75
    red = np.array([255, 0, 0])  # 1

    color = []
    # convert temp to a percentage scale of 0 to 100
    p = (value - min) / (max - min)

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


def false_color_vi(value):
    """ takes float value between -1 and 1, and returns a color for Vegetation Index false color

    dark blue -> usually represents water
    white -> very little or no vegetation present
    tan -> very little vegetation present or dirt
    green -> some vegetation
    dark green -> lush vegetation
    scale from landsat maps on https://www.usgs.gov/core-science-systems/nli/landsat/landsat-surface-reflectance-derived-spectral-indices?qt-science_support_page_related_con=0#qt-science_support_page_related_con
    """
    # print(value)
    d_blue = np.array([0, 0, 96])  # -1  -> 0
    white = np.array([255, 255, 255])  # 0   -> 0.5
    tan = np.array([210, 180, 140])  # 0.1 -> 0.55
    green = np.array([0, 255, 0])  # 0.5 -> 0.75
    d_green = np.array([0, 96, 0])  # 1   -> 1

    color = []
    # convert temp to a percentage scale of 0 to 100
    p = (value + 1) / (2)

    if p < 0.5:
        color = (1 - p / 0.5) * d_blue + (p / 0.5) * white
    elif p < 0.55:
        p = p - 0.5
        color = (1 - p / 0.05) * white + (p / 0.05) * tan
    elif p < 0.70:
        p = p - 0.55
        color = (1 - p / 0.2) * tan + (p / 0.2) * green
    else:
        p = p - 0.70
        color = (1 - p / 0.25) * green + (p / 0.25) * d_green

    return rgb_to_hex(color)


def false_two_color(value, min, max, color1, color2):
    """ Take a 3 floats where value is between min and max and 2 hex colors, return value's corresponding hex color

    color 1 pairs with min, color 2 pairs with max. White used for in between.
    """
    c1 = np.array(hex_to_rgb(color1))
    c2 = np.array(hex_to_rgb(color2))
    white = np.array([255, 255, 255])

    p = (value - min) / (max - min)

    if p < 0.5:
        color = (1 - p / 0.5) * c1 + (p / 0.5) * white
    else:
        p = p - 0.5
        color = (1 - p / 0.5) * white + (p / 0.5) * c2
    return rgb_to_hex(color)


def fade(value, color):
    """ given a value from 0->1 and a hex color string, return a faded hex color

    a value of 0 gives gray, 1 gives the color parameter
    """

    c = np.array(hex_to_rgb(color))
    grey = np.array([125, 125, 125])

    color = grey + value * (c - grey)
    OoR(color)
    return rgb_to_hex(color)
