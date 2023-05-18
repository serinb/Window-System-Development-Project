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
    def __init__(self, originX, originY, width, height, identifier, text, textColor, backgroundColor,
                 fontSize=14, fontFamily="Helvetica", fontWeight="normal"):
        super().__init__(originX, originY, width, height, identifier)
        self.text = text
        self.textColor = textColor
        self.backgroundColor = backgroundColor

        # Font
        self.fontSize = fontSize
        self.fontFamily = fontFamily
        self.fontWeight = fontWeight

    def draw(self, ctx, width, height):
        width = self.width
        height = self.height
        super().draw(ctx, width, height)
        font = Font(family=self.fontFamily, size=self.fontSize, weight=self.fontWeight)
        ctx.setFont(font)
        ctx.setStrokeColor(self.textColor)
        ctx.drawString(self.text, 10, 5)

    def handleMousePressed(self, x, y):
        print("i am in hadle mouse event in label")


class Button(Label):
    def __init__(self, originX, originY, width, height, identifier, textString, font, textColor, backgroundColor,
                 action=None):
        super().__init__(originX, originY, width, height, identifier, textString, font, textColor, backgroundColor)
        self.action = action
        self.isHovered = False
        self.isPressed = False

    def handleAction(self, function):
        # if is pressed == true and function is not none
        # return call(function)
        pass

    def draw(self, ctx, drawingWidth, drawingHeight):
        # convertedX, convertedY = self.parentWindow.convertPositionToScreen(self.x, self.y)
        # ctx.setOrigin(convertedX, convertedY)
        super().draw(ctx, drawingWidth, drawingHeight)
        if self.isHovered:
            color = COLOR_YELLOW
        elif self.isPressed:
            color = COLOR_RED
        else:
            color = COLOR_BLUE
        ctx.setStrokeColor(color)
        ctx.strokeRect(0, 0, self.width, self.height)
        ctx.strokeRect(15, 15, self.width - 5, self.height - 5)

    # handleMouse Events for Button:
    # if moved im Bereich des Buttons -> isHovered = True
    # if pressed im Bereich des Buttons und if pressed und released in den gleichen x und y -> isPressed = True


class Slider(Widget):
    def __init__(self, originX, originY, width, height, identifier):
        super().__init__(originX, originY, width, height, identifier)
        self.backgroundColor = COLOR_LIGHT_GRAY
        self.value = 0.0
        self.dragging = False

    def draw(self, ctx, drawingWidth, drawingHeight):
        super().draw(ctx, drawingWidth, drawingHeight)
