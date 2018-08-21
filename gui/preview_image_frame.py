# -*- coding: utf-8 -*-
"""

@author: Gerardo Cervantes
"""

import tkinter as tk
from PIL import ImageTk, Image


#Module in src folder that takes screenshots
from sys import path
path.insert(0, 'src/')
from screenshot_taker import ScreenshotTaker

class PreviewImageFrame(tk.Frame):
    
    #Is a tk.Label containing the image
    photo_image_label = None
    
    x_entry = None
    y_entry = None
    width_entry = None
    height_entry = None
     
    screenshot_instance = None
    
    x_stringvar = None
    y_stringvar = None
    width_stringvar = None
    height_stringvar = None
    
    DEFAULT_IMAGE_PATH = 'images/generated_preview_1.jpeg'
    
    def __init__(self, master):
        self.root = master
        tk.Frame.__init__(self, master)
        
        self.screenshot_instance = ScreenshotTaker()
        
        preview_image_widget = self.create_preview_image(self)
        preview_image_widget.grid(column = 0, row = 0, padx = 1, pady = 5)
        
        self.set_sizes_frame = self.create_set_sizes_frame(self)
        self.set_sizes_frame.grid(column = 0, row = 1)
        
        preview_button = tk.Button(self, text = 'Preview Image')
        preview_button.grid(column = 0, row = 2, padx = 1, pady = 5)
        preview_button.config(command = self.preview_button_clicked)
        

    def create_preview_image(self, master):
        
        self.photo_image_label = tk.Label(master)
        
        #Load default image
        img = Image.open(self.DEFAULT_IMAGE_PATH)
        self.show_image_on_label(img)
        
        self.photo_image_label.config(borderwidth = 0, relief = "solid")
        self.photo_image_label.config(highlightbackground = 'black')
        return self.photo_image_label
        
    def show_image_on_label(self, pil_image):
        pil_image = pil_image.resize((67, 40), Image.ANTIALIAS) #Width,height
        self.img = pil_image
        
        self.photo_image = ImageTk.PhotoImage(pil_image)
        self.photo_image_label.config(image = self.photo_image)
        
    def set_coordinates(self, coordinates):
        x, y, width, height = coordinates.get_coordinates()
        if x != None:
            self.x_stringvar.set(str(x))
        if y != None:
            self.y_stringvar.set(str(y))
        if width != None:
            self.width_stringvar.set(str(width))
        if height != None:
            self.height_stringvar.set(str(height))
        

    def set_bg_color(self, bg_color):
        self.configure(background = bg_color)
        self.set_sizes_frame.configure(background = bg_color)
        self.x_frame.configure(background = bg_color)
        self.y_frame.configure(background = bg_color)
        self.width_frame.configure(background = bg_color)
        self.height_frame.configure(background = bg_color)
        
        self.x_label.configure(background = bg_color)
        self.y_label.configure(background = bg_color)
        self.width_label.configure(background = bg_color)
        self.height_label.configure(background = bg_color)
    
    def create_set_sizes_frame(self, master):
        set_sizes_frame = tk.Frame(master)
        
        self.x_frame, self.x_label, self.x_entry, self.x_stringvar = self.create_label_entry_pair(set_sizes_frame, 'x')
        self.y_frame, self.y_label, self.y_entry, self.y_stringvar = self.create_label_entry_pair(set_sizes_frame, 'y')
        self.width_frame, self.width_label, self.width_entry, self.width_stringvar = self.create_label_entry_pair(set_sizes_frame, 'width')
        self.height_frame, self.height_label, self.height_entry, self.height_stringvar = self.create_label_entry_pair(set_sizes_frame, 'height')
        
        padx = 7
        pady = 8
        self.x_frame.grid(column = 0, row = 0, padx = padx, pady = pady)
        self.y_frame.grid(column = 1, row = 0, padx = padx, pady = pady)
        self.width_frame.grid(column = 2, row = 0, padx = padx, pady = pady)
        self.height_frame.grid(column = 3, row = 0, padx = padx, pady = pady)
        
        return set_sizes_frame
    
    def clear_entries(self):
        self.x_entry.delete(0, 'end')
        self.y_entry.delete(0, 'end')
        self.width_entry.delete(0, 'end')
        self.height_entry.delete(0, 'end')
        
    #Returns tuple with 3 items, tk.frame containing the tk.label and tk.entry, the tk.label, and the tk.entry
    def create_label_entry_pair(self, master, label_text):
        label_entry_frame = tk.Frame(master)
        font_type = 'Times New Roman'
        fontsize = 10
        label = tk.Label(label_entry_frame, text = label_text, font=(font_type, fontsize, 'bold'))
        label.grid(column = 0, row = 0)
        stringvar = tk.StringVar()
        entry = tk.Entry(label_entry_frame, textvariable = stringvar, width = 5, justify='center')
        entry.grid(column = 1, row = 0)
        
        return label_entry_frame, label, entry, stringvar
        
    def get_coordinates(self):
        x_entry_text = self.x_stringvar.get()
        y_entry_text = self.y_stringvar.get()
        width_entry_text = self.width_stringvar.get()
        height_entry_text = self.height_stringvar.get()
        
        return x_entry_text, y_entry_text, width_entry_text, height_entry_text
    
    def are_invalid_coordinates(self, x, y, width, height): 
        return not (self.is_integer(x) and self.is_integer(y) and self.is_integer(width) and self.is_integer(height))
    
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
        
        pil_img = self.screenshot_instance.screenshot_pil(int(x), int(y), int(width), int(height))
        self.show_image_on_label(pil_img)
        
    #Returns coordinates when the frame is closed
    def show(self):
        self.wait_window()
        return self.get_coordinates()

if __name__ == "__main__":
    
    root = tk.Tk()
    root.title('Preview Image Window')
    app = PreviewImageFrame(root)
    app.pack()
    root.mainloop()