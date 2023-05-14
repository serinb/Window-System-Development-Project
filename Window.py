#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Window System - Submission
by  Ulyana Lavnikevich (388633)
and Serin Bazzi (437585)
"""

from GraphicsEventSystem import *
from WindowManager import *
from collections import namedtuple

AllAnchors = namedtuple('AllAnchors', "top right bottom left")
# i.e. 1 - top, 2 - right, 4 - bottom, 8 - left corner
LayoutAnchor = AllAnchors(1 << 0, 1 << 1, 1 << 2, 1 << 3)


class Window:
    def __init__(self, originX, originY, width, height, identifier, depth=1):
        self.x = originX
        self.y = originY
        self.width = width
        self.height = height
        self.identifier = identifier
        self.depth = depth
        self.backgroundColor = COLOR_LIGHT_GRAY

        self.childWindows = []
        self.parentWindow = None

        # P3 (5)
        self.isHidden = False

        self.isClosed = False

        # P3 (7) Specify a new property layoutAnchors in Window which will contain a bitmask.
        # to fix the margin between a view and its parent view when the parent is resized.
        # default is to anchor a child window to the top-left corner
        self.layoutAnchors = LayoutAnchor.top | LayoutAnchor.left

        # a window cannot have a negative width or height, therefore define minHeight and minWidth
        self.minWidth = 170
        self.minHeight = 170

    # P2 1a
    def addChildWindow(self, window):
        # each window knows its parent
        window.parentWindow = self
        # each window knows its children
        if window not in self.childWindows:
            self.childWindows.append(window)

    # P2 1a
    def removeFromParentWindow(self):
        if self.parentWindow:
            self.parentWindow.childWindows.remove(self)
            self.parentWindow = None

    # P2 4b
    def childWindowAtLocation(self, x, y):
        # only works if calling window has children, else returns 0
        if len(self.childWindows) > 0:
            recentHitTestStatus = None
            recentHitTestDepth = 0
            depth, deepestChild = self.helperFunction(x, y, recentHitTestStatus, recentHitTestDepth)

            if deepestChild is not None:
                return deepestChild
            else:
                return None
        else:
            return None

    def helperFunction(self, x, y, recentHitTestStatus, recentHitTestDepth):
        # traverse childWindows Array right->left
        for child in reversed(self.childWindows):

            if (recentHitTestStatus is not None) and (len(recentHitTestStatus.childWindows) == 0):
                return recentHitTestDepth, recentHitTestStatus

            # coordinate conversion w.r.t child
            newX, newY = self.convertPositionToScreen(x, y)
            convertedX, convertedY = child.convertPositionFromScreen(newX, newY)

            if (child.hitTest(convertedX, convertedY)) and (recentHitTestStatus is None):
                recentHitTestStatus = child
                recentHitTestDepth = child.depth
                # print("hittest true for: " + recentHitTestStatus.identifier)

            elif (child.hitTest(convertedX, convertedY)) and (recentHitTestStatus is not None):
                if child.compareTopLevelWindows(recentHitTestStatus) == child:
                    recentHitTestStatus = child
                    recentHitTestDepth = child.depth
                    # print("hittest true for: " + recentHitTestStatus.identifier)

                elif (child.compareTopLevelWindows(recentHitTestStatus) == 0) and (
                        child.depth >= recentHitTestDepth):
                    recentHitTestStatus = child
                    recentHitTestDepth = child.depth
                    # print("hittest true for: " + recentHitTestStatus.identifier)

            if len(child.childWindows) > 0:
                recentHitTestDepth, recentHitTestStatus = child.helperFunction(convertedX, convertedY,
                                                                               recentHitTestStatus,
                                                                               recentHitTestDepth)

        return recentHitTestDepth, recentHitTestStatus

    def getTopLevelWindow(self):
        if self.parentWindow.identifier != "SCREEN_1":

            topLevelWindow = self
            # traverse the window tree upwards until the parent of the window is "screen"
            # meaning until the top level window on the path of window is found
            while topLevelWindow.parentWindow.identifier != "SCREEN_1":
                topLevelWindow = topLevelWindow.parentWindow

            # add the top level window to the end of the list of children of screen
            return topLevelWindow
        else:
            return self

    def compareTopLevelWindows(self, window):
        # calling Window
        topLevelWindow1 = self.getTopLevelWindow()
        # parameter window
        topLevelWindow2 = window.getTopLevelWindow()

        screen = topLevelWindow1.parentWindow

        if screen.childWindows.index(topLevelWindow1) > screen.childWindows.index(topLevelWindow2):
            return self
        elif screen.childWindows.index(topLevelWindow1) < screen.childWindows.index(topLevelWindow2):
            return window
        elif screen.childWindows.index(topLevelWindow1) == screen.childWindows.index(topLevelWindow2):
            return 0

    # P2 4a
    def hitTest(self, x, y):
        # x,y is a local coordinate in currentWindow
        # convert x,y to global coordinates in Screen
        # check if newX lies in range of currentWindow.X and currentWindow.width,
        # because they refer to Screen coordinates
        # check if the given x and y values lie with in the range of the window widget
        if 0 <= x <= self.width and 0 <= y <= self.height:
            return True
        else:
            return False

    # P2 2a
    def convertPositionToScreen(self, x, y):
        # check if the calling Window object is already the screen; return x, y unchanged
        if self.parentWindow is None and self.identifier == "SCREEN_1":
            return x, y
        # else if the calling Window object is not the screen
        else:
            # sum of x,y and origin of calling window in global coordinates
            convertedX = x + self.x
            convertedY = y + self.y
            return convertedX, convertedY

    # P2 2b
    def convertPositionFromScreen(self, x, y):
        # analog to the convertPositionToScreen
        if self.parentWindow is None and self.identifier == "SCREEN_1":
            return x, y
        else:
            # subtract global coordinates of calling window from x,y
            convertedX = x - self.x
            convertedY = y - self.y
            return convertedX, convertedY

    # P2 3b
    def draw(self, ctx):
        # translates the origin coordinates of the coordinate system for ctx
        # based on the global coordinates self.x and self.y
        ctx.setOrigin(self.x, self.y)

        # fill the area of the window on screen with the color specified in its backgroundColor property
        ctx.setFillColor(self.backgroundColor)

        # (0,0, ... , ...) - the first zeros refers to the top-left corner of the current window coordinate system
        ctx.fillRect(0, 0, self.width, self.height)

        if self.childWindows is not None:
            # parent window draws its child views
            for c in self.childWindows:
                c.draw(ctx)

    def handleMouseClicked(self, x, y):
        print("click")
        # print("Window " + self.identifier + " was clicked.")

    # P3 (7) Resizing windows and simple layout
    # Changes the position and size of the current window to the given parameters.
    def resize(self, x, y, width, height):
        if width < self.minWidth:
            width = self.minWidth
        if height < self.minHeight:
            height = self.minHeight
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def checkIfInTitleBar(self, givenX, givenY):
        convertedX, convertedY = self.convertPositionFromScreen(givenX, givenY)
        windowWidth = self.width
        windowHeight = self.height

        # (X1, Y1) of title bar
        titleBarX1 = 1
        titleBarY1 = 1

        # (X2, Y2) of title bar
        titleBarX2 = windowWidth
        titleBarY2 = 30

        if titleBarX1 <= convertedX <= titleBarX2 and titleBarY1 <= convertedY <= titleBarY2:
            return True
        else:
            return False


class Screen(Window):
    def __init__(self, windowSystem):
        super().__init__(0, 0, windowSystem.width, windowSystem.height, "SCREEN_1", 0)
        self.windowSystem = windowSystem

    # Override the draw method of your Screen to call your WindowManager wallpaper implementation
    # Call your WM’s decorateWindow implementation
    def draw(self, ctx):
        # super().draw(ctx)
        self.windowSystem.windowManager.drawDesktop(ctx)
        self.windowSystem.windowManager.drawTaskbar(ctx)
        if len(self.childWindows) > 0:
            for c in self.childWindows:
                if c.isHidden is False:
                    c.draw(ctx)
                    self.windowSystem.windowManager.decorateWindow(c, ctx)
                    if len(c.childWindows) > 0:
                        for gc in c.childWindows:
                            gc.draw(ctx)
                            self.windowSystem.windowManager.decorateWindow(gc, ctx)

    def resize(self, x, y, width, height):
        if len(self.childWindows) > 0:
            for c in self.childWindows:
                c.super().resize(x, y, width, height)

    def checkIfInTaskbar(self, givenX, givenY):
        # (X1, Y1) of taskbar
        taskBarX1 = 0
        taskBarY1 = self.height - 50

        # (X2, Y2) of taskbar
        taskBarX2 = self.width
        taskBarY2 = self.height

        if taskBarX1 <= givenX <= taskBarX2 and taskBarY1 <= givenY <= taskBarY2:
            return True
        else:
            return False

    def clickedTaskbarEvent(self, x, y):

        startX = 0
        startY = self.height - 50

        endX = 40
        endY = self.height

        if startX <= x <= endX and startY <= y <= endY:
            # this is when start button clicked
            print("milestone 4")

        else:
            startX = 40
            endX = 80

            for child in self.windowSystem.windowManager.openedTopLevelWindows:

                if startX <= x <= endX and startY <= y <= endY:

                    if child.isHidden:
                        child.isHidden = False
                        self.windowSystem.bringWindowToFront(child)
                        self.windowSystem.requestRepaint()

                    else:
                        child.isHidden = True
                        self.windowSystem.requestRepaint()

                    break
                else:
                    startX += 40
                    endX += 40
