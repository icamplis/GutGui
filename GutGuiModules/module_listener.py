from AnalysisModules.analysis_abs import AbsSpecAnalysis
from AnalysisModules.analysis_hist import HistogramAnalysis
from AnalysisModules.analysis_new import NewAnalysis
from AnalysisModules.analysis_recreated import RecreatedAnalysis
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
        self.params = [0.2, -0.03, -0.46, 0.45, 0.4, 1.55, 0.1, -0.5]

        # ORIGINAL IMAGE
        self.mask = []

        # DIAGRAM
        self.is_masked = False

    def get_mask(self):
        if len(self.mask) != 0:
            return self.mask
        else:
            return np.asarray([[False for _ in range(640)] for _ in range(480)])

    def get_wl(self):
        if self.is_masked:
            return self.get_result(self.current_rendered_result_path)[3].get_wl_data_masked()
        else:
            return self.get_result(self.current_rendered_result_path)[3].get_wl_data()

    def get_idx(self):
        if self.is_masked:
            return self.get_result(self.current_rendered_result_path)[3].index_masked
        else:
            return self.get_result(self.current_rendered_result_path)[3].index

    def get_current_original_data(self):
        data = self.modules[ORIGINAL_COLOUR].original_image_data
        if not self.is_masked:
            return data
        else:
            mask = np.logical_not(np.array([self.mask.T] * 3).T)
            return np.ma.array(data, mask=mask)

    def get_current_rec_data(self):
        data = self.modules[RECREATED_COLOUR].recreated_colour_image_data
        if not self.is_masked:
            return data
        else:
            return np.ma.array(data, mask=np.logical_not(self.mask))

    def get_current_norm_rec_data(self):
        image = self.modules[RECREATED_COLOUR].recreated_colour_image_data
        data = image / np.ma.max(image)
        if not self.is_masked:
            return data
        else:
            return np.ma.array(data, mask=np.logical_not(self.mask))

    def get_current_new_data(self):
        data = self.modules[NEW_COLOUR].new_colour_image_data
        if not self.is_masked:
            return data
        else:
            return np.ma.array(data, mask=np.logical_not(self.mask))

    def get_current_norm_new_data(self):
        image = self.modules[NEW_COLOUR].new_colour_image_data
        data = image / np.ma.max(image)
        if not self.is_masked:
            return data
        else:
            return np.ma.array(data, mask=np.logical_not(self.mask))

    def get_current_rec_info(self, saves=False):
        info = ''
        spec_num = self.modules[RECREATED_COLOUR].spec_number
        image_mode = self.modules[RECREATED_COLOUR].displayed_image_mode
        if not saves:
            info += '_' + str(image_mode)
        info += '_fromCSV' + str(spec_num)
        return info

    def get_current_new_info(self, mode=None):
        info = ''
        spec_num = self.modules[NEW_COLOUR].spec_number
        image_mode = self.modules[NEW_COLOUR].displayed_image_mode
        if image_mode == WL or mode == 'WL':
            mod = '_' + str(self.wavelength[0] * 5 + 500) + '-' + str(self.wavelength[1] * 5 + 500)
        elif image_mode == IDX or mode == 'IDX':
            mod = '_IDX' + str(self.index)
        info += str(mod)
        info += '_fromCSV' + str(spec_num)
        return info

    def get_current_hist_abs_info(self, hist_or_abs):
        info = ''
        if hist_or_abs == 'hist':
            spec_num = self.modules[HISTOGRAM].spec_number
        elif hist_or_abs == 'abs':
            spec_num = self.modules[ABSORPTION_SPEC].spec_number
        wl = '_' + str(self.wavelength[0] * 5 + 500) + '-' + str(self.wavelength[1] * 5 + 500)
        info += wl
        info += '_fromCSV' + str(spec_num)
        return info

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
            self.index = self.modules[ANALYSIS_AND_FORM].index_selected
            self.mask = self.modules[ORIGINAL_COLOUR].mask_raw
            self.is_masked = self.modules[DIAGRAM].is_masked

            # specs = (absorbance/reflectance, original/norm, negatives yes/no)
            self.histogram_specs = self.modules[HISTOGRAM].specs
            self.ab_spec_specs = self.modules[ABSORPTION_SPEC].specs
            self.recreated_specs = self.modules[RECREATED_COLOUR].specs
            self.new_specs = self.modules[NEW_COLOUR].specs

            # update each based on inputs
            self._make_new_hist_analysis(dc_path, data_cube, self.wavelength, self.mask,
                                         self.histogram_specs)
            self._make_new_abs_analysis(dc_path, data_cube, self.wavelength, self.mask, self.ab_spec_specs)
            self._make_new_rec_analysis(dc_path, data_cube, self.wavelength, self.mask,
                                        self.recreated_specs, self.params)
            self._make_new_new_analysis(dc_path, data_cube, self.wavelength, self.index, self.mask, self.new_specs)

    def set_data_cube(self, dc_path):
        logging.debug("SELECTED DATA CUBE AT: " + dc_path)
        self.current_rendered_result_path = dc_path
        self.broadcast_new_data()

    def ref_data_cube(self, path):
        # 1. Original reflectance
        # Data cube is originally same for all, use hist because its the first in the list
        cube = self.get_result(path)[0].data_cube.tolist()
        logging.debug("REMOVING NEGATIVE VALUES...")
        for i in range(len(cube)):
            for j in range(len(cube[i])):
                for k in range(len(cube[i][j])):
                    cube[i][j][k] = str(float(cube[i][j][k]))
                progress(j + i * len(cube[i]), 307200)
        return cube

    def ref_non_neg_cube(self, path):
        # 2. Original reflectance without negative values --> 1 with spaces for
        # negative values
        cube = self.get_result(path)[0].data_cube.tolist()
        logging.debug("REMOVING NEGATIVE VALUES...")
        for i in range(len(cube)):
            for j in range(len(cube[i])):
                for k in range(len(cube[i][j])):
                    if cube[i][j][k] < 0:
                        cube[i][j][k] = float('NaN')
                    else:
                        cube[i][j][k] = str(float(cube[i][j][k]))
                progress(j + i * len(cube[i]), 307200)
        return cube

    def ref_norm_cube(self, path):
        # 3. Normalised reflectance --> 1 divded by max(1)
        cube = self.get_result(path)[0].data_cube
        max_val = np.ma.max(cube)
        for i in range(len(cube)):
            for j in range(len(cube[i])):
                for k in range(len(cube[i][j])):
                    cube[i][j][k] = str(float(cube[i][j][k] / max_val))
                progress(j + i * len(cube[i]), 307200)
        return cube

    def ref_norm_non_neg_cube(self, path):
        # 4. Normalised reflectance without negative values --> 3 with spaces
        # for negative values
        cube = self.get_result(path)[0].data_cube
        logging.debug("REMOVING NEGATIVE VALUES...")
        cube = cube / np.ma.max(cube)
        cube = cube.tolist()
        for i in range(len(cube)):
            for j in range(len(cube[i])):
                for k in range(len(cube[i][j])):
                    if cube[i][j][k] < 0:
                        cube[i][j][k] = float('NaN')
                    else:
                        cube[i][j][k] = str(float(cube[i][j][k]))
                progress(j + i * len(cube[i]), 307200)
        return cube

    def ab_data_cube(self, path):
        # 5. Original absorbance --> -log() of 2
        cube = self.get_result(path)[0].data_cube.tolist()
        logging.debug("REMOVING NEGATIVE VALUES...")
        for i in range(len(cube)):
            for j in range(len(cube[i])):
                for k in range(len(cube[i][j])):
                    if cube[i][j][k] <= 0:
                        cube[i][j][k] = float('NaN')
                    else:
                        cube[i][j][k] = str(float(-np.log(cube[i][j][k])))
                progress(j + i * len(cube[i]), 307200)
        return cube

    def ab_non_neg_cube(self, path):
        # 6. Original absorbanve without negative values --> 5 with spaces for
        # negative values
        cube = self.get_result(path)[0].data_cube.tolist()
        logging.debug("REMOVING NEGATIVE VALUES...")
        for i in range(len(cube)):
            for j in range(len(cube[i])):
                for k in range(len(cube[i][j])):
                    if cube[i][j][k] <= 0 or cube[i][j][k] > 1:
                        cube[i][j][k] = float('NaN')
                    else:
                        cube[i][j][k] = str(float(-np.log(cube[i][j][k])))
                progress(j + i * len(cube[i]), 307200)
        return cube

    def ab_norm_cube(self, path):
        # 7. Normalised absorbance --> 5 divided by max(5)
        cube = self.get_result(path)[0].data_cube.tolist()
        logging.debug("FINDING MAX...")
        max5 = -np.ma.log(np.ma.min(np.ma.abs(cube)))
        logging.debug("REMOVING NEGATIVE VALUES...")
        for i in range(len(cube)):
            for j in range(len(cube[i])):
                for k in range(len(cube[i][j])):
                    if cube[i][j][k] <= 0:
                        cube[i][j][k] = float('NaN')
                    else:
                        cube[i][j][k] = str(float(-np.log(cube[i][j][k])) / max5)
                progress(j + i * len(cube[i]), 307200)
        return cube

    def ab_norm_non_neg_cube(self, path):
        # 8. Normalised absorbance without negative values --> 7 with spaces for
        # negative values
        cube = self.get_result(path)[0].data_cube.tolist()
        logging.debug("FINDING MAX...")
        max5 = -np.ma.log(np.ma.min(np.ma.abs(cube)))
        logging.debug("REMOVING NEGATIVE VALUES...")
        for i in range(len(cube)):
            for j in range(len(cube[i])):
                for k in range(len(cube[i][j])):
                    if cube[i][j][k] <= 0 or cube[i][j][k] > 1:
                        cube[i][j][k] = float('NaN')
                    else:
                        cube[i][j][k] = str(float(-np.log(cube[i][j][k])) / max5)
                progress(j + i * len(cube[i]), 307200)
        return cube

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
            self.broadcast_new_data()

    def submit_wavelength(self, new_wavelength):
        logging.debug("NEW WAVELENGTH: " + str(new_wavelength))
        self.wavelength = new_wavelength
        self._update_analysis(wavelength=self.wavelength)
        self.broadcast_new_data()

    def submit_index(self, new_index_number):
        logging.debug("SETTING NEW INDEX: [...]")
        self.index_number = new_index_number
        self._update_analysis(index_number=self.index_number)
        self.broadcast_new_data()

    def submit_is_masked(self, new_is_masked):
        logging.debug("USING WHOLE IMAGE? " + str(new_is_masked))
        self.is_masked = new_is_masked
        self.broadcast_new_data()

    def update_params(self):
        self.params = self.modules[PARAMETER].get_params()
        self._make_new_rec_analysis(self.dc_path, self.data_cube, self.wavelength, self.mask,
                                    self.recreated_specs, self.params)
        self.broadcast_to_recreated_image()

    def update_saved(self, saves_key, value):
        logging.debug("UPDATING " + saves_key + " TO " + str(value))
        self.modules[SAVE].update_saves(saves_key, value)

    def get_coords(self, point_bools):
        point_coords = self.modules[ORIGINAL_COLOUR].coords_list
        data = [[float(point_coords[i][0] + 1), float(point_coords[i][1] + 1)] for i in range(10) if
                point_bools[i] and point_coords[i] != (None, None)]
        return data

    def instant_save_points(self):
        point_bools = self.modules[ORIGINAL_COLOUR].get_bools()
        data = self.get_coords(point_bools)
        self.modules[SAVE].instant_save_points(data, title="MASK_COORDINATES")

    def get_source_output_info(self):
        return self.modules[INFO].source_output_info

    def get_analysis_form_info(self):
        return self.modules[INFO].analysis_form_info

    def get_csv_info(self):
        return self.modules[INFO].csv_info

    def get_save_info(self):
        return self.modules[INFO].save_info

    def get_parameter_info(self):
        return self.modules[INFO].parameter_info

    def get_original_info(self):
        return self.modules[INFO].original_info

    def get_input_info(self):
        return self.modules[INFO].input_info

    def get_original_data_info(self):
        return self.modules[INFO].original_data_info

    def get_recreated_info(self):
        return self.modules[INFO].recreated_info

    def get_recreated_data_info(self):
        return self.modules[INFO].recreated_data_info

    def get_new_info(self):
        return self.modules[INFO].new_info

    def get_new_data_info(self):
        return self.modules[INFO].new_data_info

    def get_diagram_info(self):
        return self.modules[INFO].diagram_info

    def get_hist_info(self):
        return self.modules[INFO].hist_info

    def get_abspec_info(self):
        return self.modules[INFO].abspec_info

    def get_colour_info(self):
        return self.modules[INFO].colour_info

    # Helpers
    def broadcast_new_data(self):
        self.broadcast_to_original_image()
        self.broadcast_to_recreated_image()
        self.broadcast_to_new_image()
        self.broadcast_to_histogram()
        self.broadcast_to_absorption_spec()

    def broadcast_to_original_image(self):
        # Use hist to get new images from the file as its the first in analysis list
        display_mode = self.modules[ORIGINAL_COLOUR].displayed_image_mode
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

    def broadcast_to_recreated_image(self):
        display_mode = self.modules[RECREATED_COLOUR].displayed_image_mode
        new_data = None
        if display_mode == STO2:
            new_data = self.get_result(self.current_rendered_result_path)[2].sto2
        elif display_mode == NIR:
            new_data = self.get_result(self.current_rendered_result_path)[2].nir
        elif display_mode == THI:
            new_data = self.get_result(self.current_rendered_result_path)[2].thi
        elif display_mode == TWI:
            new_data = self.get_result(self.current_rendered_result_path)[2].twi
        self.modules[RECREATED_COLOUR].update_recreated_image(new_data)

        # if self.is_masked:
        #     if display_mode == STO2:
        #         masked_new_data = self.get_result(self.current_rendered_result_path)[2].get_sto2_masked()
        #     elif display_mode == NIR:
        #         masked_new_data = self.get_result(self.current_rendered_result_path)[2].get_nir_masked()
        #     elif display_mode == THI:
        #         masked_new_data = self.get_result(self.current_rendered_result_path)[2].get_thi_masked()
        #     elif display_mode == TWI:
        #         masked_new_data = self.get_result(self.current_rendered_result_path)[2].get_twi_masked()
        #     self.modules[RECREATED_COLOUR_DATA].update_recreated_image_data(masked_new_data)
        # else:
        #     self.modules[RECREATED_COLOUR_DATA].update_recreated_image_data(new_data) 

    def broadcast_to_new_image(self):
        display_mode = self.modules[NEW_COLOUR].displayed_image_mode
        new_data = None
        if display_mode == WL:
            new_data = self.get_result(self.current_rendered_result_path)[3].get_wl_data()
        elif display_mode == IDX:
            new_data = self.get_result(self.current_rendered_result_path)[3].index
        self.modules[NEW_COLOUR].update_new_colour_image(new_data)

        # if self.is_masked:
        #     if display_mode == WL:
        #         masked_new_data = self.get_result(self.current_rendered_result_path)[3].get_wl_data_masked()
        #     elif display_mode == IDX:
        #         masked_new_data = self.get_result(self.current_rendered_result_path)[3].get_index_masked()
        #     self.modules[NEW_COLOUR_DATA].update_new_image_data(masked_new_data)
        # else:
        #     self.modules[NEW_COLOUR_DATA].update_new_image_data(new_data)

    def broadcast_to_histogram(self):
        data = self.get_result(self.current_rendered_result_path)[0].get_histogram_data(self.is_masked)
        self.modules[HISTOGRAM].update_histogram(data)

    def broadcast_to_absorption_spec(self):
        if self.is_masked:
            new_absorption_spec = self.get_result(self.current_rendered_result_path)[1].absorption_roi_masked[:, 1]
        else:
            new_absorption_spec = self.get_result(self.current_rendered_result_path)[1].absorption_roi[:, 1]
        self.modules[ABSORPTION_SPEC].update_absorption_spec(new_absorption_spec)

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
                result_list[3].update_index(index_number)

    def update_histogram_specs(self, specs):
        self.histogram_specs = specs
        self._make_new_hist_analysis(self.dc_path, self.data_cube, self.wavelength, self.mask,
                                     self.histogram_specs)
        self.broadcast_to_histogram()

    def update_abs_specs(self, specs):
        self.ab_spec_specs = specs
        self._make_new_abs_analysis(self.dc_path, self.data_cube, self.wavelength, self.mask,
                                    self.ab_spec_specs)
        self.broadcast_to_absorption_spec()

    def update_recreated_specs(self, specs):
        self.recreated_specs = specs
        self._make_new_rec_analysis(self.dc_path, self.data_cube, self.wavelength, self.mask,
                                    self.recreated_specs, self.params)
        self.broadcast_to_recreated_image()

    def update_new_specs(self, specs):
        self.new_specs = specs
        self._make_new_new_analysis(self.dc_path, self.data_cube, self.wavelength, self.index, self.mask,
                                    self.new_specs)
        self.broadcast_to_new_image()

    # Uses the path of the data cube as an identifier

    def _make_new_hist_analysis(self, path, data_cube, wavelength, mask, specs):
        self.results[path][0] = HistogramAnalysis(path, data_cube, wavelength, specs, ModuleListener(), mask)

    def _make_new_abs_analysis(self, path, data_cube, wavelength, mask, specs):
        self.results[path][1] = AbsSpecAnalysis(path, data_cube, wavelength, specs, ModuleListener(), mask)

    def _make_new_rec_analysis(self, path, data_cube, wavelength, mask, specs, params):
        self.results[path][2] = RecreatedAnalysis(path, data_cube, wavelength, specs, params, ModuleListener(),
                                                  mask)

    def _make_new_new_analysis(self, path, data_cube, wavelength, index, mask, specs):
        self.results[path][3] = NewAnalysis(path, data_cube, wavelength, index, specs, ModuleListener(), mask)
