# -*- coding: utf-8 -*-
"""

@author: Gerardo Cervantes
"""

import tkinter as tk
from tkinter.font import Font
from tkinter import messagebox
from gui.preview_image_frame import PreviewImageFrame
from gui.progress_display_frame import ProgressDisplayFrame
from gui.dropdown_frame import DropdownFrame
from gui.run_status_frame import RunStatusFrame
from gui.input_split_keys_frame import InputSplitKeys
from gui.start_button_frame import StartButtonFrame
from gui.title_bar import TitleBar
from gui.make_draggable import Draggable

from threading import Thread

from src.auto_splitter import AutoSplitter
from src.coordinates import Coordinates
from src.hotkeys import Hotkeys
from src.shared_preferences import SharedPreferences
from src.route_file_handler import RouteFileHandler
from src.splitter import Splitter


class MainWindow(tk.Frame):
    
    # Path to file including file name to file that will contain preferences.  Last saved items
    PREFERENCES_FILE_NAME = 'preferences.zd'
    
    coordinates = None
    hotkeys = None
    route_name = ''
    
    shared_preferences = None
    icon_path = 'images/icon.png'
    routes_directory = 'routes/'
    
    BG_COLOR = '#192133'
    ALT_BG_COLOR = '#263863'
    TEXT_COLOR = '#edebea'
    BLACK_TEXT_COLOR = '#000a23'
    FONT = 'Helvetica'
    FONT_SIZE = 13
    CONFIG_BUTTON_COLORS = '#0f913a'
    DROPDOWN_COLOR = ALT_BG_COLOR
    START_BUTTON_COLOR = '#dbb015'

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.root = master
        self.auto_splitter = AutoSplitter()
        self.shared_preferences = SharedPreferences()
        self.coordinates, self.route_name, self.hotkeys = self.read_preferences(self.PREFERENCES_FILE_NAME)
        master.configure(background=self.BG_COLOR)
        self.configure(background=self.BG_COLOR)
        self._init_preferences()
        self.draggable = Draggable(self.root, self.root)
        self.font = Font(family=self.FONT, size=self.FONT_SIZE, weight='bold')

        # Creates frames
        self.title_bar = TitleBar(master, width=345)
        self.progress_display_frame = ProgressDisplayFrame(master)
        self.select_route_frame = DropdownFrame(master)
        self.run_status_frame = RunStatusFrame(master)
        self.start_button = StartButtonFrame(master)
        
        self.start_button.set_button_action_handler(self.start_clicked)
        
        self.start_button.change_color(self.START_BUTTON_COLOR)
        self.start_button.change_text_color(self.BLACK_TEXT_COLOR)
        self.start_button.change_text_size(self.FONT_SIZE + 13)
        self.start_button.change_text_font(self.FONT)
        
        self.select_route_frame.change_color(self.DROPDOWN_COLOR)
        self.select_route_frame.change_text_color(self.TEXT_COLOR)
        self.select_route_frame.change_text_size(self.FONT_SIZE)
        self.select_route_frame.change_text_font(self.FONT)
        
        self.progress_display_frame.change_color(self.BG_COLOR)
        self.progress_display_frame.change_text_size(self.FONT_SIZE)
        self.progress_display_frame.change_text_font(self.FONT)

        set_coordinates_popup_button = tk.Button(master, text='Coordinates', width=13, font=self.font,
                                                 command=self.popup_image_coordinates,
                                                 background=self.CONFIG_BUTTON_COLORS, foreground=self.TEXT_COLOR)
        split_keys_popup_button = tk.Button(master, text='Setup keys', width=13, font=self.font,
                                            command=self.popup_split_keys, background=self.CONFIG_BUTTON_COLORS,
                                            foreground=self.TEXT_COLOR)
        manual_split_button = tk.Button(master, text='Manual Split', width=13, font=self.font, command=self.manual_split,
                                        background=self.CONFIG_BUTTON_COLORS, foreground=self.TEXT_COLOR)
        self.progress_display_frame.config(borderwidth=2)

        self.title_bar.grid(column=0, row=0, rowspan=1, columnspan=3, padx=2, pady=1)
        self.select_route_frame.grid(column=0, row=1, columnspan=2, padx=5, pady=5)
        self.start_button.grid(column=0, row=2, columnspan=2, padx=5, pady=5)
        
        self.progress_display_frame.grid(column=2, row=1, rowspan=3, padx=5, pady=5)
        self.run_status_frame.grid(column=2, row=4, padx=0, pady=2)
        set_coordinates_popup_button.grid(column=0, row=4, rowspan=2, padx=0, pady=1)
        split_keys_popup_button.grid(column=1, row=4, rowspan=2, padx=0, pady=1)
        manual_split_button.grid(column=0, row=6, rowspan=2, padx=0, pady=1)
        route_handler = RouteFileHandler()
        # Returns a list of route objects from route directory
        routes = route_handler.get_routes_from_directory(self.routes_directory)
        self.route_dict = self.create_route_dictionary(routes)
        self.select_route_frame.set_drop_down_options(self.route_dict.keys())
        self.select_route_frame.set_option(self.route_name)
    
    def popup_image_coordinates(self):
        popup_master = tk.Toplevel(self.root)
        coordinates = self.coordinates
        self.preview_image = PreviewImageFrame(popup_master)
        self.preview_image.set_coordinates(coordinates)
        self.preview_image.set_bg_color(self.BG_COLOR)
        self.preview_image.change_text_color(self.TEXT_COLOR)
        self.preview_image.change_text_size(self.FONT_SIZE)
        self.preview_image.change_text_font(self.FONT)
        self.preview_image.grid(column=0, row=0, columnspan=2, padx=0, pady=0)
        self.load_icon(app.icon_path, popup_master)
        x, y, width, height = self.preview_image.show()
        coordinates.set_coordinates(x, y, width, height)
        self.save_classifier_preferences(self.PREFERENCES_FILE_NAME)
        
    def popup_split_keys(self):
        popup_master = tk.Toplevel(self.root)
        self.split_keys = InputSplitKeys(popup_master)
        self.split_keys.set_hotkeys(self.hotkeys)
        self.split_keys.set_bg_color(self.BG_COLOR)
        self.split_keys.set_alt_color(self.ALT_BG_COLOR)
        self.split_keys.change_text_color(self.TEXT_COLOR)
        self.split_keys.change_text_size(self.FONT_SIZE)
        self.split_keys.change_text_font(self.FONT)
        self.split_keys.grid(column=0, row=0, columnspan=2, padx=0, pady=0)
        self.load_icon(app.icon_path, popup_master)
        self.split_keys.show()
        self.save_classifier_preferences(self.PREFERENCES_FILE_NAME)
        
    def popup_msg(self, title, msg):
        messagebox.showwarning(title, msg)
    
    # Key is the name of the route, value is the class
    def create_route_dictionary(self, routes):
        route_dict = {}
        for route in routes:
            route_dict[route.get_name()] = route
            
        return route_dict
        
    # Initializes the coordinates and hot-keys used from last session
    # If first time using application, then initializes with default values
    def _init_preferences(self):
        # If there wasn't any previous saved data on coordinates or coordinates last used, creates new
        if not self.coordinates:
            self.coordinates = Coordinates()
            
        if not self.hotkeys:
            self.hotkeys = Hotkeys()
            
        self._set_coordinates(self.coordinates)
        self._set_hotkeys(self.hotkeys)
        
    # Sets new hot-keys to be used in the classifier
    def _set_hotkeys(self, hotkeys):
        self.hotkeys = hotkeys
        self.auto_splitter.hotkeys = hotkeys
        
    # Sets new coordinates to be used in the classifier
    def _set_coordinates(self, coordinates):
        self.coordinates = coordinates
        self.auto_splitter.coordinates = coordinates
        
    # Called when start button is clicked
    # Stops classifier if was previously running, or starts if it wasn't
    # param was_running should be true if the neural network was running
    def start_clicked(self, was_running):
        # Route used is the one that was selected
        self.route_name = self.select_route_frame.get_selected_option()
        
        if was_running:
            self.auto_splitter.stop()
            self.run_status_frame.set_stopped()
        else:
            try:
                route = self.route_dict[self.route_name]
                print('Route: ', self.route_name)
                self.run_status_frame.set_loading()
                thread = Thread(target=self.start_auto_splitter, args=(route,))
                thread.start()
            except KeyError:
                self.popup_msg('Warning', 'Route not found')

    def manual_split(self):
        splitter = Splitter()
        split_key, _ = self.hotkeys.get_hotkeys()
        splitter.split(split_key, 0)

    # Starts the image classifier
    def start_auto_splitter(self, route):
        self.auto_splitter.start(route, self.progress_display_frame.update_information,
                                 start_fn=self.run_status_frame.set_running)

    def save_classifier_preferences(self, file_name):
        route_name = self.select_route_frame.get_selected_option()
        self.shared_preferences.write_preferences(file_name, self.coordinates, route_name, self.hotkeys)

    def read_preferences(self, file_name):
        coordinates, route_name, hotkeys = self.shared_preferences.parse_xml(file_name)
        return coordinates, route_name, hotkeys

    # Changes icon on the title bar of the window to given image
    # Takes the file path, and the tk toplevel window
    def load_icon(self, filepath, root):
        from PIL import ImageTk
        self.img = ImageTk.PhotoImage(file=filepath)
        root.tk.call('wm', 'iconphoto', root._w, self.img)
        
    def on_closing(self):
        self.save_classifier_preferences(self.PREFERENCES_FILE_NAME)
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.title('Star Classifier')
    app = MainWindow(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.state('normal')
    app.load_icon(app.icon_path, root)
    root.mainloop()
    root.quit()
