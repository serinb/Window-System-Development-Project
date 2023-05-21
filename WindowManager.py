#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Window System - Submission
by  Ulyana Lavnikevich (388633)
and Serin Bazzi (437585)
"""

from GraphicsEventSystem import *
from Window import *

class WindowManager:
    def __init__(self, windowSystem):
        self.windowSystem = windowSystem

        # title bar height for window decoration
        self.titleBarHeight = 30

        # screen boundaries
        # for window repositioning purposes
        self.screenTopBoundary = -15
        self.screenBottomBoundary = 559
        self.screenLeftBoundary = -100
        self.screenRightBoundary = 900

        # for taskbar
        # saves the order of the toplevel windows
        self.openedTopLevelWindows = []

    # called in createWindowOnScreen()
    # to help save the order in which the
    # top level windows were created
    # for the taskbar buttons to stay in same order
    def openWindow(self, window):
        self.openedTopLevelWindows.append(window)

    # P3 (1)
    # Add an instance of the WM to the window system
    def drawDesktop(self, ctx):
        # fill the screen with a nice color
        ctx.setFillColor("#fff")
        # your wallpaper should draw correctly even if the window system is created with a different screen size
        width, height = self.windowSystem.screen.width, self.windowSystem.screen.height
        ctx.fillRect(0, 0, width, height)

    # P3 (2)
    # adds the decorations to each top level window in screen
    def decorateWindow(self, window, ctx):
        # decoration for start menu
        if window.identifier == "Start Menu":
            # stroked border around the window
            ctx.setStrokeColor(COLOR_BLACK)
            ctx.setOrigin(window.x, window.y)
            ctx.strokeRect(0, 0, window.width, window.height)
            standardFont = Font(family="Helvetica", size=11, weight="bold")
            ctx.setFont(standardFont)

            # fills in the title bar color and adds identifier
            ctx.setFillColor("#D06929")
            ctx.fillRect(1, 1, window.width, self.titleBarHeight)
            ctx.drawString(window.identifier, 10, 7)

        # decoration for all toplevel windows except start menu
        # analog to above
        else:
            ctx.setStrokeColor(COLOR_BLACK)
            ctx.setOrigin(window.x, window.y)
            ctx.strokeRect(0, 0, window.width, window.height)
            standardFont = Font(family="Helvetica", size=11, weight="normal")
            ctx.setFont(standardFont)

            # we get the index of the most visible top level window
            lastIndex = len(self.windowSystem.screen.childWindows) - 1
            lastChild = self.windowSystem.screen.childWindows[lastIndex]

            veryLastChild = lastChild


            if veryLastChild == window:
                # visually discriminable orange titlebar for foreground window
                ctx.setFillColor("#D06929")

            else:
                # else gray colored titlebar
                ctx.setFillColor(COLOR_GRAY)

            # fills in the title bar color and adds identifier
            ctx.fillRect(1, 1, window.width, self.titleBarHeight)
            ctx.drawString(window.identifier, 10, 7)

            # closing Button
            ctx.drawString("X", window.width - 15, 7)

            # minimizing button
            ctx.drawLine(window.width - 40, 15, window.width - 33, 15)

            # resize Button
            ctx.setFillColor(COLOR_BLACK)
            ctx.strokeRect(window.width - 15, window.height - 15, window.width, window.height)

    # P3 (3)
    # for window repositioning purposes
    # checks if window lies within the preset boundaries of screen
    def checkWindowPosition(self, window, x, y, invalidSide):
        valid = True

        # for each boundary we check if window exceeds it
        # if so we return False
        # and register into the array invalidSide
        # which boundaries have been exceeded
        if self.screenTopBoundary > y:
            valid = False
            invalidSide.append("top")
        if y + window.height > self.screenBottomBoundary:
            valid = False
            invalidSide.append("bottom")
        if self.screenLeftBoundary > x:
            valid = False
            invalidSide.append("left")
        if x + window.width > self.screenRightBoundary:
            valid = False
            invalidSide.append("right")
        return valid

    # P3 (5)
    # for window repositioning purposes
    # performs the window dragging operation
    # on a window and all of its child windows
    def dragWindow(self, window, x, y):
        # window repositioning is for all toplevel windows except start menu
        if window.identifier != "Start_menu":

            # difference between old and new (x,y) coordinates of mouse cursor
            differenceX = x - self.windowSystem.recentX
            differenceY = y - self.windowSystem.recentY
            # new x,y coordinates w.r.t. calc. differnce
            newX = window.x + differenceX
            newY = window.y + differenceY

            # needed for checkWindowPosition()
            invalidSide = []

            # we save the local coordinates of windows children
            # for proper coordinate conversion
            # after repositioning
            childPostion = []
            if len(window.childWindows) > 0:
                for c in window.childWindows:
                    convertedX, convertedY = window.convertPositionFromScreen(c.x, c.y)
                    childPostion.append([convertedX, convertedY])

            # if no boundaries have been exceeded we update x,y coordinates of window
            if self.checkWindowPosition(window, newX, newY, invalidSide):
                # update origin x,y for children of lastClickedWindow
                window.x = newX
                window.y = newY

            # else we make adjustments to x,y
            # to make sure that window is not dragged outside of the boundaries
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

            # we convert the local coordinates of window's children to global coordinates
            if len(window.childWindows) > 0:
                for c in window.childWindows:
                    c.x, c.y = window.convertPositionToScreen(childPostion[window.childWindows.index(c)][0],
                                                              childPostion[window.childWindows.index(c)][1])

            # we update the recent cursor position
            self.windowSystem.recentX = x
            self.windowSystem.recentY = y
            # and repaint the screen after change
            self.windowSystem.requestRepaint()


    # P3 (5)
    # for window minimizing purposes
    def minimizeWindow(self, window):
        # for all top level windows except start menu
        if window.identifier != "Start Menu":
            # flip the hidden flag to true and repaint
            # to make window invisible
            window.isHidden = True
            self.windowSystem.requestRepaint()

    # P3 (5)
    # for window closing purposes
    def closeWindow(self, window):
        # for all top level windows except start menu
        if window.identifier != "Start_menu":
            # flip the close flag to true
            window.isClosed = True
            # remove self from window tree
            window.removeFromParentWindow()
            # and from taskbar button list
            self.openedTopLevelWindows.remove(window)
            # set as invisible
            window.isHidden = True
            # request repaint
            self.windowSystem.requestRepaint()


    # P3 (6) Task bar
    # decorates the screens taskbar and the buttons inside of it
    def drawTaskbar(self, ctx):
        # grayish fill for the entire taskbar
        ctx.setFillColor("#35393C")
        ctx.fillRect(0, self.windowSystem.screen.height - 40, self.windowSystem.screen.width,
                     self.windowSystem.screen.height)
        # filling the start button to make it distinguishable from the other buttons
        ctx.setFillColor("#D06929")
        ctx.fillRect(4, self.windowSystem.screen.height - 38, 114,
                     self.windowSystem.screen.height - 4)

        # adding a stroke to the entire taskbar
        ctx.setStrokeColor(COLOR_BLACK)
        font = Font(family="Helvetica", size=11, weight="bold")
        ctx.setFont(font)
        ctx.strokeRect(0, self.windowSystem.screen.height - 40, self.windowSystem.screen.width,
                       self.windowSystem.screen.height)

        # adding in the buttons for the apps
        if len(self.windowSystem.screen.childWindows) > 0:
            # get index of most visible window to make it distinguishable from the other windows
            lastIndex = len(self.windowSystem.screen.childWindows) - 1
            lastChild = self.windowSystem.screen.childWindows[lastIndex]

            # define offset to start drawing the next child of the screen at the offset location
            offset = 4
            for c in self.openedTopLevelWindows:
                # case for visible last child
                if lastChild == c and lastChild.isHidden == False:
                    if c.identifier == "Start Menu":
                        # gray stroke for start menu button
                        ctx.setStrokeColor("#35393C")
                    else:
                        # orange stroke for start menu button
                        ctx.setStrokeColor("#D06929")
                else:
                    # else white stroke
                    ctx.setStrokeColor(COLOR_WHITE)
                if not c.isClosed:
                    # for all windows that are not closed
                    # adjust the stroke of and text for their taskbar button
                    ctx.strokeRect(0 + offset, self.windowSystem.screen.height - 38, 110 + offset,
                                   self.windowSystem.screen.height - 4)
                    ctx.drawString(c.identifier, 10 + offset, self.windowSystem.screen.height - 28)
                    offset += 114


    # P3 (7)
    # for resizing window purposes
    def resizeWindow(self, window, x, y):
        # x,y are global coordinates and are supposed to be windows new width and height
        if window.parentWindow == self.windowSystem.screen:
            # so we convert them to local coordinates of window
            newWidth, newHeight = window.convertPositionFromScreen(x, y)
            # and call the resize() method on window, to resize it and perform layout on its child windows
            window.resize(window.x, window.y, newWidth, newHeight)
            # we make sure that the window is resized upto the visible boundaries of the screen
            if window.x + newWidth <= self.windowSystem.screen.width and window.y + newHeight <= self.windowSystem.screen.height - 40:
                # if so, we repaint
                self.windowSystem.requestRepaint()
