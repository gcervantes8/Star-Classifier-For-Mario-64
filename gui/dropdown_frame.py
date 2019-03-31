# -*- coding: utf-8 -*-
"""

@author: Gerardo Cervantes
"""

import tkinter as tk
from tkinter.font import Font

class DropdownFrame(tk.Frame):
    
    COLOR = '#47a3cc'
    FONT_SIZE = 20
    FONT = 'Arial'
    
    def __init__(self, master):
        self.root = master
        tk.Frame.__init__(self, master)
        
        self.options = ['?']
        self.drop_down = self.create_drop_down(self, self.options)
        self.drop_down.grid(column = 0, row = 0, columnspan = 2)
        self.change_color(self.COLOR)
        self.font = Font(family = self.FONT, size = self.FONT_SIZE, weight = 'bold')
        self.drop_down.config(font = self.font)
        
    def create_drop_down(self, master, OPTIONS):
        
        self.stringvar = tk.StringVar(master)
        self.stringvar.set(OPTIONS[0]) # default value
        self.drop_down = tk.OptionMenu(master, self.stringvar, *OPTIONS)
        return self.drop_down
    
    #Options is the list of items it will set the dropdown as
    def set_drop_down_options(self, options):
        self.options = list(options)
        
        self.stringvar.set('')
        self.drop_down['menu'].delete(0, 'end')
        for option in self.options:
            self.drop_down['menu'].add_command(label = option, command = tk._setit(self.stringvar, option))
        
        self.stringvar.set(self.options[0]) # default value

    #Sets the given option if found in the list of options in the dropdown
    def set_option(self, option_name):
        
        for option in self.options:
            if option_name == option:
                self.stringvar.set(option)
        
    
    def change_color(self, color):
        self.drop_down.configure(background = color)
        self.configure(background = color)
        
    def change_text_color(self, color):
        self.drop_down.configure(fg = color)
        
    def change_text_size(self, size):
        self.font.configure(size = size)
    
    def change_text_font(self, font_family):
        self.font.configure(family = font_family)

        
if __name__ == "__main__":
    root = tk.Tk()
    root.title('Select route')
    app = DropdownFrame(root)
    app.pack()
    root.mainloop()