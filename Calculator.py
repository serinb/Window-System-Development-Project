#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Calculator - Submission
by  Ulyana Lavnikevich (388633)
and Serin Bazzi (437585)
"""

from GraphicsEventSystem import *
from Window import *
from WindowManager import *
from UITK import *


class CalculatorApplication:
    def __init__(self, windowSystem):
        self.windowSystem = windowSystem
        self.window = None
        self.labelApp = None
        self.displayAreaLabel = None
        self.createApp()

    def createApp(self):
        self.window = self.windowSystem.createWindowOnScreen(220, 20, 400, 500, "Calculator", COLOR_WHITE)

        # define label for display area?
        self.displayAreaLabel = self.windowSystem.createLabelInWindow(self.window, 10, 20, 20, 20, "displayArea",
                                                                      "0", COLOR_BLACK, COLOR_CLEAR, 50, "Helvetica",
                                                                      "bold")

        buttonSize = 70
        buttonSpacing = 2

        buttonX = 10
        buttonY = 80

        rows = 5
        cols = 4

        # for schleife to create 0..9 buttons
        # for schleife to operation buttons + - + / = %
        # ODER eine Schleife mit:
        # C +/- % /
        # 7 8 9 *
        # 4 5 6 -
        # 1 2 3 +
        # 0 . =
        # also die Liste ist [C +/- % / 7 8 9 * 4 5 6 - 1 2 3 + 0 . =]
        buttonLabels = ['C', '+/-', '%', '/', '7', '8', '9', '*', '4', '5', '6', '-', '1', '2', '3', '+', '0', '=', '', '']

        iterator = 0
        for i in range(rows):
            for j in range(cols):
                if buttonLabels:
                    button = self.windowSystem.createButtonInWindow(self.window, buttonX, buttonY, buttonSize, buttonSize, buttonLabels[iterator],
                                                                    buttonLabels[iterator], COLOR_WHITE, COLOR_GRAY,
                                                                    None)
                    buttonX += buttonSize + buttonSpacing
                    iterator = iterator + 1

            buttonX = 10
            buttonY += buttonSize + buttonSpacing

    def clearDisplay(self):
        self.displayAreaLabel.text = "0"
        self.windowSystem.requestRepaint()
