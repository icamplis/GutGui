from GutGuiModules.utility import *
import numpy as np
from copy import deepcopy
from tkinter import filedialog, messagebox
import os

# Manages the source and output directory
class SourceAndOutput:
    def __init__(self, source_and_output_frame, listener):
        # Root
        self.root = source_and_output_frame

        # Listener
        self.listener = listener

        # GUI
        self.select_data_cube_button = None
        self.select_output_dir_button = None
        self.selection_listbox = None
        self.data_cube_path_label = None
        self.output_dir_label = None
        self.delete_button = None

        # Data
        self.data_cubes = []
        self.data_paths = []
        self.path = ""
        self.data_cube_path_label = None
        self.path_label = None

        # Widget Initialization
        self._init_widgets()

    # Makes a deep copy of the original data cubes
    def get_data_cubes(self):
        return deepcopy(self.data_cubes)

    def get_selected_data_cube(self):
        index = self.selection_listbox.curselection()[0]
        return self._get_data_cube_by_index(index)

    def get_selected_data_cube_path(self):
        index = self.selection_listbox.curselection()[0]
        return self.data_paths[index]

    def get_path(self):
        return self.path

    def _get_data_cube_by_index(self, index):
        return deepcopy(self.data_cubes[index])

    def get_selected_data_paths(self):
        selecteds = self.selection_listbox.curselection()
        selected_data_paths = [self.data_paths[i] for i in selecteds]
        return selected_data_paths

    # Helpers
    def _init_widgets(self):
        self._build_select_superdir_button()
        self._build_select_dir_button()
        # self._build_select_od_button()
        self._build_selection_box()
        self._build_delete_button()

    def _build_select_superdir_button(self):
        self.select_data_cube_button = make_button(self.root, text=" Select Data \n Superdirectory", command=self.__add_data_cube_dirs,
                                                   inner_padx=10, inner_pady=10, outer_padx=15, row=1, column=0, width=15)

    def _build_select_dir_button(self):
        self.select_data_cube_button = make_button(self.root, text=" Select Data Directory", command=self.__add_data_cube_dir,
                                                   inner_padx=10, inner_pady=10, outer_padx=15, row=2, column=0, width=15)

    def _build_selection_box(self):
        self.selection_listbox = make_listbox(self.root, row=1, column=1, rowspan=3, padx=(0, 15))
        self.selection_listbox.bind('<<ListboxSelect>>', self.__update_selected_data_cube)

    def _build_delete_button(self):
        self.delete_button = make_button(self.root, text="Remove Data Cube",command=self.__delete_selected_data_cube,
                                         inner_padx=10, inner_pady=10, outer_padx=15, row=3, column=0, width=15)

    # Commands (Callbacks)
    def __update_selected_data_cube(self, event):
        dc_path = self.get_selected_data_cube_path()
        self.listener.set_data_cube(dc_path)

    def __add_data_cube_dirs(self):
        super_dir = self.__get_path_to_dir("Please select folder containing all the data folders.")
        sub_dirs = self.__get_sub_folder_paths(super_dir)
        for sub_dir in sub_dirs:
            self.__add_data_cube(sub_dir)

    def __add_data_cube_dir(self):
        dc_dir_path = self.__get_path_to_dir("Please select a folder containing data.")
        self.__add_data_cube(dc_dir_path)

    def __add_data_cube(self, sub_dir):
        contents = os.listdir(sub_dir)
        dc_path = [sub_dir + "/" + i for i in contents if ".dat" in i]  # takes first data cube it finds
        if len(dc_path) > 0:
            dc_path = dc_path[0]
            if dc_path in self.data_paths:
                messagebox.showerror("Error", "That data has already been added.")
            else:
                data_cube = self.__process_data_cube(dc_path)

                # Add the new data to current class
                self.data_paths.append(dc_path)
                self.data_cubes.append(data_cube)

                # Display the data cube
                concat_path = os.path.basename(os.path.normpath(dc_path))
                self.selection_listbox.insert(END, concat_path)
                self.selection_listbox.config(width=0)

                # Add data cube to listener for analysis
                self.listener.submit_data_cube(data_cube, dc_path)

    def __process_data_cube(self, path):
        if path == '' or path is None:
            return None
        if path[-4:] != ".dat":
            messagebox.showerror("Error", "That's not a .dat file!")
            return None
        else:
            data = np.fromfile(path, dtype='>f')  # returns 1D array and reads file in big-endian binary format
            data_cube = data[3:].reshape(640, 480, 100)  # reshape to data cube and ignore first 3 values
            return data_cube

    def __get_path_to_file(self, title):
        path = filedialog.askopenfilename(parent=self.root, title=title)
        return path

    def __get_path_to_dir(self, title):
        path = filedialog.askdirectory(parent=self.root, title=title)
        return path

    def __delete_selected_data_cube(self):
        if self.selection_listbox.size() > 0 and self.selection_listbox.curselection():
            index = self.selection_listbox.curselection()[0]
            self.selection_listbox.delete(index)
            self.listener.delete_analysis_result(self.data_paths[index])
            self.data_paths.pop(index)
            self.data_cubes.pop(index)

    def __get_sub_folder_paths(self, path_to_main_folder):
        contents = os.listdir(path_to_main_folder)
        # Adds the path to the main folder in front for traversal
        sub_folders = [path_to_main_folder + "/" + i for i in contents if bool(re.match('[\d/-_]+$', i))]
        return sub_folders