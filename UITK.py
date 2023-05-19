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
    def __init__(self, originX, originY, width, height, identifier, anchoring, minWidth, minHeight):
        super().__init__(originX, originY, width, height, identifier, anchoring, minWidth, minHeight)
        self.backgroundColor = COLOR_CLEAR

    def addParent(self):
        pass


class Container(Widget):
    def __init__(self, originX, originY, width, height, identifier, anchoring, axis, spacing=20):
        super().__init__(originX, originY, width, height, identifier, anchoring)
        self.spacing = spacing
        # horizontal or vertical
        self.axis = axis

    # def addChildWindow(self, window):
        # super().addChildWindow(window)

    def resize(self, x, y, width, height):
        super().resize(x, y, width, height)
        # equally distribute its space across its children either on the horizontal or vertical axis
        if self.axis == "h":
            pass
        elif self.axis == "v":
            pass


class Label(Widget):
    def __init__(self, originX, originY, width, height, identifier, anchoring, text, textColor,
                 backgroundColor, minWidth, minHeight, fontSize=14, fontFamily="Helvetica", fontWeight="normal"):
        super().__init__(originX, originY, width, height, identifier, anchoring, minWidth, minHeight)
        self.text = text
        self.textColor = textColor
        self.backgroundColor = backgroundColor

        # Font
        self.fontSize = fontSize
        self.fontFamily = fontFamily
        self.fontWeight = fontWeight

    def draw(self, ctx, width, height):
        super().draw(ctx, width, height)
        font = Font(family=self.fontFamily, size=self.fontSize, weight=self.fontWeight)
        ctx.setFont(font)
        ctx.setStrokeColor(self.textColor)
        ctx.drawString(self.text, 10, 7)


class Button(Label):
    def __init__(self, originX, originY, width, height, identifier, textString, textColor, backgroundColor, minWidth, minHeight,
                 action=None, anchoring=None):
        super().__init__(originX, originY, width, height, identifier, anchoring, textString, textColor, backgroundColor, minWidth, minHeight)

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
    def __init__(self, originX, originY, width, height, identifier, anchoring):
        super().__init__(originX, originY, width, height, identifier, anchoring)
        self.backgroundColor = COLOR_LIGHT_GRAY
        self.value = 0.0
        self.dragging = False

    def draw(self, ctx, drawingWidth, drawingHeight):
        super().draw(ctx, drawingWidth, drawingHeight)
