# -*- coding: utf-8 -*-
"""

@author: Gerardo Cervantes
"""

import tkinter as tk
from tkinter.font import Font

class StartButtonFrame(tk.Frame):
    
    START_TEXT = 'START'
    STOP_TEXT = 'STOP'
    COLOR ='#efcf17'
    #Alternates between False and True everytime the button is pressed
    is_running = False
    
    #Function that will be called when button is pressed, takes in 1 parameter, is_running
    notify_fn = None    
    
    
    def __init__(self, master):
        self.root = master
        tk.Frame.__init__(self, master)
        
        #Button text
        self.button_text = tk.StringVar()
        
        #Creates the button
        self.button_text.set(self.START_TEXT)
        self.start_button = tk.Button(self, text = self.button_text, width = 13)
        self.start_button.grid(column = 0, row = 0, columnspan = 2, padx = 1, pady = 1)
        
        fontsize = 20
        font_type = 'Times New Roman'
        self.font = Font(family = font_type, size = fontsize, weight = 'bold')
        
        self.start_button.config(command = self.button_handler, textvariable = self.button_text, background = self.COLOR, foreground = 'black', borderwidth = 2, font = self.font)
        self.update_button_text()
        
        
    #Handler function will be given 2 params, the object and bool indicating if classifer was running before button click
    def set_button_action_handler(self, handler_fn):
        self.notify_fn = handler_fn
#        self.start_button.config(command = handler)
    
    def button_handler(self):
        
        if self.notify_fn != None:
            self.notify_fn(self.is_running)
        
        self.alternate_button()
        
        
    #If button was running, sets to stopped state.  If was in stopped state turns it to running
    #Updates state and text of button
    def alternate_button(self):
        #If was running turns to stopped, if was stopped turns to running
        self.is_running = not self.is_running
        
        #Update button text
        self.update_button_text()
    
    #Updates the button text depending on self.is_running attribute
    def update_button_text(self):
        correct_text = self.STOP_TEXT if self.is_running else self.START_TEXT
        self.button_text.set(correct_text)

    def change_text_color(self, color):
        self.start_button.configure(foreground = color)
        
    def change_color(self, color):
        self.start_button.configure(background = color)
        
    def change_text_size(self, size):
        self.font.configure(size = size)
    
    def change_text_font(self, font_family):
        self.font.configure(family = font_family)
        
    
        
        
if __name__ == "__main__":
    root = tk.Tk()
    root.title('Start!')
    app = StartButtonFrame(root)
    app.pack()
    root.mainloop()