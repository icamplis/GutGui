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
        self.oga_butt = None
        self.ogap_butt = None
        self.norma_butt = None
        self.normap_butt = None
        self.rec_butt = None
        self.new_butt = None
        self.reflectance_text = None
        self.absorbance_text = None
        self.image_text = None

        self.info_label = None

        self._init_widget()

    # Helper
    def _init_widget(self):
        self._build_og_reflectance()
        self._build_og_reflectance_positive()
        self._build_norm_reflectance()
        self._build_norm_reflectance_positive()
        self._build_og_absorbance()
        self._build_og_absorbance_positive()
        self._build_norm_absorbance()
        self._build_norm_absorbance_positive()
        self._build_rec()
        self._build_new()
        self._build_text()
        self._build_info_label()

    def _build_og_reflectance(self):
        self.ogr_butt = make_button(self.root, text="1. Original to CSV (Original Data Cube)", command=self.__ogr_to_csv, row=2, column=0, outer_pady=(0, 5), outer_padx=15, width=32)

    def _build_og_reflectance_positive(self):
        self.ogrp_butt = make_button(self.root, text="2. Original without Negative Values to CSV", command=self.__ogrp_to_csv, row=3, column=0, outer_pady=(0, 5), outer_padx=15, width=32)

    def _build_norm_reflectance(self):
        self.normr_butt = make_button(self.root, text="3. Normalised to CSV", command=self.__normr_to_csv, row=4, column=0, outer_pady=(0, 5), outer_padx=15, width=32)

    def _build_norm_reflectance_positive(self):
        self.normrp_butt = make_button(self.root, text="4. Normalised without Negative Values to CSV", command=self.__normrp_to_csv, row=5, column=0, outer_pady=(0, 5), outer_padx=15, width=32)

    def _build_og_absorbance(self):
        self.oga_butt = make_button(self.root, text="5. Original to CSV", command=self.__oga_to_csv, row=7, column=0, outer_pady=(0, 5), outer_padx=15, width=32)

    def _build_og_absorbance_positive(self):
        self.ogap_butt = make_button(self.root, text="6. Original without Negative Values to CSV", command=self.__ogap_to_csv, row=8, column=0, outer_pady=(0, 5), outer_padx=15, width=32)

    def _build_norm_absorbance(self):
        self.norma_butt = make_button(self.root, text="7. Normalised to CSV", command=self.__norma_to_csv, row=9, column=0, outer_pady=(0, 5), outer_padx=15, width=32)

    def _build_norm_absorbance_positive(self):
        self.normap_butt = make_button(self.root, text="8. Normalised without Negative Values to CSV", command=self.__normap_to_csv, row=10, column=0, outer_pady=(0, 5), outer_padx=15, width=32)

    def _build_rec(self):
        self.rec_butt = make_button(self.root, text="9. Recreated Image to CSV", command=self.__rec_to_csv, row=12, column=0, outer_pady=(0, 5), outer_padx=15, width=32)

    def _build_new(self):
        self.new_butt = make_button(self.root, text="10. New Image to CSV", command=self.__new_to_csv, row=13, column=0, outer_pady=(0, 15), outer_padx=15, width=32)

    def _build_text(self):
        self.reflectance_text = make_text(self.root, content="Reflectance:", bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB), column=0, row=1, width=12, pady=(0, 5))
        self.absorbance_text = make_text(self.root, content="Absorbance:", bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB), column=0, row=6, width=11, pady=(10, 5))
        self.image_text = make_text(self.root, content="Images:", bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB), column=0, row=11, width=7, pady=(10, 5))

    def _build_info_label(self):
        self.info_label = make_label_button(self.root, text='Data to CSV', command=self.__info, width=9)
        self.info_label.grid(padx=(0, 200))

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
                    big_path = direc + '/' + 'norm_ref_positive_data_slice_' + str(num) + '.csv'
                    np.savetxt(big_path, data[:,:,i], delimiter=",", fmt='%s')
        
    def __oga_to_csv(self):
        update = ['-', '\\', '|', '/']
        for path, _ in self.listener.get_results().items():
            selected_paths = self.listener.get_selected_paths()
            if path in selected_paths:
                data = self.listener.ab_data_cube(path)
                direc = os.path.dirname(path) + '/5. Absorbance Original to CSV'
                self._make_direc(direc)
                for i in range(100):
                    num = i*5 + 500
                    progress(i, 100)
                    big_path = direc + '/' + 'og_abs_data_slice_' + str(num) + '.csv'
                    np.savetxt(big_path, data[:,:,i], delimiter=",", fmt='%s')
        
    def __ogap_to_csv(self):
        update = ['-', '\\', '|', '/']
        for path, _ in self.listener.get_results().items():
            selected_paths = self.listener.get_selected_paths()
            if path in selected_paths:
                data = self.listener.ab_non_neg_cube(path)
                direc = os.path.dirname(path) + '/6. Absorbance Original without Negative Values to CSV'
                self._make_direc(direc)
                for i in range(100):
                    num = i*5 + 500
                    progress(i, 100)
                    big_path = direc + '/' + 'og_abs_positive_data_slice_' + str(num) + '.csv'
                    np.savetxt(big_path, data[:,:,i], delimiter=",", fmt='%s')
        
    def __norma_to_csv(self):
        update = ['-', '\\', '|', '/']
        for path, _ in self.listener.get_results().items():
            selected_paths = self.listener.get_selected_paths()
            if path in selected_paths:
                data = self.listener.ab_norm_cube(path)
                direc = os.path.dirname(path) + '/7. Absorbance Normalised to CSV'
                self._make_direc(direc)
                for i in range(100):
                    num = i*5 + 500
                    progress(i, 100)
                    big_path = direc + '/' + 'norm_abs_data_slice_' + str(num) + '.csv'
                    np.savetxt(big_path, data[:,:,i], delimiter=",", fmt='%s')
        
    def __normap_to_csv(self):
        update = ['-', '\\', '|', '/']
        for path, _ in self.listener.get_results().items():
            selected_paths = self.listener.get_selected_paths()
            if path in selected_paths:
                data = self.listener.ab_norm_non_neg_cube(path)
                direc = os.path.dirname(path) + '/8. Absorbance Normalised without Negative Values to CSV'
                self._make_direc(direc)
                for i in range(100):
                    num = i*5 + 500
                    progress(i, 100)
                    big_path = direc + '/' + 'norm_abs_positive_data_slice_' + str(num) + '.csv'
                    np.savetxt(big_path, data[:,:,i], delimiter=",", fmt='%s')

    def __rec_to_csv(self):
        for path, _ in self.listener.get_results().items():
            selected_paths = self.listener.get_selected_paths()
            if path in selected_paths:
                data = self.listener.get_current_rec_data().T
                direc = os.path.dirname(path) + '/9. Recreated Image to CSV'
                self._make_direc(direc)
                big_path = direc + '/' + 'recreated_image_data.csv'
                np.savetxt(big_path, data, delimiter=",", fmt='%s')


    def __new_to_csv(self):
        update = ['-', '\\', '|', '/']
        for path, _ in self.listener.get_results().items():
            selected_paths = self.listener.get_selected_paths()
            if path in selected_paths:
                data = self.listener.get_current_new_data().T
                direc = os.path.dirname(path) + '/10. New Image to CSV'
                self._make_direc(direc)
                big_path = direc + '/' + 'new_image_data.csv'
                np.savetxt(big_path, data, delimiter=",", fmt='%s')
    



