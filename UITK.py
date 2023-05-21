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
    def __init__(self, originX, originY, width, height, identifier, anchoring, minWidth, minHeight, depth):
        super().__init__(originX, originY, width, height, identifier, anchoring, minWidth, minHeight, depth)
        self.backgroundColor = COLOR_GRAY
        # window padding
        self.paddingTop = 5
        self.paddingLeft = 5
        self.paddingBottom = 5
        self.paddingRight = 5

    def handleMouseClicked(self, x, y):
        pass

    def resize(self, x, y, width, height):
        super().resize(x, y, width, height)



class Container(Widget):
    def __init__(self, originX, originY, width, height, identifier, anchoring, minWidth, minHeight, depth, maxSpacing=5, minSpacing=3):
        super().__init__(originX, originY, width, height, identifier, anchoring, minWidth, minHeight, depth)
        self.maxSpacing = maxSpacing
        self.minSpacing = minSpacing

    def resize(self, x, y, width, height):
        super().resize(x, y, width, height)


class Label(Widget):
    def __init__(self, originX, originY, width, height, identifier, anchoring, minWidth, minHeight, text, textColor,
                 backgroundColor, depth, fontSize=11, fontFamily="Arial", fontWeight="normal"):
        super().__init__(originX, originY, width, height, identifier, anchoring, minWidth, minHeight, depth)
        self.text = text
        self.textColor = textColor
        self.backgroundColor = backgroundColor

        # Font
        self.fontSize = fontSize
        self.fontFamily = fontFamily
        self.fontWeight = fontWeight

    def resize(self, x, y, width, height):
        super().resize(x, y, width, height)

    def draw(self, ctx, width, height):
        super().draw(ctx, width, height)
        font = Font(family=self.fontFamily, size=self.fontSize, weight=self.fontWeight)
        ctx.setFont(font)
        ctx.setStrokeColor(self.textColor)
        ctx.drawString(self.text, 10, 7)


class Button(Label):
    def __init__(self, originX, originY, width, height, identifier, anchoring, minWidth,
                 minHeight, text, textColor, backgroundColor, depth, action=None):
        super().__init__(originX, originY, width, height, identifier, anchoring, minWidth, minHeight,
                         text, textColor, backgroundColor, depth)
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
            color = COLOR_WHITE

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
