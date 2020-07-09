# -*- coding: utf-8 -*-
"""

@author: Gerardo Cervantes
"""

import tkinter as tk
from tkinter.font import Font


class ProgressDisplayFrame(tk.Frame):
    star_label = None
    prediction_label = None
    probability_label = None
    time_label = None

    star_display = ''
    prediction_str = ''
    probability_str = ''
    time_str = ''

    #    COLOR = '#47a3cc'
    FONT_SIZE = 20
    FONT = 'Arial'

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.root = master
        self.font = Font(family=self.FONT, size=self.FONT_SIZE, weight='bold')
        self.info_frame = self.create_information_frame(self)
        self.info_frame.grid(column=0, row=0)
        self.update_gui()

    def create_information_frame(self, master):
        info_frame = tk.Frame(master)

        star_frame, _, self.star_label = self.create_labels_pair(info_frame, 'Aim split')
        prediction_frame, _, self.prediction_label = self.create_labels_pair(info_frame, 'Aim fadeout')
        probability_frame, _, self.probability_label = self.create_labels_pair(info_frame, 'Certainty')
        time_frame, _, self.time_label = self.create_labels_pair(info_frame, 'Pred')

        self.update_information('0', -1, 0.0, 0.0)

        padx = 5
        pady = 3
        star_frame.grid(column=0, row=0, padx=padx, pady=pady)
        prediction_frame.grid(column=0, row=1, padx=padx, pady=pady)
        probability_frame.grid(column=0, row=2, padx=padx, pady=pady)
        time_frame.grid(column=0, row=3, padx=padx, pady=pady)

        return info_frame

    def clear_progress_display(self):
        self.star_display = ''
        self.prediction_str = ''
        self.probability_str = ''
        self.time_str = ''
        self.update_gui()

    # Returns tuple with 3 items, tk.frame containing the both tk.labels, the tk.label with description,
    # and the tk.label with the information
    def create_labels_pair(self, master, label_text):
        labels_frame = tk.Frame(master)
        label_width = 4
        description_width = 10
        label_description = tk.Label(labels_frame, width=description_width, text=label_text, font=self.font)
        label_description.grid(column=0, row=0)

        label_info = tk.Label(labels_frame, width=label_width, text='  ', font=self.font)
        label_info.grid(column=1, row=0)

        return labels_frame, label_description, label_info

    def update_gui(self):
        # Only update if they are being shown
        self.update_label(self.star_label, self.star_display)
        self.update_label(self.prediction_label, self.prediction_str)
        self.update_label(self.probability_label, self.probability_str)
        self.update_label(self.time_label, self.time_str)

        self.after(500, self.update_gui)

    def update_label(self, label, text):
        # Only update if they are being shown
        if label != None:
            label.config(text=text)

    def change_color(self, color):
        self.info_frame.configure(bg=color)

    def change_text_size(self, size):
        self.font.configure(size=size)

    def change_text_font(self, font_family):
        self.font.configure(family=font_family)

    # Star is an integer. Prediction, probability, and time are floats
    def update_information(self, star, prediction, probability, time):
        #        star_display = 0 if star == -1 else star
        self.star_display = str(star)
        #        self.prediction_str = 'N/A' if prediction == -1 else str(prediction)
        self.prediction_str = str(prediction)

        self.probability_str = "{0:.3f}".format(probability)
        #        self.time_str =  "{0:.3f}".format(time) + 's'
        self.time_str = str(time)


if __name__ == "__main__":
    root = tk.Tk()
    root.title('Progress Display Window')
    app = ProgressDisplayFrame(root)
    app.pack()
    root.mainloop()
