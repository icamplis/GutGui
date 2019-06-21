from AnalysisModules.analysis import Analysis

class ModuleListener:
    def __init__(self):
        self.results = {}

    def get_analysis(self, path):
        if self.results[path]:
            return self.results[path]

    # Uses the path of the data cube as an identifier
    def make_new_analysis(self, path, data_cube, mask, normal, absorbance, wavelength):
        self.results[path] = Analysis(data_cube, mask, normal, absorbance, wavelength)

    def update_analysis(self, path, mask=None, normal=None, absorbance=None, wavelength=None):
        if self.results[path]:  # only execute if there is an initialized data cube
            if mask:
                self.results[path].update_mask(mask)
            if normal:
                self.results[path].update_normal(normal)
            if absorbance:
                self.results[path].update_wavelength(wavelength)
            if wavelength:
                self.results[path].update_absorbance(absorbance)

    def delete_analysis(self, path):
        self.results[path] = None