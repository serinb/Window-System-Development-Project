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


class HellowWorld:

    def __init__(self, windowSystem):
        self.windowSystem = windowSystem

    def start(self):

        window = self.windowSystem.createWindowOnScreen(20, 20, 250, 300, "HelloWorld", COLOR_LIGHT_GREEN)

        languageLabel = self.windowSystem.createLabelInWindow(window, 100, 40, 100, 20, "languageLabel",
                                                              "Please select a language",  "#F6A800", COLOR_WHITE)

        btn_german = self.windowSystem.createButtonInWindow(window, 100, 90, 70, 20, "btn_german", "Deutsch", COLOR_BLACK, COLOR_LIGHT_GRAY, lambda: self.german_selected())
        # testButton = self.createButtonInWindow(gray_window, 50, 100, 120, 30, "Button on Yellow Window", "Click me",
        #         # COLOR_BLACK, COLOR_LIGHT_GRAY, lambda: self.printSomething())

    def german_selected(self):
        # set the text attribute of languageLabel
        # languageLabel.config(text="Guten Tag", width=100)
        print("hey")
        # languageLabel.text = ""

