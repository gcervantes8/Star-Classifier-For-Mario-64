# -*- coding: utf-8 -*-
"""
Created on July 10 2020

@author: Gerardo Cervantes
"""


class Draggable:

    def __init__(self, tk_frame, window_root):
        # Defaults
        self.mouse_start_x = 0
        self.mouse_start_y = 0
        self.win_start_x = 0
        self.win_start_y = 0

        self.tk_frame = tk_frame
        self.window_root = window_root
        self.make_draggable()

    def make_draggable(self):
        self.tk_frame.bind('<Button-1>', self.get_initial_drag_pos)
        self.tk_frame.bind('<B1-Motion>', self.move_window)

    def get_initial_drag_pos(self, event):
        self.mouse_start_x = event.x_root
        self.mouse_start_y = event.y_root
        self.win_start_x = self.window_root.winfo_x()
        self.win_start_y = self.window_root.winfo_y()

    def move_window(self, event):
        mouse_x, mouse_y = event.x_root, event.y_root
        displaced_x = mouse_x - self.mouse_start_x
        displaced_y = mouse_y - self.mouse_start_y
        new_win_x = self.win_start_x + displaced_x
        new_win_y = self.win_start_y + displaced_y
        self.window_root.geometry('+{0}+{1}'.format(new_win_x, new_win_y))
