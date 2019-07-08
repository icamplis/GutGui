from AnalysisModules.Indices.index_1 import get_index_1
from AnalysisModules.Indices.index_2 import get_index_2
from AnalysisModules.Indices.index_3 import get_index_3
from AnalysisModules.Indices.index_4 import get_index_4
from AnalysisModules.Indices.index_5 import get_index_5
from AnalysisModules.Indices.index_6 import get_index_6
from AnalysisModules.Indices.index_7 import get_index_7
from AnalysisModules.Indices.index_8 import get_index_8

class Index:
    def __init__(self, index_no, x_abs_or_ref, mask=None):
        self.index_no = index_no
        self.x_abs_or_ref = x_abs_or_ref
        assert index_no in [1, 2, 3, 4, 5, 6, 7, 8]

        self.mask = mask

        self.index = None

        self._calc_index()

    def get_index(self):
        return self.index

    def _calc_index(self):
        # Get raw index
        self._calc_raw_index()
        self._calc_index_gradient()

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

    # TODO: get index gradient
    def _calc_index_gradient(self):
        # Todo: I'm not sure why this isn't working
        # index_gradient = np.gradient(index)
        # index_gradient = index_gradient[:, :, wavelength[0], wavelength[1]]
        # index = (index_gradient)
        pass