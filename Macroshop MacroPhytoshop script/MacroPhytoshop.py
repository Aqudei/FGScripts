import subprocess
from ColorminisExternal import MatGenerator
from postmacro import PostMacro
from exclude_parts_dialog import ExcludePartsDialog
from alpha_tweak import AlphaTweak
from phytoshop_gui_settings import *
from generate_part_csv_inputs import GeneratePartCSVInputs
from shadow_resize_summary import ShadowResizeSummary
from resize_summary import ResizeSummary
from shadow_crop_analysis_results import ShadowCropAnalysisResults
from crop_analysis_results import CropAnalysisResults
from sequence import Sequence
import csv
import traceback
from zipfile import ZipFile
import tkinter as tk
import numpy as np
from tkinter import messagebox
from tkinter import font
from scipy import misc
from scipy import ndimage
import logging
import pickle
import sys
import shutil
import os
import re
import glob
import math
import logging

logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

includepath = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.append(includepath)


class MacroPhytoshop(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.parent = master
        self.one_click = False
        self.parent.title("Macro Phytoshop")
        self.custom_font = font.Font(family=FONT_FAMILY, size=FONT_SIZE)
        self.custom_font2 = font.Font(
            family=FONT_FAMILY, size=int(0.7 * FONT_SIZE))
        self.load_variables()
        self.create_widgets()
        self.define_bindings()
        self.script_path = os.path.abspath(os.path.dirname(sys.argv[0]))

    def define_bindings(self):
        # Bind window closing event
        self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        # Save settings
        if self.validate_dir(self.directory_entry.get()):
            self.set_directory(self.directory_entry.get())
        # if self.validate_dir(self.directory2_entry.get()):
        #    self.set_directory2(self.directory2_entry.get())
        # self.set_base_name(self.base_name_entry.get())
        # self.set_mask_name(self.mask_name_entry.get())
        # self.set_output_filename(self.output_filename_entry.get())
        # self.set_start_frame(self.start_frame_entry.get())
        # self.set_crop_override(self.crop_override_entry.get())

        self.save_variables()
        self.parent.destroy()

    def load_variables(self):
        self.init_sequences()
        try:
            #f = open(os.path.join(os.environ['HOME'], MACRO_GUI_SAVED_SETTINGS_FILE), 'rb' )
            f = open(MACRO_GUI_SAVED_SETTINGS_FILE, 'rb')
            settings = pickle.load(f)
            f.close()
            self.set_directory(settings['directory'])
            self.set_rgb_directory(settings['rgb_directory'])
            self.set_expand_directory(settings['expand_directory'])
            self.set_geometry(settings['geometry'])
            self.set_model_name('')
        except:
            logging.debug("could not load variables")
            self.initialize_saveable_variables()

    def save_variables(self):
        settings = {}
        settings['directory'] = self.get_directory()
        settings['rgb_directory'] = self.get_rgb_directory()
        settings['expand_directory'] = self.get_expand_directory()
        settings['geometry'] = self.get_geometry()
        try:
            #f = open(os.path.join(os.environ['HOME'], MACRO_GUI_SAVED_SETTINGS_FILE), 'wb' )
            f = open(MACRO_GUI_SAVED_SETTINGS_FILE, 'wb')
            pickle.dump(settings, f)
            f.close()
        except:
            logging.warning("Could not save GUI settings")

    def initialize_saveable_variables(self):
        self.set_directory(".")
        self.set_rgb_directory(".")
        self.set_expand_directory(".")
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

    def get_crop_pixels(self):
        return int(self.crop_pixels.get())

    def get_extra_pixels(self):
        return int(self.extra_pixels.get())

    def get_width(self):
        geometry = self.get_geometry()
        # print(geometry)
        return int(geometry.split('x')[0])

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

    def get_rgb_directory_entry(self):
        return self.rgb_directory_entry.get()

    def set_rgb_directory_entry(self, text):
        self.rgb_directory_entry.set(text)

    def set_rgb_directory(self, dir):
        self.rgb_directory = dir

    def get_rgb_directory(self):
        return self.rgb_directory

    def get_expand_directory_entry(self):
        return self.expand_directory_entry.get()

    def set_expand_directory_entry(self, text):
        self.expand_directory_entry.set(text)

    def set_expand_directory(self, dir):
        self.expand_directory = dir

    def get_expand_directory(self):
        return self.expand_directory

    def set_output_dir(self, directory):
        self.output_dir = directory

    def get_output_dir(self):
        # output directory changed to be the same with input dir
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
        else:
            self.set_directory_message("Invalid dir", "red")

    def set_rgb_directory_message(self, text, color):
        self.rgb_directory_message['text'] = text
        self.rgb_directory_message['foreground'] = color

    def on_rgb_directory_change(self, *args):
        self.update_gui()
        if self.validate_dir(self.rgb_directory_entry.get()):
            self.set_rgb_directory(self.rgb_directory_entry.get())

    def update_rgb_directory_message(self):
        if self.validate_dir(self.rgb_directory_entry.get()):
            self.set_rgb_directory_message("OK", "green")
        else:
            self.set_rgb_directory_message("Invalid dir", "red")

    def set_expand_directory_message(self, text, color):
        self.expand_directory_message['text'] = text
        self.expand_directory_message['foreground'] = color

    def on_expand_directory_change(self, *args):
        self.update_gui()
        if self.validate_dir(self.expand_directory_entry.get()):
            self.set_expand_directory(self.expand_directory_entry.get())

    def update_expand_directory_message(self):
        if self.validate_dir(self.expand_directory_entry.get()):
            self.set_expand_directory_message("OK", "green")
        else:
            self.set_expand_directory_message("Invalid dir", "red")

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

    def create_widgets(self):
        row = 0
        # Row 0, Input folder

        tk.Label(self.parent, font=self.custom_font,
                 text="Input directory:").grid(row=row, sticky=tk.E,
                                               columnspan=2,
                                               padx=self.get_padding(),
                                               pady=self.get_padding())

        self.directory_entry = tk.StringVar()
        # Initialize value
        self.set_directory_entry(self.get_directory())

        self.directory_entry.trace("w", self.on_directory_change)
        tk.Entry(self.parent,
                 font=self.custom_font,
                 width=64,
                 textvariable=self.directory_entry).grid(row=row,
                                                         column=3,
                                                         columnspan=8,
                                                         sticky=tk.W,
                                                         padx=self.get_padding(),
                                                         pady=self.get_padding())

        self.directory_message = tk.Label(self.parent,
                                          font=self.custom_font2,
                                          text="")
        self.directory_message.grid(row=row,
                                    column=11,
                                    columnspan=2,
                                    sticky=tk.W,
                                    padx=self.get_padding(),
                                    pady=self.get_padding())

        # Initialize dir message value
        self.update_directory_message()

        row += 1
        # Separator
        tk.Frame(height=2,
                 width=2 * MAIN_WINDOW_WIDTH,
                 # bd=1,
                 relief=tk.SUNKEN,
                 bg="black").grid(row=row,
                                  column=0,
                                  columnspan=12,
                                  sticky=tk.W + tk.E,
                                  padx=self.get_padding(),
                                  pady=self.get_padding())

        row += 1
        # Row 2 , 3 buttons:  "run macro 1", "Crop bounds", "Run macro2"
        tk.Button(self.parent,
                  font=self.custom_font,
                  text="RUN Macro 1",
                  command=self.run_macro1).grid(row=row,
                                                column=2,
                                                columnspan=2,
                                                padx=self.get_padding(),
                                                pady=self.get_padding())

        self.script1_message = tk.Label(self.parent,
                                        font=self.custom_font2, text="")
        self.script1_message.grid(row=row + 1,
                                  column=0,
                                  columnspan=4,
                                  sticky=tk.W,
                                  padx=self.get_padding(),
                                  pady=self.get_padding())

        # button "edit crop bounds"
        tk.Button(self.parent, font=self.custom_font,
                  text="Edit crop bounds",
                  command=self.edit_crop_bounds).grid(row=row,
                                                      column=4,
                                                      columnspan=4,
                                                      padx=self.get_padding(),
                                                      pady=self.get_padding())

        # button "run macro 2"
        tk.Button(self.parent, font=self.custom_font,
                  text="Run macro 2",
                  command=self.run_macro2).grid(row=row,
                                                column=8,
                                                columnspan=2,
                                                padx=self.get_padding(),
                                                pady=self.get_padding())

        # button "run one click"
        tk.Button(
            self.parent, font=self.custom_font, bg='orange',
            text="Run One Click",
            command=self.__run_one_click).grid(
                row=row,
                column=10,
                padx=self.get_padding(),
                pady=self.get_padding()
        )

        tk.Button(
            self.parent, font=self.custom_font, bg='cyan',
            text="Generate Mat/Texture for Keyshot",
            command=self.__gen_keyshot_mat).grid(
                row=row,
                column=11,
                padx=self.get_padding(),
                pady=self.get_padding()
        )

        self.script2_message = tk.Label(self.parent,
                                        font=self.custom_font2, text="")
        self.script2_message.grid(row=row + 1,
                                  column=8,
                                  columnspan=5,
                                  sticky=tk.W,
                                  padx=self.get_padding(),
                                  pady=self.get_padding())

        row += 2
        tk.Label(self.parent, font=self.custom_font,
                 text="Crop pixels+:").grid(row=row,
                                            column=2,
                                            columnspan=3,
                                            sticky=tk.E,
                                            padx=self.get_padding(),
                                            pady=self.get_padding())
        self.crop_pixels = tk.StringVar()
        self.crop_pixels.set("2")  # default value
        tk.OptionMenu(self.parent,
                      self.crop_pixels,
                      "0",
                      "1",
                      "2",
                      "3",
                      "4",
                      "5",
                      "6",
                      "7",
                      "8").grid(row=row,
                                column=4,
                                columnspan=4,
                                padx=self.get_padding(),
                                pady=self.get_padding())

        row += 1
        # Separator
        self.separator(row)
        row += 1
        # Row 4, input ModelName
        tk.Label(self.parent, font=self.custom_font,
                 text="ModelName:").grid(row=row, sticky=tk.E,
                                         column=2,
                                         columnspan=2,
                                         padx=self.get_padding(),
                                         pady=self.get_padding())

        self.model_name_entry = tk.StringVar()
        self.model_name_entry.trace("w", self.on_model_name_change)
        tk.Entry(self.parent,
                 font=self.custom_font,
                 textvariable=self.model_name_entry).grid(row=row,
                                                          column=4,
                                                          columnspan=4,
                                                          padx=self.get_padding(),
                                                          pady=self.get_padding())

        row += 1
        # Row 5, button "read data from crop_report"
        tk.Button(self.parent, font=self.custom_font,
                  text="Read data from crop_report.csv",
                  command=self.read_sequences).grid(row=row,
                                                    column=4,
                                                    columnspan=4,
                                                    padx=self.get_padding(),
                                                    pady=self.get_padding())

        self.script3_message = tk.Label(self.parent,
                                        font=self.custom_font2, text="")
        self.script3_message.grid(row=row,
                                  column=8,
                                  columnspan=4,
                                  sticky=tk.W,
                                  padx=self.get_padding(),
                                  pady=self.get_padding())

        row += 1
        # Row 6, button "generate part csv a"
        tk.Button(self.parent, font=self.custom_font,
                  text="Generate Part CSV (Part A)",
                  command=self.generate_part_csv_part_a).grid(row=row,
                                                              column=4,
                                                              columnspan=4,
                                                              padx=self.get_padding(),
                                                              pady=self.get_padding())

        self.script4_message = tk.Label(self.parent,
                                        font=self.custom_font2, text="")
        self.script4_message.grid(row=row,
                                  column=8,
                                  columnspan=4,
                                  sticky=tk.W,
                                  padx=self.get_padding(),
                                  pady=self.get_padding())

        row += 1
        # Row 6, button "generate part csv b"
        tk.Button(self.parent, font=self.custom_font,
                  text="Generate Part CSV (Part B)",
                  command=self.generate_part_csv_part_b).grid(row=row,
                                                              column=4,
                                                              columnspan=4,
                                                              padx=self.get_padding(),
                                                              pady=self.get_padding())

        self.script5_message = tk.Label(self.parent,
                                        font=self.custom_font2, text="")
        self.script5_message.grid(row=row,
                                  column=8,
                                  columnspan=4,
                                  sticky=tk.W,
                                  padx=self.get_padding(),
                                  pady=self.get_padding())

        row += 1
        self.separator(row)

        row += 1
        # Row 6, button "generate part csv"
        tk.Button(self.parent, font=self.custom_font,
                  text="Generate TMenu overlay images",
                  command=self.generate_tmenu_buttons).grid(row=row,
                                                            column=4,
                                                            columnspan=4,
                                                            padx=self.get_padding(),
                                                            pady=self.get_padding())

        self.script6_message = tk.Label(self.parent,
                                        font=self.custom_font2, text="")
        self.script6_message.grid(row=row,
                                  column=8,
                                  columnspan=4,
                                  sticky=tk.W,
                                  padx=self.get_padding(),
                                  pady=self.get_padding())

        row += 1
        # Row 6, button "generate part csv"
        tk.Button(self.parent, font=self.custom_font,
                  text="Glue overlay images on TMenu buttons",
                  command=self.glue_overlays).grid(row=row,
                                                   column=4,
                                                   columnspan=4,
                                                   padx=self.get_padding(),
                                                   pady=self.get_padding())

        self.script7_message = tk.Label(self.parent,
                                        font=self.custom_font2, text="")
        self.script7_message.grid(row=row,
                                  sticky=tk.W,
                                  column=8,
                                  columnspan=4,
                                  padx=self.get_padding(),
                                  pady=self.get_padding())

        row += 1
        # Row 6, button "generate part csv"
        tk.Button(self.parent, font=self.custom_font,
                  text="Process Shadows",
                  command=self.process_shadows).grid(row=row,
                                                     column=4,
                                                     columnspan=4,
                                                     padx=self.get_padding(),
                                                     pady=self.get_padding())

        self.script9_message = tk.Label(self.parent,
                                        font=self.custom_font2, text="")
        self.script9_message.grid(row=row,
                                  column=8,
                                  columnspan=4,
                                  sticky=tk.W,
                                  padx=self.get_padding(),
                                  pady=self.get_padding())

        row += 1
        self.separator(row)

        row += 1
        # Row 6, button "generate part csv"
        # Row 6, button "generate part csv"
        tk.Button(self.parent, font=self.custom_font,
                  text="Copy images",
                  command=self.copy_originals).grid(row=row,
                                                    column=1,
                                                    columnspan=2,
                                                    padx=self.get_padding(),
                                                    pady=self.get_padding())
        tk.Button(self.parent, font=self.custom_font,
                  text="Resize images",
                  command=self.resize_images).grid(row=row,
                                                   column=4,
                                                   columnspan=2,
                                                   padx=self.get_padding(),
                                                   pady=self.get_padding())

        self.script8_message = tk.Label(self.parent,
                                        font=self.custom_font2, text="")
        self.script8_message.grid(row=row + 1,
                                  column=4,
                                  columnspan=5,
                                  sticky=tk.W,
                                  padx=self.get_padding(),
                                  pady=self.get_padding())

        self.script81_message = tk.Label(self.parent,
                                         font=self.custom_font2, text="")
        self.script81_message.grid(row=row + 1,
                                   column=1,
                                   columnspan=5,
                                   sticky=tk.W,
                                   padx=self.get_padding(),
                                   pady=self.get_padding())

        tk.Label(self.parent, font=self.custom_font,
                 text="RGB:").grid(row=row,
                                   column=6,
                                   columnspan=1,
                                   sticky=tk.E,
                                   padx=self.get_padding(),
                                   pady=self.get_padding())

        self.interpolation_method = tk.StringVar()
        self.interpolation_method.set("bilinear")  # default value
        tk.OptionMenu(self.parent,
                      self.interpolation_method,
                      "lanczos",
                      "nearest",
                      "bilinear",
                      "bicubic",
                      "cubic").grid(row=row,
                                    column=7,
                                    columnspan=1,
                                    padx=self.get_padding(),
                                    pady=self.get_padding())

        tk.Label(self.parent, font=self.custom_font,
                 text="A:").grid(row=row,
                                 column=8,
                                 columnspan=1,
                                 sticky=tk.E,
                                 padx=self.get_padding(),
                                 pady=self.get_padding())
        self.alpha_interpolation_method = tk.StringVar()
        self.alpha_interpolation_method.set("bilinear")  # default value
        tk.OptionMenu(self.parent,
                      self.alpha_interpolation_method,
                      "lanczos",
                      "nearest",
                      "bilinear",
                      "bicubic",
                      "cubic").grid(row=row,
                                    column=9,
                                    columnspan=1,
                                    padx=self.get_padding(),
                                    pady=self.get_padding())

        row += 2
        self.separator(row)
        # Input folder for rgb reset
        row += 1
        text = "Input directory for RGB reset:"
        tk.Label(self.parent, font=self.custom_font,
                 text=text).grid(row=row,
                                 columnspan=4,
                                 sticky=tk.E,
                                 padx=self.get_padding(),
                                 pady=self.get_padding())

        self.rgb_directory_entry = tk.StringVar()
        # Initialize value
        self.set_rgb_directory_entry(self.get_rgb_directory())

        self.rgb_directory_entry.trace("w", self.on_rgb_directory_change)
        tk.Entry(self.parent,
                 width=50,
                 font=self.custom_font,
                 textvariable=self.rgb_directory_entry).grid(row=row,
                                                             column=3,
                                                             columnspan=8,
                                                             padx=self.get_padding(),
                                                             pady=self.get_padding())

        self.rgb_directory_message = tk.Label(self.parent,
                                              font=self.custom_font2, text="")
        self.rgb_directory_message.grid(row=row,
                                        column=11,
                                        columnspan=2,
                                        sticky=tk.W,
                                        padx=self.get_padding(),
                                        pady=self.get_padding())

        # Initialize dir message value
        self.update_rgb_directory_message()

        row += 1
        tk.Label(self.parent, font=self.custom_font,
                 text="RGB reset pixels:").grid(row=row,
                                                column=2,
                                                columnspan=3,
                                                sticky=tk.E,
                                                padx=self.get_padding(),
                                                pady=self.get_padding())
        self.extra_pixels = tk.StringVar()
        self.extra_pixels.set("2")  # default value
        tk.OptionMenu(self.parent,
                      self.extra_pixels,
                      "8",
                      "4",
                      "2").grid(row=row,
                                column=4,
                                columnspan=4,
                                padx=self.get_padding(),
                                pady=self.get_padding())

        row += 1

        self.var_run_rgb_rest = tk.IntVar()
        self.var_run_rgb_rest.set(1)

        # Row 6, checkbox "run rgb reset"
        tk.Checkbutton(self.parent, font=self.custom_font, bg='orange',
                       text="Include RGB reset in One Click",
                       variable=self.var_run_rgb_rest).grid(row=row,
                                                            column=2,
                                                            columnspan=2,
                                                            padx=self.get_padding(),
                                                            pady=self.get_padding())

        # Row 6, button "run rgb reset"
        tk.Button(self.parent, font=self.custom_font,
                  text="Run RGB reset",
                  command=self.run_rgb_reset).grid(row=row,
                                                   column=4,
                                                   columnspan=4,
                                                   padx=self.get_padding(),
                                                   pady=self.get_padding())

        tk.Button(self.parent, font=self.custom_font, bg='orange',
                  text="Run Texture Packer",
                  command=self.__run_texturepacker).grid(row=row,
                                                         column=8,
                                                         columnspan=2,
                                                         padx=self.get_padding(),
                                                         pady=self.get_padding())

        self.script11_message = tk.Label(self.parent,
                                         font=self.custom_font2, text="")
        self.script11_message.grid(row=row + 1,
                                   column=2,
                                   columnspan=10,
                                   sticky=tk.W,
                                   padx=self.get_padding(),
                                   pady=self.get_padding())

        row += 2
        self.separator(row)
        # Input folder for expand reset
        row += 1
        tk.Label(self.parent, font=self.custom_font,
                 text="Input directory for expand:").grid(row=row,
                                                          columnspan=4,
                                                          sticky=tk.E,
                                                          padx=self.get_padding(),
                                                          pady=self.get_padding())

        self.expand_directory_entry = tk.StringVar()
        # Initialize value
        self.set_expand_directory_entry(self.get_expand_directory())

        self.expand_directory_entry.trace("w", self.on_expand_directory_change)
        tk.Entry(self.parent,
                 width=50,
                 font=self.custom_font,
                 textvariable=self.expand_directory_entry).grid(row=row,
                                                                column=3,
                                                                columnspan=8,
                                                                padx=self.get_padding(),
                                                                pady=self.get_padding())

        self.expand_directory_message = tk.Label(self.parent,
                                                 font=self.custom_font2, text="")
        self.expand_directory_message.grid(row=row,
                                           column=11,
                                           columnspan=2,
                                           sticky=tk.W,
                                           padx=self.get_padding(),
                                           pady=self.get_padding())

        # Initialize dir message value
        self.update_expand_directory_message()

        row += 1
        tk.Label(self.parent,
                 font=self.custom_font,
                 text="Expand parts pixels:").grid(row=row,
                                                   column=1,
                                                   columnspan=3,
                                                   sticky=tk.E,
                                                   padx=self.get_padding(),
                                                   pady=self.get_padding())

        self.extra_pixels = tk.StringVar()
        self.extra_pixels.set("1")  # default value
        tk.OptionMenu(self.parent,
                      self.extra_pixels,
                      "2",
                      "3",
                      "4").grid(row=row,
                                column=4,
                                columnspan=2,
                                padx=self.get_padding(),
                                pady=self.get_padding())

        tk.Label(self.parent,
                 font=self.custom_font,
                 text="Image filter:").grid(row=row,
                                            column=5,
                                            columnspan=3,
                                            sticky=tk.E,
                                            padx=self.get_padding(),
                                            pady=self.get_padding())

        self.filter_operation = tk.StringVar()
        self.filter_operation.set("sharpen")  # default value
        tk.OptionMenu(self.parent,
                      self.filter_operation,
                      "blur",
                      "contour",
                      "detail",
                      "edge_enhance",
                      "edge_enhance_more",
                      "emboss",
                      "find_edges",
                      "smooth",
                      "smooth_more",
                      "sharpen").grid(row=row,
                                      column=8,
                                      columnspan=2,
                                      padx=self.get_padding(),
                                      pady=self.get_padding())

        row += 1
        # Row 6, button "generate part csv"
        tk.Button(self.parent,
                  font=self.custom_font,
                  text="Apply",
                  command=self.apply_filter).grid(row=row,
                                                  column=7,
                                                  columnspan=3,
                                                  padx=self.get_padding(),
                                                  pady=self.get_padding())

        self.script13_message = tk.Label(self.parent,
                                         font=self.custom_font2, text="")
        self.script13_message.grid(row=row + 1,
                                   column=6,
                                   columnspan=6,
                                   sticky=tk.W,
                                   padx=self.get_padding(),
                                   pady=self.get_padding())

        # Row 6, button "generate part csv"
        tk.Button(self.parent,
                  font=self.custom_font,
                  text="Expand part",
                  command=self.run_expand).grid(row=row,
                                                column=3,
                                                columnspan=3,
                                                padx=self.get_padding(),
                                                pady=self.get_padding())

        self.script12_message = tk.Label(self.parent,
                                         font=self.custom_font2, text="")
        self.script12_message.grid(row=row + 1,
                                   column=2,
                                   columnspan=10,
                                   sticky=tk.W,
                                   padx=self.get_padding(),
                                   pady=self.get_padding())

    def separator(self, row):
        sep = tk.Frame(height=2,
                       width=2 * MAIN_WINDOW_WIDTH,
                       # bd=1,
                       relief=tk.SUNKEN,
                       bg="black").grid(row=row,
                                        column=0,
                                        columnspan=12,
                                        sticky=tk.W + tk.E,
                                        padx=self.get_padding(),
                                        pady=self.get_padding())
        return sep

    def apply_filter(self):
        paths = []
        paths.append(self.get_expand_directory())
        for path in paths:
            images = glob.glob(path + "/*.png")
            for image_path in images:
                self.set_script13_message("Applying filter {}".format(image_path),
                                          "green")

                im = misc.imread(image_path)
                # Ensure existence of alpha channel
                im = misc.imfilter(im, self.filter_operation.get())
                basename = os.path.basename(image_path)
                misc.imsave(image_path, im)

        self.set_script13_message("Done", "green")

    def validate_image_name(self, image_name):
        part = os.path.basename(image_name).split('_')[0]
        if part in self.exclude_parts:
            return False
        else:
            return True

    def run_expand(self):
        # Check part names for exclude
        self.exclude_parts = []
        path = self.get_expand_directory()

        images = glob.glob(path + "/*.png")
        for image in images:
            #part = image.split
            part = os.path.basename(image).split('_')[0]
            if not part in self.exclude_parts:
                self.exclude_parts.append(part)
        dialog = ExcludePartsDialog(self)
        self.wait_window(dialog)

        for i in range(self.get_extra_pixels()):
            self.run_expand_loop()

    # Expand parts

    # 1 Make temp directory
    # 2 Save the results there
    # 3 Then copy back to the orig dir
    # 4 remove temp directory
    def run_expand_loop(self):
        paths = []
        paths.append(self.get_expand_directory())
        out_path = 'temp'
        for path in paths:
            try:
                os.makedirs(os.path.join(path, out_path))
            except:
                logging.debug("Could not create directory")
            images = glob.glob(path + "/*.png")
            for image_path in images:
                # Check if the image should be expanded
                if not self.validate_image_name(image_path):
                    continue
                self.set_script12_message("Expanding {}".format(image_path),
                                          "green")

                im = misc.imread(image_path)
                # Ensure existence of alpha channel
                if im.shape[2] > 3:
                    out = self.expand(im, image_path)
                    basename = os.path.basename(image_path)
                    misc.imsave(os.path.join(path,
                                             out_path,
                                             basename), out)
            # Copy images back to the original folder
            images = os.listdir(os.path.join(path, out_path))
            for image in images:
                self.set_script12_message(
                    "Copying image {}".format(image), "green")
                src = os.path.join(path, out_path, image)
                dst = os.path.join(path, image)
                try:
                    shutil.copyfile(src, dst)
                except:
                    self.set_script12_message(
                        'Could not copy {}'.format(image), "green")
            # Remove temporary directory
            try:
                self.set_script12_message('Removing temporary dir {}'.format(
                    os.path.join(path, out_path)), "green")
                shutil.rmtree(os.path.join(path, out_path))
            except:
                self.set_script12_message('Could not remove directory {}'.format(
                    os.path.join(path, out_path)), "green")
        self.set_script12_message("Done", "green")

    # Get corresponding clay image with a
    # correct index
    def get_clay(self, image_path):
        base = Sequence.parse_base(image_path)
        directory = os.path.abspath(os.path.dirname(image_path))
        index = Sequence.index(image_path)
        card = "{}*/{}_Clay*.{}.png".format(directory, base, index)
        clay = glob.glob(card)
        if len(clay) > 0:
            filename = clay[0]
            return misc.imread(filename)
        else:
            return None

    def alpha_cutout(self, images, image_path):
        new = []
        if "Clay" in image_path:
            clay = images[0]
        else:
            clay = self.get_clay(image_path)
        try:
            if clay == None:
                logging.debug("Clay not found for {}".format(image_path))
                return []
        except:
            pass

        new = []
        for i, image in enumerate(images):
            new.append(image.copy().astype(np.float64))

        for i, image in enumerate(images):
            if i != 0:
                new[i][:, :, 3] = (255 - clay[:, :, 3]) / 255 * image[:, :, 3]

        return new

    def expand(self, orig, image_path):
        im = orig.copy()
        dtype = np.float64
        out = np.zeros(im.shape, dtype)
        left = im.copy()
        right = im.copy()
        top = im.copy()
        bottom = im.copy()

        mask = im[:, :, 3] > 0
        # Shift image by 1 pixel
        left[:-1, :, :] = im[1:, :, :]
        right[1:, :, :] = im[:-1, :, :]
        top[:, :-1, :] = im[:, 1:, :]
        bottom[:, 1:, :] = im[:, :-1, :]
        images = [im, left, right, top, bottom]
        images = self.alpha_cutout(images, image_path)
        weights = []
        wsum = np.zeros(im[:, :, 0].shape, dtype)
        wtsum = np.zeros(im[:, :, 0].shape, dtype)
        tsum = np.zeros(im[:, :, 0].shape, dtype)
        transmissions = []

        # Calculate weights from alpha channel
        for image in images:
            w = image[:, :, 3] / 255
            weights.append(w.copy())

        # Weight sum
        for w in weights:
            wsum += w

        # Calculate transmissions (1-weight) of layers
        for i, w in enumerate(weights):
            if i == 0:
                t = np.ones(im[:, :, 0].shape, dtype)
                transmissions.append(t.copy())
                t *= (1 - w)
            else:
                transmissions.append(t.copy())
                t *= (1 - w)

        # Sum of transmissions
        for t in transmissions:
            tsum += t

        for i, w in enumerate(weights):
            wtsum += w * transmissions[i]
        mask = wtsum > 0
        imask = wtsum == 0
        # RGB
        for i, image in enumerate(images):
            out[mask, 0] += ((transmissions[i][mask]) * image[mask, 0]
                             * weights[i][mask] / wtsum[mask]).astype(dtype)
            out[mask, 1] += ((transmissions[i][mask]) * image[mask, 1]
                             * weights[i][mask] / wtsum[mask]).astype(dtype)
            out[mask, 2] += ((transmissions[i][mask]) * image[mask, 2]
                             * weights[i][mask] / wtsum[mask]).astype(dtype)
        out[imask, 0] += im[imask, 0]
        out[imask, 1] += im[imask, 1]
        out[imask, 2] += im[imask, 2]

        # A
        alpha = np.ones(im[:, :, 0].shape, dtype)
        for w in weights:
            alpha *= (1 - w)
        alpha = (1 - alpha) * 255

        # Try to avoid errornous rounding down
        out[:, :, 3] = alpha.round()
        return out

    def expand_old(self, im):
        out = im.copy()

        interesting = (im[:, :, 3] == 0)
        positive = (im[:, :, 0] > 0)
        process = np.logical_and(interesting, positive)
        for i in range(im.shape[0]):
            for j in range(im.shape[1]):
                if not process[i, j]:
                    continue

                if i == 0:
                    sx = i
                else:
                    sx = i - 1

                if i == im.shape[0] - 1:
                    ex = i + 1
                else:
                    ex = i + 2

                if j == 0:
                    sy = j
                else:
                    sy = j - 1

                if j == im.shape[1] - 1:
                    ey = j + 1
                else:
                    ey = j + 2

                neighbours_a = im[sx:ex, sy:ey, 3]
                if im[i, j, 3] == 0 and len(neighbours_a[neighbours_a > 0]) > 0:
                    #median = np.median(neighbours_a[neighbours_a>0])
                    avg = np.mean(neighbours_a[neighbours_a > 0])
                    #add = int(0.75*median)
                    add = 0.75 * avg
                    for k in range(sx, ex):
                        for l in range(sy, ey):
                            if im[k, l, 3] > 0:
                                #out[k,l,3] = int(np.min([im[k,l,3] + 0.6 * add + 0.4 * np.random.rand()*add, 255]))
                                out[k, l, 3] = 255
                                #out[k,l,3] = int(np.min([im[k,l,3] + add, 255]))

                    # Set the actual new alpha value
                    out[i, j, 3] = int(0.6 * add + 0.4 *
                                       np.random.rand() * add)
                    #out[i,j,3] = int(add)

        return out

    # RGB reset
    def run_rgb_reset(self):
        edge_width = 2 * int(self.extra_pixels.get())
        path = self.get_rgb_directory()
        images = glob.glob(path + "/*.png")
        for image_path in images:
            self.set_script11_message(
                "Processing rgb reset for {}".format(image_path), "green")
            im = misc.imread(image_path)
            out = im.copy()
            # Expansion of the aplha
            mask = ndimage.maximum_filter(im[:, :, 3], edge_width)
            pixels = (mask == 0)
            out[pixels, 0:3] = 0
            misc.imsave(image_path, out)
        self.set_script11_message("Done", "green")

    # Mapper for Numpy arrays
    def linear_map(self, x, b):
        a = 1 - b / 255
        y = a * x + b
        return y.astype(np.uint8)

    def tweak_alpha_edge(self, bias):
        paths = []
        paths.append(os.path.join(self.get_output_dir(),
                                  self.get_model_name(),
                                  self.get_model_name() + '_Model -HD'))
        paths.append(os.path.join(self.get_output_dir(),
                                  self.get_model_name(),
                                  self.get_model_name() + '_Model -SD'))
        paths.append(os.path.join(self.get_output_dir(),
                                  self.get_model_name(),
                                  self.get_model_name() + '_Model -LD'))
        for path in paths:
            images = glob.glob(path + "/*.png")
            for image_path in images:
                self.set_script10_message(
                    "Processing alpha edge of {}".format(image_path), "green")

                im = misc.imread(image_path)
                # Ensure existence of alpha channel
                if im.shape[2] > 3:
                    pixels = np.logical_and(
                        im[:, :, 3] > 0, im[:, :, 3] != 255)
                    im[pixels, 3] = self.linear_map(im[pixels, 3], bias)
                    misc.imsave(image_path, im)

        self.set_script10_message("Done", "green")

    def enhance_alpha_edge(self):
        AlphaTweak(self)

    def process_shadows(self):
        
        path = os.path.join(self.get_directory(),
                            "Z_SHADOW")
        images = glob.glob(path + "/*.png")
        if len(images) == 0:
            self.set_script9_message("Shadow folder not found", "red")
            return

        processed = []
        image_names = []
        masks = []
        for i in range(len(images)):
            self.set_script9_message(
                "Reading file {} of {}".format(i + 1, len(images)), "green")
            image_path = images[i]
            if i == 0:
                self.shadows = Sequence(image_path)
            else:
                self.shadows.add_image(image_path)
            image = misc.imread(image_path)
            mask = misc.imread(image_path, flatten=True)
            # Invert RGB signals
            for k in range(3):
                image[:, :, k] = 255 - image[:, :, k]
            processed.append(image)
            image_names.append(os.path.basename(image_path))
            masks.append(mask)
            # misc.imsave(os.path.join(path,
            #                        "{}_inv.png".format(i)),
            #           image)

        # Do the crop analysis
        for i, image in enumerate(processed):
            if i == 0:
                reference_shape = image.shape
                result = np.zeros(reference_shape)
            result = np.logical_or(result, image)

        nonzeros = np.nonzero(result)
        row_start = min(nonzeros[0])
        col_start = min(nonzeros[1])
        row_end = max(nonzeros[0])
        col_end = max(nonzeros[1])

        # Add "bleed pixels in all directions"
        bleed_pixels = self.get_crop_pixels()
        if row_start >= bleed_pixels:
            row_start -= bleed_pixels
        if row_end < reference_shape[0] - bleed_pixels:
            row_end += bleed_pixels
        if col_start >= bleed_pixels:
            col_start -= bleed_pixels
        if col_end < reference_shape[1] - bleed_pixels:
            col_end += bleed_pixels

        # Make crop size even
        if (row_end - row_start + 1) % 2:
            if row_start > 0:
                row_start -= 1
            elif row_end < reference_shape[0]:
                row_end += 1
            else:
                self.set_script9_message(
                    "Error occured, can't make it even!", "red")
        if (col_end - col_start + 1) % 2:
            if col_start > 0:
                col_start -= 1
            elif col_end < reference_shape[1]:
                col_end += 1
            else:
                self.set_script9_message(
                    "Error occured, can't make it even!", "red")

        crop_bounds = "{},{},{},{}".format(
            row_start, col_start, row_end + 1, col_end + 1)
        self.shadows.set_crop_bounds(crop_bounds)
        dialog = ShadowCropAnalysisResults(self)

        if self.one_click:
            dialog.quit()
        else:
            self.wait_window(dialog)

        # Update variables
        crop_bounds_str = self.shadows.get_crop_bounds()
        crop_bounds = crop_bounds_str.split(",")
        try:
            row_start = int(crop_bounds[0])
            col_start = int(crop_bounds[1])
            row_end = int(crop_bounds[2])
            col_end = int(crop_bounds[3])
        except:
            messagebox.showerror("Invalid shadow crop bound",
                                 "Invalid crop bound {}".format(crop_bounds_str))
            return

        # Crop images
        out = []
        for i, image in enumerate(processed):
            self.set_script9_message(
                "Processing file " + str(i + 1) + " of " + str(len(images)), "green")

            #o = np.zeros((row_end-row_start, col_end-col_start,4), np.uint8)
            #o[:,:,0:3] = i[row_start:row_end,col_start:col_end,0:3]
            # Set the r signal to be the alpha channel
            #o[:,:,3] = o[:,:,0]

            # test
            o = np.zeros(
                (row_end - row_start, col_end - col_start, 4), np.uint8)
            mask = masks[i][row_start:row_end, col_start:col_end]
            o[:, :, 3] = self.rgb_to_gray(
                image[row_start:row_end, col_start:col_end]) * mask / 255
            out.append(o)
        # Save shadow images
        out_path = os.path.join(self.get_directory(),
                                "Shadow")

        try:
            os.makedirs(out_path)
        except:
            logging.debug("Could not create directory {}".format(out_path))

        for i in range(len(out)):
            self.set_script9_message(
                "Saving file " + str(i + 1) + " of " + str(len(images)), "green")

            misc.imsave(os.path.join(out_path,
                                     image_names[i]),
                        out[i])

        # Power of 2 resizing
        dialog = ShadowResizeSummary(self, out[0].shape)
        if self.one_click:

            mybase = self.shadows.get_base()
            dialog.sizes[mybase].set('128,512')
            dialog.quit()

        else:
            self.wait_window(dialog)

        size = self.shadows.get_power_of_two_size()

        # Copy HD images
        out_path = os.path.join(self.get_output_dir(),
                                self.get_model_name(),
                                self.get_model_name() + '_Model -HD')
        for i in range(len(out)):
            self.set_script9_message(
                "Scaling HD " + str(i + 1) + " of " + str(len(images)), "green")
            width = int(size[0])
            height = int(size[1])
            scaled = self.resize(out[i], width, height)
            misc.imsave(os.path.join(out_path,
                                     image_names[i]),
                        scaled)

        # SD Images
        out_path = os.path.join(self.get_output_dir(),
                                self.get_model_name(),
                                self.get_model_name() + '_Model -SD')
        for i in range(len(out)):
            self.set_script9_message(
                "Scaling SD " + str(i + 1) + " of " + str(len(images)), "green")
            width = int(int(size[0]) / 2)
            height = int(int(size[1]) / 2)
            scaled = self.resize(out[i], width, height)
            misc.imsave(os.path.join(out_path,
                                     image_names[i]),
                        scaled)

        # LD Images
        out_path = os.path.join(self.get_output_dir(),
                                self.get_model_name(),
                                self.get_model_name() + '_Model -LD')

        for i in range(len(out)):
            self.set_script9_message(
                "Scaling LD " + str(i + 1) + " of " + str(len(images)), "green")
            width = int(int(size[0]) / 4)
            height = int(int(size[1]) / 4)
            scaled = self.resize(out[i], width, height)
            misc.imsave(os.path.join(out_path,
                                     image_names[i]),
                        scaled)

        # Add shadow line to the Parts.csv
        with open(os.path.join(self.script_path,
                               'part_csv_shadow.csv'), 'r') as f:
            shadow = f.read()

        # Crop bounds
        sx = (col_end - col_start) / 2
        sy = (row_end - row_start) / 2
        px = (sx + col_start) / 2
        py = 802.5 - (sy + row_start) / 2
        shadow = shadow.replace('[sx]', str(sx))
        shadow = shadow.replace('[sy]', str(sy))
        shadow = shadow.replace('[px]', str(px))
        shadow = shadow.replace('[py]', str(py))

        file_out = os.path.join(self.get_output_dir(),
                                self.get_model_name(),
                                self.get_model_name() + '_Parts.csv')
        with open(file_out, 'r') as f:
            parts = f.readlines()

        output = ""
        for i, line in enumerate(parts):
            if i == 1:
                output += shadow
            output += line
        with open(file_out, 'w') as f:
            f.write(self.mac_csv(output))

        self.set_script9_message("Done", "green")

    def resize_images(self):
        dialog = ResizeSummary(self)
        if self.one_click:
            dialog.quit()

    def on_model_name_change(self, *args):
        self.set_model_name(self.model_name_entry.get())

    def set_model_name(self, name):
        self.model_name = name

    def get_model_name(self):
        return self.model_name

    def edit_crop_bounds(self):
        if len(self.get_mask_sequences()):
            CropAnalysisResults(self)

    def init_sequences(self):
        self.mask_sequences = {}
        self.source_sequences = {}

    def get_mask_sequences(self):
        return self.mask_sequences

    def get_mask_sequence(self, base):
        return self.get_mask_sequences()[base]

    def add_mask_sequence(self, sequence):
        if not sequence.get_base() in self.get_mask_sequences():
            self.get_mask_sequences()[sequence.get_base()] = sequence

    def mask_sequence_exists(self, base):
        return base in self.get_mask_sequences()

    def get_source_sequences(self):
        return self.source_sequences

    def get_source_sequence(self, base):
        return self.get_source_sequences()[base]

    def add_source_sequence(self, sequence):
        if not sequence.get_base() in self.get_source_sequences():
            self.get_source_sequences()[sequence.get_base()] = sequence

    def source_sequence_exists(self, base):
        return base in self.get_source_sequences()

    def __extract_prefix(self, basename):
        rgx = re.compile(r'^\d+')
        rslt = rgx.search(basename)
        if rslt:
            return rslt.group(0)

    def generate_part_csv_part_a(self):
        self.set_script4_message("Running", "green")
        dialog = GeneratePartCSVInputs(self)
        if self.one_click:
            items = []
            for base, sequence in self.get_mask_sequences().items():
                prefix = self.__extract_prefix(base)
                items.append(None)
                items.append(prefix)
                items.append(prefix)
                #import pdb; pdb.set_trace()
                if self.get_model_name() in self.my_config:
                    frameSetup = self.my_config[self.get_model_name(
                    )]['frameSetup']
                    tmenu_frame = int(frameSetup.split(",")[2])
                    items.append(tmenu_frame)
                else:
                    logging.debug('Warning: TMenu frame number was not found in Real3D_V1.csv for model {}'.format(
                        self.get_model_name()))
                    logging.debug('Using frame # 8. Maybe this will throw error.')
                    items.append(8)

            i = 0
            for item in items:
                if item:
                    dialog.entries[i].set(item)
                i += 1

            dialog.quit()

        self.set_script4_message("Done", "green")

    def generate_part_csv_part_b(self):
        self.set_script5_message("Running", "green")
        self.copy_model_folder_structure()
        self.generate_part_csv()
        self.generate_features_csv()
        self.set_script5_message("Done", "green")

    def generate_tmenu_buttons(self):
        self.set_script6_message("Running", "green")
        tmenu_base_path = os.path.join(self.get_output_dir(),
                                       self.get_model_name(),
                                       self.get_model_name() + '_UI',
                                       'TMenu')
        try:
            image_path = os.path.join(tmenu_base_path,
                                      'TMenu.png')
            tmenu_base = misc.imread(image_path)
        except:
            self.set_script6_message(
                "Error, could not open image {}".format(image_path), "red")
            return

        for base, sequence in self.get_mask_sequences().items():
            # Get the image
            self.set_script6_message(
                "Generating TMenu {}".format(base), "green")
            image_path = os.path.join(self.get_directory(),
                                      base,
                                      base + '_Clay1.' + str(sequence.get_part_params()[3]) + '.png')
            try:
                overlay = misc.imread(image_path)
            except:
                self.set_script6_message(
                    "Error, could not open image {}".format(image_path), "red")
                return

            # Let's do the overlay
            # Crop overlay
            nonzeros = np.nonzero(overlay[:, :, 3])
            if len(nonzeros[0]) == 0 or len(nonzeros[1]) == 0:
                cropped = overlay.copy()
            else:
                row_start = min(nonzeros[0])
                col_start = min(nonzeros[1])
                row_end = max(nonzeros[0])
                col_end = max(nonzeros[1])
                cropped = overlay[row_start:row_end, col_start:col_end]

            # Resize overlay
            scale_factor = 0.60 * np.min([tmenu_base.shape[0] / (1.0 * cropped.shape[0]),
                                          tmenu_base.shape[1] / (1.0 * cropped.shape[1])])
            cropped = misc.imresize(
                cropped, scale_factor, interp=self.interpolation_method.get())
            zeros = np.zeros(np.shape(tmenu_base))
            # Padding
            padding_top = int((tmenu_base.shape[0] - cropped.shape[0]) / 2)
            padding_left = int((tmenu_base.shape[1] - cropped.shape[1]) / 2)
            zeros[padding_top:padding_top + cropped.shape[0],
                  padding_left:padding_left + cropped.shape[1],
                  :] = cropped

            # Contrast to 0.25
            zeros[:, :, 0:3] = 0.25 * zeros[:, :, 0:3]
            tmenu_base_path = os.path.join(self.get_output_dir(),
                                           self.get_model_name(),
                                           self.get_model_name() + '_UI',
                                           'TMenu')
            path = os.path.join(tmenu_base_path,
                                "{}_tmenu_overlay_temp.png".format(base))
            misc.imsave(path, zeros)

        self.set_script6_message("Done", "green")

    def glue_overlays(self):
        self.set_script7_message("Running", "green")
        tmenu_base_path = os.path.join(self.get_output_dir(),
                                       self.get_model_name(),
                                       self.get_model_name() + '_UI',
                                       'TMenu')
        try:
            tmenu_base = misc.imread(os.path.join(tmenu_base_path,
                                                  'TMenu.png'))
        except:
            self.set_script6_message("Error, could not open image", "red")

        # Exctract the shadow
        shadowing = np.logical_and(
            tmenu_base[:, :, 3] > 0, tmenu_base[:, :, 3] < 255)

        for base, sequence in self.get_mask_sequences().items():
            self.set_script7_message(
                "Processing image {}".format(base), "green")
            path = os.path.join(tmenu_base_path,
                                "{}_tmenu_overlay_temp.png".format(base))
            overlay = misc.imread(path)

            # Blur the image and copy blur the base border
            blurred = ndimage.uniform_filter(overlay[:, :, 3], 3)
            pixels = blurred > 0
            bg = tmenu_base.copy()
            bg[pixels, 3] = 255 - blurred[pixels]
            # Threshold
            bg[bg[:, :, 3] < 100] = 0
            out = np.zeros(overlay.shape)
            overlay[:, :, 3] = ndimage.uniform_filter(overlay[:, :, 3], 2)
            for i in range(overlay.shape[0]):
                for j in range(overlay.shape[1]):
                    if bg[i, j, 3] > 0:
                        out[i, j] = bg[i, j]
                    elif overlay[i, j, 3] > 0:
                        out[i, j] = overlay[i, j]

            # Return the original shadow
            out[shadowing] = tmenu_base[shadowing]
            misc.imsave(os.path.join(tmenu_base_path,
                                     'TMenu_{}.png'.format(base)), out)
        self.set_script7_message("Done", "green")

    def generate_features_csv(self):
        with open(os.path.join(self.script_path,
                               'features_csv_base.csv'), 'r') as f:
            start = f.read()
        with open(os.path.join(self.script_path,
                               'features_csv_end.csv'), 'r') as f:
            end = f.read()
        with open(os.path.join(self.script_path,
                               'features_csv_line.csv'), 'r') as f:
            orig_line = f.read()

        lines = ''
        for base, sequence in self.get_mask_sequences().items():
            line = orig_line
            line = line.replace('[Part]', str(base))
            lines += line

        # Glue the parts together
        output = start + lines + end
        file_out = os.path.join(self.get_output_dir(),
                                self.get_model_name(),
                                self.get_model_name() + '_Features.csv')
        with open(file_out, 'w') as f:
            f.write(self.mac_csv(output))

    def mac_csv(self, text):
        text = text.replace('\r\n', '\r')
        text = text.replace('\n', '\r')
        return text

    def generate_part_csv(self):
        with open(os.path.join(self.script_path,
                               'part_csv_base.csv'), 'r') as f:
            start = f.read()
        with open(os.path.join(self.script_path,
                               'part_csv_end.csv'), 'r') as f:
            end = f.read()
        with open(os.path.join(self.script_path,
                               'part_csv_line.csv'), 'r') as f:
            orig_line = f.read()
        with open(os.path.join(self.script_path,
                               'part_csv_1stEmpty_line.csv'), 'r') as f:
            orig_1stEmpty_line = f.read()

        lines = ''
        largest_order = 0
        for base, sequence in self.get_mask_sequences().items():
            # Update largest order
            try:
                if int(sequence.get_part_params()[1]) > largest_order:
                    largest_order = int(sequence.get_part_params()[1])
            except:
                pass

            # Check 1stEmpty
            if sequence.get_part_params()[0] == 0:
                line = orig_line
            else:
                line = orig_1stEmpty_line

            line = line.replace('[Part]', str(base))
            # Sort order
            line = line.replace('[so]', str(sequence.get_part_params()[1]))
            line = line.replace('[tmo]', str(sequence.get_part_params()[2]))
            # Crop bounds
            crop_bounds_str = sequence.get_crop_bounds()
            crop_bounds = crop_bounds_str.split(",")
            try:
                row_start = int(crop_bounds[0])
                col_start = int(crop_bounds[1])
                row_end = int(crop_bounds[2])
                col_end = int(crop_bounds[3])
            except:
                messagebox.showerror(
                    "Invalid crop bound", "Invalid crop bound {}".format(crop_bounds_str))
                continue

            sx = (col_end - col_start) / 2
            sy = (row_end - row_start) / 2
            px = (sx + col_start) / 2
            py = 802.5 - (sy + row_start) / 2
            line = line.replace('[sx]', str(sx))
            line = line.replace('[sy]', str(sy))
            line = line.replace('[px]', str(px))
            line = line.replace('[py]', str(py))

            glosses = self.gloss_files()
            # Number of Glosses
            if sequence.get_part_params()[0] == 0:
                line = line.replace('[NumberOfGloss]', str(len(glosses)))
            else:
                line = line.replace('[NumberOfGloss]', str(len(glosses) + 1))

            for i in range(20):
                if i < len(glosses):
                    line = line.replace('Tab{:02d}'.format(i + 1), glosses[i])
                else:
                    line = line.replace('Tab{:02d}'.format(i + 1), "")
            lines += line

        # Set the background order
        end = end.replace('[order]', str(largest_order))
        # Glue the parts together
        output = start + lines + end
        file_out = os.path.join(self.get_output_dir(),
                                self.get_model_name(),
                                self.get_model_name() + '_Parts.csv')
        with open(file_out, 'w') as f:
            f.write(self.mac_csv(output))

    def gloss_files(self):
        directory = os.path.join(self.get_output_dir(),
                                 self.get_model_name(),
                                 self.get_model_name() + '_UI',
                                 'Tab')
        files = os.listdir(directory)
        gloss_files = []
        special_case = 'NewTab_Mat.png'
        if special_case in files:
            gloss_files.append(special_case.replace('.png', ''))
            files.remove(special_case)

        for file in files:
            if (not 'PAT' in file) and (not 'BG' in file) and (not 'Glass' in file):
                gloss_files.append(file.replace('.png', ''))

        return gloss_files

    def update_source_sequences(self, directory):
        # Check whether the file is already in source or mask sequences
        images = glob.glob(directory + "/*.png")
        self.set_script2_message(
            "Rescanning folder {}".format(directory), "green")
        for i in range(len(images)):
            image = images[i]
            # Check if Sequence exists
            base = Sequence.parse_base(image)
            if self.mask_sequence_exists(base):
                continue
            elif self.source_sequence_exists(base):
                # Try to add image
                sequence = self.get_source_sequence(base)
                sequence.add_image(image)
                continue
            else:
                # Create new source sequence
                sequence = Sequence(image)
                self.add_source_sequence(sequence)

    def run_macro2(self):
        self.set_script2_message("Running", "green")

        # Run crop all to the sequence folders
        directory = self.get_directory()
        for base, sequence in self.get_mask_sequences().items():
            crop_bounds_str = sequence.get_crop_bounds()
            crop_bounds = crop_bounds_str.split(",")
            try:
                row_start = int(crop_bounds[0])
                col_start = int(crop_bounds[1])
                row_end = int(crop_bounds[2])
                col_end = int(crop_bounds[3])
            except:
                messagebox.showerror(
                    "Invalid crop bound", "Invalid crop bound {}".format(crop_bounds_str))
                continue

            input_dir = os.path.join(directory,
                                     sequence.get_folder())
            images = glob.glob(input_dir + "/*.png")
            for i in range(len(images)):
                self.set_script2_message(
                    "In " + base + " cropping file " + str(i + 1) + " of " + str(len(images)), "green")
                image = images[i]
                try:
                    orig = misc.imread(image)
                except:
                    logging.debug("Could not open " + image)
                    continue
                shape = np.shape(orig)
                # Save the cropped image
                if shape[0] < row_end or shape[1] < col_end:
                    continue
                try:
                    misc.imsave(
                        image, orig[row_start:row_end, col_start:col_end])
                except:
                    logging.debug("Could not save " + image)
                    continue

        # For each mask, process all the source images with the same index
        i = 0
        tot = 0
        for base, sequence in self.get_mask_sequences().items():
            tot += len(sequence.get_images()) * \
                len(self.get_source_sequences())

        for base, sequence in self.get_mask_sequences().items():
            input_dir = os.path.join(directory,
                                     sequence.get_folder())

            # Update source sequences based on the folder
            self.update_source_sequences(input_dir)

            for index, mask_name in sequence.get_images().items():
                mask = misc.imread(os.path.join(
                    input_dir, os.path.basename(mask_name)), flatten=True)
                # Get all the source images
                for source_base, source_sequence in self.get_source_sequences().items():
                    if index in source_sequence.get_images():
                        image_name = source_sequence.get_images()[index]
                        # Check whether the image exists
                        path = os.path.join(
                            input_dir, os.path.basename(image_name))
                        if not os.path.isfile(path):
                            continue
                        image = misc.imread(path)
                        shape = np.shape(image)
                        # Run cutout
                        self.set_script2_message(
                            "Running cutout " + str(i + 1) + " of " + str(tot), "green")
                        i += 1
                        if Sequence.gloss(image_name):
                            new = 255 * np.ones((shape[0], shape[1], 4))
                            new[:, :, 3] = self.rgb_to_gray(
                                image) * mask / 255.0
                        else:
                            #new = np.zeros((shape[0], shape[1], 4))
                            new = 255 * np.ones((shape[0], shape[1], 4))
                            new[:, :, 0:3] = image[:, :, 0:3]
                            new[:, :, 3] = mask

                        # save the new file
                        new_name = base + "_" + source_base + \
                            "." + str(index) + ".png"
                        try:
                            misc.imsave(os.path.join(input_dir, new_name), new)
                        except:
                            logging.debug("Could not save " + new_name)

        # Delete the process files
        self.set_script2_message("Cleaning up...", "green")
        for base, sequence in self.get_mask_sequences().items():
            input_dir = os.path.join(directory,
                                     sequence.get_folder())
            for index, mask_name in sequence.get_images().items():
                os.unlink(os.path.join(input_dir, os.path.basename(mask_name)))
            for source_base, source_sequence in self.get_source_sequences().items():
                for index, image_name in source_sequence.get_images().items():
                    path = os.path.join(
                        input_dir, os.path.basename(image_name))
                    if os.path.isfile(path):
                        os.unlink(path)

        self.generate_crop_bound_report()

        self.set_script2_message("Finished", "green")

    def generate_crop_bound_report(self):
        self.report = ""
        for base, sequence in self.get_mask_sequences().items():
            crop_bounds_str = sequence.get_crop_bounds()
            crop_bounds = crop_bounds_str.split(",")
            try:
                row_start = int(crop_bounds[0])
                col_start = int(crop_bounds[1])
                row_end = int(crop_bounds[2])
                col_end = int(crop_bounds[3])
            except:
                logging.debug('Could not report crop bounds {}'.format(base))
                continue

            self.report += base + "\n"
            self.report += ",Top,{}\n".format(row_start)
            self.report += ",Left,{}\n".format(col_start)
            self.report += ",Bottom,{}\n".format(row_end)
            self.report += ",Right,{}\n".format(col_end)

        self.save_crop_report()

    def save_crop_report(self):
        try:
            with open(os.path.join(self.get_directory(), "crop_report.csv"), "a") as f:
                f.write(self.mac_csv(self.report))
        except:
            logging.debug("Could not save Crop Report csv")

    def copy_originals(self):
        # Create the folder
        out_path = os.path.join(self.get_output_dir(),
                                self.get_model_name(),
                                self.get_model_name() + '_Model -ZD')
        try:
            os.makedirs(out_path)
        except:
            logging.debug("Could not create directory {}".format(out_path))

        for base, sequence in self.get_mask_sequences().items():
            path = os.path.join(self.get_directory(),
                                base)
            images = os.listdir(path)
            for image in images:
                self.set_script81_message(
                    "Copying image {}".format(image), "green")
                src = os.path.join(path, image)
                dst = os.path.join(out_path, image)
                try:
                    shutil.copyfile(src, dst)
                except:
                    logging.debug('Could not copy from {} to {}'.format(src,dst))
        self.set_script81_message("Done", "green")

    def resize(self, orig, new_width, new_height):
        resampled = np.zeros((new_width, new_height, 4), np.uint8)
        resampled[:, :, 0:3] = misc.imresize(
            orig[:, :, 0:3], (new_width, new_height), interp=self.interpolation_method.get())
        resampled[:, :, 3] = misc.imresize(
            orig[:, :, 3], (new_width, new_height), interp=self.alpha_interpolation_method.get())
        return resampled

    def copy_images(self):
        in_path = os.path.join(self.get_output_dir(),
                               self.get_model_name(),
                               self.get_model_name() + '_Model -ZD')
        out_path = os.path.join(self.get_output_dir(),
                                self.get_model_name(),
                                self.get_model_name() + '_Model -HD')
        self.hd_path = out_path

        for base, sequence in self.get_mask_sequences().items():
            size = sequence.get_power_of_two_size()
            path = os.path.join(self.get_directory(),
                                base)
            images = os.listdir(path)
            for image in images:
                self.set_script8_message(
                    "Resampling HD image {}".format(image), "green")

                # Note, using in_path instead of path
                # path is just to list all the copied images
                orig = misc.imread(os.path.join(in_path, image))
                width = int(size[0])
                height = int(size[1])
                resampled = self.resize(orig, width, height)
                misc.imsave(os.path.join(out_path,
                                         image), resampled)

        # SD Images
        out_path = os.path.join(self.get_output_dir(),
                                self.get_model_name(),
                                self.get_model_name() + '_Model -SD')

        self.sd_path = out_path

        for base, sequence in self.get_mask_sequences().items():
            size = sequence.get_power_of_two_size()
            path = os.path.join(self.get_directory(),
                                base)
            images = os.listdir(path)
            for image in images:
                self.set_script8_message(
                    "Resampling SD image {}".format(image), "green")

                # Note, using in_path instead of path
                # path is just to list all the copied images
                orig = misc.imread(os.path.join(in_path, image))
                width = int(int(size[0]) / 2)
                height = int(int(size[1]) / 2)
                resampled = self.resize(orig, width, height)
                misc.imsave(os.path.join(out_path,
                                         image), resampled)

        # LD Images
        out_path = os.path.join(self.get_output_dir(),
                                self.get_model_name(),
                                self.get_model_name() + '_Model -LD')
        for base, sequence in self.get_mask_sequences().items():
            size = sequence.get_power_of_two_size()
            path = os.path.join(self.get_directory(),
                                base)
            images = os.listdir(path)
            for image in images:
                self.set_script8_message(
                    "Resampling LD image {}".format(image), "green")

                # Note, using in_path instead of path
                # path is just to list all the copied images
                orig = misc.imread(os.path.join(in_path, image))
                width = int(int(size[0]) / 4)
                height = int(int(size[1]) / 4)
                resampled = self.resize(orig, width, height)
                misc.imsave(os.path.join(out_path,
                                         image), resampled)

        # LD Buttons
        path = os.path.join(self.get_output_dir(),
                            self.get_model_name(),
                            self.get_model_name() + '_UI')
        out_path = os.path.join(self.get_output_dir(),
                                self.get_model_name(),
                                self.get_model_name() + '_UI - LD')

        folders = os.listdir(path)
        for folder in folders:
            current_folder = os.path.join(path, folder)
            images = os.listdir(current_folder)
            for image in images:
                self.set_script8_message(
                    "Resampling LD buttons {}".format(image), "green")

                orig = misc.imread(os.path.join(current_folder, image))
                resampled = misc.imresize(orig,
                                          0.5,
                                          interp=self.interpolation_method.get())
                misc.imsave(os.path.join(out_path,
                                         folder,
                                         image), resampled)

        self.set_script8_message("Done", "green")

    # uses crop report to read in data
    def read_sequences(self):
        self.set_script3_message("Reading crop report", "green")
        crop_report_file = os.path.join(self.get_directory(),
                                        'crop_report.csv')
        try:
            with open(crop_report_file, 'r') as f:
                lines = f.readlines()

            # Parse the data
            seq = None
            for line in lines:
                split_line = line.replace('\n', '').split(',')
                if len(split_line) == 1:
                    if seq != None:
                        seq.set_crop_bounds(','.join(crop_bounds))
                        self.add_mask_sequence(seq)
                    crop_bounds = []
                    base = split_line[0]
                    if self.mask_sequence_exists(base):
                        seq = self.get_mask_sequence(base)
                    else:
                        # Create a new one
                        seq = Sequence()
                        seq.set_base(split_line[0])
                else:
                    crop_bounds.append(split_line[-1])

            # last sequence
            if seq != None:
                seq.set_crop_bounds(','.join(crop_bounds))
                self.add_mask_sequence(seq)

            self.set_script3_message("Done", "green")

        except Exception as e:
            logging.error("Error {} occured.".format(e))
            logging.warning("Could not open crop report file")
            self.set_script3_message("Error while reading crop report", "red")

    def rgb_to_gray(self, rgb):
        return np.dot(rgb[..., :3], [0.299, 0.587, 0.114])

    def copy_model_folder_structure(self):
        zipfile = os.path.join(self.script_path,
                               'model.zip')
        with ZipFile(zipfile) as myzip:
            myzip.extractall(path=self.get_output_dir())
        # Rename
        while(self.rename_by_model()):
            pass

    def rename_by_model(self):
        directory = self.get_output_dir()
        pattern = '[MODELNAME]'
        for path, dirs, files in os.walk(os.path.abspath(directory)):
            for filename in dirs + files:
                if pattern in filename:
                    src = os.path.join(path, filename)
                    dst = os.path.join(path,
                                       filename.replace(pattern,
                                                        self.get_model_name()))
                    shutil.move(src, dst)
                    return True

        return False

    def copy_to_all_mask_folders(self, src):
        directory = self.get_directory()
        for base, sequence in self.get_mask_sequences().items():
            dst = os.path.join(directory,
                               sequence.get_folder(),
                               os.path.basename(src))
            # Copy
            try:
                shutil.copyfile(src, dst)
            except:
                logging.debug("Could not copy file from {} to {}".format(src,dst))

    def run_macro1(self):
        self.set_script1_message("Running", "green")

        # Update the directory
        self.set_directory(self.directory_entry.get())
        directory = self.get_directory()

        input_dir = os.path.join(directory, "Z_MATTE")
        if not self.validate_dir(input_dir):
            messagebox.showerror("Invalid directory",
                                 "Invalid directory {}".format(input_dir))
            return

        self.init_sequences()
        # Scan input directory and generate sequence objects and corresponding folders
        images = glob.glob(input_dir + "/*.png")
        for i in range(len(images)):
            self.set_script1_message("Scanning file " + str(i + 1) + " of " + str(len(images)),
                                     "green")
            image = images[i]

            # Check if Sequence exists
            base = Sequence.parse_base(image)
            if self.mask_sequence_exists(base):
                sequence = self.get_mask_sequence(base)
                sequence.add_image(image)
            else:
                # Create a new one
                sequence = Sequence(image)
                self.add_mask_sequence(sequence)
                # If the directory exists, delete it
                if os.path.exists(os.path.join(directory,
                                               sequence.get_folder())):
                    shutil.rmtree(os.path.join(directory,
                                               sequence.get_folder()))
                # Create a folder
                try:
                    os.makedirs(os.path.join(directory,
                                             sequence.get_folder()))
                except:
                    logging.debug("Could not create directory: {}".format(os.path.join(directory, sequence.get_folder())))

            # Copy the image into the folder
            try:
                src = os.path.join(input_dir, os.path.basename(image))
                dst = os.path.join(directory, sequence.get_folder(),
                                   os.path.basename(image))
                shutil.copyfile(src, dst)
            except:
                print("Could not copy file from {} to {}".format(src,dst))
        # Run crop analysis for the mask sequence folders
        for base, sequence in self.get_mask_sequences().items():
            #images = list(sequence.get_images().values())
            images = glob.glob(os.path.join(directory,
                                            sequence.get_folder()) + "/*.png")
            for i in range(len(images)):
                self.set_script1_message("In {} processing file {} of {}".format(base,
                                                                                 i + 1,
                                                                                 len(images)),
                                         "green")
                image = misc.imread(images[i], flatten=True)

                if i == 0:
                    reference_shape = np.shape(image)
                    result = np.zeros(reference_shape)

                result = np.logical_or(result, image)

            try:
                nonzeros = np.nonzero(result)
                row_start = min(nonzeros[0])
                col_start = min(nonzeros[1])
                row_end = max(nonzeros[0])
                col_end = max(nonzeros[1])
            except:
                self.set_script1_message("Error occured, check input values ",
                                         "red")

            # Add "bleed pixels in all directions"
            bleed_pixels = self.get_crop_pixels()
            if row_start >= bleed_pixels:
                row_start -= bleed_pixels
            if row_end < reference_shape[0] - bleed_pixels:
                row_end += bleed_pixels
            if col_start >= bleed_pixels:
                col_start -= bleed_pixels
            if col_end < reference_shape[1] - bleed_pixels:
                col_end += bleed_pixels

            # Make crop size even
            if (row_end - row_start + 1) % 2:
                if row_start > 0:
                    row_start -= 1
                elif row_end < reference_shape[0]:
                    row_end += 1
                else:
                    self.set_script1_message("Error occured, can't make it even!",
                                             "red")
            if (col_end - col_start + 1) % 2:
                if col_start > 0:
                    col_start -= 1
                elif col_end < reference_shape[1]:
                    col_end += 1
                else:
                    self.set_script1_message("Error occured, can't make it even!",
                                             "red")

            crop_bounds = "{},{},{},{}".format(row_start,
                                               col_start,
                                               row_end + 1,
                                               col_end + 1)

            sequence.set_crop_bounds(crop_bounds)

        # Scan source Z_SOURCE sequences
        input_dir = os.path.join(directory, "Z_SOURCE")
        # Scan input directory and generate sequence objects and corresponding folders
        images = glob.glob(input_dir + "/*.png")

        for i in range(len(images)):
            self.set_script1_message("Scanning file {} of {}".format(i + 1,
                                                                     len(images)),
                                     "green")
            image = images[i]
            # Check if Sequence exists
            base = Sequence.parse_base(image)
            if self.source_sequence_exists(base):
                sequence = self.get_source_sequence(base)
                sequence.add_image(image)
            else:
                # Create a new one
                sequence = Sequence(image)
                self.add_source_sequence(sequence)

            # Copy the image to all mask folders
            src = os.path.join(input_dir, os.path.basename(image))
            self.copy_to_all_mask_folders(src)

        # Script finished
        self.set_script1_message("Finished", "green")
        dialog = CropAnalysisResults(self)

        if self.one_click:
            eyes = None
            eyes_gloss = None
            pats = []

            for base, entry in dialog.bounds.items():
                part_name = self.__remove_prefix_number(base)

                if part_name == 'Eyes':
                    eyes = entry

                if part_name == 'EyesGLOSS':
                    eyes_gloss = entry

                if self.__is_pat(base):
                    pats.append((base, entry))

            if eyes != None and eyes_gloss != None:
                largest = self.__get_largest(eyes.get(), eyes_gloss.get())
                eyes_gloss.set(largest)
                eyes.set(largest)

            if len(pats) > 0:
                largest_pat = self.__get_largest_pat(
                    [v.get() for k, v in pats])
                for pat_base, pat_entry in pats:
                    pat_entry.set(largest_pat)

            dialog.quit()

    def __is_pat(self, patname):
        rgx = re.compile(r'\d?Pat\d?')
        rslt = rgx.search(patname)
        if rslt:
            return True
        return False

    def __remove_prefix_number(self, text):
        rgx = re.compile(r'^\d*(.+)')
        rslt = rgx.search(text)
        return rslt.group(1)

    def __compute_area(self, crop_bounds_str):

        crop_bounds = crop_bounds_str.split(",")
        try:
            row_start = int(crop_bounds[0])
            col_start = int(crop_bounds[1])
            row_end = int(crop_bounds[2])
            col_end = int(crop_bounds[3])

            area = (row_end - row_start) * (col_end - col_start)
            return area

        except:
            messagebox.showerror("Invalid eyes crop bound",
                                 "Invalid crop bound {}".format(crop_bounds_str))
            return

    def __get_largest_pat(self, pats):
        try:
            bounds = []

            for p in pats:
                bounds.append([int(_p.strip()) for _p in p.split(',')])

            # print('Input pat array')
            arr = np.array(bounds)
            # print(arr)

            row_starts = arr[:, 0]
            col_starts = arr[:, 1]
            row_ends = arr[:, 2]
            col_ends = arr[:, 3]

            row_start = row_starts[np.argsort(row_starts)[0]]
            col_start = col_starts[np.argsort(col_starts)[0]]
            row_end = row_ends[np.argsort(row_ends)[-1]]
            col_end = col_ends[np.argsort(col_ends)[-1]]

            largest = "{},{},{},{}".format(
                row_start, col_start, row_end, col_end)
            logging.debug('Largest pat bounds ' + largest)
            return largest

        except:
            messagebox.showerror("Error in parsing pat values")
            return

    def __get_largest(self, crop_set1, crop_set2):

        logging.debug('Finding largest bounds from {} and {}'.format(crop_set1, crop_set2))

        crop_bounds1 = crop_set1.split(",")
        crop_bounds2 = crop_set2.split(",")

        try:
            row_start1 = int(crop_bounds1[0])
            col_start1 = int(crop_bounds1[1])
            row_end1 = int(crop_bounds1[2])
            col_end1 = int(crop_bounds1[3])

            row_start2 = int(crop_bounds2[0])
            col_start2 = int(crop_bounds2[1])
            row_end2 = int(crop_bounds2[2])
            col_end2 = int(crop_bounds2[3])

            row_start = row_start1 if row_start1 < row_start2 else row_start2
            col_start = col_start1 if col_start1 < col_start2 else col_start2
            row_end = row_end1 if row_end1 > row_end2 else row_end2
            col_end = col_end1 if col_end1 > col_end2 else col_end2

            largest = "{},{},{},{}".format(
                row_start, col_start, row_end, col_end)
            logging.debug('Largest ' + largest)
            return largest

        except:
            messagebox.showerror(
                "Cannot parse eyes crop bounds <{} and/or {}>".format(crop_set1, crop_set2))
            return

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

    def set_script30_message(self, text, color):
        self.script30_message['text'] = text
        self.script30_message['foreground'] = color
        self.update()

    def set_script4_message(self, text, color):
        self.script4_message['text'] = text
        self.script4_message['foreground'] = color
        self.update()

    def set_script5_message(self, text, color):
        self.script5_message['text'] = text
        self.script5_message['foreground'] = color
        self.update()

    def set_script6_message(self, text, color):
        self.script6_message['text'] = text
        self.script6_message['foreground'] = color
        self.update()

    def set_script7_message(self, text, color):
        self.script7_message['text'] = text
        self.script7_message['foreground'] = color
        self.update()

    def set_script8_message(self, text, color):
        self.script8_message['text'] = text
        self.script8_message['foreground'] = color
        self.update()

    def set_script81_message(self, text, color):
        self.script81_message['text'] = text
        self.script81_message['foreground'] = color
        self.update()

    def set_script9_message(self, text, color):
        self.script9_message['text'] = text
        self.script9_message['foreground'] = color
        self.update()

    def set_script10_message(self, text, color):
        self.script10_message['text'] = text
        self.script10_message['foreground'] = color
        self.update()

    def set_script11_message(self, text, color):
        self.script11_message['text'] = text
        self.script11_message['foreground'] = color
        self.update()

    def set_script12_message(self, text, color):
        self.script12_message['text'] = text
        self.script12_message['foreground'] = color
        self.update()

    def set_script13_message(self, text, color):
        self.script13_message['text'] = text
        self.script13_message['foreground'] = color
        self.update()

    def update_gui(self):
        self.update_directory_message()
        self.update_rgb_directory_message()
        self.update_expand_directory_message()
        self.update()

    def __is_model_folder(self, folder):
        rgx = re.compile(r'\d+\-\d+_.+')
        rslt = rgx.search(folder)
        return rslt != None

    def __read_config2(self):
        newconfig = dict()

        CONFIG_CSV = os.path.join(self.directory_entry.get(), 'Real3d_V1.csv')
        if not os.path.exists(CONFIG_CSV):
            logging.debug('Real3d_V1.csv was not found')
            raise FileNotFoundError()

        with open(CONFIG_CSV, 'rt', newline='') as fp:
            reader = csv.DictReader(fp.readlines())

            for item in reader:
                if not 'isReady' in item or not 'frameSetup' in item:
                    raise ValueError(
                        "'isReady' and 'frameSetup' columns must be found in Read3d_V1.csv")

                logging.debug('config values for {} loaded'.format(item['model']))
                newconfig[item['model']] = item

            return newconfig
    # wated refactor to read redies

    def __read_config(self):
        CONFIG_CSV = os.path.join(self.directory_entry.get(), 'Real3d_V1.csv')
        if not os.path.exists(CONFIG_CSV):
            logging.debug('Real3d_V1.csv was not found')
            raise FileNotFoundError()

        with open(CONFIG_CSV, 'rt', newline='') as fp:
            reader = csv.reader(fp.readlines())
            readies = dict()
            for idx, row in enumerate(reader):
                if idx == 0:
                    if 'isReady' in row:
                        isRenderIndex = row.index('isReady')
                    else:
                        raise Exception(
                            "'isReady was not found in csv config.")
                    continue

                try:
                    readies[row[0]] = int(row[isRenderIndex])
                except:
                    logging.debug(
                        'Cannot read correct isReady value of {}.\nCoercing to zero (0)'.format(row[0]))
                    readies[row[0]] = 0

        return readies

    def __get_model_name(self, folder):
        rgx = re.compile(r'\d+\-\d+_.+', re.I)
        rslt = rgx.search(folder)
        if rslt:
            return rslt.group(0).strip()

    def __get_ready_models(self):
        logging.debug('Fetching folders that are ready to process.')
        config = self.__read_config()

        skipping = []
        processing = []

        for item in os.listdir(self.directory_entry.get()):
            print('Checking {}'.format(item))
            model_name = self.__get_model_name(item)

            if not model_name:
                continue

            if not model_name in config:
                skipping.append(model_name)
                continue

            isReady = config[model_name]

            if isReady == 0:
                skipping.append(model_name)
            else:
                processing.append(model_name)

        return processing, skipping

    def __run_one_click(self):

        self.one_click = True
        self.original_root = self.directory_entry.get()

        try:
            processing, skipping = self.__get_ready_models()
            self.my_config = self.__read_config2()

            print('Processing the following models:')
            print('\n'.join(processing))
            print('Skipping the following models:')
            print('\n'.join(skipping))

            processing_directories = list(
                [os.path.join(self.directory_entry.get(), p) for p in processing])

            for folder in processing_directories:
                try:
                    print('Processing {}'.format(os.path.basename(folder)))

                    render_folder = os.path.join(folder, 'KeyShot', 'Renders')

                    self.directory_entry.set(render_folder)

                    self.run_macro1()
                    self.run_macro2()
                    self.__model_name()
                    self.read_sequences()
                    self.generate_part_csv_part_a()
                    self.generate_part_csv_part_b()
                    self.generate_tmenu_buttons()
                    self.glue_overlays()
                    self.process_shadows()
                    self.copy_originals()
                    self.resize_images()

                    if self.var_run_rgb_rest.get() == 1:
                        self.rgb_directory_entry.set(self.sd_path)
                        self.run_rgb_reset()

                        self.rgb_directory_entry.set(self.hd_path)
                        self.run_rgb_reset()

                    self.__finalize(folder)
                except Exception as e:
                    print(e)
                    traceback.print_exc()
                    print(
                        'Something went wrong while processing {}.\nMoving on to next model'.format(folder))
        except Exception as e:
            print(e)
        finally:
            self.one_click = False
            print('Operation done.')
            self.directory_entry.set(self.original_root)

    def __finalize(self, model_folder):
        post_macro = PostMacro(model_folder=model_folder)
        self.set_script11_message(
            "Running post script csv edits", "green")
        post_macro.start()
        self.set_script11_message(
            "Post scripts edit done", "green")

    def __model_name(self):
        selected_dir = self.get_directory_entry()
        rgx = re.compile(r'\d+\-\d+_[a-z]+', re.I)
        rslt = rgx.search(selected_dir)
        if not rslt:
            raise Exception('Invalid model folder name')

        self.model_name_entry.set(rslt.group(0))

    def __gen_keyshot_mat(self):

        mat_gen = MatGenerator(root=self.directory_entry.get(), parent=self)
        mat_gen.start()

    def __run_texturepacker(self):

        pid = subprocess.Popen(['C:\\Program Files (x86)\\Shade Soft\\TexturePackerSetup\\DanielApp.exe',
                                '-d', self.directory_entry.get(), '-m', 'auto']).pid


root = tk.Tk()
app = MacroPhytoshop(master=root)
app.mainloop()
