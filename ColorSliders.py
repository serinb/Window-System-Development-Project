#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ColorSliders - Submission
by  Ulyana Lavnikevich (388633)
and Serin Bazzi (437585)
"""

from WindowManager import *
from UITK import *
from Window import *


class ColorSlidersApplication:

    def __init__(self, windowSystem):
        self.windowSystem = windowSystem
        self.window = None
        self.colorLabel = None
        self.rSlider = None
        self.gSlider = None
        self.bSlider = None
        self.createApp()

    def createApp(self):
        self.window = self.windowSystem.createWindowOnScreen(400, 40, 300, 300, "Color Sliders", COLOR_WHITE, 200, 250)

        self.rSlider = self.windowSystem.createSliderInWindow(self.window, 20, 0, 200, 33, "rSlider", LayoutAnchor.top,
                                                              0.2, COLOR_RED)

        self.gSlider = self.windowSystem.createSliderInWindow(self.window, 20, 50, 200, 33, "gSlider", LayoutAnchor.top,
                                                              0.1, COLOR_GREEN)

        self.bSlider = self.windowSystem.createSliderInWindow(self.window, 20, 150, 200, 33, "bSlider",
                                                              LayoutAnchor.top,
                                                              0.4, COLOR_BLUE)

        self.colorWindow = self.windowSystem.createLabelInWindow(self.window, 20, 200, 200, 33, "colorLabel",
                                                                 self.updateColorSlider(), "#F6A800",
                                                                 self.updateColorSlider(), LayoutAnchor.top)

    def updateColorSlider(self):
        # current RGB values from the sliders above
        # convert value of the slider in RGB system
        red = int(self.rSlider.value * 255)
        green = int(self.gSlider.value * 255)
        blue = int(self.bSlider.value * 255)

        # create new color string // convert into hex
        # with '#' starts each hex color
        # for each placeholder color convert rgb value in hex value with two hexadecimal numbers
        newColorInHex = '#%02x%02x%02x' % (red, green, blue)
        return newColorInHex
