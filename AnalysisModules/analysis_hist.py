import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)
from AnalysisModules.analysis_constant import *
from AnalysisModules.Indices import Index
from GutGuiModules.utility import *
from GutGuiModules.constants import *
import logging

RGB_FILE = "_RGB-Image.png"
STO2_FILE = "_Oxygenation.png"
NIR_FILE = "_NIR-Perfusion.png"
THI_FILE = "_THI.png"
TWI_FILE = "_TWI.png"

class HistogramAnalysis:
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
        self.rgb_og = None
        self.sto2_og = None
        self.nir_og = None
        self.thi_og = None
        self.twi_og = None

        self.analysis()

    def analysis(self):
        self._calc_general()

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

    def get_data_cube(self):
        return self.data_cube

    def get_rgb_og(self):
        filename = str(self.path[:-13]) + RGB_FILE
        self.rgb_og = image_to_array(filename)
        return self.rgb_og[30:510, 3:643, :]

    def get_sto2_og(self):
        filename = str(self.path[:-13]) + STO2_FILE
        self.sto2_og = image_to_array(filename)
        return self.sto2_og[26:506, 4:644, :]

    def get_nir_og(self):
        filename = str(self.path[:-13]) + NIR_FILE
        self.nir_og = image_to_array(filename)
        return self.nir_og[26:506, 4:644, :]

    def get_thi_og(self):
        filename = str(self.path[:-13]) + THI_FILE
        self.thi_og = image_to_array(filename)
        return self.thi_og[26:506, 4:644, :]

    def get_twi_og(self):
        filename = str(self.path[:-13]) + TWI_FILE
        self.twi_og = image_to_array(filename)
        return self.twi_og[24:504, 4:644, :]

    def get_histogram_data(self, is_masked):
        if is_masked:
        # if there is a mask
            if self.absorbance:
            # if absorbance
                if self.negative:
                # if there can be negatives
                    data = self.x_absorbance_masked
                else:
                # if no negatives
                    data = self.x_absorbance_masked[self.x_absorbance_masked>=0]
            else:
            # if reflectance
                if self.negative:
                # if there can be negatives
                    data = self.x_reflectance_masked
                else:
                # if no negatives
                    data = self.x_reflectance_masked[self.x_reflectance_masked>=0]
        else:
        # if there is no mask
            if self.absorbance:
            # if absorbance
                if self.negative:
                # if there can be negatives
                    data = self.x_absorbance
                else:
                # if no negatives
                    data = self.x_absorbance[self.x_absorbance>=0]
            else:
            # if reflectance
                if self.negative:
                # if there can be negatives
                    data = self.x_reflectance
                else:
                # if no negatives
                    data = self.x_reflectance[self.x_reflectance>=0]
        return data

    def _calc_general(self):
        logging.debug("CALCULATING: HISTOGRAM...")
        self.__calc_x1(self)
        self.__calc_x_reflectance()
        self.__calc_x2()
        self.__calc_x_absorbance()

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
