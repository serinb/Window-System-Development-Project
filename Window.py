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
        # assign self as the parent of new child window
        window.parentWindow = self
        # add child window to self's list of window children, provided it does not yet exist in list
        if window not in self.childWindows:
            self.childWindows.append(window)

    def createWindowInWindow(self, childX, childY, childWidth, childHeight, childIdentifier,
                             childBackgroundColor):
        #child should not appear behind the taskbar
        offsetTitleBar = 30
        if childY <= offsetTitleBar:
            childY += offsetTitleBar
        #child should stay within left-right-bottom margin
        margin = 16
        #check left margin
        if childX <= margin:
            childX += margin
        #check bottom margin
        if childX + childWidth > self.width:
            childWidth = childWidth - (childWidth + childX - self.width) - margin
        if childY + childHeight > self.height:
            childHeight = childHeight - (childHeight - childY - self.height) - margin

        convertedX, convertedY = self.convertPositionToScreen(childX, childY)
        childWindow = Window(convertedX, convertedY, childWidth, childHeight, childIdentifier,
                             self.depth + 1)
        childWindow.backgroundColor = childBackgroundColor
        self.addChildWindow(childWindow)

    # P2 1a
    def removeFromParentWindow(self):
        # provided that self has a parent
        if self.parentWindow:
            # delete self from its parent's list of window children
            self.parentWindow.childWindows.remove(self)
            # and delete self's parent
            self.parentWindow = None

    # P2 2a
    def convertPositionToScreen(self, x, y):
        # check if the calling Window object is already the screen
        # if so, return x, y unchanged as they are the global coordinates
        if self.parentWindow is None and self.identifier == "SCREEN_1":
            return x, y
        # else if the calling Window object is not the screen
        else:
            # sum of x,y and origin of calling window's offset in global coordinates
            convertedX = x + self.x
            convertedY = y + self.y
            return convertedX, convertedY

    # P2 2b
    def convertPositionFromScreen(self, x, y):
        # analog to the convertPositionToScreen
        if self.parentWindow is None and self.identifier == "SCREEN_1":
            return x, y
        else:
            # subtract calling window's offset in global coordinates from x,y
            convertedX = x - self.x
            convertedY = y - self.y
            return convertedX, convertedY

    # P2 3b
    def draw(self, ctx, drawingWidth, drawingHeight):
        # translates the origin coordinates of the coordinate system for ctx
        # based on the global coordinates self.x and self.y
        ctx.setOrigin(self.x, self.y)

        # fill the area of the window on screen with the color specified in its backgroundColor property
        ctx.setFillColor(self.backgroundColor)

        # (0,0, ... , ...) - the first zeros refers to the top-left corner of the current window coordinate system
        ctx.fillRect(0, 0, drawingWidth, drawingHeight)

        # call the draw function on calling window objects children
        if self.childWindows is not None:
            # parent window draws its child views
            for c in self.childWindows:
                #calculate the deepest x,y coordinate of child inside of parent coordinate system
                inParentX, inParentY = self.convertPositionFromScreen(c.x,c.y)
                margin = 16
                deepestX = inParentX + c.width
                deepestY = inParentY + c.height
                drawingWidth = c.width
                drawingHeight = c.height
                if deepestX > self.width - margin:
                    drawingWidth = c.width - (c.width + inParentX - self.width) - margin
                if deepestY > self.height - margin:
                    drawingHeight = c.height - (c.height + inParentY - self.height) - margin
                print(str(drawingWidth) + " " + str(drawingHeight))
                c.draw(ctx, drawingWidth, drawingHeight)

    # P2 4a
    def hitTest(self, x, y):
        # checks whether the given x,y lie within the calling windows local coordinate system
        # x,y-axis maxima are represented by the windows witdh and height
        if 0 <= x <= self.width and 0 <= y <= self.height:
            return True
        else:
            return False


    def childWindowAtLocation2(self, x, y):
        currentWindow = self

        #calling window has to have child window to return output that is not None
        if len(currentWindow.childWindows) > 0:
            #get child on the far right in window tree, as it is the visible one (highest z-index)
            lastIndex = len(currentWindow.childWindows)-1
            lastChild = currentWindow.childWindows[lastIndex]

            #convert x,y w.r.t lastchild coordinate system
            newX, newY = currentWindow.convertPositionToScreen(x,y)
            resX, resY = lastChild.convertPositionFromScreen(newX, newY)

            # CASE 1: calling Window has no grandchild
            # in this case we return calling windows direct child
            if len(lastChild.childWindows) == 0 and lastChild.hitTest(resX,resY):
                return lastChild

            # CASE 2: calling Window has grandchild
            # We need to check if hitTest TRUE for grandchild
            # if so we do recursive call on child
            elif len(lastChild.childWindows) >= 1 and lastChild.hitTest(resX,resY):
                #get grandchild on far right in Window Tree
                lastLastIndex = len(lastChild.childWindows)-1
                lastGrandchild = lastChild.childWindows[lastLastIndex]
                #convert x,y coordinates w.r.t grandchild coordinate system
                newResX, newResY = lastGrandchild.convertPositionFromScreen(newX, newY)
                #if hitTest on grandchild is TRUE do recursive call on lastchild
                if lastGrandchild.hitTest(newResX, newResY):
                    return lastChild.childWindowAtLocation(resX, resY)
                #else return lastchild as the deepest visible descendant window
                else:
                    return lastChild
            # no visible child at position x,y
            else:
                return None
        else:
            None

    # P2 4b
    def childWindowAtLocation(self, x, y):
        # only works if calling window has children, else returns 0
        if len(self.childWindows) > 0:
            recentHitTestStatus = None
            recentHitTestDepth = 0
            # in a nutshell the tree is traversed from right to left and the deepest most visible child window is returned
            # recentHitTestDepth refers to the most recent window object with a positive Hittest result
            # recentHittest Depth represents its depth
            depth, deepestChild = self.helperFunction(x, y, recentHitTestStatus, recentHitTestDepth)

            if deepestChild is not None:
                return deepestChild
            else:
                return None
        else:
            return None

    # P2 4b -helper function
    def helperFunction(self, x, y, recentHitTestStatus, recentHitTestDepth):
        # traverse childWindows Array right->left
        for child in reversed(self.childWindows):

            # this condition holds true when the recent window with positive hittest has no children
            # this way we know that there is no child deeper in the tree (more visible) than it, so we return it
            if (recentHitTestStatus is not None) and (len(recentHitTestStatus.childWindows) == 0):
                return recentHitTestDepth, recentHitTestStatus

            # coordinate conversion w.r.t child inorder to correctly perform the hittest
            newX, newY = self.convertPositionToScreen(x, y)
            convertedX, convertedY = child.convertPositionFromScreen(newX, newY)

            # this condition holds true when the current childs hittest is positive for the very first iteration
            if (child.hitTest(convertedX, convertedY)) and (recentHitTestStatus is None):
                # we assign our placeholders (see ChildWindowAtLocation) with current window
                recentHitTestStatus = child
                recentHitTestDepth = child.depth

            # for a positive hittest here we undergo a case distinction
            elif (child.hitTest(convertedX, convertedY)) and (recentHitTestStatus is not None):
                # if child has the most visible top level window parent
                if child.compareTopLevelWindows(recentHitTestStatus) == child:
                    # we assign our placeholders (see ChildWindowAtLocation) with current window
                    recentHitTestStatus = child
                    recentHitTestDepth = child.depth

                # if both child and reventHittestStatus have the same toplevel window parent, check that child's depth in the tree
                # is greater or equal to the recentHittestStatus
                elif (child.compareTopLevelWindows(recentHitTestStatus) == 0) and (
                        child.depth >= recentHitTestDepth):
                    # we assign our placeholders (see ChildWindowAtLocation) with current window
                    recentHitTestStatus = child
                    recentHitTestDepth = child.depth

            # we proceed by recursively calling the helperfunction provided the current child has children
            if (child.hitTest(convertedX, convertedY)) and len(child.childWindows) > 0:
                recentHitTestDepth, recentHitTestStatus = child.helperFunction(convertedX, convertedY,
                                                                               recentHitTestStatus,
                                                                               recentHitTestDepth)

        return recentHitTestDepth, recentHitTestStatus

    # P2 4b -helper function: checks the order of the respective toplevel windows of two window objects
    def compareTopLevelWindows(self, window):
        # calling Window
        topLevelWindow1 = self.getTopLevelWindow()
        # parameter window
        topLevelWindow2 = window.getTopLevelWindow()

        screen = topLevelWindow1.parentWindow

        # if calling window has a more visible parent toplevel window, return calling window
        if screen.childWindows.index(topLevelWindow1) > screen.childWindows.index(topLevelWindow2):
            return self
        # else if parameter window has a more visible parent toplevel window, return parameter window
        elif screen.childWindows.index(topLevelWindow1) < screen.childWindows.index(topLevelWindow2):
            return window
        # else if both windows have the same toplevel window, return 0
        elif screen.childWindows.index(topLevelWindow1) == screen.childWindows.index(topLevelWindow2):
            return 0

    # P2 4b -helper function: returns the toplevel window of a calling window object
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


    # P2 4d
    def handleMouseClicked(self, x, y):
        print("click")

    # P3 (7) Resizing windows and simple layout
    # Changes the position and size of the current window to the given parameters
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

    def checkIfInResizingArea(self, givenX, givenY):
        convertedX, convertedY = self.convertPositionFromScreen(givenX, givenY)
        resizeX1 = self.width - 15
        resizeY1 = self.height - 15

        resizeX2 = self.width
        resizeY2 = self.height

        if resizeX1 <= convertedX <= resizeX2 and resizeY1 <= convertedY <= resizeY2:
            return True
        else:
            return False


class Screen(Window):
    def __init__(self, windowSystem):
        super().__init__(0, 0, windowSystem.width, windowSystem.height, "SCREEN_1", 0)
        self.windowSystem = windowSystem

    # Override the draw method of your Screen to call your WindowManager wallpaper implementation
    # Call your WM’s decorateWindow implementation
    def draw(self, ctx, drawingWidth, drawingHeight):
        # super().draw(ctx)
        self.windowSystem.windowManager.drawDesktop(ctx)
        self.windowSystem.windowManager.drawTaskbar(ctx)
        if len(self.childWindows) > 0:
            for c in self.childWindows:
                if c.isHidden is False:
                    drawingWidth = c.width
                    drawingHeight = c.height
                    c.draw(ctx, drawingWidth, drawingHeight)
                    if c.depth == 1:
                        self.windowSystem.windowManager.decorateWindow(c, ctx)
                        # if len(c.childWindows) > 0:
                        #     for gc in c.childWindows:
                        #         gc.draw(ctx)
                        # self.windowSystem.windowManager.decorateWindow(gc, ctx)

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
            # helloworld, calculator, color slider
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
