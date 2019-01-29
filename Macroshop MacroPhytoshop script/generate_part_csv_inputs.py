from phytoshop_gui_settings import *
import tkinter as tk
import os
from tkinter import font
import re

class GeneratePartCSVInputs(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.parent = master
        self.title("Inputs for Part CSV Generation")
        self.bounds = {}
        self.messages = {}
        self.labels = ["1stEmpty",
                       "SortOrder",
                       "TmenuOrder",
                       "TmenuFrame"]


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
            path = os.path.join(self.parent.get_output_dir(),
                                "params.csv")
            with open(path, 'r') as f:
                params = f.readlines()
            j = 0
            for line in params:
                p = line.split(',')
                for value in p:
                    s = value.replace('\n','')
                    self.entries[j].set(s)
                    j += 1
                    
        except:
            pass
        
    def save_entries(self):
        index = 0
        out = ""
        for base, sequence in self.parent.get_mask_sequences().items():
            values = []
            #out += str(base)
            for i in range(index, index + len(self.labels)):
                values.append(self.entries[i].get())
            sequence.set_part_params(values)
            index += len(self.labels)
            out += ','.join(str(x) for x in values)+'\n'
        path = os.path.join(self.parent.get_output_dir(),
                            "params.csv")
        with open(path, 'w') as f:
            f.write(self.parent.mac_csv(out))
        
            
    def create_widgets(self):
        frame = self.frame
        row = 0
        col = 1
        for label in self.labels:
            tk.Label(frame, font=self.parent.custom_font,
                     text=label).grid(row=row,
                                      column=col,
                                      sticky=tk.W,
                                      padx=self.parent.get_padding(),
                                      pady=self.parent.get_padding())
            col +=1
        # Generate table entries
        self.entries = []
        for base, sequence in self.parent.get_mask_sequences().items():
            row += 1
            col = 0
            tk.Label(frame, font=self.parent.custom_font,
                     text=base).grid(row=row,
                                     column=col,
                                     sticky=tk.W,
                                     padx=self.parent.get_padding(),
                                     pady=self.parent.get_padding())
            # Entries
            col = 1
            for label in self.labels:
                if label == "1stEmpty":
                    entry = tk.IntVar()
                    self.entries.append(entry)
                    tk.Checkbutton(frame, font=self.parent.custom_font,
                                   text="",
                                   variable=entry).grid(row=row,
                                                        column=col,
                                                        padx=self.parent.get_padding(),
                                                        pady=self.parent.get_padding())
                else:
                    entry = tk.StringVar()
                    self.entries.append(entry)
                    tk.Entry(frame,
                             font=self.parent.custom_font,
                             textvariable=entry).grid(row=row,
                                                      column=col,
                                                      padx=self.parent.get_padding(),
                                                      pady=self.parent.get_padding())
                
                col += 1


        # OK button
        row += 1
        tk.Button(frame, font=self.parent.custom_font,
                  text="OK",
                  command=self.quit).grid(row=row,
                                          column=1,
                                          padx=self.parent.get_padding(),
                                          pady=self.parent.get_padding())
        
