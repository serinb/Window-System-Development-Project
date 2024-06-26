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
import ColorSliders


class WindowSystem(GraphicsEventSystem):

    # 1b
    def __init__(self, width, height):
        super().__init__(width, height)
        # P2 1b
        self.screen = None
        self.windowManager = None
        self.helloWorld = None
        self.calculator = None
        self.colorSliders = None
        self.slider = None
        self.start_menu = None

        # variables for mouse events
        self.mousePressed = False
        self.recentX = 0
        self.recentY = 0
        self.lastClickedWindow = None
        self.lastClickedButton = None
        self.lastClickedSlider = None
        self.allowDragging = False
        self.allowResizing = False

    def start(self):
        # WINDOW MANAGER
        self.windowManager = WindowManager(self)

        # SCREEN (P2 1b)
        self.screen = Screen(self)
        # variables for mouse events
        self.mousePressed = False
        self.recentX = 0
        self.recentY = 0
        self.lastClickedWindow = None
        self.lastClickedButton = None
        self.lastClickedSlider = None
        self.allowDragging = False
        self.allowResizing = False

        # Start Menu Window
        self.start_menu = self.createWindowOnScreen(0, 350, 200, 210, "Start Menu", "#D17D49", 200, 200)

        # APPLICATIONS
        # Hello World App
        self.helloWorld = HelloWorldRevised.HelloWorld(self)

        # Calculator App
        self.calculator = Calculator.CalculatorApplication(self)

        self.colorSliders = ColorSliders.ColorSlidersApplication(self)

        # button for HelloWorld
        helloButton = self.createButtonInWindow(self.start_menu, 0, 0, 200, 30, "hello_button", "Hello World",
                                                "#35393C", "#FFA169", lambda: self.helloWorldPressed())

        # button for Calculator
        calcButton = self.createButtonInWindow(self.start_menu, 0, 40, 200, 30, "calc_button", "Calculator", "#35393C",
                                               "#FFA169", lambda: self.calcPressed())

        # button for RGB Slider
        sliderButton = self.createButtonInWindow(self.start_menu, 0, 80, 200, 30, "slider_button", "Slider", "#35393C",
                                                 "#FFA169", lambda: self.colorSlidersPressed())

        # shut down button
        shutDown = self.createButtonInWindow(self.start_menu, 0, 120, 200, 30, "shut_down_button", "Shut Down Button",
                                             "#35393C", "#FF6771", lambda: self.shutDownButtonPressed())

    """
    WINDOW MANAGEMENT
    """

    # P2 1c
    def createWindowOnScreen(self, x, y, width, height, identifier, backgroundColor, minWidth, minHeight,
                             anchoring=None):
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
                            childTextString, childTextColor, childBackgroundColor, childAnchoring, childMinWidth=50,
                            childMinHeight=50, fontSize=11, fontFamily="Helvetica", fontWeight="bold"):

        # making sure that child lies within the parents padding
        # padding top
        if childY <= parentWindow.y + parentWindow.paddingTop:
            childY += parentWindow.paddingTop

        # child should stay within left-right-bottom padding
        if childX <= parentWindow.x + parentWindow.paddingLeft:
            childX += parentWindow.paddingLeft

        # check right padding
        if childX + childWidth >= parentWindow.width - parentWindow.paddingRight:
            childWidth = parentWindow.width - parentWindow.paddingRight - childX

        # check bottom padding
        if childY + childHeight >= parentWindow.width - parentWindow.paddingBottom:
            childHeight = parentWindow.height - parentWindow.paddingBottom - childY
        if childY + childHeight >= parentWindow.height:
            childHeight = childHeight - (childHeight - childY - parentWindow.height) - parentWindow.paddingBottom

        # global coordinates
        convertedX, convertedY = parentWindow.convertPositionToScreen(childX, childY)
        newLabel = Label(convertedX, convertedY, childWidth, childHeight, childIdentifier, childAnchoring,
                         childMinWidth, childMinHeight, childTextString,
                         childTextColor, childBackgroundColor, parentWindow.depth + 1, fontSize, fontFamily, fontWeight)

        parentWindow.addChildWindow(newLabel)
        return newLabel

    def createButtonInWindow(self, parentWindow, childX, childY, childWidth, childHeight, childIdentifier,
                             childTextString, childTextColor, childBackgroundColor, childAction=None,
                             childAnchoring=None, childMinWidth=50, childMinHeight=50):

        # making sure that child lies within the parents padding
        # padding top
        if childY <= parentWindow.y + parentWindow.paddingTop:
            childY += parentWindow.paddingTop

        # child should stay within left-right-bottom padding
        if childX <= parentWindow.x + parentWindow.paddingLeft:
            childX += parentWindow.paddingLeft

        # check right padding
        if childX + childWidth >= parentWindow.width - parentWindow.paddingRight:
            childWidth = parentWindow.width - parentWindow.paddingRight - childX

        # check bottom padding
        if childY + childHeight >= parentWindow.width - parentWindow.paddingBottom:
            childHeight = parentWindow.height - parentWindow.paddingBottom - childY
        if childY + childHeight >= parentWindow.height:
            childHeight = childHeight - (childHeight - childY - parentWindow.height) - parentWindow.paddingBottom

        # global coordinates
        convertedX, convertedY = parentWindow.convertPositionToScreen(childX, childY)
        newWidget = Button(convertedX, convertedY, childWidth, childHeight, childIdentifier, childAnchoring,
                           childMinWidth, childMinHeight, childTextString,
                           childTextColor, childBackgroundColor, parentWindow.depth + 1, childAction)

        parentWindow.addChildWindow(newWidget)
        return newWidget

    def createContainerInWindow(self, parentWindow, childX, childY, childWidth, childHeight, childIdentifier,
                                childAnchoring, childMinWidth, childMinHeight):
        # making sure that child lies within the parents padding
        # padding top
        if childY <= parentWindow.y + parentWindow.paddingTop:
            childY += parentWindow.paddingTop

        # child should stay within left-right-bottom padding
        if childX <= parentWindow.x + parentWindow.paddingLeft:
            childX += parentWindow.paddingLeft

        # check right padding
        if childX + childWidth >= parentWindow.width - parentWindow.paddingRight:
            childWidth = parentWindow.width - parentWindow.paddingRight - childX

        # check bottom padding
        if childY + childHeight >= parentWindow.width - parentWindow.paddingBottom:
            childHeight = parentWindow.height - parentWindow.paddingBottom - childY
        if childY + childHeight >= parentWindow.height:
            childHeight = childHeight - (childHeight - childY - parentWindow.height) - parentWindow.paddingBottom

        # global coordinates
        convertedX, convertedY = parentWindow.convertPositionToScreen(childX, childY)
        newContainer = Container(convertedX, convertedY, childWidth, childHeight, childIdentifier, childAnchoring,
                                 childMinWidth, childMinHeight, parentWindow.depth + 1)

        parentWindow.addChildWindow(newContainer)
        return newContainer

    def createSliderInWindow(self, parentWindow, childX, childY, childWidth, childHeight, childIdentifier,
                             childAnchoring, value, handleColor=COLOR_PINK, childMinWidth=50, childMinHeight=50):

        # making sure that child lies within the parents margin
        # padding top
        if childY <= parentWindow.y + parentWindow.paddingTop:
            childY += parentWindow.paddingTop

        # child should stay within left-right-bottom margin
        if childX <= parentWindow.x + parentWindow.paddingLeft:
            childX += parentWindow.paddingLeft

        if childX + childWidth >= parentWindow.width - parentWindow.paddingRight:
            childWidth = parentWindow.width - parentWindow.paddingRight - childX

        # check bottom margin
        if childY + childHeight >= parentWindow.width - parentWindow.paddingBottom:
            childHeight = parentWindow.height - parentWindow.paddingBottom - childY
        if childY + childHeight >= parentWindow.height:
            childHeight = childHeight - (childHeight - childY - parentWindow.height) - parentWindow.paddingBottom

        # global coordinates
        convertedX, convertedY = parentWindow.convertPositionToScreen(childX, childY)
        newSlider = Slider(convertedX, convertedY, childWidth, childHeight, childIdentifier, childAnchoring,
                           childMinWidth, childMinHeight, parentWindow.depth + 1, value, handleColor)

        parentWindow.addChildWindow(newSlider)
        return newSlider

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

    # FUNCTIONS FOR START MENU BUTTONS
    # each one makes sure that if a button in start menu is pressed
    # the respective application will open if closed
    # or will appear if minimized

    def helloWorldPressed(self):
        if self.helloWorld.window not in self.screen.childWindows:
            self.helloWorld = HelloWorldRevised.HelloWorld(self)
        self.helloWorld.window.isHidden = False
        self.requestRepaint()

    def calcPressed(self):
        if self.calculator.window not in self.screen.childWindows:
            self.calculator = Calculator.CalculatorApplication(self)
        self.calculator.window.isHidden = False
        self.requestRepaint()

    def colorSlidersPressed(self):
        if self.colorSliders.window not in self.screen.childWindows:
            self.colorSliders = ColorSliders.ColorSlidersApplication(self)
        self.colorSliders.window.isHidden = False
        self.requestRepaint()

    # this shuts down the windows system when shut down button pressed
    def shutDownButtonPressed(self):
        exit()

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

            if isinstance(self.lastClickedWindow, Slider):
                self.lastClickedSlider = self.lastClickedWindow

            # as long as we are inside of lastClickedButton, provided it is not none, we flip isHovered flag and
            # requestRepaint
            if (self.lastClickedButton is not None) and (
                    self.lastClickedButton.x <= x <= self.lastClickedButton.width + self.lastClickedButton.x and self.lastClickedButton.y <= y <= self.lastClickedButton.height + self.lastClickedButton.y):
                # print("Button pressed")
                self.lastClickedButton.isPressed = True
                self.lastClickedButton.isHovered = False
                self.requestRepaint()

            # if in the slider area -> allo dragging the slider
            if (self.lastClickedSlider is not None) and (
                    self.lastClickedSlider.x <= x <= self.lastClickedSlider.width + self.lastClickedSlider.x
                    and self.lastClickedSlider.y <= y <= self.lastClickedSlider.height + self.lastClickedSlider.y):
                self.allowDragging = True

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

    def handleMouseReleased(self, x, y):
        self.mousePressed = False

        # do not allow the user to drag/resize the window if mouse is released
        self.allowDragging = False
        self.allowResizing = False

        # execute taskbar interaction event
        # if clicked window is screen
        if self.lastClickedWindow == self.screen:
            if self.lastClickedWindow.checkIfInTaskbar(x, y):
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
                # if self.lastClickedWindow == self.screen.childWindowAtLocation(x, y):
                #     if self.lastClickedWindow.identifier == "Calculator":
                #         # self.lastClickedWindow.handleMouseClicked(x, y)
                #         self.calculator.inputHandler(self.lastClickedWindow.identifier)

            elif self.lastClickedButton is not None and self.lastClickedButton.isPressed:
                self.lastClickedButton.isPressed = False
                self.lastClickedButton.isHovered = True
                self.lastClickedButton.isActive = True
                self.lastClickedButton.handleAction()
                self.requestRepaint()

    def handleMouseMoved(self, x, y):

        if self.screen.childWindowAtLocation(x, y) is not None:
            widget = self.screen.childWindowAtLocation(x, y)

            # check if the widget is of type button
            # if so, update lastClickedButton
            if isinstance(widget, Button) and self.lastClickedButton is None:
                self.lastClickedButton = widget

            # as long as we are inside of lastClickedButton, provided it is not none, we flip isHovered flag and
            # requestRepaint
            if (self.lastClickedButton is not None) and (
                    self.lastClickedButton.x <= x <= self.lastClickedButton.width + self.lastClickedButton.x
                    and self.lastClickedButton.y <= y <= self.lastClickedButton.height + self.lastClickedButton.y):
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

        if self.lastClickedWindow is not None and isinstance(self.lastClickedWindow, Slider) and self.allowDragging:
            sliderStartX = self.lastClickedSlider.x
            sliderEndX = self.lastClickedSlider.x + self.lastClickedSlider.width
            # the "x" distance between the x-mouse cursor and the origin of the slider,
            # dividing the difference by the width of the slider
            # represents the position of the x mouse courser within the slider.
            newValue = (x - sliderStartX) / self.lastClickedSlider.width
            # set a value between 0.0 and 1.0 by dragging its handle, therefore min 0.0 and max 1.0
            self.lastClickedSlider.value = max(0.0, min(1.0, newValue))
            # update the color and the text of the color window in the ColorSliders app
            newColor = self.colorSliders.updateColorSlider()
            self.colorSliders.colorWindow.backgroundColor = newColor
            self.colorSliders.colorWindow.text = newColor
            self.requestRepaint()

    def handleKeyPressed(self, char):
        # if lastClickedWindow is the Hello World App, its input handler is called to handle key input
        if self.lastClickedWindow is not None and self.lastClickedWindow.identifier == "Hello World":
            self.helloWorld.inputHandler(char)
            self.requestRepaint()
        elif self.lastClickedWindow is not None and self.lastClickedWindow.identifier == "Calculator":
            self.calculator.buttonClicked(char)


# Let's start your window system!
w = WindowSystem(800, 600)
w.start()
