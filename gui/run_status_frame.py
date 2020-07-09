# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 22:29:14 2018

@author: Gerardo Cervantes
"""

import tkinter as tk


class RunStatusFrame(tk.Frame):

    def __init__(self, master):
        self.root = master
        tk.Frame.__init__(self, master, height=20, width=25, borderwidth=1, relief="solid")
        self.set_stopped()

    def set_running(self):
        self.configure(background='green')

    def set_loading(self):
        self.configure(background='yellow')

    def set_stopped(self):
        self.configure(background='red')


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x300")
    root.title('Preview Image Window')
    app = RunStatusFrame(root)
    app.pack()
    root.mainloop()
