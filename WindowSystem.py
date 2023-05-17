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
#from UITK import *


class WindowSystem(GraphicsEventSystem):

    # 1b
    def __init__(self, width, height):
        super().__init__(width, height)
        # P2 1b
        self.screen = None
        self.windowManager = None

        # variables for mouse events
        self.mousePressed = False
        self.recentX = 0
        self.recentY = 0
        self.lastClickedWindow = None
        self.dragging = False

    def start(self):
        # WINDOW MANAGER
        self.windowManager = WindowManager(self)

        # SCREEN (P2 1b)
        self.screen = Screen(self)

        # GRAY_WINDOW
        gray_window = self.createWindowOnScreen(20, 20, 400, 350, "Gray", COLOR_GRAY)

        # Child of GRAY_WINDOW
        self.createWindowInWindow(gray_window, 20, 20, 200, 250, "Red", COLOR_RED)

        # GREEN_WINDOW
        blue_window = self.createWindowOnScreen(100, 100, 400, 350, "Blue", COLOR_LIGHT_BLUE)

        # YELLOW_WINDOW
        yellow_window = self.createWindowOnScreen(300, 200, 400, 350, "Yellow", COLOR_ORANGE)

        purple_window1 = self.createWindowInWindow(yellow_window, 30, 40, 70, 50, "Purple1", COLOR_PURPLE)

        purple_window2 = self.createWindowInWindow(yellow_window, 30, 100, 70, 50, "Purple2", COLOR_PURPLE)

        purple_window3 = self.createWindowInWindow(yellow_window, 30, 160, 70, 50, "Purple3", COLOR_PURPLE)


        #testLabel = self.createWidgetOnWindow(30, 40, 120, 30, yellow_window, "Label on Yellow Window", "Hi i am here",COLOR_ORANGE, COLOR_BLACK, 'label')

        #testButton = self.createWidgetOnWindow(30, 70, 100, 30, yellow_window, "button in yellow window", "Button1",COLOR_GREEN, COLOR_PINK, 'button', print("hey"))

        # testButton = Button(200, 100, 100, 40, "Test Button")
        # blue_window.addChildWindow(testButton)

    """
    WINDOW MANAGEMENT
    """

    # P2 1c
    def createWindowOnScreen(self, x, y, width, height, identifier, backgroundColor):
        # creates a new window object with given parameters
        # depth is needed for the P2 4b
        newWindow = Window(x, y, width, height, identifier)
        # assign preset background color for new window object
        newWindow.backgroundColor = backgroundColor
        # add new window object to parent's list of window children
        self.screen.addChildWindow(newWindow)

        # add a window to the openedTopLevelList for the fixed order in the task bar
        self.windowManager.openWindow(newWindow)
        # self.widgetOrder.append(newWindow)

        return newWindow

    #TODO implement in WINDOW class
    def createWindowInWindow(self, parentWindow, childX, childY, childWidth, childHeight, childIdentifier, childBackgroundcolor):

        if parentWindow is not None:
            convertedX, convertedY = parentWindow.convertPositionToScreen(childX, childY)
            childWindow = Window(convertedX, convertedY, childWidth, childHeight, childIdentifier, parentWindow.depth + 1)
            childWindow.backgroundColor = childBackgroundcolor
            parentWindow.addChildWindow(childWindow)


        """
        def printSomething(self):
        print("Button1 pressed.")
        """


    """
    def createWidgetOnWindow(self, x, y, width, height, parentWindow, identifier, textString, textColor,
                             backgroundColor, widgetType, action=None):
        # create new widget object anhand des coordinates
        # global coordinates
        convertedX, convertedY = parentWindow.convertPositionToScreen(x, y)
        if widgetType == "label":
            newWidget = Label(convertedX, convertedY, x, y, width, height, identifier, textString, textColor, backgroundColor)
        elif widgetType == "button":
            newWidget = Button(convertedX, convertedY, x, y, width, height, identifier, textString, textColor, backgroundColor, action)

        parentWindow.addChildWindow(newWidget)
        return newWidget
        """

    # P2 1d
    def bringWindowToFront(self, window):
        # if window is a direct child of screen
        if window.parentWindow == self.screen:
            # remove it from the list of window children of the screen to prevent duplicates
            window.removeFromParentWindow()
            # append this window to the end of the child window list of the screen
            # so that it is the most visible window on the screen
            self.screen.addChildWindow(window)
        else:
            # else if window is not a direct child of screen
            # create new variable to iterate through the tree
            topLevelWindow = window
            # traverse the window tree upwards until the parent of TOPLEVELWINDOW is Screen
            while topLevelWindow.parentWindow.identifier != "SCREEN_1":
                topLevelWindow = topLevelWindow.parentWindow

            # remove TOPLEVELWINDOW from its parents list of window children
            topLevelWindow.removeFromParentWindow()
            # and readd it to the end of that list, so that it can be displayed in the front of the screen
            # in z-direction
            self.screen.addChildWindow(topLevelWindow)

    """
    DRAWING
    """

    # P2 3c
    # makes sure that the entire window tree is drawn upon creation
    def handlePaint(self):
        self.screen.draw(self.graphicsContext)

    """
    INPUT EVENTS
    """

    def handleMousePressed(self, x, y):
        # print(str(x) + "  " + str(y))
        self.dragging = False
        self.mousePressed = True
        self.recentX = x
        self.recentY = y
        clickedWindow = self.screen.childWindowAtLocation(x, y)

        if clickedWindow is not None:
            self.lastClickedWindow = clickedWindow
            self.bringWindowToFront(clickedWindow)
            self.requestRepaint()
            if clickedWindow.checkIfInTitleBar(self.recentX, self.recentY):
                # allow the user to drag the window
                self.dragging = True
            else:
                print("not title bar area")

        else:
            self.lastClickedWindow = self.screen
            if self.screen.checkIfInTaskbar(x, y):
                pass
                # self.screen.clickedTaskbarEvent(x,y)

    def handleMouseReleased(self, x, y):
        self.mousePressed = False

        # do not allow the user to dragg the window if mouse is released
        self.dragging = False

        if self.lastClickedWindow == self.screen:
            if self.lastClickedWindow.checkIfInTaskbar(x, y):
                self.screen.clickedTaskbarEvent(x, y)

        else:
            if self.lastClickedWindow.parentWindow == self.screen:
                # for close and minimizing
                if self.lastClickedWindow.checkIfInTitleBar(x, y) :
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
        # only toplevel windows should be moved, for that we make sure that parent is screen
        if self.lastClickedWindow is not None and self.lastClickedWindow.parentWindow == self.screen:
            if self.dragging:
                # difference between old and new (x,y) coordinates
                differenceX = x - self.recentX
                differenceY = y - self.recentY
                self.lastClickedWindow.x = self.lastClickedWindow.x + differenceX
                self.lastClickedWindow.y = self.lastClickedWindow.y + differenceY

                self.recentX = x
                self.recentY = y
                if self.windowManager.checkWindowPosition(self.lastClickedWindow, x, y):
                    self.requestRepaint()

    def handleKeyPressed(self, char):
        pass


# Let's start your window system!
w = WindowSystem(800, 600)
w.start()
