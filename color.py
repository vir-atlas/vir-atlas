#!/usr/bin/env python3
import math

wavelength = [450, 500, 550, 570, 600, 650]

'''TODO: scale_brightness is crude and needs to be modified. Colors are much closer to white than they should be.'''
'''TODO: I believe it is unecessary to find the steradian for our purposes as our data is already taken in a cone.'''


class Color:

    '''Calculate and return the solid angle of the data from the altitude the data was taken at'''
    def solid_ang(self, alt):
        rad = alt * math.sin(40)
        area = math.pi * (rad ** 2)
        return area / (alt ** 2)

    '''take altitude and data in uW/cm^2 and convert to W/m^2 steridian'''
    def data_to_spec(self, alt, data):
        for x in range(0,6):
            data[x] = data[x] / self.solid_ang(alt)
        return data

    '''calculate and return gaussian function
    S represents a heaviside function following S(x,y,z) = y(1-H(x)) + zH(x)'''
    def gaussian(self, alpha, lam, beta, gamma, delta):
        S = gamma if lam-beta < 0 else delta
        return alpha * math.exp(-0.5 * (((lam-beta)*S) ** 2))

    '''spectrum power data to xyz color system
    input: spectrum data in uW/m^2 steridian and its wavelength
    conversion based on 1931 CIE standards
    gaussian conversion from http://jcgt.org/published/0002/02/01/paper.pdf'''
    def spec_to_xyz(self, data):
        XYZ = [0,0,0]
        for x in range(0,6):
            XYZ[0] += data[x] * (self.gaussian(0.362, wavelength[x], 442, 0.0624, 0.0375) + self.gaussian(1.056, wavelength[x], 599.8, 0.0264, 0.0323) + self.gaussian(-0.065, wavelength[x], 501.1, 0.0490, 0.0382))

            XYZ[1] += data[x] * (self.gaussian(0.821, wavelength[x], 568.8, 0.0213, 0.0247) + self.gaussian(0.286, wavelength[x], 530.9, 0.0613, 0.0322))

            XYZ[2] +=  data[x] * (self.gaussian(1.217, wavelength[x], 437, 0.0845, 0.0278) + self.gaussian(0.681, wavelength[x], 459, 0.0385, 0.0725))
            print(XYZ)
        return XYZ

    '''convert CIE 1931 XYZ values to RGB linearly.'''
    def xyz_to_rgb(self, XYZ):
        RGB = [0,0,0]
        RGB[0] =  3.2404542*XYZ[0] - 1.5371385*XYZ[1] - 0.4985314*XYZ[2]
        RGB[1] = -0.9692660*XYZ[0] + 1.8760108*XYZ[1] + 0.0415560*XYZ[2]
        RGB[2] = 0.0556434*XYZ[0] - 0.2040259*XYZ[1] + 1.0572252*XYZ[2]
        return RGB

    '''correct RGB values for larger range'''
    def gamma_correction(self, RGB):
        for x in range(0,3):
            if RGB[x] <= 0.0031308:
                RGB[x] *= 12.92
            elif RGB[x] > 0.0031308:
                RGB[x] = 1.055 * (RGB[x] ** (1/2.4)) - 0.055
        print(RGB)
        return RGB

    '''scale brightness so readings in high or low exposure result in high contrast colors'''
    def scale_brightness(self, RGB):
        scaled = [0,0,0]
        max = 0
        for x in RGB:
            if (x > max):
                max = x
        for i in range(0,3):
            scaled[i] = 255 * RGB[i] / max
        return scaled

    def rgb_to_hex(self, RGB):
        RGB = self.scale_brightness(RGB)
        print("#{:02x}{:02x}{:02x}".format(int(RGB[0]), int(RGB[1]), int(RGB[2])))
        return "#{:02x}{:02x}{:02x}".format(int(RGB[0]), int(RGB[1]), int(RGB[2]))

    '''complete translation from data to RGB color'''
    def data_to_hex(self, alt, data):
        return self.rgb_to_hex(self.gamma_correction(self.xyz_to_rgb(self.spec_to_xyz(self.data_to_spec(alt, data)))))
