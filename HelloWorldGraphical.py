#!/usr/bin/env
# -*- coding: utf-8 -*-

"""
Submission for Project Milestone 1, Task 3
by  Lavnikevich Ulyana (#388633)
and Serin Bazzi (#437585)
"""

from tkinter import *


def german_selected():
    # set the text attribute of languageLabel
    languageLabel.config(text="Guten Tag", width=100)


def english_selected():
    languageLabel.config(text="Hello", width=100)


def french_selected():
    languageLabel.config(text="Bonjour", width=100)


def quit_selected():
    languageLabel.config(text="Please select a language", width=100)


# based on which button was pressed, execute the corresponding function
def key_pressed(event):
    if event.keysym == "D" or event.keysym == "d":
        german_selected()
    elif event.keysym == "E" or event.keysym == "e":
        english_selected()
    elif event.keysym == "F" or event.keysym == "f":
        french_selected()
    elif event.keysym == "Q" or event.keysym == "q":
        quit_selected()


window = Tk()
window.geometry('250x300')

languageLabel = Label(window, text='Please select a language', fg='#F6A800')
languageLabel.pack(pady=4)

btn_german = Button(window, width=20, text="Deutsch", command=german_selected)
btn_german.pack(pady=5)

btn_english = Button(window, width=20, text="English", command=english_selected)
btn_english.pack(pady=5)

btn_french = Button(window, width=20, text="Français", command=french_selected)
btn_french.pack(pady=5)

quit_button = Button(window, width=5, text="Quit", command=quit_selected)
# anchoring the quit button to always stay in the bottom right corner when resizing the window
quit_button.pack(padx=5, pady=10, anchor="e", side="bottom")

# binding keyboard with the window // register which key has been pressed
window.bind("<KeyPress>", key_pressed)

window.mainloop()
