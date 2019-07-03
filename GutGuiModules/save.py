from GutGuiModules.utility import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class Save:
    def __init__(self, save_frame, listener):
        self.root = save_frame

        # Listener
        self.listener = listener

        self.save_specific_button = None
        self.save_all_button = None

        # Saves
        # by default, nothing is saved
        self.saves = {
            WHOLE_IMAGE_SAVE: False,
            MASKED_IMAGE_SAVE: False,
            STO2_DATA: False,
            NIR_DATA: False,
            TWI_DATA: False,
            THI_DATA: False,
            REC_IMAGE: False,
            REC_IMAGE_WO_SCALE: False,
            WL_DATA: False,
            IDX_DATA: False,
            NEW_IMAGE: False,
            NEW_IMAGE_WO_SCALE: False,
            HISTOGRAM_IMAGE: False,
            HISTOGRAM_IMAGE_WO_SCALE: False,
            HISTOGRAM_EXCEL: False,
            ABSORPTION_SPEC_IMAGE: False,
            ABSORPTION_SPEC_IMAGE_WO_SCALE: False,
            ABSORPTION_SPEC_EXCEL: False
        }

        self._init_widgets()

    def _init_widgets(self):
        self._build_save_specific_button()
        self._build_save_all_button()

    def _build_save_specific_button(self):
        self.save_specific_button = make_button(self.root, text="Save Selected", command=self._save_specific, row=1, column=0, outer_pady=0, outer_padx=2, width=10)

    def _build_save_all_button(self):
        self.save_all_button = make_button(self.root, text='Save All', command=self._save_all, row=1, column=2, outer_pady=0, outer_padx=5, width=10)

    def _save_specific(self):
        print('save for specific placeholder')
        #     TODO

    def _save_all(self):
        print('save for all placeholder')
        #     TODO

    def __save_whole_image(self):
        pass

    def __save_masked_image(self):
        pass

    def __save_sto2_data(self):
        pass

    def __save_nir_data(self):
        pass

    def __save_twi_data(self):
        pass

    def __save_thi_data(self):
        pass

    def __save_rec_image(self):
        pass

    def __save_rec_image_wo_scale(self):
        pass

    def __save_wl_data(self):
        pass

    def __save_idx_data(self):
        pass

    def __save_new_image(self):
        pass

    def __save_new_image_wo_scale(self):
        pass

    def __save_histogram_image(self):
        pass

    def __save_histogram_image_wo_scale(self):
        pass

    def __save_histogram_excel(self):
        pass

    def __save_absorption_spec_image(self):
        pass

    def __save_absorption_spec_wo_scale(self):
        pass

    def __save_absorption_spec_excel(self):
        pass

    def __save_data(self, data, title, format=".csv"):
        np.savetxt(title + format, data, delimiter=",")

    def __save_image(self, data, title, format=".png", vmin=0, vmax=1):
        plt.title(title)
        plt.imsave(title + format, data[:, :], cmap='jet', vmin=vmin, vmax=vmax)
        plt.clf()

    def __save_image_wo_scale(self, data, title, format=".png", vmin=0, vmax=1):
        plt.axis('off')  # removes the axis
        plt.imsave(title + format, data[:, :], cmap='jet', vmin=vmin, vmax=vmax)
        plt.clf()

    def __save_excel(self, data, title, format=".xlsx"):
        path = title + format
        df = pd.DataFrame(data)
        df.to_excel(path, index=False)