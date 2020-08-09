# -*- coding: utf-8 -*-
"""

@author: Gerardo Cervantes
"""

import tkinter as tk
from gui.title_bar import TitleBar
from gui.dropdown_frame import DropdownFrame

from PIL import ImageTk, Image

# Used code from for basic drag template: https://stackoverflow.com/a/55772675/10062180


class ImageSelect(tk.Frame):

    CANVAS_WIDTH = 1000
    CANVAS_HEIGHT = 600

    # Default selection object options.
    SELECT_OPTS = dict(dash=(2, 2), stipple='gray25', fill='royal blue',
                       outline='')
    is_initialized = False
    str_displayed = None

    def __init__(self, parent, screenshot_taker):
        self.root = parent
        tk.Frame.__init__(self, parent)
        self.screenshot_taker = screenshot_taker

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=15)

        self.dropdown = DropdownFrame(self, default_value='Select Game!', dropdown_strs=['Desktop'], set_width=45,
                                      clicked_command=self.dropdown_clicked, changed_command=self.dropdown_changed)
        self.canvas_frame = tk.Frame(self)

        self.dropdown.grid(column=0, row=0, padx=5, pady=5, sticky='w')
        self.canvas_frame.grid(column=0, row=1, padx=0, pady=0, sticky='nsew')

        # Children of canvas_frame
        self.canvas = tk.Canvas(self.canvas_frame, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT,
                                borderwidth=0, highlightthickness=0, cursor='crosshair')

        vert_scroll_bar = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL)
        horz_scroll_bar = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL)

        vert_scroll_bar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
        horz_scroll_bar.pack(side=tk.BOTTOM, fill=tk.X, expand=False)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        vert_scroll_bar.config(command=self.canvas.yview)
        horz_scroll_bar.config(command=self.canvas.xview)

        # Set the scroll region
        def set_scrollregion(event):
            self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        self.canvas_frame.bind('<Configure>', set_scrollregion)
        self.canvas.is_mouse_in_img = self.is_mouse_in_img
        self.canvas.config(xscrollcommand=horz_scroll_bar.set, yscrollcommand=vert_scroll_bar.set)
        self.canvas.bind_all('<MouseWheel>', self._on_mousewheel)

        # Change image being displayed
        path = 'images/Coordinates.png'
        pil_img = Image.open(path)
        self.change_canvas_image(pil_img)

        # Create selection object to show current selection boundaries.
        self.selection_obj = SelectionObject(self.canvas, self.SELECT_OPTS)

        # Callback function to update given two points of its diagonal.
        def on_drag(start, end, **kwarg):
            self.selection_obj.update(start, end)

        # Create mouse position tracker that uses the function.
        self.posn_tracker = MousePositionTracker(self.canvas)
        self.posn_tracker.autodraw(command=on_drag)  # Enable callbacks.

        # Change mouse cursor on image hover
        self.canvas.bind('<Motion>', self.check_hand)
        self.is_initialized = True

    def _on_mousewheel(self, event):
        scroll_units = int(-1 * (event.delta / 120))
        self.canvas.yview_scroll(scroll_units, 'units')

    def dropdown_clicked(self, event):
        window_and_monitor_names = self.screenshot_taker.get_windows_and_monitors_names()
        self.dropdown.set_drop_down_options(window_and_monitor_names)

    def dropdown_changed(self, str_displayed, *args):
        str_displayed = str_displayed.get()
        print('Previous dropdown op ' + str(self.str_displayed) + ' new op: ' + str(str_displayed))

        is_changed = self.str_displayed is not str_displayed
        if self.is_initialized and is_changed:
            self.str_displayed = str_displayed
            selected_option = self.dropdown.get_selected_option()
            print('Selected option: ' + str(selected_option))
            self.screenshot_taker.select_window(selected_option)
            pil_img = self.screenshot_taker.screenshot_all_window()
            if pil_img is not None:
                self.change_canvas_image(pil_img)

    # https://stackoverflow.com/a/54605894/10062180
    # Checks if mouse cursor is hovering of the image, change to cross-hair cursor if so, image has to be created first
    def check_hand(self, event):  # runs on mouse motion

        if self.is_mouse_in_img(event):
            self.canvas.config(cursor='crosshair')
        else:
            self.canvas.config(cursor='')

    def is_mouse_in_img(self, event):
        bbox = self.canvas.bbox(self.canvas.img_id)
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        # Checks boundaries
        if bbox[0] < x < bbox[2] and bbox[1] < y < bbox[3]:
            return True
        return False

    def change_canvas_image(self, pil_img):
        self.canvas.delete('all')
        photo_img = ImageTk.PhotoImage(pil_img)
        self.canvas.img_id = self.canvas.create_image(0, 0, image=photo_img, anchor=tk.NW)
        self.canvas.img = photo_img
        self.canvas.config(width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)
        self.canvas_frame.config(width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)
        if self.is_initialized:
            self.selection_obj.init_redraw()
            self.posn_tracker.init_redraw()

    def set_new_image(self, new_img):
        self.canvas.img = new_img

    def set_bg_color(self, color):
        self.configure(background=color)
        self.dropdown.change_color(color=color)
        self.canvas.config(background=color)

    def change_text_size(self, size):
        self.dropdown.change_text_size(size)
        self.dropdown.change_text_color('white')

    def change_text_font(self, font_family):
        self.dropdown.change_text_font(font_family)

    def change_dropdown_color(self, dropdown_color):
        self.dropdown.change_color(dropdown_color)

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
        self.start = self.end = self.lines = None
        self._command = None
        self.reset()
        self.init_redraw()

    def init_redraw(self):
        # Create canvas cross-hair lines.
        crosshair_opts = dict(dash=(3, 2), fill='white', width=1.5, state=tk.HIDDEN)
        self.lines = (self.canvas.create_line(0, 0, 0, self.canvas.img.height(), **crosshair_opts),
                      self.canvas.create_line(0, 0, self.canvas.img.width(),  0, **crosshair_opts))

    def cur_selection(self):
        return self.start, self.end

    def _convert_x_coord(self, x):
        x = self.canvas.canvasx(x)
        if x < 0:
            x = 0
        if x > self.canvas.img.width():
            x = self.canvas.img.width() - 1
        return x

    def _convert_y_coord(self, y):
        y = self.canvas.canvasy(y)
        if y < 0:
            y = 0
        if y > self.canvas.img.height():
            y = self.canvas.img.height() - 1
        return y

    def begin(self, event):
        if self.canvas.is_mouse_in_img(event):
            self.hide()
            # Scroll-bar safe mouse coordinates
            x, y = self._convert_x_coord(event.x), self._convert_y_coord(event.y)

            self.start = (x, y)

    def update(self, event):
        # Only if initial click was in the image
        if self.start is not None:
            # Scroll-bar safe mouse coordinates
            x, y = self._convert_x_coord(event.x), self._convert_y_coord(event.y)
            # End is current coordinates being selected
            self.end = (x, y)
            self._update(event)
            self._command(self.start, (x, y))  # User callback.

    def _update(self, event):
        # Scroll-bar safe mouse coordinates
        x, y = self._convert_x_coord(event.x), self._convert_y_coord(event.y)
        # Update cross-hair lines.
        self.canvas.coords(self.lines[0], x, 0, x, self.canvas.img.height())
        self.canvas.coords(self.lines[1], 0, y, self.canvas.img.width(), y)
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
        # Only if initial click was in the image
        if self.start is not None:
            self.hide()  # Hide cross-hairs.
            self.reset()


class SelectionObject:
    """ Widget to display a rectangular area on given canvas defined by two points
        representing its diagonal.
    """

    select_opts2 = dict(fill='', outline='black', width=2, state=tk.HIDDEN)
    select_opts3 = dict(dash=(12, 8), fill='', outline='white', width=2, state=tk.HIDDEN)

    def __init__(self, canvas, select_opts):
        # Create a selection objects for updating.
        self.canvas = canvas
        self.select_opts1 = select_opts
        self.rects = None
        self.init_redraw()
        self.min_x, self.min_y, self.max_x, self.max_y = 0, 0, 0, 0

    # Called when image is changed, canvas redraws the rectangles (Canvas should be cleared before)
    def init_redraw(self):
        # Options for areas outside rectangular selection.
        select_opts1 = self.select_opts1.copy()
        select_opts1.update({'state': tk.HIDDEN})  # Hide initially.
        # Separate options for area inside rectangular selection.

        # Initial extrema of inner and outer rectangles.
        self.min_x, self.min_y,  self.max_x, self.max_y = 0, 0,  1, 1
        omin_x, omin_y,  omax_x, omax_y = 0, 0,  self.canvas.img.width(), self.canvas.img.height()

        self.rects = (
            # Area *outside* selection (inner) rectangle.
            self.canvas.create_rectangle(omin_x, omin_y,  omax_x, self.min_y, **select_opts1),
            self.canvas.create_rectangle(omin_x, self.min_y,  self.min_x, self.max_y, **select_opts1),
            self.canvas.create_rectangle(self.max_x, self.min_y,  omax_x, self.max_y, **select_opts1),
            self.canvas.create_rectangle(omin_x, self.max_y,  omax_x, omax_y, **select_opts1),
            # Inner rectangle. (Black outline)
            self.canvas.create_rectangle(self.min_x, self.min_y, self.max_x, self.max_y, ** self.select_opts2),
            # Inner rectangle. (White dashed outline)
            self.canvas.create_rectangle(self.min_x, self.min_y, self.max_x, self.max_y, ** self.select_opts3)
        )

    def update(self, start, end):
        # Current extrema of inner and outer rectangles.
        self.min_x, self.min_y,  self.max_x, self.max_y = self._get_coords(start, end)
        omin_x, omin_y,  omax_x, omax_y = 0, 0,  self.canvas.img.width(), self.canvas.img.height()

        # Update coords of all rectangles based on these extrema.
        self.canvas.coords(self.rects[0], omin_x, omin_y,  omax_x, self.min_y),
        self.canvas.coords(self.rects[1], omin_x, self.min_y,  self.min_x, self.max_y),
        self.canvas.coords(self.rects[2], self.max_x, self.min_y,  omax_x, self.max_y),
        self.canvas.coords(self.rects[3], omin_x, self.max_y,  omax_x, omax_y),
        self.canvas.coords(self.rects[4], self.min_x, self.min_y,  self.max_x, self.max_y),
        self.canvas.coords(self.rects[5], self.min_x, self.min_y, self.max_x, self.max_y),
        for rect in self.rects:  # Make sure all are now visible.
            self.canvas.itemconfigure(rect, state=tk.NORMAL)

    def get_coordinates(self):

        # min_x and y are the top-left corner
        x = self.min_x
        y = self.min_y

        # max x and y are the bottom-right corner
        x2 = self.max_x
        y2 = self.max_y
        width = x2 - x
        height = y2 - y
        return x, y, width, height

    def _get_coords(self, start, end):
        """ Determine coords of a polygon defined by the start and
            end points one of the diagonals of a rectangular area.
        """
        min_x = min((start[0], end[0]))
        min_y = min((start[1], end[1]))
        max_x = max((start[0], end[0]))
        max_y = max((start[1], end[1]))
        return min_x, min_y, max_x, max_y

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
