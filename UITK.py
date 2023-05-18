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

    def createWindowInWindow(self, parentWindow, childX, childY, childWidth, childHeight, childIdentifier,
                             childBackgroundColor):
        pass

    def draw(self, ctx, drawingWidth, drawingHeight):
        # calculates the label's global coordinates w.r.t to its position within the parent window
        # and w.r.t to the new global position of the parent window
        # convertedX, convertedY = self.parentWindow.convertPositionToScreen(self.positionInParentX, self.positionInParentY)
        # update the global coordinates of the label to current position
        #self.x, self.y = convertedX, convertedY

        #ctx.setOrigin(convertedX, convertedY)

        ctx.setFillColor(self.backgroundColor)

        ctx.fillRect(0, 0, drawingWidth, drawingHeight)

        ctx.setStrokeColor(self.textColor)

        # ctx.setFont(self.font)

        # ctx.setFont(Font(family="Helvetica", size=22, weight="normal"))

        ctx.drawString(self.textString, 5, 5)

    def handleMousePressed(self, x, y):
        print("i am in hadle mouse event in label")


class Button(Label):
    def __init__(self, originX, originY, positionInParentX, positionInparentY, width, height, identifier, textString, textColor, backgroundColor, action=None):
        # super().__init__(originX, originY, width, height, identifier)
        # quit the app, in the calculator zifferneingabe
        super().__init__(originX, originY, positionInParentX, positionInparentY, width, height, identifier)
        self.action = action
        self.isHovered = False
        self.isPressed = False
        self.textColor = textColor
        self.backgroundColor = backgroundColor
        self.textString = textString

    def handleAction(self, function):
        #if is pressed == true and function is not none
         #return call(function)
        pass




    def draw(self, ctx, drawingWidth, drawingHeight):
        #convertedX, convertedY = self.parentWindow.convertPositionToScreen(self.x, self.y)
        #ctx.setOrigin(convertedX, convertedY)
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
