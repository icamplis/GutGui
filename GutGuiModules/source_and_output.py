from GutGuiModules.utility import *
import numpy as np
from copy import deepcopy
from tkinter import filedialog, messagebox
import os

# Manages the source and output directory
class SourceAndOutput:
    def __init__(self, source_and_output_frame):
        # Root
        self.root = source_and_output_frame

        # GUI
        self.select_data_cube_button = None
        self.select_output_dir_button = None
        self.selection_listbox = None
        self.data_cube_path_label = None
        self.output_dir_label = None
        self.delete_button = None

        # Data
        self.data_cubes = []
        self.data_cube_paths = []
        self.path = ""
        self.data_cube_path_label = None
        self.path_label = None

        # Widget Initialization
        self._init_widgets()

    # Makes a deep copy of the original data cubes
    def get_data_cubes(self):
        return deepcopy(self.data_cubes)

    def get_selected_data_cube(self):
        index = self.selection_listbox.curselection()
        return self._get_data_cube_by_index(index)

    def _get_data_cube_by_index(self, index):
        return deepcopy(self.data_cubes[index])

    def get_path(self):
        return self.path

    # Helpers
    def _init_widgets(self):
        self._build_select_dc_button()
        self._build_select_od_button()
        self._build_selection_box()
        self._build_delete_button()

    def _build_select_dc_button(self):
        self.select_data_cube_button = make_button(self.root, text="Select Data Cube", command=self.__set_data_cube, inner_padx=10, inner_pady=10, outer_padx=15, row=1, column=0, width=15)

    def _build_select_od_button(self):
        self.select_output_dir_button = make_button(self.root, text="Select Output Folder", command=self.__set_output_dir, inner_padx=10, inner_pady=10, outer_padx=15, row=2, column=0, width=15)

    def _build_selection_box(self):
        self.selection_listbox = make_listbox(self.root, input=None, row=1, column=1, rowspan=3, padx=(0, 15))

    def _build_delete_button(self):
        self.delete_button = make_button(self.root, text="Remove Data Cube",command=self.__delete_selected_data_cube, inner_padx=10, inner_pady=10, outer_padx=15, row=3, column=0, width=15)

    # Commands (Callbacks)
    def __set_data_cube(self):
        (data_cube, dc_path) = self.__process_data_cube()
        concat_dc_path = os.path.basename(os.path.normpath(dc_path))
        if dc_path in self.data_cube_paths:
            messagebox.showinfo("Error", "That data cube has already been added.")
        else:
            self.data_cube_paths.append(dc_path)
            self.data_cubes.append(data_cube)
            self.selection_listbox.insert(END, concat_dc_path)
            self.selection_listbox.config(width=0)  # resizes to widest path

    def __set_output_dir(self):
        self.path = self.__get_path_to_dir("Select a folder for the output to be stored.")
        self.path_label = make_label(self.root, "Using Output Folder at: " + str(self.path),
                                               row=3, column=0, wraplength=160, outer_pady=(2, 5), outer_padx=(15, 0))

    def __process_data_cube(self):
        path = self.__get_path_to_file("Select a data cube (ending in .dat)")
        if path == '':
            return
        if path[-4:] != ".dat":
            messagebox.showinfo("Error", "That's not a .dat file!")
            return
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

    def __delete_selected_data_cube(self):
        if self.selection_listbox.size() > 0 and self.selection_listbox.curselection:
            self.selection_listbox.delete(self.selection_listbox.curselection())