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
        self.window = self.windowSystem.createWindowOnScreen(220, 20, 400, 500, "Calculator", COLOR_WHITE,200,200)

        # define label for display area?
        self.displayAreaLabel = self.windowSystem.createLabelInWindow(self.window, 10, 20, 20, 20, "displayArea",
                                                                      "0", COLOR_BLACK, COLOR_CLEAR, 50, "Helvetica",
                                                                      "bold")

        buttonWidth = 70
        buttonHeight = 70
        buttonSpacing = 2

        buttonX = 16
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
        buttonLabels = ['C', '+/-', '%', '/', '7', '8', '9', '*', '4', '5', '6', '-', '1', '2', '3', '+', '0', ',', '=']
        allButtons = []

        iterator = 0
        for i in range(rows):
            for j in range(cols):
                if buttonLabels:
                    if iterator == 16:
                        buttonWidth *= 2
                        button = self.windowSystem.createButtonInWindow(self.window, buttonX, buttonY, buttonWidth , buttonHeight, buttonLabels[iterator],
                                                                    buttonLabels[iterator], COLOR_WHITE, COLOR_GRAY, None, LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.right | LayoutAnchor.left)
                    else:
                        button = self.windowSystem.createButtonInWindow(self.window, buttonX, buttonY, buttonWidth, buttonHeight, buttonLabels[iterator],
                                                                    buttonLabels[iterator], COLOR_WHITE, COLOR_GRAY, None, LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.right | LayoutAnchor.left)

                    allButtons.append(button)

                if iterator == 16:
                    buttonX += buttonWidth + buttonSpacing
                    buttonWidth = buttonWidth / 2
                else:
                    buttonX += buttonWidth + buttonSpacing
                if iterator in range(0,18):
                    iterator += 1
                else:
                    break

            buttonX = 16
            buttonY += buttonHeight + buttonSpacing

    def clearDisplay(self):
        self.displayAreaLabel.text = "0"
        self.windowSystem.requestRepaint()
