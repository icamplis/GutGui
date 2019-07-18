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
        self.normrp_butt = None
        self.ogap_butt = None
        self.norma_butt = None
        self.reflectance_text = None
        self.absorbance_text = None

        self.info_button = None

        self._init_widget()

    # Helper
    def _init_widget(self):
        self._build_og_reflectance()
        self._build_og_reflectance_positive()
        self._build_norm_reflectance()
        self._build_norm_reflectance_positive()
        self._build_og_absorbance_positive()
        self._build_norm_absorbance()
        self._build_text()
        self._build_info_button()

    def _build_og_reflectance(self):
        self.ogr_butt = make_button(self.root, text="1. Original to CSV (Original Data Cube)", command=self.__ogr_to_csv, row=2, column=0, outer_pady=(0, 5), outer_padx=15, width=32)

    def _build_og_reflectance_positive(self):
        self.ogrp_butt = make_button(self.root, text="2. Original without Negative Values to CSV", command=self.__ogrp_to_csv, row=3, column=0, outer_pady=(0, 5), outer_padx=15, width=32)

    def _build_norm_reflectance(self):
        self.normr_butt = make_button(self.root, text="3. Normalised to CSV", command=self.__normr_to_csv, row=4, column=0, outer_pady=(0, 5), outer_padx=15, width=32)

    def _build_norm_reflectance_positive(self):
        self.normrp_butt = make_button(self.root, text="4. Normalised without Negative Values to CSV", command=self.__normrp_to_csv, row=5, column=0, outer_pady=(0, 5), outer_padx=15, width=32)

    def _build_og_absorbance_positive(self):
        self.ogap_butt = make_button(self.root, text="5. Original to CSV", command=self.__ogap_to_csv, row=7, column=0, outer_pady=(0, 5), outer_padx=15, width=32)

    def _build_norm_absorbance(self):
        self.norma_butt = make_button(self.root, text="6. Normalised to CSV", command=self.__norma_to_csv, row=8, column=0, outer_pady=(0, 15), outer_padx=15, width=32)

    def _build_text(self):
        self.reflectance_text = make_text(self.root, content="Reflectance:", bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB), column=0, row=1, width=12, pady=(0, 5))
        self.absorbance_text = make_text(self.root, content="Absorbance:", bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB), column=0, row=6, width=11, pady=(10, 5))

    def _build_info_button(self):
        self.info_button = make_button(self.root, text='?', width=1, command=self.__info, row=0, column=0, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=(280, 0), outer_pady=5, highlightthickness=0)

    def _make_direc(self, direc):
        if not os.path.isdir(direc):
            os.mkdir(direc)

    # callbacks
    def __info(self):
        info = self.listener.get_csv_info()
        title = "Data to CSV Information"
        make_info(title=title, info=info)

    def __ogr_to_csv(self):
        for path, _ in self.listener.get_results().items():
            selected_paths = self.listener.get_selected_paths()
            if path in selected_paths:
                data = self.listener.ref_data_cube(path)
                direc = os.path.dirname(path) + '/1. Reflectance Original to CSV'
                self._make_direc(direc)
                for i in range(100):
                    num = i*5 + 500
                    progress(i, 100)
                    big_path = direc + '/' + 'og_ref_data_slice_' + str(num) + '.csv'
                    np.savetxt(big_path, data[:,:,i], delimiter=",", fmt='%s')

    def __ogrp_to_csv(self):
        update = ['-', '\\', '|', '/']
        for path, _ in self.listener.get_results().items():
            selected_paths = self.listener.get_selected_paths()
            if path in selected_paths:
                data = self.listener.ref_non_neg_cube(path)
                direc = os.path.dirname(path) + '/2. Reflectance Original without Negative Values to CSV'
                self._make_direc(direc)
                for i in range(100):
                    num = i*5 + 500
                    progress(i, 100)
                    big_path = direc + '/' + 'og_ref_positive_data_slice_' + str(num) + '.csv'
                    np.savetxt(big_path, data[:,:,i], delimiter=",", fmt='%s')
        
    def __normr_to_csv(self):
        update = ['-', '\\', '|', '/']
        for path, _ in self.listener.get_results().items():
            selected_paths = self.listener.get_selected_paths()
            if path in selected_paths:
                data = self.listener.ref_norm_cube(path)
                direc = os.path.dirname(path) + '/3. Reflectance Normalised to CSV'
                self._make_direc(direc)
                for i in range(100):
                    num = i*5 + 500
                    progress(i, 100)
                    big_path = direc + '/' + 'norm_ref_data_slice_' + str(num) + '.csv'
                    np.savetxt(big_path, data[:,:,i], delimiter=",", fmt='%s')

    def __normrp_to_csv(self):
        update = ['-', '\\', '|', '/']
        for path, _ in self.listener.get_results().items():
            selected_paths = self.listener.get_selected_paths()
            if path in selected_paths:
                data = self.listener.ref_norm_non_neg_cube(path)
                direc = os.path.dirname(path) + '/4. Reflectance Normalised without Negative Values to CSV'
                self._make_direc(direc)
                for i in range(100):
                    num = i*5 + 500
                    progress(i, 100)
                    big_path = direc + '/' + 'norm_ref_data_slice_' + str(num) + '.csv'
                    np.savetxt(big_path, data[:,:,i], delimiter=",", fmt='%s')
        
    def __ogap_to_csv(self):
        update = ['-', '\\', '|', '/']
        for path, _ in self.listener.get_results().items():
            selected_paths = self.listener.get_selected_paths()
            if path in selected_paths:
                data = self.listener.ab_non_neg_cube(path)
                direc = os.path.dirname(path) + '/5. Absorbance Original to CSV'
                self._make_direc(direc)
                for i in range(100):
                    num = i*5 + 500
                    progress(i, 100)
                    big_path = direc + '/' + 'og_abs_data_slice_' + str(num) + '.csv'
                    np.savetxt(big_path, data[:,:,i], delimiter=",", fmt='%s')
        
    def __norma_to_csv(self):
        update = ['-', '\\', '|', '/']
        for path, _ in self.listener.get_results().items():
            selected_paths = self.listener.get_selected_paths()
            if path in selected_paths:
                data = self.listener.ab_norm_cube(path)
                direc = os.path.dirname(path) + '/6. Absorbance Normalised to CSV'
                self._make_direc(direc)
                for i in range(100):
                    num = i*5 + 500
                    progress(i, 100)
                    big_path = direc + '/' + 'norm_abs_data_slice_' + str(num) + '.csv'
                    np.savetxt(big_path, data[:,:,i], delimiter=",", fmt='%f')

