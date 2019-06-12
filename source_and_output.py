from constants import *
from tkinter import *
from utility import *
import numpy as np
from copy import deepcopy
from tkinter import filedialog

# Manages the source and output directory
class SourceAndOutput:
    def __init__(self, source_and_output_frame):
        # Root
        self.root = source_and_output_frame

        # GUI
        self.select_data_cube_button = None
        self.select_output_dir_button = None

        # Data
        self.data_cube = None
        self.path = ""

        # Widget Initialization
        self._init_widgets()

    # Makes a deep copy of the original data cube
    def get_data_cube(self):
        return deepcopy(self.data_cube)

    def get_path(self):
        return self.path

    def _init_widgets(self):
        self._build_select_dc_button()
        self._build_select_od_button()

    def _build_select_dc_button(self):
        self.select_data_cube_button = make_button(self.source_and_output_frame, text="Select Data Cube",
                                                   command=self._select_data_cube, padx=10, pady=10, row=1, column=0)

    def _build_select_od_button(self):
        self.select_output_dir_button = make_button(self.source_and_output_frame, text="Select Output Folder",
                                                   command=self._select_output_dir, padx=10, pady=10, row=2, column=0)

    def _select_data_cube(self):
        print("select data cube placeholder")

    def _select_output_dir(self):
        print("select output dir placeholder")

    def __get_file_upload(self):
        print("getting file uploaded placeholder")

    def __get_path(self):
        print("getting specified path placeholder")