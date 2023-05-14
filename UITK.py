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

    def draw(self, ctx):
        super().draw(ctx)
        ctx.setFillColor(self.backgroundColor)
        ctx.fillRect(0, 0, self.width, self.height)
        ctx.setStrokeColor(COLOR_WHITE)
        ctx.drawString(self.textString, 10, 10)


class Button(Label):
    def __init__(self, originX, originY, width, height, identifier, action=None):
        super().__init__(originX, originY, width, height, identifier)
        self.action = action
        self.isHovered = False
        self.isPressed = False

    def draw(self, ctx):
        super().draw(ctx)
        if self.isHovered:
            color = COLOR_YELLOW
        elif self.isPressed:
            color = COLOR_RED
        else:
            color = COLOR_BLUE
        ctx.setStrokeColor(color)
        ctx.strokeRect(0, 0, self.width, self.height)
        ctx.strokeRect(3, 3, self.width - 3, self.height - 3)

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

