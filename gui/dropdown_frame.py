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

    def __init__(self, master, default_value='Select', dropdown_strs=None, set_width=None, clicked_command=None,
                 changed_command=None):
        self.root = master
        tk.Frame.__init__(self, master)
        self.options = [default_value]
        self._string_var = tk.StringVar(master)
        self.drop_down = self.create_drop_down(self, self._string_var, set_width, self.options)
        self.drop_down.grid(column=0, row=0, columnspan=2)
        self.change_color(self.COLOR)
        self.font = Font(family=self.FONT, size=self.FONT_SIZE, weight='bold')
        self.drop_down.config(font=self.font)
        self.drop_down.configure(highlightthickness=0)

        if clicked_command is not None:
            self.drop_down.bind('<Button-1>', clicked_command)
        if changed_command is not None:
            self._string_var.trace('w', lambda *_, var=self._string_var: changed_command(var))

        if dropdown_strs is not None:
            self.set_drop_down_options(dropdown_strs)
        
    def create_drop_down(self, master, string_var, set_width, menu_options):

        string_var.set(menu_options[0])  # default value is the first value
        self.drop_down = tk.OptionMenu(master, string_var, *menu_options)
        if set_width is not None:
            self.drop_down.config(width=set_width)
        return self.drop_down
    
    # Options is the list of items it will set the drop-down as
    def set_drop_down_options(self, options):
        self.options = list(options)
        
        # Delete options
        self.drop_down['menu'].delete(0, 'end')

        if len(self.options) == 0:
            self._string_var.set(self.options[0])  # default value
        else:
            for option in self.options:
                # Private command used to add options at run time
                self.drop_down['menu'].add_command(label=option, command=tk._setit(self._string_var, option))

    # Sets the given option if found in the list of options in the drop-down menu
    def set_option(self, option_name):

        for option in self.options:
            if option_name == option:
                self._string_var.set(option)

    def change_color(self, color):
        self.drop_down.configure(background=color)
        self.configure(background=color)
        self.drop_down['menu'].config(bg=color, fg='white', bd=0)

    def get_selected_option(self):
        return self._string_var.get()

    def change_text_color(self, color):
        self.drop_down.configure(fg=color)
        
    def change_text_size(self, size):
        self.font.configure(size=size)
    
    def change_text_font(self, font_family):
        self.font.configure(family=font_family)

        
if __name__ == "__main__":
    root = tk.Tk()
    root.title('Select route')
    app = DropdownFrame(root)
    app.pack()
    root.mainloop()
