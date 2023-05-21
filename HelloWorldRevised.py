#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HelloWorldRevised - Submission
by  Ulyana Lavnikevich (388633)
and Serin Bazzi (437585)
"""

from WindowManager import *
from UITK import *
from Window import *


class HelloWorld:

    def __init__(self, windowSystem):
        self.windowSystem = windowSystem
        self.window = None
        self.languageLabel = None
        self.btn_german = None
        self.btn_english = None
        self.btn_french = None
        self.quit_button = None
        self.createApp()

    def createApp(self):

        self.window = self.windowSystem.createWindowOnScreen(50, 20, 250, 300, "Hello World", COLOR_WHITE, 200, 250)

        #self.containerLabel = self.windowSystem.createContainerInWindow(self.window, 50, 0, self.window.width, 100, 'labelContainer', LayoutAnchor.bottom, self.window.width , 100)


        self.languageLabel = self.windowSystem.createLabelInWindow(self.window, 19, 0, 180, 33, "languageLabel",
                                                                   "Please select a language", "#F6A800", COLOR_CLEAR, LayoutAnchor.top)

        self.btn_german = self.windowSystem.createButtonInWindow(self.window, 64, 90, 90, 30, "btn_german", "  Deutsch",
                                                                 COLOR_BLACK, COLOR_LIGHT_GRAY, lambda: self.german_selected(), LayoutAnchor.top)

        self.btn_english = self.windowSystem.createButtonInWindow(self.window, 64, 130, 90, 30, "btn_english", "   English",
                                                                  COLOR_BLACK, COLOR_LIGHT_GRAY,lambda: self.english_selected(), LayoutAnchor.top)


        self.btn_french = self.windowSystem.createButtonInWindow(self.window, 64, 170, 90, 30, "btn_french", "  Français",
                                                                COLOR_BLACK, COLOR_LIGHT_GRAY, lambda: self.french_selected(), LayoutAnchor.top)

        self.quit_button = self.windowSystem.createButtonInWindow(self.window, 184, 254, 50,0, "quit_button", "Quit", COLOR_BLACK, COLOR_LIGHT_GRAY,
                                                                 lambda: self.quit_selected(), LayoutAnchor.bottom | LayoutAnchor.right)

    def german_selected(self):
        # set the text attribute of languageLabel
        self.languageLabel.text = "Guten Tag"
        self.windowSystem.requestRepaint()

    def english_selected(self):
        self.languageLabel.text = "Hello"

    def french_selected(self):
        self.languageLabel.text = "Bonjour"

    def quit_selected(self):
        self.windowSystem.windowManager.closeWindow(self.window)

    def inputHandler(self, char):
        if char == 'g' or char == 'G':
            self.german_selected()
        elif char == 'e' or char == 'E':
            self.english_selected()
        elif char == 'f' or char == 'F':
            self.french_selected()
        elif char == 'q' or char == 'Q':
            self.quit_selected()
        else:
            self.languageLabel.text = "Please select a language"
