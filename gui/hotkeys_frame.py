# -*- coding: utf-8 -*-
"""
Created on Sat Aug 11 09:13:41 2018

@author: Gerardo Cervantes
"""

import tkinter as tk
from tkinter.font import Font
from gui.title_bar import TitleBar
from gui.make_draggable import Draggable

# Module in src folder that captures keyboard input and convert to windows format
from src.capture_keys import CaptureKeys
from src.splitter import Splitter


class HotkeysFrame(tk.Frame):

    hotkeys = None
    FONT = 'Times New Roman'
    FONT_SIZE = 16
    cap_keys = CaptureKeys()
    TEST_BUTTONS_COLOR = '#4286f4'
    PRESS_TEXT = '-Press key-'

    def __init__(self, master, custom_title_bar=True):
        self.root = master
        tk.Frame.__init__(self, master)

        if custom_title_bar:
            self.title_bar = TitleBar(self, window_root=master, width=180, height=5)
            self.title_bar.grid(column=0, row=0, rowspan=1, columnspan=2, padx=2, pady=1)
        self.draggable = Draggable(self, master)

        self.font = Font(family=self.FONT, size=self.FONT_SIZE)
        self.entry_font = Font(family=self.FONT, size=self.FONT_SIZE, weight='bold')
        self.button_font = Font(family=self.FONT, size=self.FONT_SIZE)
        split_keys_frame = self.create_split_keys_frame(self)
        split_keys_frame.grid(column=0, row=1, columnspan=2, padx=10, pady=5)
        self.split_test_button = tk.Button(self, text='Split Test', bg=self.TEST_BUTTONS_COLOR, font=self.font,
                                           command=self.test_split_key)
        self.reset_test_button = tk.Button(self, text='Reset Test', bg=self.TEST_BUTTONS_COLOR, font=self.font,
                                           command=self.test_reset_key)
        self.split_test_button.grid(column=0, row=2, columnspan=1, padx=0, pady=15)
        self.reset_test_button.grid(column=1, row=2, columnspan=1, padx=0, pady=15)

    # Updates self.hotkeys variable with what's on the entries
    def update_hotkeys(self):
        split_key = self.split_stringvar.get()
        reset_key = self.reset_stringvar.get()

        if self.hotkeys is not None:
            self.hotkeys.set_split_key(split_key)
            self.hotkeys.set_reset_key(reset_key)

    def split_button_pressed(self):
        self.cap_keys.fn = self.split_key_captured
        print(self.reset_stringvar.get())
        print(self.PRESS_TEXT)
        if self.reset_stringvar.get() == self.PRESS_TEXT:
            self.revert_reset_key()
        self.split_stringvar.set(self.PRESS_TEXT)
        self.cap_keys.capture_key()

    def reset_button_pressed(self):
        self.cap_keys.fn = self.reset_key_captured
        if self.split_stringvar.get() == self.PRESS_TEXT:
            self.revert_split_key()
        self.reset_stringvar.set(self.PRESS_TEXT)
        self.cap_keys.capture_key()

    def split_key_captured(self, key):
        self.split_stringvar.set(key)
        self.update_hotkeys()

    def reset_key_captured(self, key):
        self.reset_stringvar.set(key)
        self.update_hotkeys()

    def revert_split_key(self):
        self.split_stringvar.set(self.hotkeys.get_split_key())

    def revert_reset_key(self):
        self.reset_stringvar.set(self.hotkeys.get_reset_key())

    def test_split_key(self):
        self.update_hotkeys()
        split_key = self.hotkeys.get_split_key()
        Splitter.split(split_key, 0)

    def test_reset_key(self):
        self.update_hotkeys()
        reset_key = self.hotkeys.get_reset_key()
        Splitter.split(reset_key, 0)

    def create_split_keys_frame(self, master):
        split_keys_frame = tk.Frame(master)

        self.split_frame, self.split_label, self.split_button, self.split_stringvar = self.create_label_button_pair(
            split_keys_frame, 'Split Key', self.split_button_pressed)
        self.reset_frame, self.reset_label, self.reset_button, self.reset_stringvar = self.create_label_button_pair(
            split_keys_frame, 'Reset Key', self.reset_button_pressed)
        self.split_label.config(justify=tk.LEFT, anchor='w')
        self.reset_label.config(justify=tk.LEFT, anchor='w')

        self.split_frame.grid(column=0, row=1)
        self.reset_frame.grid(column=0, row=2)

        if self.hotkeys is not None:
            self.split_button.insert(0, self.hotkeys.get_split_key())
            self.reset_button.insert(0, self.hotkeys.get_reset_key())

        return split_keys_frame

    def set_hotkeys(self, hotkeys):
        self.hotkeys = hotkeys

        self.split_stringvar.set(self.hotkeys.get_split_key())
        self.reset_stringvar.set(self.hotkeys.get_reset_key())

    # Clears the entry items
    def clear_entries(self):
        self.split_stringvar.set('Click')
        self.reset_stringvar.set('Click')

    # Returns tuple with 3 items, tk.frame containing the tk.label and tk.button, the tk.label, and the tk.button
    def create_label_button_pair(self, master, label_text, button_handler):
        label_entry_frame = tk.Frame(master)

        label = tk.Label(label_entry_frame, text=label_text, font=self.font, width=12)

        label.grid(column=0, row=1, padx=2, pady=3)
        string_var = tk.StringVar()

        button = tk.Button(label_entry_frame, textvariable=string_var, width=12, font=self.entry_font, justify='center')
        button.config(command=button_handler)
        button.grid(column=1, row=1, padx=5, pady=3)

        return label_entry_frame, label, button, string_var

    def set_bg_color(self, bg_color):
        self.configure(background=bg_color)
        self.split_frame.configure(background=bg_color)
        self.split_label.configure(background=bg_color)
        self.reset_frame.configure(background=bg_color)
        self.reset_label.configure(background=bg_color)

    def change_text_color(self, color):
        self.split_label.configure(fg=color)
        self.reset_label.configure(fg=color)
        self.split_button.configure(fg=color)
        self.reset_button.configure(fg=color)

    def change_text_size(self, size):
        self.font.configure(size=size + 1)
        self.entry_font.configure(size=size)
        self.button_font.configure(family=size - 1)

    def set_alt_color(self, color):
        self.split_button.configure(background=color)
        self.reset_button.configure(background=color)

    def change_text_font(self, font_family):
        self.font.configure(family=font_family)
        self.entry_font.configure(family=font_family)
        self.button_font.configure(family=font_family)

    def show(self):
        self.wait_window()
        self.update_hotkeys()


if __name__ == "__main__":
    root = tk.Tk()
    root.title('Select route')
    app = HotkeysFrame(root)
    app.grid(column=0, row=1, columnspan=2, padx=1, pady=5)
    root.mainloop()
