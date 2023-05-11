#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Window System - Submission
by  Ulyana Lavnikevich (388633)
and Serin Bazzi (437585)
"""

from GraphicsEventSystem import *
from Window import *
from WindowManager import *


class WindowSystem(GraphicsEventSystem):

    # 1b
    def __init__(self, width, height):
        super().__init__(width, height)
        self.screen = None
        self.windowManager = None

        # variables for mouse events
        self.mousePressed = False
        self.recentX = 0
        self.recentY = 0
        self.lastClickedWindow = None

    def start(self):
        self.windowManager = WindowManager(self)
        # SCREEN
        self.screen = Screen(self)

        # WHITE_WINDOW
        white_window = self.createWindowOnScreen(20, 20, 400, 400, "White", self.screen, COLOR_WHITE)

        # GREEN_WINDOW
        green_window = self.createWindowOnScreen(100, 100, 300, 300, "Green", self.screen, COLOR_GREEN)

        # YELLOW_WINDOW
        yellow_window = self.createWindowOnScreen(500, 400, 160, 150, "Yellow", self.screen, COLOR_YELLOW)

        blue_window = self.createWindowOnScreen(30, 30, 160, 150, "Blue", green_window, COLOR_BLUE)

    """
    WINDOW MANAGEMENT
    """

    # 1c
    def createWindowOnScreen(self, x, y, width, height, identifier, parentWindow, backgroundColor):

        if parentWindow is not None:
            newWindow = Window(x, y, width, height, identifier, parentWindow.depth + 1)
            parentWindow.addChildWindow(newWindow)
            # self.widgetOrder.append(newWindow)
        else:
            newWindow = Screen(self)

        newWindow.backgroundColor = backgroundColor

        return newWindow

    # 1d
    def bringWindowToFront(self, window):
        # if window is a direct child of screen
        if window.parentWindow.identifier == "SCREEN_1":
            # remove from the children list of the screen to prevent the duplicates
            window.removeFromParentWindow()
            #  append this window to the end of the child window list of the screen
            self.screen.addChildWindow(window)
        else:
            # else if window is not a direct child of screen
            # create new variable to iterate through the tree
            topLevelWindow = window
            # traverse the window tree upwards until the parent of the window is "screen"
            # meaning until the toplevelwindow on the path of window is found
            while topLevelWindow.parentWindow.identifier != "SCREEN_1":
                topLevelWindow = topLevelWindow.parentWindow

            # add the top level window to the end of the list of children of screen
            topLevelWindow.removeFromParentWindow()
            self.screen.addChildWindow(topLevelWindow)

    """
    DRAWING
    """

    # P2 3c
    def handlePaint(self):
        self.screen.draw(self.graphicsContext)

    """
    INPUT EVENTS
    """

    def handleMousePressed(self, x, y):
        # print(str(x) + "  " + str(y))
        self.mousePressed = True
        self.recentX = x
        self.recentY = y
        clickedWindow = self.screen.childWindowAtLocation(x, y)

        if clickedWindow is not None:
            self.lastClickedWindow = clickedWindow
            self.bringWindowToFront(clickedWindow)
            self.requestRepaint()
            if clickedWindow.checkIfInTitleBar(self.recentX, self.recentY):
                print("title bar area")
            else:
                print("not title bar area")

        else:
            self.lastClickedWindow = self.screen
            if self.screen.checkIfInTaskbar(x, y):
                pass
                # self.screen.clickedTaskbarEvent(x,y)

    def handleMouseReleased(self, x, y):
        self.mousePressed = False

        if self.lastClickedWindow == self.screen:
            if self.lastClickedWindow.checkIfInTaskbar(x, y):
                self.screen.clickedTaskbarEvent(x, y)

        else:
            # for close and minimizing
            if self.lastClickedWindow.checkIfInTitleBar(x, y):
                convertedX, convertedY = self.lastClickedWindow.convertPositionFromScreen(x, y)

                # defining regions for close and minimizing
                # (X1, Y1) of close button
                closeX1 = self.lastClickedWindow.width - 29
                closeY1 = 0

                # (X2, Y2) of close button
                closeX2 = self.lastClickedWindow.width
                closeY2 = 30

                # (X1, Y1) of minimize button
                minimizeX1 = self.lastClickedWindow.width - 43
                minimizeY1 = 0

                # (X2, Y2) of minimize button
                minimizeX2 = self.lastClickedWindow.width - 30
                minimizeY2 = 30

                # closing
                if closeX1 <= convertedX <= closeX2 and closeY1 <= convertedY <= closeY2:
                    self.windowManager.closeWindow(self.lastClickedWindow)

                # minimizing
                if minimizeX1 <= convertedX <= minimizeX2 and minimizeY1 <= convertedY <= minimizeY2:
                    self.windowManager.minimizeWindow(self.lastClickedWindow)

            if self.lastClickedWindow == self.screen.childWindowAtLocation(x, y):
                self.lastClickedWindow.handleMouseClicked(x, y)

    def handleMouseMoved(self, x, y):
        pass

    def handleMouseDragged(self, x, y):
        pass

    def handleKeyPressed(self, char):
        pass


# Let's start your window system!
w = WindowSystem(800, 600)
w.start()
