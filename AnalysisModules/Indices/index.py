from AnalysisModules.Indices.index_1 import get_index_1
from AnalysisModules.Indices.index_2 import get_index_2
from AnalysisModules.Indices.index_3 import get_index_3
from AnalysisModules.Indices.index_4 import get_index_4
from AnalysisModules.Indices.index_5 import get_index_5
from AnalysisModules.Indices.index_6 import get_index_6
from AnalysisModules.Indices.index_7 import get_index_7
from AnalysisModules.Indices.index_8 import get_index_8

class Index:
    def __init__(self, index_no, x_absorbance):
        self.index_no = index_no
        self.x_absorbance = x_absorbance
        assert index_no in [1, 2, 3, 4, 5, 6, 7, 8]
        self._calc_index()

    def get_index(self):
        return self.index

    def _calc_index(self):
        if self.index_no == 1:
            self.index = get_index_1(self.x_absorbance)
        elif self.index_no == 2:
            self.index = get_index_2(self.x_absorbance)
        elif self.index_no == 2:
            self.index = get_index_3(self.x_absorbance)
        elif self.index_no == 2:
            self.index = get_index_4(self.x_absorbance)
        elif self.index_no == 2:
            self.index = get_index_5(self.x_absorbance)
        elif self.index_no == 2:
            self.index = get_index_6(self.x_absorbance)
        elif self.index_no == 2:
            self.index = get_index_7(self.x_absorbance)
        elif self.index_no == 2:
            self.index = get_index_8(self.x_absorbance)