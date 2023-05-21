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
        self.result = ''
        self.operand1 = ''
        self.operand2 = ''
        self.operator = ''
        self.createApp()

    def createApp(self):
        self.window = self.windowSystem.createWindowOnScreen(220, 20, 380, 480, "Calculator", COLOR_WHITE, 200, 200)

        # self.containerDisplay = self.windowSystem.createContainerInWindow(self.window, 0, 0, 300,
        #                                                                   150, "container_display",
        #                                                                   LayoutAnchor.top | LayoutAnchor.right | LayoutAnchor.left,
        #                                                                   500,
        #                                                                   80)

        # define label for display area
        self.displayAreaLabel = self.windowSystem.createLabelInWindow(self.window, 0, 10, 100, 20, "displayArea",
                                                                      "0", COLOR_BLACK, COLOR_CLEAR, LayoutAnchor.top,
                                                                      50, 50, 44, "Helvetica",
                                                                      "bold")

        buttonSize = 70
        buttonSpacing = 2
        buttonX = 10
        buttonY = 110

        rows = 5
        cols = 4

        buttonLabels = ['C', '+/-', '%', '/', '7', '8', '9', '*', '4', '5', '6', '-', '1', '2', '3', '+', '0', '=', '.']

        iterator = 0
        for i in range(rows):
            for j in range(cols):
                if iterator < len(buttonLabels):
                    if buttonLabels[iterator] == '0':
                        self.windowSystem.createButtonInWindow(self.window, buttonX, buttonY,
                                                               buttonSize * 2 + buttonSpacing,
                                                               buttonSize, buttonLabels[iterator],
                                                               buttonLabels[iterator], COLOR_WHITE, COLOR_GRAY,
                                                               lambda label=buttonLabels[iterator]: self.buttonClicked(
                                                                   label),
                                                               LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.right | LayoutAnchor.left)
                        buttonX += (buttonSize * 2) + (buttonSpacing * 2)
                    else:
                        self.windowSystem.createButtonInWindow(self.window, buttonX, buttonY, buttonSize,
                                                               buttonSize, buttonLabels[iterator],
                                                               buttonLabels[iterator], COLOR_WHITE, COLOR_GRAY,
                                                               lambda label=buttonLabels[iterator]: self.buttonClicked(
                                                                   label),
                                                               LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.right | LayoutAnchor.left)
                        buttonX += buttonSize + buttonSpacing
                    iterator = iterator + 1

            buttonX = 10
            buttonY += buttonSize + buttonSpacing

    def clearDisplay(self):
        self.result = ""
        self.operand1 = ""
        self.operand2 = ""
        self.operator = ""
        self.displayAreaLabel.text = "0"
        self.windowSystem.requestRepaint()

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> b96c936a43f455eca1b93d12a7e966fa60d0a702
    def buttonClicked(self, label):
        # clear operation
        if label == 'C':
            self.clearDisplay()
        # distinguish between numbers and operators
        elif label.isdigit() or label == '.':
            if self.operand1 and self.operator:
                self.operand2 = self.operand2 + label
                self.displayAreaLabel.text = self.displayAreaLabel.text + self.operand2
                self.windowSystem.requestRepaint()
            else:
                self.result += label
                self.displayAreaLabel.text = self.result
                self.windowSystem.requestRepaint()
        # % operation
        elif self.operand1 and not self.operator and label == '%':
            self.result = str(float(float(self.operand1) / 100))
<<<<<<< HEAD
=======
    def concatenate(self, input):
        return self.result + input


    def inputHandler(self, btnidentifier):
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        if self.operand1 == '' and numbers.index(btnidentifier):
            self.operand1 = self.concatenate(btnidentifier)
>>>>>>> main
=======
>>>>>>> b96c936a43f455eca1b93d12a7e966fa60d0a702
            self.displayAreaLabel.text = self.result
            self.windowSystem.requestRepaint()
        # '+/- operation
        elif label == '+/-':
            if not self.result:
                self.operand1 = str(float(self.operand1) * -1)
                self.displayAreaLabel.text = self.operand1 + self.operator + self.operand2
                self.windowSystem.requestRepaint()
            else:
                self.result = str(float(self.result) * -1)
                self.displayAreaLabel.text = self.result
                self.windowSystem.requestRepaint()
        # other basic operations
        elif label in ['/', '*', '-', '+']:
            if self.operand1 and not self.operator:
                self.operator = label
                self.displayAreaLabel.text += self.operator
                self.windowSystem.requestRepaint()

        # Calculate and display displayAreaLabel.text value only after one presses an equals sign or
        # 'enter' on the keyboard
        elif label == '=' or label == "":
            if self.operand1 and self.operand2 and self.operator:
                try:
                    if self.operator == '+':
                        self.result = str(float(self.operand1) + float(self.operand2))
                    elif self.operator == '-':
                        self.result = str(float(self.operand1) - float(self.operand2))
                    elif self.operator == '*':
                        self.result = str(float(self.operand1) * float(self.operand2))
                    elif self.operator == '/':
                        self.result = str(float(self.operand1) / float(self.operand2))
                    self.displayAreaLabel.text = self.result
                # the app does not crash when dividing with zero:
                except ZeroDivisionError:
                    self.displayAreaLabel.text = "invalid"
                # reset everything
                # self.result = ""
                self.operand1 = ""
                self.operand2 = ""
                self.operator = ""
                self.windowSystem.requestRepaint()

        if not self.operator:
            self.operand1 = self.result
        elif self.operand1 and self.operator and not self.operand2:
            self.displayAreaLabel.text = self.operand1 + self.operator
        elif self.operand1 and self.operator and self.operand2:
            self.displayAreaLabel.text = self.operand1 + self.operator + self.operand2
