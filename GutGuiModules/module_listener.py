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

        # ORIGINAL IMAGE
        self.mask = None

        # DIAGRAM
        self.iswholeimage = True #  TODO: uncomment once diagram is placed back in GUI

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
            # self.iswholeimage = self.modules[DIAGRAM].get_iswholeimage()
            #  TODO: uncomment once diagram is placed back in GUI
            self._make_new_analysis(dc_path, data_cube,
                                    self.normal, self.absorbance, self.wavelength, self.index, self.mask)

    def set_data_cube(self, dc_path):
        self.current_result_path = dc_path
        self._broadcast_new_data()

    def delete_analysis_result(self, path):
        self.results[path] = None

    def submit_output_folder(self, path):
        logging.debug("NEW OUTPUT FOLDER: " + path)
        self.output_folder = path

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
        if not self.iswholeimage:
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
        self._update_analysis(self.current_result_path, new_index_number)
        self._broadcast_new_data()

    def submit_iswholeimage(self, new_iswholeimage):
        self.iswholeimage = new_iswholeimage
        self._broadcast_new_data()

    # Helpers
    def _broadcast_new_data(self):
        # TODO
        # Broadcast changes based on new data
        # Called when changes in display are necessitated
        # Recalculates the results based on the current path and invokes rebuild of related modules
        return None

    def _get_analysis(self, path):
        if self.results[path]:
            return self.results[path]

    def _update_analysis(self, path, mask=None, normal=None, absorbance=None, wavelength=None, index_number=None):
        if self.results[path]:  # only execute if there is an initialized data cube
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