# -*- coding: utf-8 -*-
"""

@author: Gerardo Cervantes
"""

import tkinter as tk
import sys

sys.path.insert(0, 'gui')
from preview_image_frame import PreviewImageFrame
from progress_display_frame import ProgressDisplayFrame
from select_route_frame import SelectRouteFrame
from run_status_frame import RunStatusFrame
from input_split_keys_frame import InputSplitKeys
from start_button_frame import StartButtonFrame

sys.path.insert(0, 'src')
from threading import Thread

from star_classifier import StarClassifier
from coordinates import Coordinates
from hotkeys import Hotkeys
from shared_preferences import SharedPreferences
from route_file_handler import RouteFileHandler

class MainWindow(tk.Frame):
    
    #Path to file including file name to file that will contain preferences.  Last saved items
    PREFERENCES_FILE_NAME = 'preferences.zd'
    
    coordiantes = None
    hotkeys = None
    route_name = ''
    
    shared_preferences = None
    icon_path = 'images/icon.png'
    routes_directory = 'routes/'
    
    bg_color = '#47a3cc'
    
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.root = master
        self.star_classifier = StarClassifier()
        self.shared_preferences = SharedPreferences()
        
        self.coordinates, route_name, self.hotkeys = self.read_preferences(self.PREFERENCES_FILE_NAME)
        
        master.configure(background = self.bg_color)
        self._init_preferences()
        
        
        #Creates frames
        self.progress_display_frame = ProgressDisplayFrame(master)
        self.select_route_frame = SelectRouteFrame(master)
        self.run_status_frame = RunStatusFrame(master)
        self.start_button = StartButtonFrame(master)
        
        self.start_button.set_button_action_handler(self.start_clicked)
        
        setup_button_colors = '#0fba00'
        set_coordinates_popup_button = tk.Button(master, text = 'Coordinates', width = 13, command = self.popup_image_coordinates, background = setup_button_colors)
        split_keys_popup_button = tk.Button(master, text = 'Setup keys', width = 13, command = self.popup_split_keys, background = setup_button_colors)
        
        self.progress_display_frame.config(borderwidth = 2)
        
        self.select_route_frame.grid(column = 0, row = 0, columnspan = 2, padx = 5, pady = 5)
        self.start_button.grid(column = 0, row = 1, columnspan = 2, padx = 5, pady = 5)
        
        self.progress_display_frame.grid(column = 3, row = 0, rowspan = 2, padx = 5, pady = 5) #, columnspan = 3, rowspan=3, 
        self.run_status_frame.grid(column = 3, row = 3, padx = 0, pady = 2)
        set_coordinates_popup_button.grid(column = 0, row = 2, rowspan = 2, padx = 0, pady = 1)
        split_keys_popup_button.grid(column = 1, row = 2, rowspan = 2, padx = 0, pady = 1)
        
        route_handler = RouteFileHandler()
        routes = route_handler.get_routes_from_directory(self.routes_directory)
        
        self.route_dict = self.create_route_dictionary(routes)
        self.select_route_frame.set_drop_down_options(self.route_dict.keys())
    
    def popup_image_coordinates(self):
        popup_master = tk.Toplevel(self.root)
        coordinates = self.coordinates
        self.preview_image = PreviewImageFrame(popup_master)
        self.preview_image.set_coordinates(coordinates)
        self.preview_image.set_bg_color(self.bg_color)
        self.preview_image.grid(column = 0, row = 0, columnspan = 2, padx = 1, pady = 1)
        self.load_icon(app.icon_path, popup_master)
        x, y, width, height = self.preview_image.show()
        coordinates.set_coordinates(x, y, width, height)
        self.save_classifier_preferences(self.PREFERENCES_FILE_NAME)
        
        
    def popup_split_keys(self):
        popup_master = tk.Toplevel(self.root)
        self.split_keys = InputSplitKeys(popup_master)
        self.split_keys.set_hotkeys(self.hotkeys)
        self.split_keys.set_bg_color(self.bg_color)
        self.split_keys.grid(column = 0, row = 0, columnspan = 2, padx = 1, pady = 0)
        self.load_icon(app.icon_path, popup_master)
        self.split_keys.show()
        self.save_classifier_preferences(self.PREFERENCES_FILE_NAME)
        
    
    #Key is the name of the route, value is the class
    def create_route_dictionary(self, routes):
        route_dict = {}
        for route in routes:
            route_dict[route.get_name()] = route
            
        return route_dict
        
    def _init_preferences(self):
        #If there wasn't any previous saved data on coordiantes or coordinates last used, creates new
        if self.coordinates == None:
            self.coordinates = Coordinates()
            
        if self.hotkeys == None:
            self.hotkeys = Hotkeys()
            
        self._set_coordinates(self.coordinates)
        self._set_hotkeys(self.hotkeys)
        
    def _set_hotkeys(self, hotkeys):
        self.hotkeys = hotkeys
        self.star_classifier.set_hotkeys(hotkeys)
        
    def _set_coordinates(self, coordinates):
        self.coordinates = coordinates
        self.star_classifier.set_coordinates(coordinates)
        
    #Uses route from selectroute window
    #was_running is true if the neural network was running
    def start_clicked(self, was_running):
        
        if was_running:
            self.star_classifier.stop()
            self.run_status_frame.set_stopped()
        else:
            self.run_status_frame.set_loading()
            route_name = self.select_route_frame.stringvar.get()
            thread = Thread(target = self.start_auto_splitter, args = (route_name,))
            thread.start()
        
    #Starts the star_classifier
    def start_auto_splitter(self, route_name):
        
        route = self.route_dict[route_name]
        print('Route: ', route_name)
    
        progress_display_frame = self.progress_display_frame
        self.star_classifier.start(route, progress_display_frame.update_information, start_fn = self.run_status_frame.set_running)
    
    def save_classifier_preferences(self, file_name):
        self.shared_preferences.write_preferences(file_name, self.coordinates, self.route_name, self.hotkeys)
        
    def read_preferences(self, file_name):
        coordinates, route_name, hotkeys = self.shared_preferences.parse_xml(file_name)
        return coordinates, route_name, hotkeys

    #Changes icon on the title bar of the window to given image
    #Takes the file path, and the tk toplevel window
    def load_icon(self, filepath, root):
        from PIL import ImageTk
        self.img = ImageTk.PhotoImage(file = filepath)
        root.tk.call('wm', 'iconphoto', root._w, self.img)
        
if __name__ == "__main__":
    root = tk.Tk()
    root.title('Star Classifier')
    app = MainWindow(root)
    app.load_icon(app.icon_path, root)
    root.mainloop()
    root.quit()