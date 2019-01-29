from phytoshop_gui_settings import *
import tkinter as tk
from tkinter import font

class ShadowCropAnalysisResults(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.parent = master
        self.title("Crop analysis results for shadow series")
        self.create_widgets()
        self.on_crop_override_change()
        
    def quit(self):
        self.destroy()

    def on_crop_override_change(self, *args):
        # Get bounds
        crop_bounds_str = self.bounds.get()
        crop_bounds = crop_bounds_str.split(",")
        try:
            row_start = int(crop_bounds[0])
            col_start = int(crop_bounds[1])
            row_end = int(crop_bounds[2])
            col_end = int(crop_bounds[3])
            self.parent.shadows.set_crop_bounds(crop_bounds_str)
            self.set_message("green", "Resulting Image Size {} x {}".format(row_end - row_start, col_end-col_start))
        except:
            self.set_message("red", "Invalid crop bound")

    def set_message(self, color, text):
        self.message['text'] = text
        self.message['foreground'] = color

    def create_widgets(self):
        row = 0
        shadows = self.parent.shadows
        base = shadows.get_base()
        tk.Label(self, font=self.parent.custom_font,
                 text=base).grid(row=row,
                                 column=0,
                                 sticky=tk.W,
                                 padx=self.parent.get_padding(),
                                 pady=self.parent.get_padding())

            
        self.bounds = tk.StringVar()
        self.bounds.set(shadows.get_crop_bounds())
        self.bounds.trace("w", self.on_crop_override_change)
            
        tk.Entry(self,
                 font=self.parent.custom_font,
                 textvariable=self.bounds).grid(row=row,
                                                column=1,
                                                padx=self.parent.get_padding(),
                                                pady=self.parent.get_padding())

        self.message = tk.Label(self, font=self.parent.custom_font2, text="")
        self.message.grid(row=row,column=2,sticky=tk.W,
                          padx=self.parent.get_padding(),
                          pady=self.parent.get_padding())

            

        row += 1

        tk.Button(self, font=self.parent.custom_font,
                  text="OK",
                  command=self.quit).grid(row=row,
                                          column=1,
                                          padx=self.parent.get_padding(),
                                          pady=self.parent.get_padding())
        
