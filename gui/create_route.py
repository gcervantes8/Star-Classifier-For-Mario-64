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
        description_label = tk.Label(self, text='Description', anchor='w')
        description_entry = tk.Entry(self, textvariable=self.title_string_var)
        self.key_event_canvas = KeyEventsEdit(self)
        add_row_button = tk.Button(self, text='+', bg='green', command=self.add_row_clicked, width=10)

        title_label.grid(column=0, row=0, padx=5, pady=8, sticky='nsew')
        title_entry.grid(column=1, row=0, padx=5, pady=8, sticky='nsew')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=50)
        description_label.grid(column=0, row=1, padx=5, pady=8, sticky='nsew')
        description_entry.grid(column=1, row=1, padx=5, pady=8, sticky='nsew')
        self.key_event_canvas.grid(column=0, row=2, columnspan=2, padx=5, pady=5, sticky='nsew')
        add_row_button.grid(column=1, row=3, padx=5, pady=5, sticky='e')

    def add_row_clicked(self):
        self.key_event_canvas.add_row()

    def set_bg_color(self, color):
        self.configure(background=color)
        self.key_event_canvas.configure(background='red')

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
        self.bind('<Configure>', self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()
        self.configure(highlightthickness=0)

        icon_header = tk.Label(self, text='Icon')
        type_header = tk.Label(self, text='Type')
        coord_header = tk.Label(self, text='Select Region')
        is_split_header = tk.Label(self, text='Split')

        icon_header.grid(column=0, row=0, padx=1, pady=5, sticky='nsew')
        type_header.grid(column=1, row=0, padx=1, pady=5, sticky='nsew')
        coord_header.grid(column=2, row=0, padx=1, pady=5, sticky='nsew')
        is_split_header.grid(column=3, row=0, padx=1, pady=5, sticky='nsew')

        # Makes all columns of equal size
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        self.addtag_all('all')


    # https://stackoverflow.com/a/22837522/10062180
    def on_resize(self, event):
        # determine the ratio of old width/height to new width/height
        width_scale = float(event.width)/self.width
        height_scale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale('all', 0, 0, width_scale, height_scale)

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
        self.addtag_all('all')


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
