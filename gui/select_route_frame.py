# -*- coding: utf-8 -*-
"""

@author: Gerardo Cervantes
"""

import tkinter as tk

class SelectRouteFrame(tk.Frame):
    
    COLOR = '#47a3cc'
    
    def __init__(self, master):
        self.root = master
        tk.Frame.__init__(self, master)
        
        OPTIONS = ['?']
        self.drop_down = self.create_drop_down(self, OPTIONS)
        self.drop_down.grid(column = 0, row = 0, columnspan = 2)
        self.drop_down.configure(background = self.COLOR)
    def create_drop_down(self, master, OPTIONS):
        
        self.stringvar = tk.StringVar(master)
        
        self.stringvar.set(OPTIONS[0]) # default value
        
        self.drop_down = tk.OptionMenu(master, self.stringvar, *OPTIONS)
        return self.drop_down
    
    def set_drop_down_options(self, options):
        self.stringvar.set('')
        drop_down = self.drop_down
        drop_down['menu'].delete(0, 'end')
        for option in options:
            drop_down['menu'].add_command(label = option, command = tk._setit(self.stringvar, option))
        
        self.stringvar.set(list(options)[0]) # default value


        
if __name__ == "__main__":
    root = tk.Tk()
    root.title('Select route')
    app = SelectRouteFrame(root)
    app.pack()
    root.mainloop()