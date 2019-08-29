from AnalysisModules.Indices.index_1 import get_index_1
from AnalysisModules.Indices.index_2 import get_index_2
from AnalysisModules.Indices.index_3 import get_index_3
from AnalysisModules.Indices.index_4 import get_index_4
from AnalysisModules.Indices.index_5 import get_index_5
from AnalysisModules.Indices.index_6 import get_index_6
from AnalysisModules.Indices.index_7 import get_index_7
from AnalysisModules.Indices.index_8 import get_index_8
import numpy as np

class Index:
    def __init__(self, index_no, x_abs_or_ref, wavelength=None):
        self.index_no = index_no
        self.x_abs_or_ref = x_abs_or_ref
        assert index_no in [1, 2, 3, 4, 5, 6, 7, 8]
        self.wavelength = wavelength

        self.index = None

        self._calc_index()

    def get_index(self):
        return self.index

    """
    NOTE REGARDING INDICES
    In the original implementation, the index gradient calculation assumed there being 3 axis,
        and that wavelength is not yet bounded.
    That assumption was false, 
        as the index used to calculate the index gradient was ALREADY based on a subset of wavelengths.
    If you look at the implementation of the existant indices, 
        they are an average of a subset of the wavelengths.
    HOWEVER, that subset has nothing to do with the input wavelength, which is very odd.
    """

    def _calc_index(self):
        # Get raw index
        self._calc_raw_index()

    def _calc_raw_index(self):
        if self.index_no == 1:
            self.index = get_index_1(self.x_abs_or_ref)
        elif self.index_no == 2:
            self.index = get_index_2(self.x_abs_or_ref)
        elif self.index_no == 3:
            self.index = get_index_3(self.x_abs_or_ref)
        elif self.index_no == 4:
            self.index = get_index_4(self.x_abs_or_ref)
        elif self.index_no == 5:
            self.index = get_index_5(self.x_abs_or_ref)
        elif self.index_no == 6:
            self.index = get_index_6(self.x_abs_or_ref)
        elif self.index_no == 7:
            self.index = get_index_7(self.x_abs_or_ref)
        elif self.index_no == 8:
            self.index = get_index_8(self.x_abs_or_ref)
        print(self.index[:, :10])
