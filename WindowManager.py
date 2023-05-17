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
        # the height of the window’s title bar decoration
        # We will use it in the future to avoid the placement of widgets under the window decorations
        self.titleBarHeight = 30

        self.openedTopLevelWindows = []

    def openWindow(self, window):
        self.openedTopLevelWindows.append(window)

    # P3 (3) Negotiating window positions
    # to identify whether a window can exist at a given location
    # return a boolean value whether the passed proposed position for a window is valid.
    # Valid - if at least some part of the title bar is visible on screen
    # use this method in task 5 to prevent dragging a window outside the screen.
    def checkWindowPosition(self, window, x, y):
        print(window.identifier)

        halfTitleBarHeight = 0.5 * self.titleBarHeight
        halfWindowWidth = 0.5 * window.width

        # we define that a window is only allowed to exceed the boundaries of the screen
        # by half of its titlebar width and height
        topBoundary = - self.titleBarHeight
        bottomBoundary = self.windowSystem.screen.height - 50

        leftBoundary = - halfWindowWidth
        rightBoundary = self.windowSystem.screen.width + halfWindowWidth

        if leftBoundary <= x <= rightBoundary and topBoundary <= y <= bottomBoundary:
            return True
        else:
            return False

    def decorateWindow(self, window, ctx):
        # stroked border around the window
        ctx.setStrokeColor(COLOR_BLACK)
        ctx.setOrigin(window.x, window.y)
        ctx.strokeRect(0, 0, window.width, window.height)

        # foreground window should be visually discriminable
        lastIndex = len(self.windowSystem.screen.childWindows) - 1
        lastChild = self.windowSystem.screen.childWindows[lastIndex]

        veryLastChild = lastChild

        while len(veryLastChild.childWindows) > 0:
            lastLastIndex = len(veryLastChild.childWindows) - 1
            veryLastChild = veryLastChild.childWindows[lastLastIndex]

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

    # P3 (5)
    def minimizeWindow(self, window):
        if window.getTopLevelWindow() != window:
            minimizingWindow = window.getTopLevelWindow()
        else:
            minimizingWindow = window
        minimizingWindow.isHidden = True
        self.windowSystem.requestRepaint()

    # P3 (5)
    def closeWindow(self, window):
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

        # "terminate / start menu" button
        ctx.setFillColor("#6459cb")
        ctx.fillRect(0, self.windowSystem.screen.height - 50, 40, self.windowSystem.screen.height)
        ctx.drawString("S", 13.5, self.windowSystem.screen.height - 35)

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
                    ctx.strokeRect(40 + offset, self.windowSystem.screen.height - 50, 80 + offset,
                                   self.windowSystem.screen.height)
                    ctx.drawString(c.identifier[0], 50 + offset, self.windowSystem.screen.height - 33)
                    offset += 40
