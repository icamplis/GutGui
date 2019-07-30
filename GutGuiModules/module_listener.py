from AnalysisModules.analysis_abs import AbsSpecAnalysis
from AnalysisModules.analysis_hist import HistogramAnalysis
from AnalysisModules.analysis_new import NewAnalysis
from AnalysisModules.analysis_recreated import RecreatedAnalysis
from GutGuiModules.constants import *
from GutGuiModules.utility import *
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

        self.data_cube = None
        self.dc_path = None

        # ANALYSIS AND FORM
        self.normal = None
        self.absorbance = None
        self.wavelength = None
        self.index = None
        self.index_number = None
        self.histogram_specs = None
        self.ab_spec_specs = None
        self.recreated_specs = None
        self.new_specs = None

        # ORIGINAL IMAGE
        self.mask = None

        # DIAGRAM
        self.is_masked = False

    def get_masked(self):
        return self.is_masked

    def get_wl(self):
        if self.is_masked:
            return self.get_result(self.current_rendered_result_path)[3].get_wl_data_masked()
        else:
            return self.get_result(self.current_rendered_result_path)[3].get_wl_data()

    def get_idx(self):
        if self.is_masked:
            return self.get_result(self.current_rendered_result_path)[3].get_index_masked()
        else:
            return self.get_result(self.current_rendered_result_path)[3].get_index()

    def get_current_rec_data(self):
        return self.modules[RECREATED_COLOUR].get_current_data()

    def get_current_new_data(self):
        return self.modules[NEW_COLOUR].get_current_data()

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

        self.data_cube = data_cube
        self.dc_path = dc_path
        self.results[dc_path] = ['hist', 'abs', 'rec', 'new']

        if self.modules[ANALYSIS_AND_FORM]:
            self.wavelength = self.modules[ANALYSIS_AND_FORM].get_wavelength()
            self.index = self.modules[ANALYSIS_AND_FORM].get_index()
            self.mask = self.modules[ORIGINAL_COLOUR].get_mask()
            self.is_masked = self.modules[DIAGRAM].get_is_masked()

            # specs = (absorbance/reflectance, original/norm, negatives yes/no)
            self.histogram_specs = self.modules[HISTOGRAM].get_specs()
            self.ab_spec_specs = self.modules[ABSORPTION_SPEC].get_specs()
            self.recreated_specs = self.modules[RECREATED_COLOUR].get_specs()
            self.new_specs = self.modules[NEW_COLOUR].get_specs()

            # update each based on inputs
            self._make_new_hist_analysis(dc_path, data_cube, self.wavelength, self.index, self.mask, self.histogram_specs)
            self._make_new_abs_analysis(dc_path, data_cube, self.wavelength, self.index, self.mask, self.ab_spec_specs)
            self._make_new_rec_analysis(dc_path, data_cube, self.wavelength, self.index, self.mask, self.recreated_specs)
            self._make_new_new_analysis(dc_path, data_cube, self.wavelength, self.index, self.mask, self.new_specs)

    def set_data_cube(self, dc_path):
        logging.debug("SELECTED DATA CUBE AT: " + dc_path)
        self.current_rendered_result_path = dc_path
        self._broadcast_new_data()

    def ref_data_cube(self, path):
        # 1. Original reflectance
        # Data cube is originally same for all, use hist because its the first in the list
        cube = self.get_result(path)[0].get_data_cube().tolist()
        for i in range(len(cube)):
            for j in range(len(cube[i])):
                progress(j+i*len(cube[i]), 307200)
                for k in range(len(cube[i][j])):
                    cube[i][j][k] = str(float(cube[i][j][k]))
        return np.asarray(cube)

    def ref_non_neg_cube(self, path):
        # 2. Original reflectance without negative values --> 1 with spaces for
        # negative values
        cube = self.get_result(path)[0].get_data_cube().tolist()
        logging.debug("REMOVING NEGATIVE VALUES...")
        for i in range(len(cube)):
            for j in range(len(cube[i])):
                progress(j+i*len(cube[i]), 307200)
                for k in range(len(cube[i][j])):
                    if cube[i][j][k] < 0:
                        cube[i][j][k] = ''
                    else:
                        cube[i][j][k] = str(float(cube[i][j][k]))
        return np.asarray(cube)

    def ref_norm_cube(self, path):
        # 3. Normalised reflectance --> 1 divded by max(1)
        cube = self.get_result(path)[0].get_data_cube()
        max_val = np.max(cube)
        for i in range(len(cube)):
            for j in range(len(cube[i])):
                progress(j+i*len(cube[i]), 307200)
                for k in range(len(cube[i][j])):
                    cube[i][j][k] = str(float(cube[i][j][k]/max_val))
        return np.asarray(cube)

    def ref_norm_non_neg_cube(self, path):
        # 4. Normalised reflectance without negative values --> 3 with spaces
        # for negative values
        cube = self.get_result(path)[0].get_data_cube()
        logging.debug("REMOVING NEGATIVE VALUES...")
        cube = cube/np.max(cube)
        cube = cube.tolist()
        for i in range(len(cube)):
            for j in range(len(cube[i])):
                progress(j+i*len(cube[i]), 307200)
                for k in range(len(cube[i][j])):
                    if cube[i][j][k] < 0:
                        cube[i][j][k] = ''
                    else:
                        cube[i][j][k] = str(float(cube[i][j][k]))
        return np.asarray(cube)

    def ab_data_cube(self, path):
        # 5. Original absorbance --> -log() of 2
        cube = self.get_result(path)[0].get_data_cube().tolist()
        logging.debug("REMOVING NEGATIVE VALUES...")
        for i in range(len(cube)):
            for j in range(len(cube[i])):
                progress(j+i*len(cube[i]), 307200)
                for k in range(len(cube[i][j])):
                    if cube[i][j][k] <= 0:
                        cube[i][j][k] = ''
                    else:
                        cube[i][j][k] = str(float(-np.log(cube[i][j][k])))
        return np.asarray(cube)

    def ab_non_neg_cube(self, path):
        # 6. Original absorbanve without negative values --> 5 with spaces for
        # negative values
        cube = self.get_result(path)[0].get_data_cube().tolist()
        logging.debug("REMOVING NEGATIVE VALUES...")
        for i in range(len(cube)):
            for j in range(len(cube[i])):
                progress(j+i*len(cube[i]), 307200)
                for k in range(len(cube[i][j])):
                    if cube[i][j][k] <= 0 or cube[i][j][k] > 1:
                        cube[i][j][k] = ''
                    else:
                        cube[i][j][k] = str(float(-np.log(cube[i][j][k])))
        return np.asarray(cube)

    def ab_norm_cube(self, path):
        # 7. Normalised absorbance --> 5 divided by max(5)
        cube = self.get_result(path)[0].get_data_cube().tolist()
        logging.debug("FINDING MAX...")
        max5 = -np.log(np.min(np.abs(cube)))
        logging.debug("REMOVING NEGATIVE VALUES...")
        for i in range(len(cube)):
            for j in range(len(cube[i])):
                progress(j+i*len(cube[i]), 307200)
                for k in range(len(cube[i][j])):
                    if cube[i][j][k] <= 0:
                        cube[i][j][k] = ''
                    else:
                        cube[i][j][k] = str(float(-np.log(cube[i][j][k]))/max5)
        return np.asarray(cube)

    def ab_norm_non_neg_cube(self, path):
        # 8. Normalised absorbance without negative values --> 7 with spaces for
        # negative values
        cube = self.get_result(path)[0].get_data_cube().tolist()
        logging.debug("FINDING MAX...")
        max5 = -np.log(np.min(np.abs(cube)))
        logging.debug("REMOVING NEGATIVE VALUES...")
        for i in range(len(cube)):
            for j in range(len(cube[i])):
                progress(j+i*len(cube[i]), 307200)
                for k in range(len(cube[i][j])):
                    if cube[i][j][k] <= 0 or cube[i][j][k] > 1:
                        cube[i][j][k] = ''
                    else:
                        cube[i][j][k] = str(float(-np.log(cube[i][j][k]))/max5)
        return np.asarray(cube)

    def update_selected_paths(self, selected_paths):
        self.selected_paths = selected_paths

    def delete_analysis_result(self, path):
        logging.debug("DELETING DATA CUBE: " + path)
        self.results[path] = None

    def submit_mask(self, new_mask):
        logging.debug("NEW MASK: [...]")
        self.mask = new_mask
        self._update_analysis(mask=self.mask)
        if self.is_masked:
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
        data = [[float(point_coords[i][0]+1), float(point_coords[i][1]+1)] for i in range(10) if point_bools[i] and point_coords[i] != (None, None)]
        return data

    def instant_save_points(self):
        point_bools = self.modules[ORIGINAL_COLOUR].get_bools()
        data = self.get_coords(point_bools)
        self.modules[SAVE].instant_save_points(data, title="MASK_COORDINATES")

    def get_source_output_info(self):
        return self.modules[INFO].get_source_output_info()

    def get_analysis_form_info(self):
        return self.modules[INFO].get_analysis_form_info()

    def get_csv_info(self):
        return self.modules[INFO].get_csv_info()

    def get_save_info(self):
        return self.modules[INFO].get_save_info()

    def get_original_info(self):
        return self.modules[INFO].get_original_info()

    def get_input_info(self):
        return self.modules[INFO].get_input_info()

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
        # Use hist to get new images from the file as its the first in analysis list
        display_mode = self.modules[ORIGINAL_COLOUR].get_displayed_image_mode()
        new_data = None
        if display_mode == RGB:
            logging.debug("GETTING RGB IMAGE")
            new_data = self.get_result(self.current_rendered_result_path)[0].get_rgb_og()
        elif display_mode == STO2:
            logging.debug("GETTING STO2 IMAGE")
            new_data = self.get_result(self.current_rendered_result_path)[0].get_sto2_og()
        elif display_mode == NIR:
            logging.debug("GETTING NIR IMAGE")
            new_data = self.get_result(self.current_rendered_result_path)[0].get_nir_og()
        elif display_mode == THI:
            logging.debug("GETTING THI IMAGE")
            new_data = self.get_result(self.current_rendered_result_path)[0].get_thi_og()
        elif display_mode == TWI:
            logging.debug("GETTING TWI IMAGE")
            new_data = self.get_result(self.current_rendered_result_path)[0].get_twi_og()
        self.modules[ORIGINAL_COLOUR].update_original_image(new_data)
        self.modules[ORIGINAL_COLOUR_DATA].update_original_image_data(new_data)

    def _broadcast_to_recreated_image(self):
        display_mode = self.modules[RECREATED_COLOUR].get_displayed_image_mode()
        new_data = None
        if display_mode == STO2:
            new_data = self.get_result(self.current_rendered_result_path)[2].get_sto2()
        elif display_mode == NIR:
            new_data = self.get_result(self.current_rendered_result_path)[2].get_nir()
        elif display_mode == THI:
            new_data = self.get_result(self.current_rendered_result_path)[2].get_thi()
        elif display_mode == TWI:
            new_data = self.get_result(self.current_rendered_result_path)[2].get_twi()
        self.modules[RECREATED_COLOUR].update_recreated_image(new_data)
        
        if self.is_masked:
            if display_mode == STO2:
                masked_new_data = self.get_result(self.current_rendered_result_path)[2].get_sto2_masked()
            elif display_mode == NIR:
                masked_new_data = self.get_result(self.current_rendered_result_path)[2].get_nir_masked()
            elif display_mode == THI:
                masked_new_data = self.get_result(self.current_rendered_result_path)[2].get_thi_masked()
            elif display_mode == TWI:
                masked_new_data = self.get_result(self.current_rendered_result_path)[2].get_twi_masked()
            self.modules[RECREATED_COLOUR_DATA].update_recreated_image_data(masked_new_data)
        else:
            self.modules[RECREATED_COLOUR_DATA].update_recreated_image_data(new_data) 

    def _broadcast_to_new_image(self):
        display_mode = self.modules[NEW_COLOUR].get_displayed_image_mode()
        new_data = None
        if display_mode == WL:
            new_data = self.get_result(self.current_rendered_result_path)[3].get_wl_data()
        elif display_mode == IDX:
            new_data = self.get_result(self.current_rendered_result_path)[3].get_index()
        self.modules[NEW_COLOUR].update_new_colour_image(new_data)

        if self.is_masked:
            if display_mode == WL:
                masked_new_data = self.get_result(self.current_rendered_result_path)[3].get_wl_data_masked()
            elif display_mode == IDX:
                masked_new_data = self.get_result(self.current_rendered_result_path)[3].get_index_masked()
            self.modules[NEW_COLOUR_DATA].update_new_image_data(masked_new_data)
        else:
            self.modules[NEW_COLOUR_DATA].update_new_image_data(new_data)

    def _broadcast_to_histogram(self):
        data = self.get_result(self.current_rendered_result_path)[0].get_histogram_data(self.is_masked)
        self.modules[HISTOGRAM].update_histogram(data)

    def _broadcast_to_absorption_spec(self):
        if self.is_masked:
            new_absorption_spec = self.get_result(self.current_rendered_result_path)[1].get_absorption_spec_masked()
        else:
            new_absorption_spec = self.get_result(self.current_rendered_result_path)[1].get_absorption_spec()
        self.modules[ABSORPTION_SPEC].update_absorption_spec(new_absorption_spec)
    def _image_array_to_og_data(self, image_array):
        self.modules[ORIGINAL_COLOUR_DATA].update_original_image_data(image_array)

    def _image_array_to_new_data(self, image_array):
        self.modules[NEW_COLOUR_DATA].update_new_image_data(image_array)

    def _image_array_to_rec_data(self, image_array):
        self.modules[RECREATED_COLOUR_DATA].update_recreated_image_data(image_array)

    def _update_analysis(self, mask=None, wavelength=None, index_number=None):
        for path, result_list in self.results.items():  # for each of the cubes
            if mask is not None:
                logging.debug("UPDATING MASK")
                for i in range(4):
                    # for each affected module
                    result_list[i].update_mask(mask)
            if wavelength is not None:
                logging.debug("UPDATING WAVELENGTH TO: " + str(wavelength))
                for i in range(4):
                    # for each affected module
                    result_list[i].update_wavelength(wavelength)
            if index_number is not None:
                logging.debug("UPDATING INDEX TO: " + str(index_number))
                for i in range(4):
                    # for each affected module
                    result_list[i].update_index(index_number)

    def _update_histogram_specs(self, specs):
        self.histogram_specs = specs
        self._make_new_hist_analysis(self.dc_path, self.data_cube, self.wavelength, self.index, self.mask, self.histogram_specs)
        self._broadcast_to_histogram()

    def _update_abs_specs(self, specs):
        self.ab_spec_specs = specs
        self._make_new_abs_analysis(self.dc_path, self.data_cube, self.wavelength, self.index, self.mask, self.ab_spec_specs)
        self._broadcast_to_absorption_spec()

    def _update_recreated_specs(self, specs):
        self.recreated_specs = specs
        self._make_new_rec_analysis(self.dc_path, self.data_cube, self.wavelength, self.index, self.mask, self.recreated_specs)
        self._broadcast_to_recreated_image()

    def _update_new_specs(self, specs):
        self.new_specs= specs
        self._make_new_new_analysis(self.dc_path, self.data_cube, self.wavelength, self.index, self.mask, self.new_specs)
        self._broadcast_to_new_image()

    # Uses the path of the data cube as an identifier

    def _make_new_hist_analysis(self, path, data_cube, wavelength, index, mask, specs):
        self.results[path][0] = HistogramAnalysis(path, data_cube, wavelength, index, specs, mask)

    def _make_new_abs_analysis(self, path, data_cube, wavelength, index, mask, specs):
        self.results[path][1] = AbsSpecAnalysis(path, data_cube, wavelength, index, specs, mask)

    def _make_new_rec_analysis(self, path, data_cube, wavelength, index, mask, specs):
        self.results[path][2] = RecreatedAnalysis(path, data_cube, wavelength, index, specs, mask)

    def _make_new_new_analysis(self, path, data_cube, wavelength, index, mask, specs):
        self.results[path][3] = NewAnalysis(path, data_cube, wavelength, index, specs, mask)

