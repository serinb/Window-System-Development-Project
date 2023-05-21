#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Window System - Submission
by  Ulyana Lavnikevich (388633)
and Serin Bazzi (437585)
"""

from GraphicsEventSystem import *
from Window import *


# The window manager (WM) implements a user interface to window functions
# — like positioning, resizing, minimizing
class WindowManager:
    def __init__(self, windowSystem):
        self.windowSystem = windowSystem
        # th4e height of the window’s title bar decoration
        # We will use it in the future to avoid the placement of widgets under the window decorations
        self.titleBarHeight = 30

        # screen boundaries
        self.screenTopBoundary = -15
        self.screenBottomBoundary = 550
        self.screenLeftBoundary = -100
        self.screenRightBoundary = 900


        self.openedTopLevelWindows = []
        self.startMenu = None

    def openWindow(self, window):
        self.openedTopLevelWindows.append(window)



    def decorateWindow(self, window, ctx):
        # stroked border around the window
        ctx.setStrokeColor(COLOR_BLACK)
        ctx.setOrigin(window.x, window.y)
        ctx.strokeRect(0, 0, window.width, window.height)
        standardFont = Font(family="Helvetica", size=11, weight="normal")
        ctx.setFont(standardFont)

        # foreground window should be visually discriminable
        lastIndex = len(self.windowSystem.screen.childWindows) - 1
        lastChild = self.windowSystem.screen.childWindows[lastIndex]

        veryLastChild = lastChild

        if veryLastChild == window:
            ctx.setFillColor(COLOR_PINK)
        else:
            # colored title bar
            ctx.setFillColor("#f5daf7")

        ctx.fillRect(1, 1, window.width, self.titleBarHeight)
        # title string of a window with the identifier of the window
        ctx.drawString(window.identifier, 10, 7)

        # closing Button
        ctx.drawString("X", window.width - 15, 7)

        # minimizing button
        ctx.drawLine(window.width - 40, 15, window.width - 33, 15)

        # resize Button
        ctx.setFillColor(COLOR_BLACK)
        ctx.strokeRect(window.width - 15, window.height - 15, window.width, window.height)


    def checkWindowPosition(self, window, x, y, invalidSide):

        valid = True

        if (self.screenTopBoundary > y):
            valid = False
            invalidSide.append("top")
        if (y + window.height > self.screenBottomBoundary):
            valid = False
            invalidSide.append("bottom")
        if (self.screenLeftBoundary > x):
            valid = False
            invalidSide.append("left")
        if (x + window.width > self.screenRightBoundary):
            valid = False
            invalidSide.append("right")
        return valid

    def dragChildren(self, window, x, y):

        if len(window.childWindows) > 0:
            for c in window.childWindows:
                oldX, oldY = c.x, c.y
                convertedX, convertedY = x - window.x, y - window.y
                c.x, c.y = window.convertPositionToScreen(convertedX, convertedY)
                self.dragChildren(c, oldX, oldY)


    def dragWindow(self, window, x, y):

        if window.identifier != "Start_menu":

            # difference between old and new (x,y) coordinates
            differenceX = x - self.windowSystem.recentX
            differenceY = y - self.windowSystem.recentY
            newX = window.x + differenceX
            newY = window.y + differenceY

            invalidSide = []
            childPostion = []
            iterator = 0
            if len(window.childWindows) > 0:
                for c in window.childWindows:
                    convertedX, convertedY = window.convertPositionFromScreen(c.x, c.y)
                    childPostion.append([convertedX, convertedY])

            if self.checkWindowPosition(window, newX, newY, invalidSide):
                # update origin x,y for children of lastClickedWindow
                window.x = newX
                window.y = newY

            else:
                for side in invalidSide:
                    if side == "left":
                        window.x = self.screenLeftBoundary
                    elif side == "right":
                        window.x = self.screenRightBoundary - window.width
                    elif side == "top":
                        window.y = self.screenTopBoundary
                    elif side == "bottom":
                        window.y = self.screenBottomBoundary - window.height

            if len(window.childWindows) > 0:

                    iterator in range(len(childPostion))
                    for c in window.childWindows:
                        oldX, oldY = c.x, c.y
                        c.x, c.y = window.convertPositionToScreen(childPostion[iterator][0], childPostion[iterator][1])
                        self.dragChildren(c, oldX, oldY)

            self.windowSystem.recentX = x
            self.windowSystem.recentY = y
            self.windowSystem.requestRepaint()





    def resizeWindow(self, window, x, y):
        # x,y are global coordinates
        if window.parentWindow == self.windowSystem.screen:
            newWidth, newHeight = window.convertPositionFromScreen(x, y)
            window.resize(window.x, window.y, newWidth, newHeight)
            if window.x + newWidth <= self.windowSystem.screen.width and window.y + newHeight <= self.windowSystem.screen.height - 50:
                self.windowSystem.requestRepaint()

    # P3 (5)
    def minimizeWindow(self, window):
        if window.identifier != "Start_menu":
            if window.getTopLevelWindow() != window:
                minimizingWindow = window.getTopLevelWindow()
            elif window.identifier:
                minimizingWindow = window
            minimizingWindow.isHidden = True
            self.windowSystem.requestRepaint()


    # P3 (5)
    def closeWindow(self, window):
        if window.identifier != "Start_menu":
            window.isClosed = True
            window.removeFromParentWindow()
            self.openedTopLevelWindows.remove(window)
            window.isHidden = True
            self.windowSystem.requestRepaint()


    # P3 (1)
    # Add an instance of the WM to the window system
    def drawDesktop(self, ctx):
        # fill the screen with a nice color
        ctx.setFillColor("#fff")
        # your wallpaper should draw correctly even if the window system is created with a different screen size
        width, height = self.windowSystem.screen.width, self.windowSystem.screen.height
        ctx.fillRect(0, 0, width, height)

    # P3 (6) Task bar
    def drawTaskbar(self, ctx):
        ctx.setFillColor("#3b28a2")
        ctx.fillRect(0, self.windowSystem.screen.height - 50, self.windowSystem.screen.width,
                     self.windowSystem.screen.height)

        """
        # "terminate / start menu" button
        ctx.setFillColor("#6459cb")
        ctx.fillRect(0, self.windowSystem.screen.height - 50, 40, self.windowSystem.screen.height)
        ctx.drawString("S", 13.5, self.windowSystem.screen.height - 35)

        """

        if len(self.windowSystem.screen.childWindows) > 0:
            lastIndex = len(self.windowSystem.screen.childWindows) - 1
            lastChild = self.windowSystem.screen.childWindows[lastIndex]

            # define offset to start drawing the next child of the screen at the offset location
            offset = 0
            for c in self.openedTopLevelWindows:
                if lastChild == c:
                    ctx.setStrokeColor(COLOR_PINK)
                else:
                    ctx.setStrokeColor(COLOR_GRAY)
                if not c.isClosed:
                    ctx.strokeRect(0 + offset, self.windowSystem.screen.height - 50, 40 + offset,
                                   self.windowSystem.screen.height)
                    ctx.drawString(c.identifier[0], 10 + offset, self.windowSystem.screen.height - 33)
                    offset += 42
