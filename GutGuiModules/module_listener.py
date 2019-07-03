from AnalysisModules.analysis import Analysis
from GutGuiModules.constants import *
import logging

class ModuleListener:
    def __init__(self):
        # {module_name: module}
        self.modules = {}

        # SOURCE AND OUTPUT VALUES
        # {data_cube_path: analysis object}
        self.results = {}
        self.current_result_path = None
        self.output_folder = None  # init with None intentionally

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
            self.iswholeimage = self.modules[DIAGRAM].get_is_masked()
            self._make_new_analysis(dc_path, data_cube,
                                    self.normal, self.absorbance, self.wavelength, self.index, self.mask)

    def set_data_cube(self, dc_path):
        logging.debug("SELECTED DATA CUBE AT: " + dc_path)
        self.current_result_path = dc_path
        self._broadcast_new_data()

    def delete_analysis_result(self, path):
        logging.debug("DELETING DATA CUBE: " + path)
        self.results[path] = None

    def submit_normal(self, new_normal):
        assert type(new_normal) == bool
        logging.debug("NEW NORMAL: " + str(new_normal))
        self.normal = new_normal
        self._update_analysis(self.current_result_path, normal=self.normal)
        self._broadcast_new_data()

    def submit_mask(self, new_mask):
        logging.debug("NEW MASK: [...]")
        self.mask = new_mask
        self._update_analysis(self.current_result_path, mask=self.mask)
        if self.is_masked:
            self._broadcast_new_data()

    def submit_absorbance(self, new_absorbance):
        logging.debug("NEW (USING) ABSORBANCE: " + str(new_absorbance))
        assert type(new_absorbance) == bool
        self.absorbance = new_absorbance
        self._update_analysis(self.current_result_path, absorbance=self.absorbance)
        self._broadcast_new_data()

    def submit_wavelength(self, new_wavelength):
        logging.debug("NEW WAVELENGTH: " + str(new_wavelength))
        self.wavelength = new_wavelength
        self._update_analysis(self.current_result_path, wavelength=self.wavelength)
        self._broadcast_new_data()

    def submit_index(self, new_index_number):
        logging.debug("SETTING NEW INDEX: [...]")
        self.index_number = new_index_number
        self._update_analysis(self.current_result_path, index_number=new_index_number)
        self._broadcast_new_data()

    def submit_is_masked(self, new_is_masked):
        logging.debug("USING WHOLE IMAGE? " + str(new_is_masked))
        self.is_masked = new_is_masked
        self._broadcast_new_data()

    def render_new_recreated_image_data(self):
        self._broadcast_to_recreated_image()

    def render_new_new_image_data(self):
        self._broadcast_to_new_image()

    # Helpers
    def _broadcast_new_data(self):
        self._broadcast_to_original_image()
        self._broadcast_to_recreated_image()
        self._broadcast_to_new_image()
        self._broadcast_to_histogram()
        self._broadcast_to_absorption_spec()

    def _broadcast_to_original_image(self):
        # TODO
        pass

    def _broadcast_to_recreated_image(self):
        display_mode = self.modules[RECREATED_COLOUR].get_displayed_image_mode()
        new_data = None
        if display_mode == STO2:
            logging.debug("GETTING STO2 IMAGE")
            if not self.is_masked:
                new_data = self._get_analysis(self.current_result_path).get_sto2()
            else:
                new_data = self._get_analysis(self.current_result_path).get_sto2_masked()
        elif display_mode == NIR:
            logging.debug("GETTING NIR IMAGE")
            if not self.is_masked:
                new_data = self._get_analysis(self.current_result_path).get_nir()
            else:
                new_data = self._get_analysis(self.current_result_path).get_nir_masked()
        elif display_mode == THI:
            logging.debug("GETTING THI IMAGE")
            if not self.is_masked:
                new_data = self._get_analysis(self.current_result_path).get_thi()
            else:
                new_data = self._get_analysis(self.current_result_path).get_thi_masked()
        elif display_mode == TWI:
            logging.debug("GETTING TWI IMAGE")
            if not self.is_masked:
                new_data = self._get_analysis(self.current_result_path).get_twi()
            else:
                new_data = self._get_analysis(self.current_result_path).get_twi_masked()
        self.modules[RECREATED_COLOUR].update_recreated_image(new_data)

    def _broadcast_to_new_image(self):
        display_mode = self.modules[NEW_COLOUR].get_displayed_image_mode()
        new_data = None
        if self.is_masked:
            if display_mode == WL:
                # todo: ask Alex what WL data is wrt to notebook
                new_data = None
            elif display_mode == IDX:
                new_data = self._get_analysis(self.current_result_path).get_masked_index()
        else:
            if display_mode == WL:
                # todo: ask Alex what WL data is wrt to notebook
                new_data = None
            elif display_mode == IDX:
                new_data = self._get_analysis(self.current_result_path).get_index()
        self.modules[NEW_COLOUR].update_new_colour_image(new_data)

    def _broadcast_to_histogram(self):
        new_data_cube = self._get_analysis(self.current_result_path).get_data_cube()
        self.modules[HISTOGRAM].update_histogram(new_data_cube)

    def _broadcast_to_absorption_spec(self):
        if self.mask:
            new_absorption_spec = self._get_analysis(self.current_result_path).get_absorption_spec_masked()
        else:
            new_absorption_spec = self._get_analysis(self.current_result_path).get_absorption_spec()
        self.modules[ABSORPTION_SPEC].update_absorption_spec(new_absorption_spec)

    def _get_analysis(self, path):
        if self.results[path] is not None:
            return self.results[path]

    def _update_analysis(self, path, mask=None, normal=None, absorbance=None, wavelength=None, index_number=None):
        if self.results[path] is not None:  # only execute if there is an initialized data cube
            if mask:
                self.results[path].update_mask(mask)
            if normal:
                self.results[path].update_normal(normal)
            if absorbance:
                self.results[path].update_wavelength(wavelength)
            if wavelength:
                self.results[path].update_absorbance(absorbance)
            if index_number:
                self.results[path].update_index(index_number)

    # Uses the path of the data cube as an identifier
    def _make_new_analysis(self, path, data_cube, normal, absorbance, wavelength, index, mask=None):
        self.results[path] = Analysis(data_cube, normal, absorbance, wavelength, index, mask)