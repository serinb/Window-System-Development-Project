#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Window System - Submission
by  Ulyana Lavnikevich (388633)
and Serin Bazzi (437585)
"""

from GraphicsEventSystem import *
from Window import *


class Widget(Window):
    def __init__(self, originX, originY, width, height, identifier):
        super().__init__(originX, originY, width, height, identifier)
        self.backgroundColor = COLOR_CLEAR

    def addParent(self):
        pass


class Container(Widget):
    def resize(self, x, y, width, height):
        super().resize(x, y, width, height)


class Label(Widget):
    def __init__(self, originX, originY, width, height, identifier, textString="", textColor=COLOR_BLACK,
                 backgroundColor=COLOR_CLEAR):
        super().__init__(originX, originY, width, height, identifier)
        self.textString = textString
        self.textColor = textColor
        self.backgroundColor = backgroundColor
        # self.font = font

    def draw(self, ctx):
        # provide label's coordinates as local coordinates of the parent window and convert these to global coordinates
        #convertedX, convertedY = self.parentWindow.convertPositionToScreen(self.x, self.y)
        print("Yellow window  " + str(self.parentWindow.x) + "  " + str(self.parentWindow.y))
        #print("draw methode" + " : " + str(convertedX) + "  " + str(convertedY))
        # newX, newY = self
        # self.x = 530 self.y = 440
        # globale koordinaten von dem Label
        convertedX, convertedY = self.parentWindow.convertPositionFromScreen(self.x, self.y) # 30, 40
        print("Converted " + str(convertedX) + "  " + str(convertedY))
        newX, newY = self.parentWindow.convertPositionToScreen(convertedX, convertedY)

        ctx.setOrigin(newX, newY)

        ctx.setFillColor(self.backgroundColor)

        ctx.fillRect(0, 0, self.width, self.height)

        ctx.setStrokeColor(self.textColor)

        # ctx.setFont(self.font)

        # ctx.setFont(Font(family="Helvetica", size=22, weight="normal"))

        ctx.drawString(self.textString, 5, 5)


class Button(Label):
    def __init__(self, originX, originY, width, height, identifier, action=None):
        # super().__init__(originX, originY, width, height, identifier)
        # quit the app, in the calculator zifferneingabe
        super().__init__(originX, originY, width, height, identifier)
        self.action = action
        self.isHovered = False
        self.isPressed = False

    def draw(self, ctx):
        convertedX, convertedY = self.parentWindow.convertPositionToScreen(self.x, self.y)
        ctx.setOrigin(convertedX, convertedY)
        # super().draw(ctx)
        if self.isHovered:
            color = COLOR_YELLOW
        elif self.isPressed:
            color = COLOR_RED
        else:
            color = COLOR_BLUE
        ctx.setStrokeColor(color)
        ctx.strokeRect(0, 0, self.width, self.height)
        ctx.strokeRect(15, 15, self.width - 15, self.height - 15)

    # handleMouse Events for Button:
    # if moved im Bereich des Buttons -> isHovered = True
    # if pressed im Bereich des Buttons und if pressed und released in den gleichen x und y -> isPressed = True


class Slider(Widget):
    def __init__(self, originX, originY, width, height, identifier):
        super().__init__(originX, originY, width, height, identifier)
        self.backgroundColor = COLOR_LIGHT_GRAY
        self.value = 0.0
        self.dragging = False

    def draw(self, ctx):
        super().draw(ctx)
