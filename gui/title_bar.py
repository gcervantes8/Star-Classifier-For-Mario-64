# -*- coding: utf-8 -*-
"""
Created on July 9 2020

@author: Gerardo Cervantes
"""

from gui.make_draggable import Draggable
import tkinter as tk
from tkinter.font import Font
from PIL import ImageTk, Image

from ctypes import windll


class TitleBar(tk.Frame):

    ICON_IMG_PATH = 'images/icon.png'
    COLOR = '#2a3247'
    CLOSE_BTN_HOVER_COLOR = 'red'
    MIN_BTN_HOVER_COLOR = 'gray'
    FONT_COLOR = 'white'
    FONT_SIZE = 13
    FONT = 'Arial'

    def __init__(self, master, width=425, height=35, icon_path=ICON_IMG_PATH):
        self.root = master
        tk.Frame.__init__(self, master)
        self.configure(background=self.COLOR)
        font = Font(family=self.FONT, size=self.FONT_SIZE)
        button_widths = 5
        button_heights = 1
        # put a close button on the title bar
        self.close_button = tk.Button(self, text='X', command=self.root.destroy, bg=self.COLOR, fg=self.FONT_COLOR,
                                      font=font, height=button_heights, width=button_widths, borderwidth=1)
        self.close_button.bind("<Enter>", self.close_btn_hover_enter)
        self.close_button.bind("<Leave>", self.close_btn_hover_leave)

        self.min_button = tk.Button(self, text='-', command=self.minimize, bg=self.COLOR, fg=self.FONT_COLOR,
                                    font=font, height=button_heights, width=button_widths, borderwidth=1)
        self.min_button.bind("<Enter>", self.min_btn_hover_enter)
        self.min_button.bind("<Leave>", self.min_btn_hover_leave)
        self.image_label = self.create_image_frame(icon_path)

        # a canvas for the main area of the window
        self.canvas = tk.Frame(self, bg=self.COLOR, width=width, height=height)

        self.image_label.grid(column=0, row=0, padx=5, pady=5)
        self.min_button.grid(column=2, row=0, padx=0, pady=1)
        self.close_button.grid(column=3, row=0, padx=0, pady=1)
        self.canvas.grid(column=1, row=0, padx=0, pady=0)

        self.canvas_draggable = Draggable(self.canvas, self.root)
        self.image_draggable = Draggable(self.image_label, self.root)

        self.delay_set_appwindow(None)

    # https://stackoverflow.com/a/30819099/10062180 -
    # Adds icon to taskbar, then calls frame_mapped, which turns off default title_bar
    def set_appwindow(self, event):
        self.unbind('<Map>')
        self.root.overrideredirect(True)

        gwl_exstyle = -20
        ws_ex_appwindow = 0x00040000
        ws_ex_toolwindow = 0x00000080

        hwnd = windll.user32.GetParent(self.root.winfo_id())
        style = windll.user32.GetWindowLongPtrW(hwnd, gwl_exstyle)
        style = style & ~ws_ex_toolwindow
        style = style | ws_ex_appwindow
        res = windll.user32.SetWindowLongPtrW(hwnd, gwl_exstyle, style)
        # re-assert the new window style
        self.root.wm_withdraw()
        self.frame_mapped()
        self.root.after(5, lambda: self.root.wm_deiconify())
        self.root.after(10, lambda: self.bind('<Map>', self.delay_set_appwindow))

    def delay_set_appwindow(self, event):
        self.root.after(5, lambda: self.set_appwindow(None))

    def close_btn_hover_enter(self, event):
        self.close_button.config(bg=self.CLOSE_BTN_HOVER_COLOR, fg='white')

    def close_btn_hover_leave(self, event):
        self.close_button.config(bg=self.COLOR, fg='white')

    def min_btn_hover_enter(self, event):
        self.min_button.config(bg=self.MIN_BTN_HOVER_COLOR, fg='white')

    def min_btn_hover_leave(self, event):
        self.min_button.config(bg=self.COLOR, fg='white')

    def create_image_frame(self, icon_path):

        pil_image = Image.open(icon_path)

        pil_image = pil_image.resize((25, 25), Image.ANTIALIAS)  # Width,height
        photo_image = ImageTk.PhotoImage(pil_image)

        photo_image_label = tk.Label(self, image=photo_image)
        photo_image_label.photo = photo_image
        photo_image_label.config(borderwidth=0, relief='solid', highlightbackground='black')
        return photo_image_label

    # https://stackoverflow.com/questions/52714026/python-tkinter-restore-window-without-title-bar
    def frame_mapped(self):
        self.root.update_idletasks()
        self.root.state('normal')
        self.root.overrideredirect(True)

    def minimize(self):
        self.root.update_idletasks()
        self.root.overrideredirect(False)
        self.root.state('iconic')


if __name__ == "__main__":
    root = tk.Tk()
    root.overrideredirect(True)  # turns default title bar
    root.geometry('400x100+200+200')
    root.title('This is literally the title bar')
    app = TitleBar(root, icon_path='../images/icon.png')
    app.pack()
    root.mainloop()
