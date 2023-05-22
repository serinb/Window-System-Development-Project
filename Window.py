# !/usr/bin/env python3
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
LayoutAnchor = AllAnchors(1 << 0, 1 << 1, 1 << 2, 1 << 3)


class Window:
    def __init__(self, originX, originY, width, height, identifier, anchoring, minWidth, minHeight, depth=1):
        self.x = originX
        self.y = originY
        self.width = width
        self.height = height
        self.identifier = identifier
        self.depth = depth
        self.backgroundColor = COLOR_LIGHT_GRAY
        self.childWindows = []
        self.parentWindow = None

        # P3 (5) flags for minimizing and closing window
        self.isHidden = True
        self.isClosed = False

        # P3 (7) for resizing window
        self.layoutAnchors = anchoring
        self.minWidth = minWidth
        self.minHeight = minHeight

        # window padding to make sure that
        # children stay within window boundaries
        self.paddingTop = 45
        self.paddingLeft = 16
        self.paddingBottom = 16
        self.paddingRight = 16

    # P2 1a adds window to self's list of children
    def addChildWindow(self, window):
        # assign self as the parent of new child window
        window.parentWindow = self
        # add child window to self's list of window children,
        # provided it does not yet exist in list
        if window not in self.childWindows:
            self.childWindows.append(window)

    # P2 1a removes self's parent window
    def removeFromParentWindow(self):
        # provided that self has a parent
        if self.parentWindow:
            # delete self from its parent's list of window children
            self.parentWindow.childWindows.remove(self)
            # and delete self's parent
            self.parentWindow = None

    # P2 2a converts x,y from local coordinates (w.r.t to self) to global coordinates
    def convertPositionToScreen(self, x, y):
        # check if the self is already the screen
        # if so, return x, y unchanged as they are the global coordinates
        if self.parentWindow is None and self.identifier == "SCREEN_1":
            return x, y
        # else if self is not the screen
        else:
            # sum of x,y and origin of self's offset in global coordinates
            convertedX = x + self.x
            convertedY = y + self.y
            return convertedX, convertedY

    # P2 2b converts x.y from global coordinates to local coordinates (w.r.t self)
    def convertPositionFromScreen(self, x, y):
        # analog to the convertPositionToScreen
        if self.parentWindow is None and self.identifier == "SCREEN_1":
            return x, y
        else:
            # subtract calling window's offset in global coordinates from x,y
            convertedX = x - self.x
            convertedY = y - self.y
            return convertedX, convertedY

    # P2 3b draws a window onto the screen
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
                # calculate the deepest x,y coordinate of child inside of parent coordinate system
                inParentX, inParentY = self.convertPositionFromScreen(c.x, c.y)
                c.draw(ctx, c.width, c.height)

    # P2 4a checks whether there exists a window at a given x,y position
    def hitTest(self, x, y):
        # checks whether the given x,y lie within the calling windows local coordinate system
        # x,y-axis maxima are represented by the windows witdh and height
        if 0 <= x <= self.width and 0 <= y <= self.height:
            return True
        else:
            return False

    # P2 4b returns deepest most visible child window at a given x,y position
    def childWindowAtLocation(self, x, y):
        # only works if calling window has children, else returns 0
        if len(self.childWindows) > 0:
            recentHitTestStatus = None
            recentHitTestDepth = 0
            # in a nutshell the tree is traversed from right to left and the deepest most visible child window is
            # returned recentHitTestDepth refers to the most recent window object with a positive Hittest result
            # recentHittest Depth represents its depth
            depth, deepestChild = self.helperFunction(x, y, recentHitTestStatus, recentHitTestDepth)

            if deepestChild is not None:
                return deepestChild
            else:
                return None
        else:
            return None

    # P2 4b - helper function
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

                # if both child and reventHittestStatus have the same toplevel window parent, check that child's
                # depth in the tree is greater or equal to the recentHittestStatus
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

    # P2 4b - helper function: checks the order of the respective toplevel windows of two window objects
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

    # P2 4b - helper function: returns the toplevel window of a calling window object
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
    def resize(self, x, y, newWidth, newHeight):

        # needed for layout calculation
        oldY = self.y
        oldWidth, oldHeight = self.width, self.height
        # make sure that the window is not resized
        # to size smaller than minimum width and height
        if newWidth <= self.minWidth:
            newWidth = self.minWidth
        if newHeight <= self.minHeight:
            newHeight = self.minHeight
        self.width = newWidth
        self.height = newHeight
        self.x = x
        self.y = y

        if self.childWindows is not None:

            for c in self.childWindows:

                # TOP RIGHT BOTTOM LEFT
                # window changes width and height size, so that distance to all 4 sides of parent stay the same
                if c.layoutAnchors & LayoutAnchor.top and c.layoutAnchors & LayoutAnchor.right and c.layoutAnchors & LayoutAnchor.bottom and c.layoutAnchors & LayoutAnchor.left:
                    # to keep distance to left and right edge of parent the same
                    # we adjust the width of the window
                    childGreatestX = c.width + c.x
                    rightDistanceChildParent = oldWidth - childGreatestX
                    newChildGreatestX = self.width - rightDistanceChildParent
                    childSmallestX = c.x
                    newChildWidth = newChildGreatestX - childSmallestX
                    c.width = newChildWidth

                    # analog to above we also adjust the height of the window
                    # w.r.t to its distance to the bottom edge of parent window
                    childGreatestY = c.y + c.height
                    bottomDistanceChildParent = oldHeight - childGreatestY
                    newChildGreatestY = self.height - bottomDistanceChildParent
                    newChildHeight = newChildGreatestY - c.y
                    c.height = newChildHeight

                    # no need to calculate the distance to the top edge, as window stays put by default

                # TOP RIGHT LEFT
                # window changes width size, so that its distance to top, left, right of parent stay the same
                elif c.layoutAnchors & LayoutAnchor.top and c.layoutAnchors & LayoutAnchor.right and c.layoutAnchors & LayoutAnchor.left:
                    # anolog to the above case we adjust the width of the window
                    # height is not changed, as there is no anchor in bottom
                    childGreatestX = c.width + c.x
                    rightDistanceChildParent = oldWidth - childGreatestX
                    newChildGreatestX = self.width - rightDistanceChildParent
                    childSmallestX = c.x
                    newChildWidth = newChildGreatestX - childSmallestX
                    c.width = newChildWidth

                # TOP RIGHT
                # size of window stays the same
                # distance to top and right of parent stays the same
                # approach analog to cases above
                elif c.layoutAnchors & LayoutAnchor.top and c.layoutAnchors & LayoutAnchor.right:
                    childGreatestX = c.width + c.x
                    rightDistanceChildParent = oldWidth - childGreatestX
                    newChildGreatestX = self.width - rightDistanceChildParent
                    newChildX = newChildGreatestX - c.width
                    c.x = newChildX

                # TOP
                # allows a window to slide horizontally with respect to the width of the parent window
                # while being anchorred to top
                elif c.layoutAnchors & LayoutAnchor.top:
                    # calculate the y coordinate of child in local coordinates of parent
                    localY = c.y - oldY
                    # middle of parent window width
                    parentMiddle = self.width / 2
                    # middle of child window width
                    childMiddle = c.width / 2
                    # new x allows for child window to be centered within its parent
                    newX = parentMiddle - childMiddle
                    c.x, c.y = self.convertPositionToScreen(newX, localY)

                # BOTTOM RIGHT LEFT
                # analog top,left,right only that window is anchored to bottom instead of top
                elif c.layoutAnchors & LayoutAnchor.bottom and c.layoutAnchors & LayoutAnchor.left and c.layoutAnchors & LayoutAnchor.right:
                    childGreatestX = c.width + c.x
                    rightDistanceChildParent = oldWidth - childGreatestX
                    newChildGreatestX = self.width - rightDistanceChildParent
                    childSmallestX = c.x
                    newChildWidth = newChildGreatestX - childSmallestX
                    c.width = newChildWidth

                    childGreatestY = c.y + c.height
                    bottomDistanceChildParent = oldHeight - childGreatestY
                    newChildGreatestY = self.height - bottomDistanceChildParent
                    childSmallestY = newChildGreatestY - c.height
                    c.y = childSmallestY

                # BOTTOM LEFT
                # analog top,left only that window is anchored to bottom instead of top
                elif c.layoutAnchors & LayoutAnchor.bottom and c.layoutAnchors & LayoutAnchor.left:
                    childGreatestY = c.y + c.height
                    bottomDistanceChildParent = oldHeight - childGreatestY
                    newChildGreatestY = self.height - bottomDistanceChildParent
                    childSmallestY = newChildGreatestY - c.height
                    c.y = childSmallestY

                # BOTTTOM RIGHT
                # analog top,left only that window is anchored to bottom instead of top
                elif c.layoutAnchors & LayoutAnchor.bottom and c.layoutAnchors & LayoutAnchor.right:
                    childGreatestX = c.x + c.width
                    rightDistanceChildParent = oldWidth - childGreatestX

                    newChildGreatestX = self.width - rightDistanceChildParent
                    childSmallestX = newChildGreatestX - c.width
                    c.x = childSmallestX

                    childGreatestY = c.y + c.height
                    bottomDistanceChildParent = oldHeight - childGreatestY

                    newChildGreatestY = self.height - bottomDistanceChildParent
                    childSmallestY = newChildGreatestY - c.height
                    c.y = childSmallestY

                # BOTTOM (analog to top)
                # allows a window to slide horizontally with respect to the width of the parent window
                # while being anchorred to top
                elif c.layoutAnchors & LayoutAnchor.bottom:
                    childGreatestY = c.y + c.height
                    bottomDistanceChildParent = oldHeight - childGreatestY
                    newChildGreatestY = self.height - bottomDistanceChildParent
                    childSmallestY = newChildGreatestY - c.height
                    c.y = childSmallestY

                    localY = c.y - oldY
                    parentMiddle = self.width / 2
                    childMiddle = c.width / 2
                    newX = parentMiddle - childMiddle
                    convertedX, convertedY = self.convertPositionToScreen(newX, localY)
                    c.x = convertedX

    # checks if a given position lies in the titlebar
    # helpful for closing, minimizing, repositioning window
    def checkIfInTitleBar(self, x, y):
        # convert x,y to local coordinates of self for easy titlebar boundary control
        convertedX, convertedY = self.convertPositionFromScreen(x, y)
        windowWidth = self.width

        # Starting (X1, Y1) of title bar
        titleBarX1 = 1
        titleBarY1 = 1

        # Ending (X2, Y2) of title bar
        titleBarX2 = windowWidth
        titleBarY2 = 30

        # check that converted x,y lie within boundaries of titlebar
        if titleBarX1 <= convertedX <= titleBarX2 and titleBarY1 <= convertedY <= titleBarY2:
            return True
        else:
            return False

    # checks if a given position lies in the
    # close button area of a window's title bar
    # analog to checkIfInTitleBar()
    def checkIfInCloseButton(self, x, y):
        if self.checkIfInTitleBar(x, y):
            convertedX, convertedY = self.convertPositionFromScreen(x, y)

            # Starting (X1, Y1) of close button
            closeX1 = self.width - 29
            closeY1 = 0

            # Ending (X2, Y2) of close button
            closeX2 = self.width
            closeY2 = 30

            if closeX1 <= convertedX <= closeX2 and closeY1 <= convertedY <= closeY2:
                return True
            else:
                return False

    # checks if a given position lies in the
    # minimizing button area of a window's title bar
    # analog to checkIfInCloseButton()
    def checkIfInMinimizeButton(self, x, y):
        if self.checkIfInTitleBar(x, y) and self.identifier != "Start Menu":
            convertedX, convertedY = self.convertPositionFromScreen(x, y)

            # Starting (X1, Y1) of minimize button
            minimizeX1 = self.width - 43
            minimizeY1 = 0

            # Ending (X2, Y2) of minimize button
            minimizeX2 = self.width - 30
            minimizeY2 = 30

            if minimizeX1 <= convertedX <= minimizeX2 and minimizeY1 <= convertedY <= minimizeY2:
                return True
            else:
                return False

    # check if a given position lies in the
    # bottom right corner of a window
    # for window resizing purposes
    # analog to above
    def checkIfInResizingArea(self, x, y):
        if self.identifier != "Start_menu":
            convertedX, convertedY = self.convertPositionFromScreen(x, y)
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
        super().__init__(0, 0, windowSystem.width, windowSystem.height, "SCREEN_1", windowSystem.width,
                         windowSystem.height, 0)
        self.windowSystem = windowSystem

    # calls functions necessary to draw the desktop, taskbar
    # and all of screens child windows and their decorations
    def draw(self, ctx, drawingWidth, drawingHeight):
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

    # checks if a given position is in the
    # taskbar area of screen
    # for taskbar event purposes
    # analog to check function in Window
    def checkIfInTaskbar(self, x, y):
        # (X1, Y1) of taskbar
        taskBarX1 = 0
        taskBarY1 = self.height - 50
        # (X2, Y2) of taskbar
        taskBarX2 = self.width
        taskBarY2 = self.height

        if taskBarX1 <= x <= taskBarX2 and taskBarY1 <= y <= taskBarY2:
            return True
        else:
            return False

    # for task event purposes
    # assigns Windows minimizing event to buttons
    # in taskbar
    def clickedTaskbarEvent(self, x, y):
        # Starting (X1,X2)
        startX = 4
        startY = self.height - 40
        # Ending (X1,X2)
        endX = 114
        endY = self.height

        # goes through all toplevel windows in screen
        for child in self.windowSystem.windowManager.openedTopLevelWindows:
            # checks if x,y lie inside assigned button of window in taskbar
            if startX <= x <= endX and startY <= y <= endY:
                # if window is minimized (not visible)
                # its hidden flag is flipped and screen is repainted
                # to make the window visible again
                if child.isHidden:
                    child.isHidden = False
                    self.windowSystem.bringWindowToFront(child)
                    self.windowSystem.requestRepaint()
                # otherwise hidden flag is flipped
                # and screen is repainted to make
                # window disappear
                else:
                    child.isHidden = True
                    self.windowSystem.requestRepaint()
                break
            else:
                # increments
                startX += 114
                endX += 114
