import numpy as np
from AnalysisModules.analysis_constant import *

# TODO: Need to make an analysis object for each data cube loaded
class Analysis:
    def __init__(self, data_cube, mask, normal=True, wavelength=64):
        self.data_cube = data_cube
        self.mask = mask
        self.wavelength = wavelength
        self.normal = normal

        self.x1 = None
        self.x2 = None
        self.x_absorbance = None
        self.x_reflectance = None
        self.x_absorbance_w = None
        self.x_reflectance_w = None
        self.x_absorbance_masked = None
        self.x_absorbance_masked_w = None

        self.sto2 = None
        self.sto2_masked = None
        self.nir = None
        self.nir_masked = None
        self.thi = None
        self.thi_masked = None
        self.twi = None
        self.twi_masked = None

        self._x_absorbance_gradient = None
        self._x_absorbance_gradient_min_1 = None
        self._x_absorbance_gradient_min_2 = None
        self._x_absorbance_min_570_590 = None
        self._x_absorbance_min_740_780 = None
        self._x_absorbance_mean_825_925 = None
        self._x_absorbance_mean_655_735 = None
        self._x_absorbance_mean_530_590 = None
        self._x_absorbance_mean_785_825 = None
        self._x_absorbance_mean_880_900 = None
        self._x_absorbance_mean_955_980 = None

        self.analysis()

    def analysis(self):
        self._calc_general()
        self._calc_sto2()
        self._calc_nir()
        self._calc_thi()
        self._calc_twi()

    def update_mask(self, new_mask):
        self.mask = new_mask
        self.analysis()

    def update_wavelength(self, new_wavelength):
        self.wavelength = new_wavelength
        self.analysis()

    def update_normal(self, new_normal):
        self.normal = new_normal
        self.analysis()

    def get_x_absorbance(self):
        return self.x_absorbance

    def get_x_reflectance(self):
        return self.x_reflectance

    def get_x_absorbance_w(self):
        return self.x_absorbance_w

    def get_x_reflectance_w(self):
        return self.x_reflectance_w

    def get_x_absorbance_masked(self):
        return self.x_absorbance_masked

    def get_x_absorbance_masked_w(self):
        return self.x_absorbance_masked_w

    def get_sto2(self):
        return self.sto2

    def get_sto2_masked(self):
        return self.sto2_masked

    def get_nir(self):
        return self.nir

    def get_nir_masked(self):
        return self.nir_masked

    def get_thi(self):
        return self.thi

    def get_thi_masked(self):
        return self.thi_masked

    def get_twi(self):
        return self.twi

    def get_twi_masked(self):
        return self.twi_masked

    def _calc_general(self):
        self.__calc_x1()
        self.__calc_x_reflectance()
        self.__calc_x2()
        self.__calc_x_absorbance()

    def _calc_sto2(self):
        self._x_absorbance_gradient = np.gradient(self.x_absorbance, axis=2)
        self._x_absorbance_gradient_min_1 = self._x_absorbance_gradient[:, :, 14:18].min(axis=2)  # between 570nm and 590nm
        self._x_absorbance_gradient_min_2 = self._x_absorbance_gradient[:, :, 48:56].min(axis=2)  # between 740nm and 780nm
        self._x_absorbance_min_570_590 = self._x_absorbance_gradient[:, :, 14:18].min(axis=2)  # between 570nm and 590nm
        self._x_absorbance_min_740_780 = self._x_absorbance_gradient[:, :, 48:56].min(axis=2)  # between 740nm and 780nm
        temp1 = self._x_absorbance_min_570_590 / R1
        temp2 = self._x_absorbance_min_740_780 / R2
        self.sto2 = temp1 / (temp1 + temp2)
        self.sto2_masked = np.ma.array(self.sto2[:, :], mask=[self.mask])

    def _calc_nir(self):
        self._x_absorbance_mean_825_925 = self.x_absorbance[:, :, 65:85].mean(axis=2)  # between (825nm : 925nm)
        self._x_absorbance_mean_655_735 = self.x_absorbance[:, :, 31:47].mean(axis=2)  # between (655nm : 735nm)
        temp1 = self._x_absorbance_mean_825_925 / self._x_absorbance_mean_655_735
        self.nir = (temp1 - S1) / (S2 - S1)
        self.nir_masked = np.ma.array(self.nir[:, :], mask=[self.mask])

    def _calc_thi(self):
        self._x_absorbance_mean_530_590 = self.x_absorbance[:, :, 6:18].mean(axis=2)  # between (530nm : 590nm)
        self._x_absorbance_mean_785_825 = self.x_absorbance[:, :, 57:65].mean(axis=2)  # between (785nm : 825nm)
        temp1 = self._x_absorbance_mean_530_590 / self._x_absorbance_mean_785_825
        self.thi = (temp1 - T1) / (T2 - T1)
        self.thi_masked = np.ma.array(self.thi[:, :], mask=[self.mask])

    def _calc_twi(self):
        self._x_absorbance_mean_880_900 = self.x_absorbance[:, :, 76:80].mean(axis=2)  # between (880nm : 900nm)
        self._x_absorbance_mean_955_980 = self.x_absorbance[:, :, 91:96].mean(axis=2)  # between (955nm : 980nm)
        temp1 = self._x_absorbance_mean_880_900 / self._x_absorbance_mean_955_980
        self.twi = (temp1 - U1) / (U2 - U1)
        self.twi_masked = np.ma.array(self.twi[:, :], mask=[self.mask])

    def __calc_x1(self):
        if self.normal:
            self.x1 = self.data_cube/self.data_cube.max()
        else:
            self.x1 = self.data_cube

    def __calc_x_reflectance(self):
        self.x_reflectance = self.x1
        self.x_reflectance = np.ma.array(self.x_reflectance, mask=self.data_cube < 0)
        self.x_reflectance_w = self.x_reflectance[:, :, self.wavelength]

    def __calc_x2(self):
        self.x1 = self.x1.clip(min=0)
        self.x2 = -np.log(self.x1)

    def __calc_x_absorbance(self):
        self.x_absorbance = np.ma.array(self.x2, mask=~np.isfinite(self.x2))
        if self.normal:
            self.x_absorbance = self.x_absorbance / self.x_absorbance.max()
        self.x_absorbance_w = self.x_absorbance[:, :, self.wavelength]
        self.x_absorbance_masked = np.ma.array(self.x_absorbance[:, :, :], mask=[self.mask] * 100)
        self.x_absorbance_masked_w = np.ma.array(self.x_absorbance[:, :, self.wavelength], mask=self.mask)
