# -*- coding: utf-8 -*-
"""
Created on August 10, 2020

@author: Gerardo Cervantes
"""

import tkinter as tk
from gui.dropdown_frame import DropdownFrame

from PIL import ImageTk, Image


class CreateRoute(tk.Frame):

    def __init__(self, parent):
        self.root = parent
        tk.Frame.__init__(self, parent)
        self.title_string_var = tk.StringVar()
        self.description_string_var = tk.StringVar()
        title_label = tk.Label(self, text='Name', anchor='w')
        title_entry = tk.Entry(self, textvariable=self.title_string_var)
        description_label = tk.Label(self, text='Description', anchor='w', width=12)
        description_entry = tk.Entry(self, textvariable=self.title_string_var, width=40)
        self.key_event_canvas = KeyEventsEdit(self)
        add_row_button = tk.Button(self, text='+', bg='green', command=self.add_row_clicked)

        title_label.grid(column=0, row=0, padx=5, pady=5, sticky='w')
        title_entry.grid(column=1, row=0, padx=5, pady=5, sticky='w')
        description_label.grid(column=0, row=1, padx=5, pady=5)
        description_entry.grid(column=1, row=1, padx=5, pady=5)
        self.key_event_canvas.grid(column=0, row=2, columnspan=2, padx=5, pady=5)
        add_row_button.grid(column=0, row=3, padx=5, pady=5)

    def add_row_clicked(self):
        self.key_event_canvas.add_row()

    def set_bg_color(self, color):
        self.configure(background=color)

    def change_text_size(self, size):
        pass
        # self.dropdown.change_text_size(size)
        # self.dropdown.change_text_color('white')

    def change_text_color(self, color):
        pass

    def change_text_font(self, font_family):
        pass
        # self.dropdown.change_text_font(font_family)


class KeyEventsEdit(tk.Canvas):
    # Inherits from Canvas so it can have scroll bar

    rows = []

    def __init__(self, parent):
        self.root = parent
        tk.Canvas.__init__(self, parent)
        # tableFrame = tk.Frame(self)

        icon_header = tk.Label(self, text='Icon')
        type_header = tk.Label(self, text='Type')
        coord_header = tk.Label(self, text='Select Region')
        is_split_header = tk.Label(self, text='Split')

        icon_header.grid(column=0, row=0, padx=5, pady=5)
        type_header.grid(column=1, row=0, padx=5, pady=5)
        coord_header.grid(column=2, row=0, padx=5, pady=5)
        is_split_header.grid(column=3, row=0, padx=5, pady=5)

    # Adds a new row at the bottom of the table
    def add_row(self):

        # photo_img = ImageTk.PhotoImage(pil_img)
        icon = tk.Label(self)

        event_type = DropdownFrame(self, default_value='', set_width=3, dropdown_strs=[''])
        coordinates = tk.Button(self, text='Screen region')
        is_split = tk.Checkbutton(self)

        items = [icon, event_type, coordinates, is_split]
        for i, item in enumerate(items):
            item.grid(column=i, row=len(self.rows) + 1, padx=5, pady=5)

        self.rows.append(items)


if __name__ == "__main__":
    WIDTH, HEIGHT = 900, 900
    BACKGROUND = 'grey'
    TITLE = 'Create Route Menu'

    root = tk.Tk()
    root.title(TITLE)
    # root.geometry('%sx%s' % (WIDTH, HEIGHT))

    app = CreateRoute(root)

    app.pack()
    app.mainloop()
