from GutGuiModules.utility import *
import numpy as np
import os
import logging

class CSVSaver:
    def __init__(self, csv_frame, listener):
        self.root = csv_frame

        # Listener
        self.listener = listener

        self.ogr_butt = None
        self.ogrp_butt = None
        self.normr_butt = None
        self.ogap_butt = None
        self.norma_butt = None

        self._init_widget()

    # Helper
    def _init_widget(self):
        self._build_og_reflectance()
        self._build_og_reflectance_positive()
        self._build_norm_reflectance()
        self._build_og_absorbance_positive()
        self._build_norm_absorbance()

    def _build_og_reflectance(self):
        self.ogr_butt = make_button(self.root, text="Original Reflectance to CSV", command=self.__ogr_to_csv, row=1, column=0, outer_pady=(0, 5), outer_padx=15, width=40)

    def _build_og_reflectance_positive(self):
        self.ogrp_butt = make_button(self.root, text="Original Reflectance without Negative Values to CSV", command=self.__ogrp_to_csv, row=2, column=0, outer_pady=(0, 5), outer_padx=15, width=40)

    def _build_norm_reflectance(self):
        self.normr_butt = make_button(self.root, text="Normalised Reflectance to CSV", command=self.__normr_to_csv, row=3, column=0, outer_pady=(0, 5), outer_padx=15, width=40)

    def _build_og_absorbance_positive(self):
        self.ogap_butt = make_button(self.root, text="Original Absorbance to CSV", command=self.__ogap_to_csv, row=4, column=0, outer_pady=(0, 5), outer_padx=15, width=40)

    def _build_norm_absorbance(self):
        self.norma_butt = make_button(self.root, text="Normalised Absorbance to CSV", command=self.__norma_to_csv, row=5, column=0, outer_pady=(0, 5), outer_padx=15, width=40)

    # callbacks

    def __ogr_to_csv(self):
        for path, _ in self.listener.get_results().items():
            selected_paths = self.listener.get_selected_paths()
            if path in selected_paths:
                data = self.listener.ref_data_cube(path)
                direc = os.path.dirname(path) + '/og_ref_data_slices'
                os.mkdir(direc)
                for i in range(100):
                    num = i*5 + 500
                    logging.debug("SAVING SLICE " + str(i))
                    big_path = direc + '/' + 'data_slice_' + str(num) + '.csv'
                    np.savetxt(big_path, data[:,:,i], delimiter=",", fmt='%f')

    def __ogrp_to_csv(self):
        for path, _ in self.listener.get_results().items():
            selected_paths = self.listener.get_selected_paths()
            if path in selected_paths:
                data = self.listener.ref_non_neg_cube(path)
                direc = os.path.dirname(path) + '/og_ref_positive_data_slices'
                os.mkdir(direc)
                for i in range(100):
                    num = i*5 + 500
                    logging.debug("SAVING SLICE " + str(i))
                    big_path = direc + '/' + 'data_slice_' + str(num) + '.csv'
                    np.savetxt(big_path, data[:,:,i], delimiter=",", fmt='%f')
        
    def __normr_to_csv(self):
        for path, _ in self.listener.get_results().items():
            selected_paths = self.listener.get_selected_paths()
            if path in selected_paths:
                data = self.listener.ref_norm_cube(path)
                direc = os.path.dirname(path) + '/norm_ref_data_slices'
                os.mkdir(direc)
                for i in range(100):
                    num = i*5 + 500
                    logging.debug("SAVING SLICE " + str(i))
                    big_path = direc + '/' + 'data_slice_' + str(num) + '.csv'
                    np.savetxt(big_path, data[:,:,i], delimiter=",", fmt='%f')
        
    def __ogap_to_csv(self):
        for path, _ in self.listener.get_results().items():
            selected_paths = self.listener.get_selected_paths()
            if path in selected_paths:
                data = self.listener.ab_non_neg_cube(path)
                direc = os.path.dirname(path) + '/og_abs_positive_data_slices'
                os.mkdir(direc)
                for i in range(100):
                    num = i*5 + 500
                    logging.debug("SAVING SLICE " + str(i))
                    big_path = direc + '/' + 'data_slice_' + str(num) + '.csv'
                    np.savetxt(big_path, data[:,:,i], delimiter=",", fmt='%f')
        
    def __norma_to_csv(self):
        for path, _ in self.listener.get_results().items():
            selected_paths = self.listener.get_selected_paths()
            if path in selected_paths:
                data = self.listener.ab_norm_cube(path)
                direc = os.path.dirname(path) + '/norm_abs_data_slices'
                os.mkdir(direc)
                for i in range(100):
                    num = i*5 + 500
                    logging.debug("SAVING SLICE " + str(i))
                    big_path = direc + '/' + 'data_slice_' + str(num) + '.csv'
                    np.savetxt(big_path, data[:,:,i], delimiter=",", fmt='%f')








