from phytoshop_gui_settings import *
import tkinter as tk
import os
from tkinter import font
import re

class ExcludePartsDialog(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.parent = master
        self.title("Exclude Part from expansion")

        self.canvas = tk.Canvas(self, borderwidth=0)
        self.frame = tk.Frame(self.canvas)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw", 
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.create_widgets()
        self.load_entries()
        
    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def quit(self):
        self.save_entries()
        self.destroy()

        
    def load_entries(self):
        try:
            path = os.path.join(self.parent.get_expand_directory(),
                                "excluded.csv")
            with open(path, 'r') as f:
                entries = f.readlines()
            for i, line in enumerate(entries):
                s = line.replace('\n','')
                self.entries[i].set(s)
                    
        except:
            pass

    def save_entries(self):
        out = ""
        for entry in self.entries:
            out += '{}\n'.format(entry.get())
            
        path = os.path.join(self.parent.get_expand_directory(),
                                "excluded.csv")
        with open(path, 'w') as f:
            f.write(self.parent.mac_csv(out))
                
        parts = self.parent.exclude_parts.copy()
        for i, part in enumerate(parts):
            if self.entries[i].get() == 0:
                self.parent.exclude_parts.remove(parts[i])

            
    def create_widgets(self):
        frame = self.frame
        row = 0
        col = 0
        labels = ["Part","Exclude"]
        for label in labels:
            tk.Label(frame, font=self.parent.custom_font,
                     text=label).grid(row=row,
                                      column=col,
                                      sticky=tk.W,
                                      padx=self.parent.get_padding(),
                                      pady=self.parent.get_padding())
            col +=1

        # Generate table entries
        self.entries = []
        for part in self.parent.exclude_parts:
            row += 1
            col = 0
            tk.Label(frame,
                     font=self.parent.custom_font,
                     text=part).grid(row=row,
                                     column=col,
                                     sticky=tk.W,
                                     padx=self.parent.get_padding(),
                                     pady=self.parent.get_padding())
            # Entries
            col = 1
            entry = tk.IntVar()
            self.entries.append(entry)
            tk.Checkbutton(frame,
                           font=self.parent.custom_font,
                           text="",
                           variable=entry).grid(row=row,
                                                column=col,
                                                padx=self.parent.get_padding(),
                                                pady=self.parent.get_padding())
            

        # OK button
        row += 1
        tk.Button(frame, font=self.parent.custom_font,
                  text="OK",
                  command=self.quit).grid(row=row,
                                          column=1,
                                          padx=self.parent.get_padding(),
                                          pady=self.parent.get_padding())
        
