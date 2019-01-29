from phytoshop_gui_settings import *
import tkinter as tk
import numpy as np
from tkinter import messagebox
from tkinter import font
from scipy import misc
import logging
import pickle
import sys
import os
import re
import glob

class Phytoshop(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.parent = master
        self.parent.title("Phytoshop")
        self.custom_font = font.Font(family=FONT_FAMILY, size=FONT_SIZE)
        self.custom_font2 = font.Font(family=FONT_FAMILY, size=int(0.7*FONT_SIZE))
        self.initialize_variables()
        self.create_widgets()
        self.define_bindings()

    def define_bindings(self):
        # Bind window closing event
        self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        # Save settings
        if self.validate_dir(self.directory_entry.get()):
            self.set_directory(self.directory_entry.get())
        if self.validate_dir(self.directory2_entry.get()):
            self.set_directory2(self.directory2_entry.get())
        self.set_base_name(self.base_name_entry.get())
        self.set_mask_name(self.mask_name_entry.get())
        self.set_output_filename(self.output_filename_entry.get())
        self.set_start_frame(self.start_frame_entry.get())
        self.set_crop_override(self.crop_override_entry.get())

        self.save_variables()
        self.parent.destroy()

    def load_variables(self):
        try:
            #f = open(os.path.join(os.environ['HOME'], GUI_SAVED_SETTINGS_FILE), 'rb' )
            f = open(GUI_SAVED_SETTINGS_FILE, 'rb' )
            settings = pickle.load(f)
            f.close()
            self.set_directory(settings['directory'])
            self.set_directory2(settings['directory2'])
            self.set_base_name(settings['base_name'])
            self.set_mask_name(settings['mask_name'])
            self.set_output_filename(settings['output_filename'])
            self.set_start_frame(settings['start_frame'])
            self.set_crop_override(settings['crop_override'])
            self.set_number_of_frames(settings['number_of_frames'])
            self.set_gloss(settings['gloss'])
            self.set_geometry(settings['geometry'])
        except:
            print("could not load variables")
            self.initialize_saveable_variables()
    
    def save_variables(self):
        settings = {}
        settings['directory'] = self.get_directory()
        settings['directory2'] = self.get_directory2()
        settings['base_name'] = self.get_base_name()
        settings['mask_name'] = self.get_mask_name()
        settings['output_filename'] = self.get_output_filename()
        settings['start_frame'] = self.get_start_frame()
        settings['crop_override'] = self.get_crop_override()
        settings['number_of_frames'] = self.get_number_of_frames()
        settings['gloss'] = self.get_gloss_entry()
        settings['geometry'] = self.get_geometry()
        try:
            #f = open(os.path.join(os.environ['HOME'], GUI_SAVED_SETTINGS_FILE), 'wb' )
            f = open(GUI_SAVED_SETTINGS_FILE, 'wb')
            pickle.dump( settings, f )
            f.close()
        except:
            logging.warning("Could not save GUI settings")
            
    def initialize_saveable_variables(self):
        self.set_directory(".")
        self.set_directory2(".")
        self.set_base_name("")
        self.set_mask_name("")
        self.set_output_filename("")
        self.set_start_frame("")
        self.set_crop_override("")
        self.set_number_of_frames("")
        self.set_gloss(0)
        # Default size
        sw = self.get_screen_width()
        sh = self.get_screen_height()
        # Put to the middle of the screen by default
        x = int((sw - MAIN_WINDOW_WIDTH) / 2)
        y = int((sh - MAIN_WINDOW_HEIGHT) / 2)
        geometry = "%dx%d+%d+%d" % (MAIN_WINDOW_WIDTH,
                                    MAIN_WINDOW_HEIGHT,
                                    x, y)

        self.parent.geometry(geometry)
        self.set_padding(PADDING)
        
    def initialize_variables(self):
        self.load_variables()
        
    def get_window_x(self):
        return self.parent.winfo_x()
        
    def get_window_y(self):
        return self.parent.winfo_y()
        
    def get_window_width(self):
        return self.parent.winfo_width()

    def get_window_height(self):
        return self.parent.winfo_height()

    def get_screen_width(self):
        return self.parent.winfo_screenwidth()

    def get_screen_height(self):
        return self.parent.winfo_screenheight()

    def get_geometry(self):
        return self.parent.geometry()

    def set_geometry(self, geometry):
        self.parent.geometry(geometry)

    def set_padding(self, padding):
        self.padding = PADDING

    def get_padding(self):
        self.padding = PADDING
        return self.padding

    def get_directory_entry(self):
        return self.directory_entry.get()

    def set_directory_entry(self, text):
        self.directory_entry.set(text)

    def set_directory(self, dir):
        self.directory = dir

    def get_directory(self):
        return self.directory

    def set_directory_message(self, text, color):
        self.directory_message['text'] = text
        self.directory_message['foreground'] = color

    def on_directory_change(self, *args):
        self.update_gui()
        if self.validate_dir(self.directory_entry.get()):
            self.set_directory(self.directory_entry.get())
            
    def update_directory_message(self):
        if self.validate_dir(self.directory_entry.get()):
            self.set_directory_message("OK", "green")
        else: self.set_directory_message("Invalid dir", "red")

    def get_directory2_entry(self):
        return self.directory2_entry.get()

    def set_directory2_entry(self, text):
        self.directory2_entry.set(text)

    def set_directory2(self, dir):
        self.directory2 = dir

    def get_directory2(self):
        return self.directory2

    def set_directory2_message(self, text, color):
        self.directory2_message['text'] = text
        self.directory2_message['foreground'] = color

    def on_directory2_change(self, *args):
        self.update_gui()
        if self.validate_dir(self.directory2_entry.get()):
            self.set_directory2(self.directory2_entry.get())
            
    def update_directory2_message(self):
        if self.validate_dir(self.directory2_entry.get()):
            self.set_directory2_message("OK", "green")
        else: self.set_directory2_message("Invalid dir", "red")

    def validate_dir(self, dir):
        # Validate selected directory as a proper dir
        if not dir:
            return False
        if os.path.isdir(dir):
            return True
        else:
            return False

    def validate_dir_file(self, dir, file):
        # Validate selected file and directory as a proper file
        if not self.validate_dir(dir):
            return False
        if os.path.isfile(os.path.join(dir, file)):
            return True
        else:
            return False

    def validate_int(self, s):
        try: 
            int(s)
            return True
        except ValueError:
            return False

    
       
    def get_base_name_entry(self):
        return self.base_name_entry.get()

    def set_base_name_entry(self, text):
        self.base_name_entry.set(text)

    def set_base_name(self, name):
        self.base_name = name

    def get_base_name(self):
        return self.base_name

    def set_base_name_message(self, text, color):
        self.base_name_message['text'] = text
        self.base_name_message['foreground'] = color

    def on_base_name_change(self, *args):
        self.set_base_name(self.get_base_name_entry())
        self.update_gui()
        
    def update_base_name_message(self):
        # Count files with this base name
        result = self.find_number_of_matches(self.get_directory_entry(), self.get_base_name_entry())
        if not result:
            self.set_base_name_message("No matching files", "red")
        elif result == 1:
            self.set_base_name_message("One match", "green")
        else:
            self.set_base_name_message(str(result) + " matches", "green")

        
    def get_mask_name_entry(self):
        return self.mask_name_entry.get()

    def set_mask_name_entry(self, text):
        self.mask_name_entry.set(text)

    def set_mask_name(self, name):
        self.mask_name = name

    def get_mask_name(self):
        return self.mask_name

    def set_mask_name_message(self, text, color):
        self.mask_name_message['text'] = text
        self.mask_name_message['foreground'] = color

    def on_mask_name_change(self, *args):
        self.set_mask_name(self.get_mask_name_entry())
        self.update_gui()
        
    def update_mask_name_message(self):
        # Count files with this base name
        result = self.find_number_of_matches(self.get_directory_entry(), self.get_mask_name_entry())
        if not result:
            self.set_mask_name_message("No matching files", "red")
        elif result == 1:
            self.set_mask_name_message("One match", "green")
        else:
            self.set_mask_name_message(str(result) + " matches", "green")
        
    def get_output_filename_entry(self):
        return self.output_filename_entry.get()

    def set_output_filename_entry(self, text):
        self.output_filename_entry.set(text)

    def set_output_filename(self, name):
        self.output_filename = name

    def get_output_filename(self):
        return self.output_filename

    def set_output_filename_message(self, text, color):
        self.output_filename_message['text'] = text
        self.output_filename_message['foreground'] = color

    def on_output_filename_change(self, *args):
        self.set_output_filename(self.get_output_filename_entry())
        self.update_gui()
        
    def update_output_filename_message(self):
        # Count files with this base name
        result = self.find_number_of_matches(self.get_directory_entry(), self.get_output_filename_entry())
        if not result:
            self.set_output_filename_message("No matching files", "green")
        elif result == 1:
            self.set_output_filename_message("One match", "red")
        else:
            self.set_output_filename_message(str(result) + " matches", "red")


    def get_start_frame_entry(self):
        return self.start_frame_entry.get()

    def set_start_frame_entry(self, text):
        self.start_frame_entry.set(text)

    def set_start_frame(self, name):
        self.start_frame = name

    def get_start_frame(self):
        return self.start_frame

    def set_start_frame_message(self, text, color):
        self.start_frame_message['text'] = text
        self.start_frame_message['foreground'] = color

    def on_start_frame_change(self, *args):
        self.set_start_frame(self.get_start_frame_entry())
        self.update_gui()
        
    def update_start_frame_message(self):
        # Count files with this base name
        if not self.validate_int(self.get_start_frame_entry()):
            self.set_start_frame_message("Insert number", "red")
            return
        if not self.validate_dir_file(self.get_directory_entry(),
                                      self.get_base_name().replace(".png",
                                                                   "").replace("%n",
                                                                               str(self.get_start_frame_entry()))+
                                      '.png'):
            self.set_start_frame_message("No such frame", "red")
        else: self.set_start_frame_message("OK", "green")

    def get_number_of_frames_entry(self):
        return self.number_of_frames_entry.get()

    def set_number_of_frames_entry(self, text):
        self.number_of_frames_entry.set(text)

    def set_number_of_frames(self, name):
        self.number_of_frames = name

    def get_number_of_frames(self):
        return self.number_of_frames

    def set_number_of_frames_message(self, text, color):
        self.number_of_frames_message['text'] = text
        self.number_of_frames_message['foreground'] = color

    def on_number_of_frames_change(self, *args):
        self.set_number_of_frames(self.get_number_of_frames_entry())
        self.update_gui()
        
    def update_number_of_frames_message(self):
        # Count files with this base name
        if not self.validate_int(self.get_number_of_frames_entry()):
            self.set_number_of_frames_message("Insert number", "red")
        else: self.set_number_of_frames_message("OK", "green")

    def get_crop_override_entry(self):
        return self.crop_override_entry.get()

    def set_crop_override_entry(self, text):
        self.crop_override_entry.set(text)

    def set_crop_override(self, name):
        self.crop_override = name

    def get_crop_override(self):
        return self.crop_override

    def set_crop_override_message(self, text, color):
        self.crop_override_message['text'] = text
        self.crop_override_message['foreground'] = color

    def on_crop_override_change(self, *args):
        self.set_crop_override(self.get_crop_override_entry())
        self.update_gui()
        
    def update_crop_override_message(self):
        # Validate four ints
        regex = "[0-9]+,[\s]?[0-9]+,[\s]?[0-9]+,[\s]?[0-9]+"
        
        if not re.compile(regex).search(self.get_crop_override_entry()):
            self.set_crop_override_message("Insert values", "red")
        else: self.set_crop_override_message("OK", "green")

    def update_crop_values(self):
        # Calculate the crop values
        # Crop override values
        crop_bounds_str = self.get_crop_override_entry()
        crop_bounds = crop_bounds_str.split(",")
        try:
            row_start = int(crop_bounds[0])
        except:
            self.crop_values['text'] = ""
            return
        try:
            col_start = int(crop_bounds[1])
        except:
            self.crop_values['text'] = ""
            return
        try:
            row_end = int(crop_bounds[2])
        except:
            self.crop_values['text'] = ""
            return
        try:
            col_end = int(crop_bounds[3])
        except:
            self.crop_values['text'] = ""
            return
        self.crop_values['text'] = " Size after cropping: " + str(row_end - row_start) + ", " + str(col_end-col_start)
        
    def set_gloss(self, gloss):
        self.gloss = gloss

    def get_gloss(self):
        return self.gloss

    def get_gloss_entry(self):
        return self.gloss_entry.get()

    def set_gloss_entry(self, value):
        self.gloss_entry.set(value)

    def set_script1_message(self, text, color):
        self.script1_message['text'] = text
        self.script1_message['foreground'] = color
        self.update()
        
    def set_script2_message(self, text, color):
        self.script2_message['text'] = text
        self.script2_message['foreground'] = color
        self.update()
        
    def set_script3_message(self, text, color):
        self.script3_message['text'] = text
        self.script3_message['foreground'] = color
        self.update()
        
    def set_script4_message(self, text, color):
        self.script4_message['text'] = text
        self.script4_message['foreground'] = color
        self.update()
        
    def create_widgets(self):
        tk.Label(self.parent, font=self.custom_font,
                 text="Input directory:").grid(row=0, sticky=tk.E,
                                            padx=self.get_padding(),
                                              pady=self.get_padding())

        self.directory_entry = tk.StringVar()
        # Initialize value
        self.set_directory_entry(self.get_directory())
        
        self.directory_entry.trace("w", self.on_directory_change)
        tk.Entry(self.parent,
                 font=self.custom_font,
                 textvariable=self.directory_entry).grid(row=0,
                                                         column=1,
                                                         padx=self.get_padding(),
                                                         pady=self.get_padding())
        
        self.directory_message = tk.Label(self.parent, font=self.custom_font2, text="")
        self.directory_message.grid(row=0,
                                    column=2,
                                    sticky=tk.W,
                                    padx=self.get_padding(),
                                    pady=self.get_padding())

        # Initialize dir message value
        self.update_directory_message()

        # Row 2, base image sequence
        tk.Label(self.parent, font=self.custom_font,
                 text="Base image sequence name:").grid(row=1,
                                                       sticky=tk.E,
                                                       padx=self.get_padding(),
                                                       pady=self.get_padding())

        self.base_name_entry = tk.StringVar()
        # Initialize value
        self.set_base_name_entry(self.get_base_name())
        
        self.base_name_entry.trace("w", self.on_base_name_change)
        tk.Entry(self.parent,
                 font=self.custom_font,
                 textvariable=self.base_name_entry).grid(row=1,
                                                         column=1,
                                                         padx=self.get_padding(),
                                                         pady=self.get_padding())

        
        self.base_name_message = tk.Label(self.parent, font=self.custom_font2, text="")
        self.base_name_message.grid(row=1,
                                    column=2,
                                    sticky=tk.W,
                                    padx=self.get_padding(),
                                    pady=self.get_padding())
        
        # Initialize base name message value
        self.update_base_name_message()


        # Row 3, mask sequence
        tk.Label(self.parent, font=self.custom_font,
                 text="Base mask sequence name:").grid(row=2,column=0,sticky=tk.E,
                                                       padx=self.get_padding(),
                                                       pady=self.get_padding())

        self.mask_name_entry = tk.StringVar()
        # Initialize value
        self.set_mask_name_entry(self.get_mask_name())
        
        self.mask_name_entry.trace("w", self.on_mask_name_change)
        tk.Entry(self.parent,
                 font=self.custom_font,
                 textvariable=self.mask_name_entry).grid(row=2,column=1,
                                                         padx=self.get_padding(),
                                                         pady=self.get_padding())

        
        self.mask_name_message = tk.Label(self.parent, font=self.custom_font2, text="")
        self.mask_name_message.grid(row=2,column=2,sticky=tk.W,
                                    padx=self.get_padding(),
                                    pady=self.get_padding())

        # Initialize base name message value
        self.update_mask_name_message()



        # Row 4, output filename
        tk.Label(self.parent, font=self.custom_font,
                 text="Output filename:").grid(row=3, column=0, sticky=tk.E,
                                                       padx=self.get_padding(),
                                                       pady=self.get_padding())

        self.output_filename_entry = tk.StringVar()
        # Initialize value
        self.set_output_filename_entry(self.get_output_filename())
        
        self.output_filename_entry.trace("w", self.on_output_filename_change)
        tk.Entry(self.parent,
                 font=self.custom_font,
                 textvariable=self.output_filename_entry).grid(row=3,column=1,
                                                         padx=self.get_padding(),
                                                         pady=self.get_padding())

        
        self.output_filename_message = tk.Label(self.parent,
                                                font=self.custom_font2,
                                                text="")
        self.output_filename_message.grid(row=3,column=2,sticky=tk.W,
                                    padx=self.get_padding(),
                                    pady=self.get_padding())

        # Initialize base name message value
        self.update_output_filename_message()

        # Row 5, start frame
        tk.Label(self.parent, font=self.custom_font,
                 text="Start frame number:").grid(row=4,column=0,sticky=tk.E,
                                                       padx=self.get_padding(),
                                                       pady=self.get_padding())

        self.start_frame_entry = tk.StringVar()
        # Initialize value
        self.set_start_frame_entry(self.get_start_frame())
        
        self.start_frame_entry.trace("w", self.on_start_frame_change)
        tk.Entry(self.parent,
                 font=self.custom_font,
                 textvariable=self.start_frame_entry).grid(row=4,column=1,
                                                         padx=self.get_padding(),
                                                         pady=self.get_padding())

        
        self.start_frame_message = tk.Label(self.parent, font=self.custom_font2, text="")
        self.start_frame_message.grid(row=4,column=2,sticky=tk.W,
                                    padx=self.get_padding(),
                                    pady=self.get_padding())

        # Initialize base name message value
        self.update_start_frame_message()


        # Row 6, number of frames
        tk.Label(self.parent, font=self.custom_font,
                 text="Number of frames:").grid(row=5,column=0,sticky=tk.E,
                                                       padx=self.get_padding(),
                                                       pady=self.get_padding())

        self.number_of_frames_entry = tk.StringVar()
        # Initialize value
        self.set_number_of_frames_entry(self.get_number_of_frames())
        
        self.number_of_frames_entry.trace("w", self.on_number_of_frames_change)
        tk.Entry(self.parent,
                 font=self.custom_font,
                 textvariable=self.number_of_frames_entry).grid(row=5,column=1,
                                                         padx=self.get_padding(),
                                                         pady=self.get_padding())

        
        self.number_of_frames_message = tk.Label(self.parent,
                                                 font=self.custom_font2, text="")
        self.number_of_frames_message.grid(row=5,column=2,sticky=tk.W,
                                           padx=self.get_padding(),
                                           pady=self.get_padding())

        # Initialize base name message value
        self.update_number_of_frames_message()


        # Row 7, number of frames
        self.gloss_entry = tk.IntVar()
        # Initialize variable
        self.set_gloss_entry(self.get_gloss())
        
        tk.Checkbutton(self.parent, font=self.custom_font,
                       text="MASK-GLOSS",
                       variable=self.gloss_entry).grid(row=6,
                                                       column=1,
                                                       padx=self.get_padding(),
                                                       pady=self.get_padding())
        

        # Row 8, button 1
        tk.Button(self.parent, font=self.custom_font,
                  text="RUN Mask Coutout Script",
                  command=self.run_mask_cutout).grid(row=7,
                                                     column=1,
                                                     padx=self.get_padding(),
                                                     pady=self.get_padding())


        self.script1_message = tk.Label(self.parent,
                                                 font=self.custom_font2, text="")
        self.script1_message.grid(row=7,column=2,sticky=tk.W,
                                           padx=self.get_padding(),
                                           pady=self.get_padding())


        
        # Row 9, button 2
        tk.Button(self.parent, font=self.custom_font,
                  text="RUN Crop Analysis Script",
                  command=self.run_crop_analysis).grid(row=8,
                                                     column=1,
                                                     padx=self.get_padding(),
                                                     pady=self.get_padding())

        self.script2_message = tk.Label(self.parent,
                                                 font=self.custom_font2, text="")
        self.script2_message.grid(row=8,column=2,sticky=tk.W,
                                           padx=self.get_padding(),
                                           pady=self.get_padding())

        # Row 10, crop value overrides
        tk.Label(self.parent, font=self.custom_font,
                 text="Crop value overrides:").grid(row=9,column=0,sticky=tk.E,
                                                       padx=self.get_padding(),
                                                       pady=self.get_padding())

        self.crop_override_entry = tk.StringVar()
        # Initialize value
        self.set_crop_override_entry(self.get_crop_override())
        
        self.crop_override_entry.trace("w", self.on_crop_override_change)
        tk.Entry(self.parent,
                 font=self.custom_font,
                 textvariable=self.crop_override_entry).grid(row=9,column=1,
                                                         padx=self.get_padding(),
                                                         pady=self.get_padding())

        
        self.crop_override_message = tk.Label(self.parent, font=self.custom_font2, text="")
        self.crop_override_message.grid(row=9,column=2,sticky=tk.W,
                                    padx=self.get_padding(),
                                    pady=self.get_padding())

        # Initialize crop override message value
        self.update_crop_override_message()

        # Row 10, crop value overrides
        self.crop_values = tk.Label(self.parent, font=self.custom_font,
                                    text="")
        self.crop_values.grid(row=10,column=1,sticky=tk.E,
                              padx=self.get_padding(),
                              pady=self.get_padding())


        
        # Row 11, button 3
        tk.Button(self.parent, font=self.custom_font,
                  text="RUN Crop Script",
                  command=self.run_crop).grid(row=11,
                                                     column=1,
                                                     padx=self.get_padding(),
                                                     pady=self.get_padding())


        self.script3_message = tk.Label(self.parent,
                                                 font=self.custom_font2, text="")
        self.script3_message.grid(row=11,column=2,sticky=tk.W,
                                           padx=self.get_padding(),
                                           pady=self.get_padding())


        tk.Label(self.parent, font=self.custom_font,
                 text="Input directory2:").grid(row=12, sticky=tk.E,
                                            padx=self.get_padding(),
                                              pady=self.get_padding())

        self.directory2_entry = tk.StringVar()
        # Initialize value
        self.set_directory2_entry(self.get_directory2())
        
        self.directory2_entry.trace("w", self.on_directory2_change)
        tk.Entry(self.parent,
                 font=self.custom_font,
                 textvariable=self.directory2_entry).grid(row=12,
                                                         column=1,
                                                         padx=self.get_padding(),
                                                         pady=self.get_padding())
        
        self.directory2_message = tk.Label(self.parent, font=self.custom_font2, text="")
        self.directory2_message.grid(row=12,
                                    column=2,
                                    sticky=tk.W,
                                    padx=self.get_padding(),
                                    pady=self.get_padding())

        # Initialize dir message value
        self.update_directory2_message()

        # Row 8, button 1
        tk.Button(self.parent, font=self.custom_font,
                  text="RUN Crop All",
                  command=self.run_crop_all).grid(row=13,
                                                     column=1,
                                                     padx=self.get_padding(),
                                                     pady=self.get_padding())

        self.script4_message = tk.Label(self.parent,
                                                 font=self.custom_font2, text="")
        self.script4_message.grid(row=12,column=2,sticky=tk.W,
                                           padx=self.get_padding(),
                                           pady=self.get_padding())
        
    def rgb_to_gray(self, rgb):
        return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

    def to_rgb(self, im):
        w, h = im.shape
        ret = np.empty((w, h, 3), dtype=np.uint8)
        ret[:, :, 2] =  ret[:, :, 1] =  ret[:, :, 0] =  im
        return ret

    def update_gui(self):
        self.update_directory_message()
        self.update_directory2_message()
        self.update_base_name_message()
        self.update_mask_name_message()
        self.update_output_filename_message()
        self.update_start_frame_message()
        self.update_number_of_frames_message()
        self.update_crop_override_message()
        self.update_crop_values()
        self.update()
        
    def run_mask_cutout(self):
        self.set_script1_message("Running", "green")
        self.init_mismatch_report()

        # Update the directory
        self.set_directory(self.directory_entry.get())
        # Update base name
        self.set_base_name(self.get_base_name_entry())
        # Update mask name
        self.set_mask_name(self.get_mask_name_entry())
        # Update mask name
        self.set_output_filename(self.get_output_filename_entry())
        # Update start frame
        self.set_start_frame(self.get_start_frame_entry())
        # Update number of frames
        self.set_number_of_frames(self.get_number_of_frames_entry())
        
        directory = self.get_directory()
        base_pattern = self.get_base_name().replace(".png","")
        mask_pattern = self.get_mask_name().replace(".png","")
        output_pattern = self.get_output_filename().replace(".png","")
        try:
            start_frame = int(self.get_start_frame())
        except:
            start_frame = 0
        number_of_frames = self.get_number_of_frames()
        if number_of_frames == "":
            number_of_frames = -1
        else:
            number_of_frames = int(number_of_frames)

        gloss = False
        if self.get_gloss_entry() == 1:
            gloss = True
            
        self.set_script1_message("Reading directory...", "green")
        # Load images
        images = self.get_images(directory, base_pattern, start_frame, number_of_frames)
        # Process each image
        for i in range(len(images)):
            self.set_script1_message("Processing file "+str(i+1)+" of "+str(len(images)), "green")
            image = images[i]
            try:
                orig = misc.imread(image)
            except:
                print("Could not open "+image)
                continue
            shape = np.shape(orig)
            number = self.get_number_from_pattern_and_string(base_pattern, image)

            
            # add as alpha channel in image
            mask_name = os.path.join(directory,
                                     self.get_filename_from_pattern(
                                         mask_pattern,
                                         number))
            try:
                mask = misc.imread(mask_name, flatten=True)
            except:
                print("Could not open "+mask_name)
                continue
            mask_shape = np.shape(mask) 
            # Check shape mismatch
            if shape[:2] != mask_shape[:2]:
                self.append_into_mismatch(image, mask_name,
                                          shape, mask_shape)
                continue
            if not gloss:
                new = np.zeros((shape[0], shape[1], 4))
                new[:,:,0:3] = orig[:,:,0:3]
                new[:,:,3] = mask
                
            else:
                new = 255* np.ones((shape[0], shape[1], 4))
                new[:,:,3] = self.rgb_to_gray(orig)* mask/255.0

                # Mask again


                
            # Save the new file
            new_name = os.path.join(directory,
                                    self.get_filename_from_pattern(output_pattern,
                                                                   number))
            try:
                misc.imsave(new_name, new)
            except:
                print("Could not save "+new_name)
                continue
                
        # Show the mismatch report
        self.create_mismatch_report()
        # Script finished
        self.set_script1_message("Finished", "green")


            
    def run_crop_analysis(self):
        self.init_mismatch_report()
        # Update the directory
        self.set_directory(self.directory_entry.get())
        # Update base name
        self.set_base_name(self.get_base_name_entry())
        # Update mask name
        self.set_mask_name(self.get_mask_name_entry())
        # Update mask name
        self.set_output_filename(self.get_output_filename_entry())
        # Update start frame
        self.set_start_frame(self.get_start_frame_entry())
        # Update number of frames
        self.set_number_of_frames(self.get_number_of_frames_entry())

        directory = self.get_directory()
        base_pattern = self.get_base_name().replace(".png","")
        mask_pattern = self.get_mask_name().replace(".png","")
        output_pattern = self.get_output_filename().replace(".png","")

        try:
            start_frame = int(self.get_start_frame())
        except:
            start_frame = 0
        number_of_frames = self.get_number_of_frames()
        if number_of_frames == "":
            number_of_frames = -1
        else:
            number_of_frames = int(number_of_frames)

        self.set_script2_message("Reading directory...", "green")
        # Load masks
        result = None
        masks = self.get_images(directory, mask_pattern, start_frame, number_of_frames)

        for i in range(len(masks)):
            self.set_script2_message("Processing file "+str(i+1)+" of "+str(len(masks)), "green")
            mask = masks[i]
            number = self.get_number_from_pattern_and_string(mask_pattern, mask)
            try:
                mask = misc.imread(
                    os.path.join(directory,
                                 self.get_filename_from_pattern(mask_pattern,
                                                                number)), flatten=True)
            except:
                print("Could not open "+mask)
                continue
                
            # Take the first image as a reference
            if i == 0:
                reference_shape = np.shape(mask)
                reference_name = masks[i]
                result = np.zeros(reference_shape)
                
            shape = np.shape(mask)
            # Check for shape mismatch
            if shape[:2] != reference_shape[:2]:
                self.append_into_mismatch(reference_name, masks[i],
                                          reference_shape, shape)
                continue
            
            result = np.logical_or(result, mask)

        # Do the crop for the base images
        try:
            nonzeros = np.nonzero(result)
            row_start = min(nonzeros[0])
            col_start = min(nonzeros[1])
            row_end = max(nonzeros[0])
            col_end = max(nonzeros[1])
        except:
            self.set_script2_message("Error occured, check input values ", "red")
            return
        self.set_script2_message("Finished ", "green")

        # Show the mismatch report
        self.create_mismatch_report()
        
        # Show the results
        self.crop_bounds = "{},{},{},{}".format(row_start, col_start, row_end+1, col_end+1)
        CropAnalysisResults(self, "Original image size: " + str(reference_shape[0]) +", "+ str(reference_shape[1]) +
                            "\nSize after cropping: " + str(row_end - row_start+1) +
                            ", " + str(col_end-col_start+1) +
                            "\nCrop bound values: " + self.crop_bounds)

        

    def init_mismatch_report(self):
        self.mismatch_files = "Mismatching file pairs\n"
        self.mismatch_sizes = "height, width"
        
    def append_into_mismatch(self, filename1, filename2, shape1, shape2):
        self.mismatch_files += "Pair:\n"+filename1+"\n"+filename2+"\n"
        self.mismatch_sizes += "\n"+str(shape1[0])+", "+str(shape1[1])+"\n"+str(shape2[0])+", "+str(shape2[1])+"\n"

    def create_mismatch_report(self):
        if self.mismatch_files != "Mismatching file pairs\n":
            MismatchReport(self, self.mismatch_files, self.mismatch_sizes)
        
    def init_crop_report(self):
        self.report = ""

    def append_into_crop_report(self, line):
        self.report += line + "\n"

    def save_crop_report(self):
        try:
            with open(os.path.join(self.get_directory(), "crop_report.csv"), "a") as f:
                f.write(self.report)
        except:
            print("Could not save csv")

            
    def run_crop(self):
        self.init_crop_report()
        # Update the directory
        self.set_directory(self.directory_entry.get())
        # Update base name
        self.set_base_name(self.get_base_name_entry())
        # Update output
        self.set_output_filename(self.get_output_filename_entry())
        # Update start frame
        self.set_start_frame(self.get_start_frame_entry())
        # Update number of frames
        self.set_number_of_frames(self.get_number_of_frames_entry())
        # Crop override values
        crop_bounds_str = self.get_crop_override_entry()
        crop_bounds = crop_bounds_str.split(",")
        try:
            row_start = int(crop_bounds[0])
        except:
            messagebox.showerror("Invalid crop bound", "Invalid crop bound {}".format(crop_bounds[0]))
            return
        try:
            col_start = int(crop_bounds[1])
        except:
            messagebox.showerror("Invalid crop bound", "Invalid crop bound {}".format(crop_bounds[1]))
            return
        try:
            row_end = int(crop_bounds[2])
        except:
            messagebox.showerror("Invalid crop bound", "Invalid crop bound {}".format(crop_bounds[2]))
            return
        try:
            col_end = int(crop_bounds[3])
        except:
            messagebox.showerror("Invalid crop bound", "Invalid crop bound {}".format(crop_bounds[3]))
            return
        
        directory = self.get_directory()
        base_pattern = self.get_base_name().replace(".png","")
        output_pattern = self.get_output_filename().replace(".png","")

        try:
            start_frame = int(self.get_start_frame())
        except:
            start_frame = 0
        number_of_frames = self.get_number_of_frames()
        if number_of_frames == "":
            number_of_frames = -1
        else:
            number_of_frames = int(number_of_frames)

        # Apply to crop
        images = self.get_images(directory, base_pattern, start_frame, number_of_frames)
        # Process each image
        crop_report_added = False
        for i in range(len(images)):
            self.set_script3_message("Cropping file "+str(i+1)+" of "+str(len(images)), "green")
            image = images[i]
            try:
                orig = misc.imread(image)
            except:
                print("Could not open "+image)
                continue            
            number = self.get_number_from_pattern_and_string(base_pattern, image)
            
            # Save the new file
            new_name = os.path.join(directory,
                                    self.get_filename_from_pattern(output_pattern,
                                                                   number))
            try:
                misc.imsave(new_name,
                            orig[row_start:row_end,col_start:col_end])
                if not crop_report_added:
                    line = image + "," + crop_bounds_str
                    self.append_into_crop_report(line)
                    crop_report_added = True
            except:
                print("Could not save "+new_name)
                continue


                
        self.save_crop_report()
        self.set_script3_message("Finished", "green")


    def get_number_from_pattern_and_string(self, pattern, string):
        if not "%n" in pattern:
            return ""
        string = os.path.basename(string)
        string = string.replace(".png","")
        start = pattern.split("%n")[0]
        end = pattern.split("%n")[1]
        if start == "" and end == "":
            number = int(string)
        elif start == "" and end != "":
            number = int(string.split(end)[0])
        elif start != "" and end == "":
            number = int(string.split(start)[1])

        elif start != "" and end != "":
            number = int(string.split(end)[0].split(start)[1])
        return number
    
    def get_filename_from_pattern(self, pattern, number):
        return pattern.replace('%n', str(number)).replace(".png","")+".png"
        
    def run_crop_all(self):

        # Update the directory
        self.set_directory2(self.directory2_entry.get())
        
        # Crop override values
        crop_bounds_str = self.get_crop_override_entry()
        crop_bounds = crop_bounds_str.split(",")
        try:
            row_start = int(crop_bounds[0])
        except:
            messagebox.showerror("Invalid crop bound", "Invalid crop bound {}".format(crop_bounds[0]))
            return
        try:
            col_start = int(crop_bounds[1])
        except:
            messagebox.showerror("Invalid crop bound", "Invalid crop bound {}".format(crop_bounds[1]))
            return
        try:
            row_end = int(crop_bounds[2])
        except:
            messagebox.showerror("Invalid crop bound", "Invalid crop bound {}".format(crop_bounds[2]))
            return
        try:
            col_end = int(crop_bounds[3])
        except:
            messagebox.showerror("Invalid crop bound", "Invalid crop bound {}".format(crop_bounds[3]))
            return
        
        directory = self.get_directory2()

        # Get all the png images of the given directory
        
        images = glob.glob(directory+"/*.png")
        # Process each image
        for i in range(len(images)):
            self.set_script4_message("Cropping file "+str(i+1)+" of "+str(len(images)), "green")
            image = images[i]
            try:
                orig = misc.imread(image)
            except:
                print("Could not open "+image)
                continue
            shape = np.shape(orig)
            # Save the cropped image
            if shape[0] < row_end or shape[1] < col_end:
                continue
            try:
                misc.imsave(image, orig[row_start:row_end,col_start:col_end])
            except:
                print("Could not save "+image)
                continue
            
        self.set_script4_message("Finished", "green")

        

        

    def find_number_of_matches(self, directory, pattern):
        if not self.validate_dir(directory):
            return 0
        
        counter = 0
        b = r'(\s|^|$)'
        for file in os.listdir(directory):
            regex = b+pattern.replace("%n","[0-9]+").replace(".png","")+b
            
            if re.compile(regex).match(file.replace(".png","")) != None:
                counter += 1
        return counter
            
    def get_images(self, directory, pattern, first="", number=-1):
        files = os.listdir(directory)
        selected = []
        if first == "":
            first = 0
            
        if number != -1:
            ints = range(first,first + number)
        else:
            ints = range(first, first + len(files))
        for i in ints:
            test = self.get_filename_from_pattern(pattern, i)
            if test in files:
                if not str(os.path.join(directory, test)) in selected:
                    selected.append(str(os.path.join(directory, test)))
        return selected



class MismatchReport(tk.Toplevel):
    def __init__(self, master, text1, text2):
        tk.Toplevel.__init__(self, master)
        self.parent = master
        self.title("Mismatch report")
        self.text1 = text1
        self.text2 = text2
        self.create_widgets()

    def quit(self):
        self.destroy()
                            
    def create_widgets(self):
        tk.Label(self, font=self.parent.custom_font,
                 text="The following files are of different sizes, and process was skipped.").grid(row=0,
                                                                                                   columnspan=2,
                                                                                                   sticky=tk.W,
                                                                                                   padx=self.parent.get_padding(),
                                                                                                   pady=self.parent.get_padding())


        tk.Label(self, font=self.parent.custom_font,
                 text=self.text1).grid(row=1,
                                      column=0,
                                      sticky=tk.W,
                                      padx=self.parent.get_padding(),
                                      pady=self.parent.get_padding())


        tk.Label(self, font=self.parent.custom_font,
                 text=self.text2).grid(row=1,
                                      column=1,
                                      sticky=tk.W,
                                      padx=self.parent.get_padding(),
                                      pady=self.parent.get_padding())


        # Row 8, button 1
        tk.Button(self, font=self.parent.custom_font,
                  text="OK",
                  command=self.quit).grid(row=2,
                                          columnspan=2,
                                          padx=self.parent.get_padding(),
                                          pady=self.parent.get_padding())


class CropAnalysisResults(tk.Toplevel):
    def __init__(self, master, text):
        tk.Toplevel.__init__(self, master)
        self.parent = master
        self.title("Crop analysis results")
        self.text = text
        self.create_widgets()

    def quit(self):
        self.destroy()

    def copy(self):
        self.parent.set_crop_override_entry(self.parent.crop_bounds)
        self.parent.update()
                            
    def create_widgets(self):
        tk.Label(self, font=self.parent.custom_font,
                 text=self.text).grid(row=0,
                                      columnspan=2,
                                      sticky=tk.W,
                                      padx=self.parent.get_padding(),
                                      pady=self.parent.get_padding())


        # Row 8, button 1
        tk.Button(self, font=self.parent.custom_font,
                  text="OK",
                  command=self.quit).grid(row=1,
                                          column=0,
                                          padx=self.parent.get_padding(),
                                          pady=self.parent.get_padding())

        tk.Button(self, font=self.parent.custom_font,
                  text="Copy crop bounds into entry field",
                  command=self.copy).grid(row=1,
                                          column=1,
                                          padx=self.parent.get_padding(),
                                          pady=self.parent.get_padding())

        
root = tk.Tk()
app = Phytoshop(master=root)
app.mainloop()
