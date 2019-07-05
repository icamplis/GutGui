from GutGuiModules.utility import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import logging

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

        # The current data cube whose data is being saved.
        # Used to access results from listener
        self.current_result_key = ""
        self.current_result = None  # for readability
        # The current path to save to
        # i.e the current result key's dirname
        self.current_output_path = ""

        self._init_widgets()

    def update_saves(self, key, value):
        assert type(value) == bool
        self.saves[key] = value

    def _init_widgets(self):
        self._build_save_specific_button()
        self._build_save_all_button()

    def _build_save_specific_button(self):
        self.save_specific_button = make_button(self.root, text="Save Selected", command=self._save_specific, row=1, column=0, outer_pady=0, outer_padx=15, width=10)

    def _build_save_all_button(self):
        self.save_all_button = make_button(self.root, text='Save All', command=self._save_all, row=2, column=0, outer_pady=5, outer_padx=15, width=10)

    # Callbacks
    def _save_specific(self):
        for path, _ in self.listener.get_results().items():
            selected_paths = self.listener.get_selected_paths()
            if path in selected_paths:
                self._save_to_path(path)

    def _save_all(self):
        for path, analysis in self.listener.get_results().items():
            self._save_to_path(path)

    # Callback helper
    def _save_to_path(self, path):
        self.current_result_key = path
        self.current_result = self.listener.get_result(self.current_result_key)
        self.current_output_path = os.path.dirname(path)

        if self.saves[STO2_DATA]:
            self.__save_sto2_data_and_image()

        if self.saves[NIR_DATA]:
            self.__save_nir_data_and_image()

        if self.saves[TWI_DATA]:
            self.__save_twi_data_and_image()

        if self.saves[THI_DATA]:
            self.__save_thi_data_and_image()

        if self.saves[WL_DATA]:
            self.__save_wl_data_and_image()

        if self.saves[IDX_DATA]:
            self.__save_idx_data_and_image()

        if self.saves[HISTOGRAM_IMAGE] or \
                self.saves[HISTOGRAM_IMAGE_WO_SCALE] or \
                self.saves[HISTOGRAM_EXCEL]:
            self.__save_histogram()

        if self.saves[ABSORPTION_SPEC_IMAGE] or \
                self.saves[ABSORPTION_SPEC_IMAGE_WO_SCALE] or \
                self.saves[ABSORPTION_SPEC_EXCEL]:
            self.__save_absorption_spec()

    # Module savers
    def __save_sto2_data_and_image(self):
        if self.saves[STO2_DATA]:
            if self.saves[WHOLE_IMAGE_SAVE]:
                self.__save_data(self.current_result.get_sto2(), "STO2_DATA")
                self.__save_image(self.current_result.get_sto2(), "STO2_WHOLE_IMAGE",
                                  self.saves[REC_IMAGE], self.saves[REC_IMAGE_WO_SCALE])
            if self.saves[MASKED_IMAGE_SAVE]:
                self.__save_data(self.current_result.get_sto2_masked(), "STO2_DATA_MASKED")
                self.__save_image(self.current_result.get_sto2_masked(), "STO2_MASKED_IMAGE",
                                  self.saves[REC_IMAGE], self.saves[REC_IMAGE_WO_SCALE])

    def __save_nir_data_and_image(self):
        if self.saves[NIR_DATA]:
            if self.saves[WHOLE_IMAGE_SAVE]:
                self.__save_data(self.current_result.get_nir(), "NIR_DATA")
                self.__save_image(self.current_result.get_nir(), "NIR_WHOLE_IMAGE",
                                  self.saves[REC_IMAGE], self.saves[REC_IMAGE_WO_SCALE])
            if self.saves[MASKED_IMAGE_SAVE]:
                self.__save_data(self.current_result.get_nir_masked(), "NIR_DATA_MASKED")
                self.__save_image(self.current_result.get_nir_masked(), "NIR_MASKED_IMAGE",
                                  self.saves[REC_IMAGE], self.saves[REC_IMAGE_WO_SCALE])

    def __save_twi_data_and_image(self):
        if self.saves[TWI_DATA]:
            if self.saves[WHOLE_IMAGE_SAVE]:
                self.__save_data(self.current_result.get_twi(), "TWI_DATA")
                self.__save_image(self.current_result.get_twi(), "TWI_WHOLE_IMAGE",
                                  self.saves[REC_IMAGE], self.saves[REC_IMAGE_WO_SCALE])
            if self.saves[MASKED_IMAGE_SAVE]:
                self.__save_data(self.current_result.get_twi_masked(), "TWI_DATA_MASKED")
                self.__save_image(self.current_result.get_twi_masked(), "TWI_MASKED_IMAGE",
                                  self.saves[REC_IMAGE], self.saves[REC_IMAGE_WO_SCALE])

    def __save_thi_data_and_image(self):
        if self.saves[THI_DATA]:
            if self.saves[WHOLE_IMAGE_SAVE]:
                self.__save_data(self.current_result.get_thi(), "THI_DATA")
                self.__save_image(self.current_result.get_thi(), "THI_WHOLE_IMAGE",
                                  self.saves[REC_IMAGE], self.saves[REC_IMAGE_WO_SCALE])
            if self.saves[MASKED_IMAGE_SAVE]:
                self.__save_data(self.current_result.get_thi_masked(), "THI_DATA_MASKED")
                self.__save_image(self.current_result.get_thi_masked(), "THI_MASKED_IMAGE",
                                  self.saves[REC_IMAGE], self.saves[REC_IMAGE_WO_SCALE])

    def __save_wl_data_and_image(self):
        if self.saves[WL_DATA]:
            if self.saves[WHOLE_IMAGE_SAVE]:
                self.__save_data(self.current_result.get_wl_data(), "WL_DATA")
                self.__save_image(self.current_result.get_wl_data(), "WL_WHOLE_IMAGE",
                                  self.saves[NEW_IMAGE], self.saves[NEW_IMAGE_WO_SCALE])
            if self.saves[MASKED_IMAGE_SAVE]:
                self.__save_data(self.current_result.get_wl_data_masked(), "WL_DATA_MASKED")
                self.__save_image(self.current_result.get_wl_data_masked(), "WL_MASKED_IMAGE",
                                  self.saves[NEW_IMAGE], self.saves[NEW_IMAGE_WO_SCALE])

    def __save_idx_data_and_image(self):
        if self.saves[IDX_DATA]:
            if self.saves[WHOLE_IMAGE_SAVE]:
                self.__save_data(self.current_result.get_index(), "INDEX_DATA")
                self.__save_image(self.current_result.get_index(), "INDEX_WHOLE_IMAGE",
                                  self.saves[NEW_IMAGE], self.saves[NEW_IMAGE_WO_SCALE])
            if self.saves[MASKED_IMAGE_SAVE]:
                self.__save_data(self.current_result.get_index_masked(), "INDEX_DATA_MASKED")
                self.__save_image(self.current_result.get_index_masked(), "INDEX_MASKED_IMAGE",
                                  self.saves[NEW_IMAGE], self.saves[NEW_IMAGE_WO_SCALE])

    def __save_histogram(self):
        if self.saves[WHOLE_IMAGE_SAVE]:
            data = self.current_result.get_whole_image_data().flatten()
            self.__save_histogram_graph(data, "HISTOGRAM_WHOLE_IMAGE",
                                        self.saves[HISTOGRAM_IMAGE], self.saves[HISTOGRAM_IMAGE_WO_SCALE])
        if self.saves[MASKED_IMAGE_SAVE]:
            data = self.current_result.get_masked_image_data().flatten()
            self.__save_histogram_graph(data, "HISTOGRAM_MASKED_IMAGE",
                                        self.saves[HISTOGRAM_IMAGE], self.saves[HISTOGRAM_IMAGE_WO_SCALE])
        if self.saves[HISTOGRAM_EXCEL]:
            data = self.current_result.get_histogram_data(self.saves[MASKED_IMAGE_SAVE]).flatten()
            self.__save_excel(data, "HISTOGRAM_EXCEL")

    def __save_absorption_spec(self):
        if self.saves[WHOLE_IMAGE_SAVE]:
            data = self.current_result.get_absorption_spec()
            self.__save_absorption_spec_graph(data, "ABSORPTION_SPEC_WHOLE_IMAGE",
                                              self.saves[ABSORPTION_SPEC_IMAGE],
                                              self.saves[ABSORPTION_SPEC_IMAGE_WO_SCALE])
        if self.saves[MASKED_IMAGE_SAVE]:
            data = self.current_result.get_absorption_spec_masked()
            self.__save_absorption_spec_graph(data, "ABSORPTION_SPEC_MASKED_IMAGE",
                                              self.saves[ABSORPTION_SPEC_IMAGE],
                                              self.saves[ABSORPTION_SPEC_IMAGE_WO_SCALE])
        if self.saves[ABSORPTION_SPEC_EXCEL]:
            data = self.current_result.get_absorption_spec()
            self.__save_excel(data, "ABSORPTION_SPEC_EXCEL")

    # Saving helpers
    def __save_data(self, data, title, format=".csv"):
        print("save csv data placeholder")
        output_path = self.current_output_path + "/" + title + format
        logging.debug("SAVING DATA TO " + output_path)
        # np.savetxt(self.current_output_path + "/" + title + format, data, delimiter=",")

    def __save_image(self, data, title, is_image_with_scale, is_image_wo_scale,
                     format=".png", vmin=0, vmax=1):
        if is_image_with_scale:
            self.__save_image_with_scale(data, title, format, vmin, vmax)
        if is_image_wo_scale:
            self.__save_image_wo_scale(data, title, format, vmin, vmax)

    def __save_image_with_scale(self, data, title, format=".png", vmin=0, vmax=1):
        print("save image with scale placeholder")
        output_path = self.current_output_path + "/" + title + format
        logging.debug("SAVING IMAGE TO " + output_path)
        # plt.title(title)
        # plt.imsave(output_path, data[:, :], cmap='jet', vmin=vmin, vmax=vmax)
        # plt.clf()

    def __save_image_wo_scale(self, data, title, format=".png", vmin=0, vmax=1):
        print("save image without scale placeholder")
        output_path = self.current_output_path + "/" + title + format
        logging.debug("SAVING IMAGE WO SCALE TO " + output_path)
        # plt.axis('off')  # removes the axis
        # plt.imsave(output_path, data[:, :], cmap='jet', vmin=vmin, vmax=vmax)
        # plt.clf()

    def __save_excel(self, data, title, format=".xlsx"):
        print("save excel")
        output_path = self.current_output_path + "/" + title + format
        logging.debug("SAVING EXCEL TO " + output_path)
        # df = pd.DataFrame(data)
        # df.to_excel(output_path, index=False)

    def __save_histogram_graph(self, data, title, is_hist_with_scale, is_hist_wo_scale,
                         format=".png", min=0, max=1):
        if is_hist_with_scale:
            self.__save_histogram_with_scale(data, title, format=format, min=min, max=max)
        if is_hist_wo_scale:
            self.__save_histogram_wo_scale(data, title, format=format, min=min, max=max)

    def __save_histogram_with_scale(self, data, title, format=".png", min=0, max=1):
        print("save histogram with scale placeholder")
        # todo
        pass

    def __save_histogram_wo_scale(self, data, title, format=".png", min=0, max=1):
        print("save histogram wo scale placeholder")
        # todo
        pass

    def __save_absorption_spec_graph(self, data, title, is_abspc_with_scale, is_abspc_wo_scale,
                         format=".png", min=0, max=1):
        if is_abspc_with_scale:
            self.__save_absorption_spec_with_scale(data, title, format=format, min=min, max=max)
        if is_abspc_wo_scale:
            self.__save_absorption_spec_wo_scale(data, title, format=format, min=min, max=max)

    def __save_absorption_spec_with_scale(self, data, title, format=".png", min=0, max=1):
        print("save absorptionspec with scale placeholder")
        # todo
        pass

    def __save_absorption_spec_wo_scale(self, data, title, format=".png", min=0, max=1):
        print("save absorptionspec wo scale placeholder")
        # todo
        pass