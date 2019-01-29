from phytoshop_gui_settings import *
from scipy import misc
import numpy as np
import tkinter as tk
from tkinter import font
import os
import math

class ResizeSummary(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.parent = master
        self.title("Verify image sizes")
        self.sizes = {}


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


    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        
    def quit(self):
        for base, sequence in self.parent.get_mask_sequences().items():
            sequence.set_power_of_two_size(self.sizes[base].get().split(','))
        self.destroy()
        self.parent.copy_images()
        
    def get_image_size(self, base):
        path = os.path.join(self.parent.get_directory(),
                            base)
        first_image = os.listdir(path)[0]
        try:
            image = misc.imread(os.path.join(path, first_image))
            return image.shape[:2]
        except:
            return [0,0]
        
    def get_new_image_size(self, size):
        if size[0] == 0 or size[1] == 0:
            return (0,0)
        nx = int(math.log(size[0], 2))
        new_x1 = 2**nx
        new_x2 = 2**(nx+1)
        ny = int(math.log(size[1], 2))
        new_y1 = 2**ny
        new_y2 = 2**(ny+1)
        if np.abs(size[0]-new_x1) < np.abs(size[0]-new_x2):
            new_x = new_x1
        else:
            new_x = new_x2

        if np.abs(size[1]-new_y1) < np.abs(size[1]-new_y2):
            new_y = new_y1
        else:
            new_y = new_y2
        return "{},{}".format(new_x, new_y)
    
    def create_widgets(self):

        #frame = ScrolledWindow(self,400,400).grid(row=0,
        #                                  column=0)

        frame = self.frame
        row = 0
        for base, sequence in self.parent.get_mask_sequences().items():
            # Read in first image 
            size = self.get_image_size(base)
            tk.Label(frame, font=self.parent.custom_font,
                     text="{} original size: {}. New size:".format(base, size)).grid(row=row,
                                                                                     column=0,
                                                                                     sticky=tk.W,
                                                                                    padx=self.parent.get_padding(),
                                                                                     pady=self.parent.get_padding())

            
            self.sizes[base] = tk.StringVar()
            self.sizes[base].set(self.get_new_image_size(size))
            #self.sizes[base].trace("w", self.on_crop_override_change)
            
            tk.Entry(frame,
                     font=self.parent.custom_font,
                     textvariable=self.sizes[base]).grid(row=row,
                                                         column=1,
                                                         padx=self.parent.get_padding(),
                                                         pady=self.parent.get_padding())
            
            
            

            row += 1

        tk.Button(frame, font=self.parent.custom_font,
                  text="OK",
                  command=self.quit).grid(row=row,
                                          column=1,
                                          padx=self.parent.get_padding(),
                                          pady=self.parent.get_padding())
            
