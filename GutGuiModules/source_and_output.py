from GutGuiModules.utility import *
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
        self.data_cube_path_label = ""
        self.output_dir_label = ""

        # Data
        self.data_cube = None
        self.path = ""
        self.data_cube_path_label = None
        self.path_label = None

        # Widget Initialization
        self._init_widgets()

    # Makes a deep copy of the original data cube
    def get_data_cube(self):
        return deepcopy(self.data_cube)

    def get_path(self):
        return self.path

    # Helpers
    def _init_widgets(self):
        self._build_select_dc_button()
        self._build_select_od_button()

    def _build_select_dc_button(self):
        self.select_data_cube_button = make_button(self.root, text="Select Data Cube",
                                                   command=self.__set_data_cube, inner_padx=21, inner_pady=5,
                                                   outer_padx=10, outer_pady=(20, 10), row=1, column=0)

    def _build_select_od_button(self):
        self.select_output_dir_button = make_button(self.root, text="Select Output Folder",
                                                    command=self.__set_output_dir, inner_padx=10, inner_pady=5,
                                                    outer_padx=10, outer_pady=5, row=3, column=0)

    # Commands (Callbacks)
    def __set_data_cube(self):
        (self.data_cube, dc_path) = self.__process_data_cube()
        self.data_cube_path_label = make_label(self.root, "Using Data Cube at: " + str(dc_path),
                                               row=2, column=0, wraplength=160)

    def __set_output_dir(self):
        self.path = self.__get_path_to_dir("Select a folder for the output to be stored.")
        self.path_label = make_label(self.root, "Using Output Folder at: " + str(self.path),
                                               row=4, column=0, wraplength=160)

    def __process_data_cube(self):
        path = self.__get_path_to_file("Select a data cube (ending in .dat)")
        if path == '':
            return
        if path[-4:] != ".dat":
            make_pop_up("That's not a .dat file!")
            return None, None
        else:
            data = np.fromfile(path, dtype='>f')  # returns 1D array and reads file in big-endian binary format
            data_cube = data[3:].reshape(640, 480, 100)  # reshape to data cube and ignore first 3 values which are wrong
            return data_cube, path

    def __get_path_to_file(self, title):
        path = filedialog.askopenfilename(parent=self.root, title=title)
        return path

    def __get_path_to_dir(self, title):
        path = filedialog.askdirectory(parent=self.root, title=title)
        return path