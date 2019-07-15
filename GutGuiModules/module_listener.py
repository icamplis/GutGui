from AnalysisModules.analysis import Analysis
from GutGuiModules.constants import *
import numpy as np
import logging

class ModuleListener:
    def __init__(self):
        # {module_name: module}
        self.modules = {}

        # SOURCE AND OUTPUT VALUES
        # {data_cube_path: analysis object}
        self.results = {}
        self.current_rendered_result_path = None
        self.selected_paths = []
        self.output_folder = None  # init with None intentionally

        # NOTE: THE FOLLOWING ONLY CONTROLS WHAT TO RENDER, NOT WHAT IS SAVED

        # ANALYSIS AND FORM
        self.normal = None
        self.absorbance = None
        self.wavelength = None
        self.index = None
        self.index_number = None

        # ORIGINAL IMAGE
        self.mask = None

        # DIAGRAM
        self.is_masked = False

    def get_normal(self):
        return self.normal

    def get_masked(self):
        return self.is_masked

    def get_wl(self):
        if self.is_masked:
            return self.get_result(self.current_rendered_result_path).get_wl_data_masked()
        else:
            return self.get_result(self.current_rendered_result_path).get_wl_data()

    def get_idx(self):
        if self.is_masked:
            return self.get_result(self.current_rendered_result_path).get_index_masked()
        else:
            return self.get_result(self.current_rendered_result_path).get_index()

    def get_selected_paths(self):
        return self.selected_paths

    def get_results(self):
        return self.results

    def get_result(self, path):
        if self.results[path] is not None:
            return self.results[path]

    def attach_module(self, module_name, mod):
        self.modules[module_name] = mod

    # Updaters
    def submit_data_cube(self, data_cube, dc_path):
        logging.debug("ANALYZING DATA CUBE AT " + dc_path)
        if self.modules[ANALYSIS_AND_FORM]:
            self.normal = self.modules[ANALYSIS_AND_FORM].get_normal()
            self.absorbance = self.modules[ANALYSIS_AND_FORM].get_absorbance()
            self.wavelength = self.modules[ANALYSIS_AND_FORM].get_wavelength()
            self.index = self.modules[ANALYSIS_AND_FORM].get_index()
            self.mask = self.modules[ORIGINAL_COLOUR].get_mask()
            self.is_masked = self.modules[DIAGRAM].get_is_masked()
            self._make_new_analysis(dc_path, data_cube, self.normal, self.absorbance, self.wavelength, self.index, self.mask)

    def set_data_cube(self, dc_path):
        logging.debug("SELECTED DATA CUBE AT: " + dc_path)
        self.current_rendered_result_path = dc_path
        self._broadcast_new_data()

    def ref_data_cube(self, path):
        return self.get_result(path).get_data_cube()

    def ref_non_neg_cube(self, path):
        cube = self.get_result(path).get_data_cube()
        return np.ma.array(cube, mask=cube<0)

    def ref_norm_cube(self, path):
        cube = self.get_result(path).get_data_cube()
        return cube/cube.max()

    def ref_norm_non_neg_cube(self, path):
        cube = self.get_result(path).get_data_cube()
        np.ma.array(cube, mask=cube<0)
        return pos_cube/pos_cube.max()

    def ab_non_neg_cube(self, path):
        cube = self.get_result(path).get_x_absorbance()
        return cube[cube > 0]

    def ab_norm_cube(self, path):
        cube = self.get_result(path).get_x_absorbance()
        return cube/cube.max()

    def update_selected_paths(self, selected_paths):
        self.selected_paths = selected_paths

    def delete_analysis_result(self, path):
        logging.debug("DELETING DATA CUBE: " + path)
        self.results[path] = None

    def submit_normal(self, new_normal):
        assert type(new_normal) == bool
        logging.debug("NEW NORMAL: " + str(new_normal))
        self.normal = new_normal
        self._update_analysis(normal=self.normal)
        self._broadcast_new_data()

    def submit_mask(self, new_mask):
        logging.debug("NEW MASK: [...]")
        self.mask = new_mask
        self._update_analysis(mask=self.mask)
        if self.is_masked:
            self._broadcast_new_data()

    def submit_absorbance(self, new_absorbance):
        logging.debug("NEW (USING) ABSORBANCE: " + str(new_absorbance))
        assert type(new_absorbance) == bool
        self.absorbance = new_absorbance
        self._update_analysis(absorbance=self.absorbance)
        self._broadcast_new_data()

    def submit_wavelength(self, new_wavelength):
        logging.debug("NEW WAVELENGTH: " + str(new_wavelength))
        self.wavelength = new_wavelength
        self._update_analysis(wavelength=self.wavelength)
        self._broadcast_new_data()

    def submit_index(self, new_index_number):
        logging.debug("SETTING NEW INDEX: [...]")
        self.index_number = new_index_number
        self._update_analysis(index_number=self.index_number)
        self._broadcast_new_data()

    def submit_is_masked(self, new_is_masked):
        logging.debug("USING WHOLE IMAGE? " + str(new_is_masked))
        self.is_masked = new_is_masked
        self._broadcast_new_data()

    def render_original_image_data(self):
        self._broadcast_to_original_image()

    def render_new_recreated_image_data(self):
        self._broadcast_to_recreated_image()

    def render_new_new_image_data(self):
        self._broadcast_to_new_image()

    def update_saved(self, saves_key, value):
        logging.debug("UPDATING " + saves_key + " TO " + str(value))
        self.modules[SAVE].update_saves(saves_key, value)

    def get_coords(self, point_bools):
        point_coords = self.modules[ORIGINAL_COLOUR].get_coords()
        data = [[point_coords[i][0], point_coords[i][1]] for i in range(10) if point_bools[i] and point_coords[i] != (None, None)]
        return data

    def get_original_info(self):
        return self.modules[INFO].get_original_info()

    def get_recreated_info(self):
        return self.modules[INFO].get_recreated_info()

    def get_new_info(self):
        return self.modules[INFO].get_new_info()

    def get_diagram_info(self):
        return self.modules[INFO].get_diagram_info()

    def get_hist_info(self):
        return self.modules[INFO].get_hist_info()

    def get_abspec_info(self):
        return self.modules[INFO].get_abspec_info()

    # Helpers
    def _broadcast_new_data(self):
        self._broadcast_to_original_image()
        self._broadcast_to_recreated_image()
        self._broadcast_to_new_image()
        self._broadcast_to_histogram()
        self._broadcast_to_absorption_spec()

    def _broadcast_to_original_image(self):
        display_mode = self.modules[ORIGINAL_COLOUR].get_displayed_image_mode()
        new_data = None
        if display_mode == RGB:
            logging.debug("GETTING RGB IMAGE")
            new_data = self.get_result(self.current_rendered_result_path).get_rgb_og()
        elif display_mode == STO2:
            logging.debug("GETTING STO2 IMAGE")
            new_data = self.get_result(self.current_rendered_result_path).get_sto2_og()
        elif display_mode == NIR:
            logging.debug("GETTING NIR IMAGE")
            new_data = self.get_result(self.current_rendered_result_path).get_nir_og()
        elif display_mode == THI:
            logging.debug("GETTING THI IMAGE")
            new_data = self.get_result(self.current_rendered_result_path).get_thi_og()
        elif display_mode == TWI:
            logging.debug("GETTING TWI IMAGE")
            new_data = self.get_result(self.current_rendered_result_path).get_twi_og()
        self.modules[ORIGINAL_COLOUR].update_original_image(new_data)
        self.modules[ORIGINAL_COLOUR_DATA].update_original_image_data(new_data)

    def _broadcast_to_recreated_image(self):
        display_mode = self.modules[RECREATED_COLOUR].get_displayed_image_mode()
        new_data = None
        if display_mode == STO2:
            logging.debug("GETTING STO2 IMAGE")
            if not self.is_masked:
                new_data = self.get_result(self.current_rendered_result_path).get_sto2()
            else:
                new_data = self.get_result(self.current_rendered_result_path).get_sto2_masked()
        elif display_mode == NIR:
            logging.debug("GETTING NIR IMAGE")
            if not self.is_masked:
                new_data = self.get_result(self.current_rendered_result_path).get_nir()
            else:
                new_data = self.get_result(self.current_rendered_result_path).get_nir_masked()
        elif display_mode == THI:
            logging.debug("GETTING THI IMAGE")
            if not self.is_masked:
                new_data = self.get_result(self.current_rendered_result_path).get_thi()
            else:
                new_data = self.get_result(self.current_rendered_result_path).get_thi_masked()
        elif display_mode == TWI:
            logging.debug("GETTING TWI IMAGE")
            if not self.is_masked:
                new_data = self.get_result(self.current_rendered_result_path).get_twi()
            else:
                new_data = self.get_result(self.current_rendered_result_path).get_twi_masked()
        self.modules[RECREATED_COLOUR].update_recreated_image(new_data)
        self.modules[RECREATED_COLOUR_DATA].update_recreated_image_data(new_data)

    def _broadcast_to_new_image(self):
        display_mode = self.modules[NEW_COLOUR].get_displayed_image_mode()
        new_data = None
        if self.is_masked:
            if display_mode == WL:
                new_data = self.get_result(self.current_rendered_result_path).get_wl_data_masked()
            elif display_mode == IDX:
                new_data = self.get_result(self.current_rendered_result_path).get_index_masked()
        else:
            if display_mode == WL:
                new_data = self.get_result(self.current_rendered_result_path).get_wl_data()
            elif display_mode == IDX:
                new_data = self.get_result(self.current_rendered_result_path).get_index()
        self.modules[NEW_COLOUR].update_new_colour_image(new_data)
        self.modules[NEW_COLOUR_DATA].update_new_image_data(new_data)

    def _broadcast_to_histogram(self):
        data = self.get_result(self.current_rendered_result_path).get_histogram_data(self.is_masked)
        self.modules[HISTOGRAM].update_histogram(data)

    def _broadcast_to_absorption_spec(self):
        if self.is_masked:
            new_absorption_spec = self.get_result(self.current_rendered_result_path).get_absorption_spec_masked()
        else:
            new_absorption_spec = self.get_result(self.current_rendered_result_path).get_absorption_spec()
        self.modules[ABSORPTION_SPEC].update_absorption_spec(new_absorption_spec)

    def _image_array_to_og_data(self, image_array):
        self.modules[ORIGINAL_COLOUR_DATA].update_array(image_array)

    def _image_array_to_new_data(self, image_array):
        self.modules[NEW_COLOUR_DATA].update_array(image_array)

    def _image_array_to_rec_data(self, image_array):
        self.modules[RECREATED_COLOUR_DATA].update_array(image_array)

    def _update_analysis(self, mask=None, normal=None, absorbance=None, wavelength=None, index_number=None):
        for path, result in self.results.items():  # for each of the data cubes
            if mask is not None:
                logging.debug("UPDATING MASK")
                result.update_mask(mask)
            if normal is not None:
                logging.debug("UPDATING NORMAL TO: " + str(normal))
                result.update_normal(normal)
            if absorbance is not None:
                logging.debug("UPDATING ABSORBANCE TO: " + str(absorbance))
                result.update_absorbance(absorbance)
            if wavelength is not None:
                logging.debug("UPDATING WAVELENGTH TO: " + str(wavelength))
                result.update_wavelength(wavelength)
            if index_number is not None:
                logging.debug("UPDATING INDEX TO: " + str(index_number))
                result.update_index(index_number)

    # Uses the path of the data cube as an identifier
    def _make_new_analysis(self, path, data_cube, normal, absorbance, wavelength, index, mask=None):
        self.results[path] = Analysis(path, data_cube, normal, absorbance, wavelength, index, mask)