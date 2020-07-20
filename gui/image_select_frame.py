# -*- coding: utf-8 -*-
"""

@author: Gerardo Cervantes
"""

import tkinter as tk
from tkinter.font import Font
from gui.title_bar import TitleBar
from gui.make_draggable import Draggable
from gui.dropdown_frame import DropdownFrame

from PIL import ImageTk, Image

# Module in src folder that takes screenshots
from src.screenshot_taker import ScreenshotTaker

# Used code from: https://stackoverflow.com/a/55772675/10062180


class ImageSelect(tk.Frame):

    CANVAS_WIDTH = 800
    CANVAS_HEIGHT = 600

    # Default selection object options.
    SELECT_OPTS = dict(dash=(2, 2), stipple='gray25', fill='red',
                       outline='')

    def __init__(self, parent, custom_title_bar=True):
        self.root = parent
        tk.Frame.__init__(self, parent)
        if custom_title_bar:
            self.title_bar = TitleBar(self, window_root=parent, width=400, height=5)
            self.title_bar.grid(column=0, row=0, rowspan=1, columnspan=2, padx=2, pady=1)

        path = 'images/Coordinates.png'
        img = ImageTk.PhotoImage(Image.open(path))
        self.canvas_frame = tk.Frame(self, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)
        self.canvas_frame.grid(column=0, row=1, rowspan=10, padx=20, pady=20)

        self.canvas = tk.Canvas(self.canvas_frame, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT,
                                borderwidth=0, highlightthickness=0)
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        self.canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        vert_scroll_bar = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL)
        horz_scroll_bar = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL)

        vert_scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        horz_scroll_bar.pack(side=tk.BOTTOM, fill=tk.X)

        vert_scroll_bar.config(command=self.canvas.yview)
        horz_scroll_bar.config(command=self.canvas.xview)

        self.canvas.config(xscrollcommand=horz_scroll_bar.set, yscrollcommand=vert_scroll_bar.set)

        # Create outline surrounding canvas
        self.canvas.config(highlightbackground='white', highlightthickness=2)

        self.canvas.create_image(0, 0, image=img, anchor=tk.NW)
        self.canvas.img = img  # Keep reference.
        self.canvas.bind_all('<MouseWheel>', self._on_mousewheel)
        self.dropdown = DropdownFrame(self, dropdown_strs=['Desktop'], set_width=12, command=self.dropdown_changed)
        self.dropdown.grid(column=1, row=1, padx=5, pady=3)

        # self. = tk.Button(self)
        # self.dropdown.grid(column=1, row=0, padx=5, pady=3)

        # Create selection object to show current selection boundaries.
        self.selection_obj = SelectionObject(self.canvas, self.SELECT_OPTS)

        # Callback function to update it given two points of its diagonal.
        def on_drag(start, end, **kwarg):  # Must accept these arguments.
            self.selection_obj.update(start, end)

        # Create mouse position tracker that uses the function.
        self.posn_tracker = MousePositionTracker(self.canvas)
        self.posn_tracker.autodraw(command=on_drag)  # Enable callbacks.

    def _on_mousewheel(self, event):
        scroll_units = int(-1 * (event.delta / 120))
        self.canvas.yview_scroll(scroll_units, 'units')

    def dropdown_changed(self, *args):

        # window_selected = self.dropdown.get_selected_option()
        screenshot_taker = ScreenshotTaker()
        width = 1920
        height = 1080
        pil_img, _ = screenshot_taker.screenshot_mss(0, 0, width, height)
        self.canvas.img = ImageTk.PhotoImage(pil_img)
        self.canvas.create_image(0, 0, image=self.canvas.img, anchor=tk.NW)
        # print(self.canvas.keys())
        self.canvas.config(width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)
        self.canvas_frame.config(width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)
        print('Screenshot changed')

    def set_new_image(self, new_img):
        self.canvas.img = new_img

    def set_bg_color(self, color):
        self.configure(background=color)
        self.dropdown.change_color(color=color)

    def change_text_size(self, size):
        self.dropdown.change_text_size(size)
        self.dropdown.change_text_color('white')

    def change_text_font(self, font_family):
        self.dropdown.change_text_font(font_family)

    def get_coordinates(self):
        return self.selection_obj.get_coordinates()

    # Returns coordinates when the frame is closed
    def show(self):
        self.wait_window()
        return self.get_coordinates()


class MousePositionTracker:
    """ Tkinter Canvas mouse position widget. """

    def __init__(self, canvas):
        self.canvas = canvas
        self.canv_width = self.canvas.cget('width')
        self.canv_height = self.canvas.cget('height')
        self.reset()

        # Create canvas cross-hair lines.
        xhair_opts = dict(dash=(3, 2), fill='white', state=tk.HIDDEN)
        self.lines = (self.canvas.create_line(0, 0, 0, self.canv_height, **xhair_opts),
                      self.canvas.create_line(0, 0, self.canv_width,  0, **xhair_opts))

    def cur_selection(self):
        return self.start, self.end

    def begin(self, event):
        self.hide()
        # Scroll-bar safe mouse coordinates
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        self.start = (x, y)

    def update(self, event):
        # Scroll-bar safe mouse coordinates
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        self.end = (x, y)
        self._update(event)
        self._command(self.start, (x, y))  # User callback.

    def _update(self, event):
        # Scroll-bar safe mouse coordinates
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        # Update cross-hair lines.
        self.canvas.coords(self.lines[0], x, 0, x, self.canv_height)
        self.canvas.coords(self.lines[1], 0, y, self.canv_width, y)
        self.show()

    def reset(self):
        self.start = self.end = None

    def hide(self):
        self.canvas.itemconfigure(self.lines[0], state=tk.HIDDEN)
        self.canvas.itemconfigure(self.lines[1], state=tk.HIDDEN)

    def show(self):
        self.canvas.itemconfigure(self.lines[0], state=tk.NORMAL)
        self.canvas.itemconfigure(self.lines[1], state=tk.NORMAL)

    def autodraw(self, command=lambda *args: None):
        """Setup automatic drawing; supports command option"""
        self.reset()
        self._command = command
        self.canvas.bind("<Button-1>", self.begin)
        self.canvas.bind("<B1-Motion>", self.update)
        self.canvas.bind("<ButtonRelease-1>", self.quit)

    def quit(self, event):
        self.hide()  # Hide cross-hairs.
        self.reset()


class SelectionObject:
    """ Widget to display a rectangular area on given canvas defined by two points
        representing its diagonal.
    """
    def __init__(self, canvas, select_opts):
        # Create a selection objects for updating.
        self.canvas = canvas
        self.select_opts1 = select_opts
        self.width = self.canvas.cget('width')
        self.height = self.canvas.cget('height')

        # Options for areas outside rectangular selection.
        select_opts1 = self.select_opts1.copy()
        select_opts1.update({'state': tk.HIDDEN})  # Hide initially.
        # Separate options for area inside rectangular selection.
        select_opts2 = dict(dash=(2, 2), fill='', outline='white', state=tk.HIDDEN)

        # Initial extrema of inner and outer rectangles.
        self.imin_x, self.imin_y,  self.imax_x, self.imax_y = 0, 0,  1, 1
        omin_x, omin_y,  omax_x, omax_y = 0, 0,  self.width, self.height

        self.rects = (
            # Area *outside* selection (inner) rectangle.
            self.canvas.create_rectangle(omin_x, omin_y,  omax_x, self.imin_y, **select_opts1),
            self.canvas.create_rectangle(omin_x, self.imin_y,  self.imin_x, self.imax_y, **select_opts1),
            self.canvas.create_rectangle(self.imax_x, self.imin_y,  omax_x, self.imax_y, **select_opts1),
            self.canvas.create_rectangle(omin_x, self.imax_y,  omax_x, omax_y, **select_opts1),
            # Inner rectangle.
            self.canvas.create_rectangle(self.imin_x, self.imin_y,  self.imax_x, self.imax_y, **select_opts2)
        )

    def update(self, start, end):
        # Current extrema of inner and outer rectangles.
        self.imin_x, self.imin_y,  self.imax_x, self.imax_y = self._get_coords(start, end)
        omin_x, omin_y,  omax_x, omax_y = 0, 0,  self.width, self.height

        # Update coords of all rectangles based on these extrema.
        self.canvas.coords(self.rects[0], omin_x, omin_y,  omax_x, self.imin_y),
        self.canvas.coords(self.rects[1], omin_x, self.imin_y,  self.imin_x, self.imax_y),
        self.canvas.coords(self.rects[2], self.imax_x, self.imin_y,  omax_x, self.imax_y),
        self.canvas.coords(self.rects[3], omin_x, self.imax_y,  omax_x, omax_y),
        self.canvas.coords(self.rects[4], self.imin_x, self.imin_y,  self.imax_x, self.imax_y),

        for rect in self.rects:  # Make sure all are now visible.
            self.canvas.itemconfigure(rect, state=tk.NORMAL)

    def get_coordinates(self):

        # imin_x and y are the top-left corner
        x = self.imin_x
        y = self.imin_y

        # imax x and y are the bottom-right corner
        x2 = self.imax_x
        y2 = self.imax_y

        width = x2 - x
        height = y2 - y
        return x, y, width, height

    def _get_coords(self, start, end):
        """ Determine coords of a polygon defined by the start and
            end points one of the diagonals of a rectangular area.
        """
        return (min((start[0], end[0])), min((start[1], end[1])),
                max((start[0], end[0])), max((start[1], end[1])))

    def hide(self):
        for rect in self.rects:
            self.canvas.itemconfigure(rect, state=tk.HIDDEN)


if __name__ == "__main__":
    WIDTH, HEIGHT = 900, 900
    BACKGROUND = 'grey'
    TITLE = 'Image Cropper'

    root = tk.Tk()
    root.title(TITLE)
    # root.geometry('%sx%s' % (WIDTH, HEIGHT))
    root.configure(background=BACKGROUND)

    app = ImageSelect(root)

    app.pack()
    app.mainloop()
