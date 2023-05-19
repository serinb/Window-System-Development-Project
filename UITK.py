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
        ctx.drawString(self.text, 10, 7)


class Button(Label):
    def __init__(self, originX, originY, width, height, identifier, textString, textColor, backgroundColor,
                 action=None):
        super().__init__(originX, originY, width, height, identifier, textString, textColor, backgroundColor)

        self.isHovered = False
        self.isPressed = False
        self.isActive = False
        self.action = action

    def handleAction(self):
        if self.isActive:
            self.isActive = False
            self.action()

    def draw(self, ctx, drawingWidth, drawingHeight):
        super().draw(ctx, drawingWidth, drawingHeight)
        if self.isHovered:
            color = COLOR_YELLOW
        elif self.isPressed:
            color = COLOR_RED
        else:
            color = COLOR_GRAY

        ctx.setStrokeColor(color)
        ctx.strokeRect(0, 0, self.width, self.height)
        ctx.strokeRect(6, 6, self.width - 6, self.height - 6)


class Slider(Widget):
    def __init__(self, originX, originY, width, height, identifier):
        super().__init__(originX, originY, width, height, identifier)
        self.backgroundColor = COLOR_LIGHT_GRAY
        self.value = 0.0
        self.dragging = False

    def draw(self, ctx, drawingWidth, drawingHeight):
        super().draw(ctx, drawingWidth, drawingHeight)
