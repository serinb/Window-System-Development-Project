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
        self.window = self.windowSystem.createWindowOnScreen(220, 20, 380, 420, "Calculator", COLOR_WHITE,200,200)

        self.containerDisplay = self.windowSystem.createContainerInWindow(self.window, 0, 0, 300,
                                150, "container_display", LayoutAnchor.top | LayoutAnchor.right | LayoutAnchor.left, 500,
                                80)

                # define label for display area?
        self.displayAreaLabel = self.windowSystem.createLabelInWindow(self.containerDisplay, 0, 0, 300, 80, "displayArea",
                                                                      "0", COLOR_BLACK, COLOR_GREEN)

        #containerRow1 = self.windowSystem.createWidgetInWindow(self.Window)

        buttonWidth = 60
        buttonHeight = 60
        buttonSpacing = 2
        buttonX = 16
        buttonY = 150


        # first Row (left-right)
        self.button00 = self.windowSystem.createButtonInWindow(self.window, buttonX, buttonY, buttonWidth , buttonHeight, 'C',
                'C', COLOR_WHITE, COLOR_GRAY, lambda: self.concatenate("C"), LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.right | LayoutAnchor.left)

        buttonX += buttonWidth + buttonSpacing

        self.button01 = self.windowSystem.createButtonInWindow(self.window, buttonX, buttonY, buttonWidth , buttonHeight, '+/-',
                '+/-', COLOR_WHITE, COLOR_GRAY, None, LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.right | LayoutAnchor.left)

        buttonX += buttonWidth + buttonSpacing

        self.button02 = self.windowSystem.createButtonInWindow(self.window, buttonX, buttonY, buttonWidth , buttonHeight, '%',
                '%', COLOR_WHITE, COLOR_GRAY, None, LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.right | LayoutAnchor.left)

        buttonX += buttonWidth + buttonSpacing

        self.button03 = self.windowSystem.createButtonInWindow(self.window, buttonX, buttonY, buttonWidth , buttonHeight, '/',
                '/', COLOR_WHITE, COLOR_GRAY, None, LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.right | LayoutAnchor.left)

        buttonX = 16
        buttonY += buttonHeight + buttonSpacing

        # second Row (left-right)
        self.button10 = self.windowSystem.createButtonInWindow(self.window, buttonX, buttonY, buttonWidth , buttonHeight, '7',
                '7', COLOR_WHITE, COLOR_GRAY, None, LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.right | LayoutAnchor.left)

        buttonX += buttonWidth + buttonSpacing

        self.button11 = self.windowSystem.createButtonInWindow(self.window, buttonX, buttonY, buttonWidth , buttonHeight, '8',
                '8', COLOR_WHITE, COLOR_GRAY, None, LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.right | LayoutAnchor.left)

        buttonX += buttonWidth + buttonSpacing

        self.button12 = self.windowSystem.createButtonInWindow(self.window, buttonX, buttonY, buttonWidth , buttonHeight, '9',
                '9', COLOR_WHITE, COLOR_GRAY, None, LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.right | LayoutAnchor.left)

        buttonX += buttonWidth + buttonSpacing

        self.button13 = self.windowSystem.createButtonInWindow(self.window, buttonX, buttonY, buttonWidth , buttonHeight, '*',
                '*', COLOR_WHITE, COLOR_GRAY, None, LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.right | LayoutAnchor.left)

        buttonX = 16
        buttonY += buttonHeight + buttonSpacing

        # third Row (left-right)
        self.button20 = self.windowSystem.createButtonInWindow(self.window, buttonX, buttonY, buttonWidth , buttonHeight, '4',
                '4', COLOR_WHITE, COLOR_GRAY, None, LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.right | LayoutAnchor.left)

        buttonX += buttonWidth + buttonSpacing

        self.button21 = self.windowSystem.createButtonInWindow(self.window, buttonX, buttonY, buttonWidth , buttonHeight, '5',
                '5', COLOR_WHITE, COLOR_GRAY, None, LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.right | LayoutAnchor.left)

        buttonX += buttonWidth + buttonSpacing

        self.button22 = self.windowSystem.createButtonInWindow(self.window, buttonX, buttonY, buttonWidth , buttonHeight, '6',
                '6', COLOR_WHITE, COLOR_GRAY, None, LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.right | LayoutAnchor.left)

        buttonX += buttonWidth + buttonSpacing

        self.button23 = self.windowSystem.createButtonInWindow(self.window, buttonX, buttonY, buttonWidth , buttonHeight, '-',
                '-', COLOR_WHITE, COLOR_GRAY, None, LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.right | LayoutAnchor.left)

        buttonX = 16
        buttonY += buttonHeight + buttonSpacing

        # forth Row (left-right)
        self.button30 = self.windowSystem.createButtonInWindow(self.window, buttonX, buttonY, buttonWidth , buttonHeight, '1',
                '1', COLOR_WHITE, COLOR_GRAY, lambda: self.concatenate(1), LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.right | LayoutAnchor.left)

        buttonX += buttonWidth + buttonSpacing

        self.button31 = self.windowSystem.createButtonInWindow(self.window, buttonX, buttonY, buttonWidth , buttonHeight, '2',
                '2', COLOR_WHITE, COLOR_GRAY, lambda: self.concatenate(1), LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.right | LayoutAnchor.left)

        buttonX += buttonWidth + buttonSpacing

        self.button32 = self.windowSystem.createButtonInWindow(self.window, buttonX, buttonY, buttonWidth , buttonHeight, '3',
                '3', COLOR_WHITE, COLOR_GRAY, None, LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.right | LayoutAnchor.left)

        buttonX += buttonWidth + buttonSpacing

        self.button33 = self.windowSystem.createButtonInWindow(self.window, buttonX, buttonY, buttonWidth , buttonHeight, '+',
                '+', COLOR_WHITE, COLOR_GRAY, None, LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.right | LayoutAnchor.left)

        buttonX = 16
        buttonWidth *= 2
        buttonWidth += buttonSpacing
        buttonY += buttonHeight + buttonSpacing

        # fifth Row (left-right)
        self.button40 = self.windowSystem.createButtonInWindow(self.window, buttonX, buttonY, buttonWidth , buttonHeight, '0',
                '0', COLOR_WHITE, COLOR_GRAY, None, LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.right | LayoutAnchor.left)

        buttonX += buttonWidth + buttonSpacing
        buttonWidth = buttonWidth / 2
        buttonWidth -= 2

        self.button41 = self.windowSystem.createButtonInWindow(self.window, buttonX, buttonY, buttonWidth , buttonHeight, ',',
                ',', COLOR_WHITE, COLOR_GRAY, None, LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.right | LayoutAnchor.left)

        buttonX += buttonWidth + buttonSpacing
        buttonWidth += 2

        self.button42 = self.windowSystem.createButtonInWindow(self.window, buttonX, buttonY, buttonWidth , buttonHeight, '=',
                '=', COLOR_WHITE, COLOR_GRAY, None, LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.right | LayoutAnchor.left)


        #buttonLabels = ['C', '+/-', '%', '/', '7', '8', '9', '*', '4', '5', '6', '-', '1', '2', '3', '+', '0', ',', '=']

    def clearDisplay(self):
        self.result = "0"
        self.displayAreaLabel.text = self.result
        self.windowSystem.requestRepaint()

    def concatenate(self, input):
        return self.result + str(input)


    def inputHandler(self, btnidentifier):
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        if self.operand1 == '' and numbers.index(btnidentifier):
            self.operand1 = self.concatenate(btnidentifier)
            self.displayAreaLabel.text = self.result
        elif self.operator == '':
            self.result = self.calculate()
            self.displayAreaLabel.text = self.result
        elif self.operand2 == '' and numbers.index(btnidentifier):
            self.operand2 = self.concatenate(btnidentifier)








