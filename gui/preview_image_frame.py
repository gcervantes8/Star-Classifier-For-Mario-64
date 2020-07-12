# -*- coding: utf-8 -*-
"""

@author: Gerardo Cervantes
"""

import tkinter as tk
from tkinter.font import Font
from gui.title_bar import TitleBar
from gui.make_draggable import Draggable

from PIL import ImageTk, Image
import pyautogui

# Module in src folder that takes screenshots
from src.screenshot_taker import ScreenshotTaker


class PreviewImageFrame(tk.Frame):
    # photo_image_label is a tk.Label containing the image
    photo_image_label = None

    x_entry = None
    y_entry = None
    width_entry = None

    screenshot_instance = None

    x_stringvar = None
    y_stringvar = None
    width_stringvar = None

    DEFAULT_IMAGE_PATH = 'images/two_digit.png'

    FONT_SIZE = 20
    FONT = 'Arial'
    PREVIEW_BUTTON_COLOR = '#4286f4'

    def __init__(self, master, custom_title_bar=True):
        self.root = master
        tk.Frame.__init__(self, master)

        if custom_title_bar:
            self.title_bar = TitleBar(self, window_root=master, width=170, height=5)
            self.title_bar.grid(column=0, row=0, rowspan=1, columnspan=1, padx=2, pady=1)
        self.draggable = Draggable(self, master)
        self.font = Font(family=self.FONT, size=self.FONT_SIZE, weight='bold')
        self.entry_font = Font(family=self.FONT, size=self.FONT_SIZE)
        self.screenshot_instance = ScreenshotTaker()

        preview_image_widget = self.create_preview_image(self)
        preview_image_widget.grid(column=0, row=1, padx=1, pady=5)
        self.draggable = Draggable(preview_image_widget, master)
        self.set_sizes_frame = self.create_set_sizes_frame(self)
        self.set_sizes_frame.grid(column=0, row=2)

        preview_button = tk.Button(self, text='Preview', background='#4286f4', font=self.font)
        preview_button.grid(column=0, row=3, padx=1, pady=5)
        preview_button.config(command=self.preview_button_clicked)

        self.mouse_coord_stringvar = tk.StringVar()
        self.mouse_coord_label = tk.Label(self, textvariable=self.mouse_coord_stringvar, font=self.font)
        self.mouse_coord_label.grid(column=0, row=4, padx=1, pady=5)

        self.poll_mouse_coordinates()

    def create_preview_image(self, master):

        self.photo_image_label = tk.Label(master)

        # loads default image
        img = Image.open(self.DEFAULT_IMAGE_PATH)
        self.show_image_on_label(img)

        self.photo_image_label.config(borderwidth=0, relief='solid')
        self.photo_image_label.config(highlightbackground='black')
        return self.photo_image_label

    def show_image_on_label(self, pil_image):
        pil_image = pil_image.resize((67, 40), Image.ANTIALIAS)  # Width,height
        self.img = pil_image

        self.photo_image = ImageTk.PhotoImage(pil_image)
        self.photo_image_label.config(image=self.photo_image)

    def set_coordinates(self, coordinates):
        x, y, width, height = coordinates.get_coordinates()
        if x != None:
            self.x_stringvar.set(str(x))
        if y != None:
            self.y_stringvar.set(str(y))
        if width != None:
            self.width_stringvar.set(str(width))

    def poll_mouse_coordinates(self):
        x, y = pyautogui.position()
        coords = 'Mouse cooordinates ' + str(x) + ', ' + str(y)
        self.mouse_coord_stringvar.set(coords)
        self.after(100, self.poll_mouse_coordinates)

    def set_bg_color(self, bg_color):
        self.configure(background=bg_color)
        self.set_sizes_frame.configure(background=bg_color)
        self.x_frame.configure(background=bg_color)
        self.y_frame.configure(background=bg_color)
        self.width_frame.configure(background=bg_color)

        self.x_label.configure(background=bg_color)
        self.y_label.configure(background=bg_color)
        self.width_label.configure(background=bg_color)
        self.mouse_coord_label.configure(background=bg_color)

    def change_text_color(self, color):
        self.x_label.configure(foreground=color)
        self.y_label.configure(foreground=color)
        self.width_label.configure(foreground=color)
        self.mouse_coord_label.configure(foreground=color)

    def change_text_size(self, size):
        self.font.configure(size=size)
        self.entry_font.configure(size=size)

    def change_text_font(self, font_family):
        self.font.configure(family=font_family)
        self.entry_font.configure(family=font_family)

    def create_set_sizes_frame(self, master):
        set_sizes_frame = tk.Frame(master)
        self.x_frame, self.x_label, self.x_entry, self.x_stringvar = self.create_label_entry_pair(set_sizes_frame, 'X')
        self.y_frame, self.y_label, self.y_entry, self.y_stringvar = self.create_label_entry_pair(set_sizes_frame, 'Y')
        self.width_frame, self.width_label, self.width_entry, self.width_stringvar = self.create_label_entry_pair(
            set_sizes_frame, 'Size')

        padx = 7
        pady = 8
        self.x_frame.grid(column=0, row=0, padx=padx, pady=pady)
        self.y_frame.grid(column=1, row=0, padx=padx, pady=pady)
        self.width_frame.grid(column=2, row=0, padx=padx, pady=pady)

        return set_sizes_frame

    def clear_entries(self):
        self.clear_entry(self.x_entry)
        self.clear_entry(self.y_entry)
        self.clear_entry(self.width_entry)

    def clear_entry(self, tk_entry):
        try:
            self.tk_entry.delete(0, 'end')
        except:
            pass

    # Returns tuple with 3 items, tk.frame containing the tk.label and tk.entry, the tk.label, and the tk.entry
    def create_label_entry_pair(self, master, label_text):
        label_entry_frame = tk.Frame(master)
        label = tk.Label(label_entry_frame, text=label_text, font=self.font)
        label.grid(column=0, row=0, padx=2)
        stringvar = tk.StringVar()
        entry = tk.Entry(label_entry_frame, textvariable=stringvar, width=6, font=self.entry_font, justify='center')
        entry.grid(column=1, row=0)

        return label_entry_frame, label, entry, stringvar

    def get_entry_item(self, tk_stringvar):
        try:
            return tk_stringvar.get()
        except:
            return ''

    # Returns 4-tuple of integers (x,y,with, height)
    # Returns -1 for any integer if it wasn't an integer
    def get_coordinates(self):
        x_entry_text = self.get_entry_item(self.x_stringvar)

        y_entry_text = self.get_entry_item(self.y_stringvar)
        width_entry_text = self.get_entry_item(self.width_stringvar)
        width_int = self.str_to_int(width_entry_text)
        if width_int == -1:
            height_int = -1
        else:
            height_int = round(width_int / 1.675)  # 1.675 is the ratio we are using for resizing

        return self.str_to_int(x_entry_text), self.str_to_int(y_entry_text), width_int, height_int

    def str_to_int(self, string):
        if self.is_integer(string):
            return int(string)
        return -1

    def are_invalid_coordinates(self, x, y, width, height):
        return not (self.is_valid_coordinate(x) and self.is_valid_coordinate(y) and self.is_valid_coordinate(
            width) and self.is_valid_coordinate(height))

    def is_valid_coordinate(self, item):
        return self.is_integer(item) and item >= 0

    def is_integer(self, var):
        try:
            int(var)
            return True
        except (ValueError, TypeError) as e:
            return False

    def preview_button_clicked(self):
        x, y, width, height = self.get_coordinates()

        if self.are_invalid_coordinates(x, y, width, height):
            print('Invalid coordinates')
            return

        pil_img, _ = self.screenshot_instance.screenshot_mss(int(x), int(y), int(width), int(height))
        self.show_image_on_label(pil_img)

    # Returns coordinates when the frame is closed
    def show(self):
        self.wait_window()
        return self.get_coordinates()


if __name__ == "__main__":
    root = tk.Tk()
    root.title('Preview Image Window')
    app = PreviewImageFrame(root)
    app.pack()
    root.mainloop()
