# -*- coding: utf-8 -*-
"""
Created on Sat Aug 11 09:13:41 2018

@author: Gerardo Cervantes
"""


import tkinter as tk

class InputSplitKeys(tk.Frame):
    
    hotkeys = None
    
    def __init__(self, master):
        self.root = master
        tk.Frame.__init__(self, master)

        split_keys_frame = self.create_split_keys_frame(self)
        split_keys_frame.grid(column = 0, row = 0, columnspan = 2, padx = 1, pady = 5)
    
    #Updates self.hotkeys variable with what's on the entries
    def update_hotkeys(self):
        split_key = self.split_stringvar.get()
#        reset_key = self.reset_springvar.get()
        
        if self.hotkeys != None:
            self.hotkeys.set_split_key(split_key)
#            self.hotkeys.set_reset_key(reset_key)
            
    def create_split_keys_frame(self, master):
        split_keys_frame = tk.Frame(master)
        
        self.split_frame, _, self.split_entry, self.split_stringvar = self.create_label_entry_pair(split_keys_frame, 'Split Key ')
#        self.reset_frame, _, self.reset_entry, self.reset_springvar = self.create_label_entry_pair(split_keys_frame, 'Reset Key')
        
        self.split_frame.grid(column = 0, row = 0)
#        self.reset_frame.grid(column = 0, row = 1)
        
        if self.hotkeys != None:
            self.split_entry.insert(0, self.hotkeys.get_split_key())
            self.reset_entry.insert(0, self.hotkeys.get_reset_key())

        return split_keys_frame
    
    
    def set_bg_color(self, bg_color):
        self.configure(background = bg_color)
        self.split_frame.configure(background = bg_color)
#        self.reset_frame.configure(background = bg_color)
    def set_hotkeys(self, hotkeys):
        self.hotkeys = hotkeys
        
        self.clear_entries()
        
        self.split_entry.insert(0, self.hotkeys.get_split_key())
#        self.reset_entry.insert(0, self.hotkeys.get_reset_key())
    
    #Clears the entry items
    def clear_entries(self):
        self.split_entry.delete(0, 'end')
#        self.reset_entry.delete(0, 'end')
    
    #Returns tuple with 3 items, tk.frame containing the tk.label and tk.entry, the tk.label, and the tk.entry
    def create_label_entry_pair(self, master, label_text):
        label_entry_frame = tk.Frame(master)
        font_type = 'Times New Roman'
        fontsize = 10
        label = tk.Label(label_entry_frame, text = label_text, font=(font_type, fontsize, 'bold'))
        label.grid(column = 0, row = 0, padx = 5, pady = 3)
        stringvar = tk.StringVar()
        entry = tk.Entry(label_entry_frame, textvariable = stringvar, width = 11, justify = 'center')
        entry.grid(column = 1, row = 0, padx = 5, pady = 3)
        
        return label_entry_frame, label, entry, stringvar
        
    def show(self):
        self.wait_window()
        self.update_hotkeys()
        
if __name__ == "__main__":
    root = tk.Tk()
    root.title('Select route')
    app = InputSplitKeys(root)
    app.grid(column = 0, row = 0, columnspan = 2, padx = 1, pady = 5)
    root.mainloop()