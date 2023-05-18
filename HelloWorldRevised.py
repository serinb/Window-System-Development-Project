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
        window = None

    def start(self):

        window = self.windowSystem.createWindowOnScreen(20, 20, 200, 200, "HelloWorld", COLOR_PINK)



