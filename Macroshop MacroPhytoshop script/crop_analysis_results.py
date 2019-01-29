from phytoshop_gui_settings import *
import tkinter as tk
from tkinter import font

class CropAnalysisResults(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.parent = master
        self.title("Crop analysis results")
        self.bounds = {}
        self.messages = {}
        self.create_widgets()
        self.on_crop_override_change()
        
    def quit(self):
        self.destroy()

    def on_crop_override_change(self, *args):
        for base, entry in self.bounds.items():
            # Get bounds
            crop_bounds_str = entry.get()
            crop_bounds = crop_bounds_str.split(",")
            try:
                row_start = int(crop_bounds[0])
                col_start = int(crop_bounds[1])
                row_end = int(crop_bounds[2])
                col_end = int(crop_bounds[3])
                self.parent.get_mask_sequences()[base].set_crop_bounds(crop_bounds_str)
                self.set_message(base, "green", "Resulting Image Size {} x {}".format(row_end - row_start, col_end-col_start))
            except:
                self.set_message(base, "red", "Invalid crop bound")

    def set_message(self, base, color, text):
        self.messages[base]['text'] = text
        self.messages[base]['foreground'] = color

    def create_widgets(self):
        row = 0
        for base, sequence in self.parent.get_mask_sequences().items():
            
            tk.Label(self, font=self.parent.custom_font,
                     text=base).grid(row=row,
                                      column=0,
                                      sticky=tk.W,
                                      padx=self.parent.get_padding(),
                                      pady=self.parent.get_padding())

            
            self.bounds[base] = tk.StringVar()
            self.bounds[base].set(sequence.get_crop_bounds())
            self.bounds[base].trace("w", self.on_crop_override_change)
            
            tk.Entry(self,
                     font=self.parent.custom_font,
                     textvariable=self.bounds[base]).grid(row=row,
                                                          column=1,
                                                          padx=self.parent.get_padding(),
                                                          pady=self.parent.get_padding())

            self.messages[base] = tk.Label(self, font=self.parent.custom_font2, text="")
            self.messages[base].grid(row=row,column=2,sticky=tk.W,
                                     padx=self.parent.get_padding(),
                                     pady=self.parent.get_padding())

            

            row += 1

        tk.Button(self, font=self.parent.custom_font,
                      text="OK",
                  command=self.quit).grid(row=row,
                                          column=1,
                                          padx=self.parent.get_padding(),
                                          pady=self.parent.get_padding())
