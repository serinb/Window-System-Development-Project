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
from UITK import *
import HelloWorldRevised
import Calculator


class WindowSystem(GraphicsEventSystem):

    # 1b
    def __init__(self, width, height):
        super().__init__(width, height)
        # P2 1b
        self.screen = None
        self.windowManager = None
        self.helloWorld = None
        self.calculator = None
        self.start_menu = None

        # variables for mouse events
        self.mousePressed = False
        self.recentX = 0
        self.recentY = 0
        self.lastClickedWindow = None
        self.lastClickedButton = None
        self.allowDragging = False
        self.allowResizing = False
        self.startMenuAcive = False

    def start(self):
        # WINDOW MANAGER
        self.windowManager = WindowManager(self)

        # SCREEN (P2 1b)
        self.screen = Screen(self)
        self.mousePressed = False
        self.recentX = 0
        self.recentY = 0
        self.lastClickedWindow = None
        self.lastClickedButton = None
        self.allowDragging = False
        self.allowResizing = False
        self.startMenuAcive = False


        self.start_menu = self.createWindowOnScreen(0, 550 - 200, 200, 200, "Start_menu", COLOR_BLUE, 200, 200)

        self.helloWorld = HelloWorldRevised.HelloWorld(self)

        #self.calculator = Calculator.CalculatorApplication(self)





        # yo.window = self.createWindowOnScreen(20, 20, 200, 200, "HelloWorld", COLOR_PINK)

        # GRAY_WINDOW
        #gray_window = self.createWindowOnScreen(30, 20, 400, 500, "Gray", COLOR_GRAY, 200, 200)

        # Child of GRAY_WINDOW
        #redWindow = gray_window.createWindowInWindow(5, 201, 401, 300, "Red", COLOR_RED,  50, 50, LayoutAnchor.top | LayoutAnchor.left)
        # GREEN_WINDOW
        #blue_window = self.createWindowOnScreen(100, 100, 400, 350, "Blue", COLOR_LIGHT_BLUE, 200, 200)

        # YELLOW_WINDOW
        #yellow_window = self.createWindowOnScreen(300, 200, 400, 350, "Yellow", COLOR_ORANGE, 50, 50)

        #purple_window1 = yellow_window.createWindowInWindow(30, 40, 70, 50, "Purple1", COLOR_PURPLE, 100, 100, LayoutAnchor.top | LayoutAnchor.left)

        # purple_window2 = yellow_window.createWindowInWindow(30, 100, 70, 50, "Purple2", COLOR_PURPLE)

        # purple_window3 = yellow_window.createWindowInWindow(30, 160, 70, 50, "Purple3", COLOR_PURPLE)

    """
    WINDOW MANAGEMENT
    """

    # P2 1c
    def createWindowOnScreen(self, x, y, width, height, identifier, backgroundColor, minWidth, minHeight, anchoring=None):
        # creates a new window object with given parameters
        # depth is needed for the P2 4b
        newWindow = Window(x, y, width, height, identifier, anchoring, minWidth, minHeight)
        # assign preset background color for new window object
        newWindow.backgroundColor = backgroundColor
        # add new window object to parent's list of window children
        self.screen.addChildWindow(newWindow)

        # add a window to the openedTopLevelList for the fixed order in the task bar
        self.windowManager.openWindow(newWindow)

        return newWindow

    def createLabelInWindow(self, parentWindow, childX, childY, childWidth, childHeight, childIdentifier,
                            childTextString, childTextColor, childBackgroundColor, childAnchoring, childMinWidth=50, childMinHeight=50):


        # making sure that child lies within the parents margin
        # padding top
        if childY <= parentWindow.y + parentWindow.paddingTop:
            childY += parentWindow.paddingTop

        # child should stay within left-right-bottom margin
        if childX <= parentWindow.x + parentWindow.paddingLeft:
            childX += parentWindow.paddingLeft

        # TODO check right margin
        if childX + childWidth >= parentWindow.width - parentWindow.paddingRight:
            childWidth = parentWindow.width - parentWindow.paddingRight - childX

        # check bottom margin
        if childY + childHeight >= parentWindow.width - parentWindow.paddingBottom:
            childHeight = parentWindow.height - parentWindow.paddingBottom - childY
        if childY + childHeight >= parentWindow.height:
            childHeight = childHeight - (childHeight -  childY - parentWindow.height) - parentWindow.paddingBottom


        # global coordinates
        convertedX, convertedY = parentWindow.convertPositionToScreen(childX, childY)
        newLabel = Label(convertedX, convertedY, childWidth, childHeight, childIdentifier, childAnchoring, childMinWidth, childMinHeight, childTextString,
                          childTextColor, childBackgroundColor, parentWindow.depth + 1)

        parentWindow.addChildWindow(newLabel)
        return newLabel

    def createButtonInWindow(self, parentWindow, childX, childY, childWidth, childHeight, childIdentifier,
                             childTextString, childTextColor, childBackgroundColor, childAction=None, childAnchoring=None, childMinWidth=50, childMinHeight=50):

        # making sure that child lies within the parents margin
        # padding top
        if childY <= parentWindow.y + parentWindow.paddingTop:
            childY += parentWindow.paddingTop

        # child should stay within left-right-bottom margin
        if childX <= parentWindow.x + parentWindow.paddingLeft:
            childX += parentWindow.paddingLeft

        # TODO check right margin
        if childX + childWidth >= parentWindow.width - parentWindow.paddingRight:
            childWidth = parentWindow.width - parentWindow.paddingRight - childX

        # check bottom margin
        if childY + childHeight >= parentWindow.width - parentWindow.paddingBottom:
            childHeight = parentWindow.height - parentWindow.paddingBottom - childY
        if childY + childHeight >= parentWindow.height:
            childHeight = childHeight - (childHeight -  childY - parentWindow.height) - parentWindow.paddingBottom

        # global coordinates
        convertedX, convertedY = parentWindow.convertPositionToScreen(childX, childY)
        newWidget = Button(convertedX, convertedY, childWidth, childHeight, childIdentifier, childAnchoring, childMinWidth, childMinHeight, childTextString,
                           childTextColor, childBackgroundColor, parentWindow.depth + 1, childAction)

        parentWindow.addChildWindow(newWidget)
        return newWidget

    def createContainerInWindow(self, parentWindow, childX, childY, childWidth, childHeight, childIdentifier, childAnchoring, childMinWidth, childMinHeight):
        # making sure that child lies within the parents margin
        # padding top
        if childY <= parentWindow.y + parentWindow.paddingTop:
            childY += parentWindow.paddingTop

        # child should stay within left-right-bottom margin
        if childX <= parentWindow.x + parentWindow.paddingLeft:
            childX += parentWindow.paddingLeft

        # TODO check right margin
        if childX + childWidth >= parentWindow.width - parentWindow.paddingRight:
            childWidth = parentWindow.width - parentWindow.paddingRight - childX

        # check bottom margin
        if childY + childHeight >= parentWindow.width - parentWindow.paddingBottom:
            childHeight = parentWindow.height - parentWindow.paddingBottom - childY
        if childY + childHeight >= parentWindow.height:
            childHeight = childHeight - (childHeight -  childY - parentWindow.height) - parentWindow.paddingBottom

        # global coordinates
        convertedX, convertedY = parentWindow.convertPositionToScreen(childX, childY)
        newContainer = Container(convertedX, convertedY, childWidth, childHeight, childIdentifier, childAnchoring, childMinWidth, childMinHeight, parentWindow.depth + 1)

        parentWindow.addChildWindow(newContainer)
        return newContainer


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
        self.screen.draw(self.graphicsContext, self.screen.width, self.screen.height)

    """
    INPUT EVENTS
    """

    def handleMousePressed(self, x, y):
        self.mousePressed = True
        self.recentX = x
        self.recentY = y

        if self.screen.childWindowAtLocation(x, y) is not None:

            # handling bringing toplevel Window to front
            self.lastClickedWindow = self.screen.childWindowAtLocation(x, y)
            self.bringWindowToFront(self.lastClickedWindow)



            self.requestRepaint()

            if isinstance(self.lastClickedWindow, Button):
                self.lastClickedButton = self.lastClickedWindow

            # as long as we are inside of lastClickedButton, provided it is not none, we flip isHovered flag and
            # requestRepaint
            if (self.lastClickedButton is not None) and (
                    self.lastClickedButton.x <= x <= self.lastClickedButton.width + self.lastClickedButton.x and self.lastClickedButton.y <= y <= self.lastClickedButton.height + self.lastClickedButton.y):
                print("Button pressed")
                self.lastClickedButton.isPressed = True
                self.lastClickedButton.isHovered = False
                self.requestRepaint()

            # preparing for dragging operation
            if self.lastClickedWindow.checkIfInTitleBar(self.recentX, self.recentY):
                # flip dragging flag
                self.allowDragging = True

            # preparing for resizing operation
            elif self.lastClickedWindow.checkIfInResizingArea(self.recentX, self.recentY):
                # flip resizing flag
                self.allowResizing = True


        else:
            # prepare for taskbar interaction
            self.lastClickedWindow = self.screen
            if self.screen.checkIfInTaskbar(x, y):
                if self.screen.checkIfInTaskBarArea(x,y):
                    print('in start menu pressed')
                    #TODO start_menu
                    #self.startMenuAcive = True

    def handleMouseReleased(self, x, y):
        self.mousePressed = False

        # do not allow the user to drag/resize the window if mouse is released
        self.allowDragging = False
        self.allowResizing = False

        # TODO hier müssen wir checken dass bei der gleichen position released wurde,
        # TODO wie bei pressed
        # execute taskbar interaction event
        # if clicked window is screen
        if self.lastClickedWindow == self.screen:
            if self.lastClickedWindow.checkIfInTaskbar(x, y):

                """
                if self.lastClickedWindow.checkIfInTaskBarArea(x,y) and self.startMenuAcive:
                    print("in start menu released")
                    self.windowManager.openCloseStartMenu(self.startMenuActive)
                else:

                 """
                self.screen.clickedTaskbarEvent(x, y)

        else:
            # if clicked window is a toplevel w
            if self.lastClickedWindow.parentWindow == self.screen:
                # for close and minimizing
                if self.lastClickedWindow.checkIfInTitleBar(x, y):
                    convertedX, convertedY = self.lastClickedWindow.convertPositionFromScreen(x, y)

                    # handle the close window event
                    if self.lastClickedWindow.checkIfInCloseButton(x, y):
                        self.windowManager.closeWindow(self.lastClickedWindow)

                    # handle the minimize window event
                    if self.lastClickedWindow.checkIfInMinimizeButton(x, y):
                        self.windowManager.minimizeWindow(self.lastClickedWindow)


                # register that mouseclick event just happened
                if self.lastClickedWindow == self.screen.childWindowAtLocation(x, y):
                    if self.lastClickedWindow.identifier == "Calculator":
                        #self.lastClickedWindow.handleMouseClicked(x, y)
                        self.calculator.inputHandler(self.lastClickedWindow.identifier)

            elif self.lastClickedButton is not None and self.lastClickedButton.isPressed:
                self.lastClickedButton.isPressed = False
                self.lastClickedButton.isHovered = True
                self.lastClickedButton.isActive = True
                self.lastClickedButton.handleAction()
                self.requestRepaint()

    def handleMouseMoved(self, x, y):

        if self.screen.childWindowAtLocation(x,y) is not None:
            widget = self.screen.childWindowAtLocation(x, y)


            # check if the widget is of type button
            # if so, update lastClickedButton
            if isinstance(widget, Button) and self.lastClickedButton is None:
                self.lastClickedButton = widget

            # as long as we are inside of lastClickedButton, provided it is not none, we flip isHovered flag and
            # requestRepaint
            if (self.lastClickedButton is not None) and (
                    self.lastClickedButton.x <= x <= self.lastClickedButton.width + self.lastClickedButton.x and self.lastClickedButton.y <= y <= self.lastClickedButton.height + self.lastClickedButton.y):
                self.lastClickedButton.isHovered = True
                self.requestRepaint()

            # if we are outside lastClickedButton, we flip isHovered flag again to false and requestRepaint
            elif self.lastClickedButton is not None:
                self.lastClickedButton.isHovered = False
                self.lastClickedButton = None
                self.requestRepaint()

    def handleMouseDragged(self, x, y):
        # here dragging and resizing operations are handled

        # only toplevel windows should be moved, for that we make sure that parent is screen
        if self.lastClickedWindow is not None and self.lastClickedWindow.parentWindow == self.screen:

            # dragging operation
            if self.allowDragging:
                self.windowManager.dragWindow(self.lastClickedWindow, x, y)

            # resizing operation
            if self.allowResizing:
                self.windowManager.resizeWindow(self.lastClickedWindow, x, y)

    def handleKeyPressed(self, char):
        if self.lastClickedWindow is not None and self.lastClickedWindow.identifier == "HelloWorld":
            self.helloWorld.inputHandler(char)
            self.requestRepaint()


# Let's start your window system!
w = WindowSystem(800, 600)
w.start()
