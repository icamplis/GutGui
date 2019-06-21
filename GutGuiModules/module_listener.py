from AnalysisModules.analysis import Analysis
from GutGuiModules.constants import *

class ModuleListener:
    def __init__(self):
        # {module_name: module}
        self.modules = {}

        # SOURCE AND OUTPUT VALUES
        # {data_cube_path: analysis object}
        self.results = {}
        self.output_folder = None  # init with None intentionally

        # ANALYSIS AND FORM
        self.normal = None
        self.absorbance = None
        self.wavelength = None
        self.index = None

        # ORIGINAL IMAGE
        self.mask = None

        # DIAGRAM
        self.iswholeimage = None

    def attach_module(self, module_name, module):
        self.modules[module_name] = module

    def submit_data_cube(self, data_cube, dc_path):
        if self.modules[ANALYSIS_AND_FORM]:
            self.normal = self.modules[ANALYSIS_AND_FORM].get_normal()
            self.absorbance = self.modules[ANALYSIS_AND_FORM].get_absorbance()
            self.wavelength = self.modules[ANALYSIS_AND_FORM].get_wavelength()
            self.mask = self.modules[ORIGINAL_COLOUR].get_mask()
            self._make_new_analysis(dc_path, data_cube, normal, absorbance, wavelength, mask)

    def submit_output_folder(self, path):
        self.output_folder = path

    # Update based on new data
    def update_data(self):
        # todo
        return None

    def delete_analysis_result(self, path):
        self.results[path] = None

    def _get_analysis(self, path):
        if self.results[path]:
            return self.results[path]

    def _update_analysis(self, path, mask=None, normal=None, absorbance=None, wavelength=None):
        if self.results[path]:  # only execute if there is an initialized data cube
            if mask:
                self.results[path].update_mask(mask)
            if normal:
                self.results[path].update_normal(normal)
            if absorbance:
                self.results[path].update_wavelength(wavelength)
            if wavelength:
                self.results[path].update_absorbance(absorbance)

    # Uses the path of the data cube as an identifier
    def _make_new_analysis(self, path, data_cube, normal, absorbance, wavelength, mask=None):
        self.results[path] = Analysis(data_cube, normal, absorbance, wavelength, mask)