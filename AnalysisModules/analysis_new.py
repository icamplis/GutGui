import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)
from AnalysisModules.analysis_constant import *
from AnalysisModules.Indices import Index
from GutGuiModules.utility import *
from GutGuiModules.constants import *
import logging

class NewAnalysis:
    # performs analyses necessary for new image
    def __init__(self, path, data_cube, wavelength, index_number, specs, mask=None):

        # inputs
        self.path = path
        self.data_cube = data_cube
        self.mask = mask
        self.wavelength = wavelength
        self.absorbance = bool(specs[0])
        self.normal = not bool(specs[1])
        self.negative = bool(specs[2])

        # calculated generally
        self.x1 = None
        self.x2 = None
        self.x_absorbance = None
        self.x_reflectance = None
        self.x_absorbance_w = None
        self.x_reflectance_w = None
        self.x_absorbance_masked = None
        self.x_absorbance_masked_w = None
        self.x_reflectance_masked = None
        self.x_reflectance_masked_w = None

        # specific to module
        self.index_number = index_number
        self.index = None
        self.index_masked = None

        self.analysis()

    def analysis(self):
        self._calc_general()
        self._calc_index(self.index_number)

    def update_mask(self, new_mask):
        self.mask = new_mask
        self.analysis()

    def update_wavelength(self, new_wavelength):
        self.wavelength = new_wavelength
        self.analysis()

    def update_normal(self, new_normal):
        self.normal = new_normal
        self.analysis()

    def update_absorbance(self, new_absorbance):
        self.absorbance = new_absorbance
        self.analysis()

    def update_index(self, new_index_number):
        self.index_number = new_index_number
        self.analysis()

    def get_index(self):
        if self.negative:
            return self.index
        else:
            return self.index

    def get_index_masked(self):
        if self.negative:
            return self.index_masked
        else:
            return self.index_masked

    def get_wl_data(self):
        if self.absorbance:
            if self.negative:
                new_data = self.x_absorbance_w
            else:
                new_data = self.x_absorbance_w
        else:
            if self.negative:
                new_data = self.x_reflectance_w
            else:
                new_data = self.x_reflectance_w
        return new_data

    def get_wl_data_masked(self):
        if self.absorbance:
            if self.negative:
                new_data = self.x_absorbance_masked_w
            else:
                new_data = self.x_absorbance_masked_w
        else:
            if self.negative:
                new_data = self.x_reflectance_masked_w
            else:
                new_data = self.x_reflectance_masked_w
        return new_data

    def _calc_general(self):
        logging.debug("CALCULATING: NEW IMAGE...")
        self.__calc_x1(self)
        self.__calc_x_reflectance()
        self.__calc_x2()
        self.__calc_x_absorbance()

    def _calc_index(self, index_number):
        logging.debug("CALCULATING: INDEX...")
        if self.absorbance:
            index_module = Index(index_number, self.x_absorbance, wavelength=self.wavelength)
            self.index = index_module.get_index()
            if self.mask is not None:
                masked_index_module = Index(index_number, self.x_absorbance_masked, wavelength=self.wavelength)
                self.index_masked = masked_index_module.get_index()
        else:
            index_module = Index(index_number, self.x_reflectance, wavelength=self.wavelength)
            self.index = index_module.get_index()
            if self.mask is not None:
                masked_index_module = Index(index_number, self.x_reflectance_masked, wavelength=self.wavelength)
                self.index_masked = masked_index_module.get_index()

    @staticmethod
    def __calc_x1(self):
        if self.normal:
            self.x1 = self.data_cube/self.data_cube.max()
        else:
            self.x1 = self.data_cube

    def __calc_x_reflectance(self):
        self.x_reflectance = np.ma.array(self.x1, mask=self.data_cube<0)

        if self.wavelength[0] != self.wavelength[1]:
            wav_lower = int(round(max(0, min(self.wavelength)), 0))
            wav_upper = int(round(min(max(self.wavelength), 99), 0))
            self.x_reflectance_w = np.mean(self.x_reflectance[:, :, wav_lower : wav_upper], axis=2)
        else:
            self.x_reflectance_w = self.x_reflectance[:, :, self.wavelength[0]]

        if self.mask is not None:
            mask = np.logical_not(np.array([self.mask.T] * 100).T)
            self.x_reflectance_masked = np.ma.array(self.x_reflectance[:, :, :], mask=mask)
            # self.x_reflectance_masked_w = np.ma.array(self.x_reflectance[:, :, self.wavelength[0]], mask=self.mask)
            if self.wavelength[0] != self.wavelength[1]:
                wav_lower = int(round(max(0, min(self.wavelength)), 0))
                wav_upper = int(round(min(max(self.wavelength), 99), 0))
                self.x_reflectance_masked_w = np.ma.array(np.mean(self.x_reflectance[:, :, wav_lower: wav_upper], axis=2), mask=self.mask)
            else:
                self.x_reflectance_masked_w = np.ma.array(self.x_reflectance[:, :, self.wavelength[0]], mask=self.mask)

    def __calc_x2(self):
        copy = self.x1.copy()
        self.x2 = -np.log(copy.clip(min=0))

    def __calc_x_absorbance(self):
        self.x_absorbance = np.ma.array(self.x2, mask=~np.isfinite(self.x2))

        if self.normal:
            self.x_absorbance = self.x_absorbance / self.x_absorbance.max()

        if self.wavelength[0] != self.wavelength[1]:
            wav_lower = int(round(max(0, min(self.wavelength)), 0))
            wav_upper = int(round(min(max(self.wavelength), 99), 0))
            self.x_absorbance_w = np.mean(self.x_absorbance[:, :, wav_lower : wav_upper], axis=2)
        else:
            self.x_absorbance_w = self.x_absorbance[:, :, self.wavelength[0]]

        if self.mask is not None:
            # self.x_absorbance_masked = self.__apply_2DMask_on_3DArray(self.mask, self.x_absorbance)
            mask = np.logical_not(np.array([self.mask.T] * 100).T)
            self.x_absorbance_masked = np.ma.array(self.x_absorbance[:, :, :], mask=mask)
            # self.x_absorbance_masked = np.ma.array(self.x_absorbance[:, :, :], mask=np.array([self.mask] * 100))
            if self.wavelength[0] != self.wavelength[1]:
                wav_lower = int(round(min(0, min(self.wavelength)), 0))
                wav_upper = int(round(max(max(self.wavelength), 99), 0))
                self.x_absorbance_masked_w = np.ma.array(np.mean(self.x_absorbance[:, :, wav_lower: wav_upper], axis=2),
                                                         mask=self.mask)
            else:
                self.x_absorbance_masked_w = np.ma.array(self.x_absorbance[:, :, self.wavelength[0]], mask=self.mask)
