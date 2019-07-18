from GutGuiModules.utility import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
import os
import logging

class Save:
    def __init__(self, save_frame, listener):
        self.root = save_frame

        # Listener
        self.listener = listener

        self.save_specific_button = None
        self.save_all_button = None

        self.info_button = None

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
            ABSORPTION_SPEC_EXCEL: False,
            PT1: False, 
            PT2: False,
            PT3: False, 
            PT4: False,
            PT5: False, 
            PT6: False,
            PT7: False, 
            PT8: False,
            PT9: False, 
            PT10: False,
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
        # print(self.saves)

    def _init_widgets(self):
        self._build_save_specific_button()
        self._build_save_all_button()
        self._build_info_button()

    def _build_save_specific_button(self):
        self.save_specific_button = make_button(self.root, text="Save Selected", command=self._save_specific, row=1, column=0, outer_pady=(0, 15), outer_padx=(90, 0), width=10)

    def _build_save_all_button(self):
        self.save_all_button = make_button(self.root, text='Save All', command=self._save_all, row=1, column=1, outer_pady=(0, 15), outer_padx=15, width=10)

    def _build_info_button(self):
        self.info_button = make_button(self.root, text='?', width=1, command=self.__info, row=0, column=1, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=(222, 0), outer_pady=5, highlightthickness=0)

    # Callbacks
    def __info(self):
        info = self.listener.get_save_info()
        title = "Save Information"
        make_info(title=title, info=info)

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

        if self.saves[PT1] or self.saves[PT2] or self.saves[PT3] or \
                self.saves[PT4] or self.saves[PT5] or self.saves[PT6] or \
                self.saves[PT7] or self.saves[PT8] or self.saves[PT9] or \
                self.saves[PT10]:
            self.__save_points()

    # Module savers
    def __save_points(self):
        point_bools = [self.saves[PT1], self.saves[PT2], self.saves[PT3], self.saves[PT4], self.saves[PT5], self.saves[PT6], self.saves[PT7], self.saves[PT8], self.saves[PT9], self.saves[PT10]]
        data = self.listener.get_coords(point_bools)
        self.__save_data(data, title="MASK_COORDINATES")

    def __save_sto2_data_and_image(self):
        if self.saves[STO2_DATA]:
            if self.saves[WHOLE_IMAGE_SAVE]:
                self.__save_data(self.current_result.get_sto2(), "STO2_DATA")
                self.__save_image(self.current_result.get_sto2(), "STO2_WHOLE_IMAGE",
                                  self.saves[REC_IMAGE], self.saves[REC_IMAGE_WO_SCALE])
            if self.saves[MASKED_IMAGE_SAVE]:
                self.__save_data(self.current_result.get_sto2_masked(), "STO2_DATA_MASKED")
                self.__save_image(self.current_result.get_sto2_masked(), "STO2_MASKED_IMAGE",self.saves[REC_IMAGE], self.saves[REC_IMAGE_WO_SCALE])

    def __save_nir_data_and_image(self):
        if self.saves[NIR_DATA]:
            if self.saves[WHOLE_IMAGE_SAVE]:
                self.__save_data(self.current_result.get_nir(), "NIR_DATA")
                self.__save_image(self.current_result.get_nir(), "NIR_WHOLE_IMAGE", self.saves[REC_IMAGE], self.saves[REC_IMAGE_WO_SCALE])
            if self.saves[MASKED_IMAGE_SAVE]:
                self.__save_data(self.current_result.get_nir_masked(), "NIR_DATA_MASKED")
                self.__save_image(self.current_result.get_nir_masked(), "NIR_MASKED_IMAGE",
                                  self.saves[REC_IMAGE], self.saves[REC_IMAGE_WO_SCALE])

    def __save_twi_data_and_image(self):
        if self.saves[TWI_DATA]:
            if self.saves[WHOLE_IMAGE_SAVE]:
                self.__save_data(self.current_result.get_twi(), "TWI_DATA")
                self.__save_image(self.current_result.get_twi(), "TWI_WHOLE_IMAGE", self.saves[REC_IMAGE], self.saves[REC_IMAGE_WO_SCALE])
            if self.saves[MASKED_IMAGE_SAVE]:
                self.__save_data(self.current_result.get_twi_masked(), "TWI_DATA_MASKED")
                self.__save_image(self.current_result.get_twi_masked(), "TWI_MASKED_IMAGE", self.saves[REC_IMAGE], self.saves[REC_IMAGE_WO_SCALE])

    def __save_thi_data_and_image(self):
        if self.saves[THI_DATA]:
            if self.saves[WHOLE_IMAGE_SAVE]:
                self.__save_data(self.current_result.get_thi(), "THI_DATA")
                self.__save_image(self.current_result.get_thi(), "THI_WHOLE_IMAGE", self.saves[REC_IMAGE], self.saves[REC_IMAGE_WO_SCALE])
            if self.saves[MASKED_IMAGE_SAVE]:
                self.__save_data(self.current_result.get_thi_masked(), "THI_DATA_MASKED")
                self.__save_image(self.current_result.get_thi_masked(), "THI_MASKED_IMAGE", self.saves[REC_IMAGE], self.saves[REC_IMAGE_WO_SCALE])

    def __save_wl_data_and_image(self):
        if self.saves[WL_DATA]:
            if self.saves[WHOLE_IMAGE_SAVE]:
                self.__save_data(self.current_result.get_wl_data(), "WL_DATA")
                self.__save_image(self.current_result.get_wl_data(), "WL_WHOLE_IMAGE", self.saves[NEW_IMAGE], self.saves[NEW_IMAGE_WO_SCALE])
            if self.saves[MASKED_IMAGE_SAVE]:
                self.__save_data(self.current_result.get_wl_data_masked(), "WL_DATA_MASKED")
                self.__save_image(self.current_result.get_wl_data_masked(), "WL_MASKED_IMAGE", self.saves[NEW_IMAGE], self.saves[NEW_IMAGE_WO_SCALE])

    def __save_idx_data_and_image(self):
        if self.saves[IDX_DATA]:
            if self.saves[WHOLE_IMAGE_SAVE]:
                self.__save_data(self.current_result.get_index(), "INDEX_DATA")
                self.__save_image(self.current_result.get_index(), "INDEX_WHOLE_IMAGE", self.saves[NEW_IMAGE], self.saves[NEW_IMAGE_WO_SCALE])
            if self.saves[MASKED_IMAGE_SAVE]:
                self.__save_data(self.current_result.get_index_masked(), "INDEX_DATA_MASKED")
                self.__save_image(self.current_result.get_index_masked(), "INDEX_MASKED_IMAGE",
                                  self.saves[NEW_IMAGE], self.saves[NEW_IMAGE_WO_SCALE])

    def __save_histogram(self):
        if self.saves[WHOLE_IMAGE_SAVE]:
            data = self.current_result.get_whole_image_data().flatten()
            self.__save_histogram_graph(data, "HISTOGRAM_WHOLE_IMAGE", self.saves[HISTOGRAM_IMAGE], self.saves[HISTOGRAM_IMAGE_WO_SCALE])
        if self.saves[MASKED_IMAGE_SAVE]:
            data = self.current_result.get_masked_image_data().flatten()
            self.__save_histogram_graph(data, "HISTOGRAM_MASKED_IMAGE", self.saves[HISTOGRAM_IMAGE], self.saves[HISTOGRAM_IMAGE_WO_SCALE])
        if self.saves[HISTOGRAM_EXCEL]:
            data = self.current_result.get_histogram_data(self.saves[MASKED_IMAGE_SAVE]).flatten()
            self.__save_data(data, "HISTOGRAM_EXCEL")  # it's too slow to save it as an actual xlsx

    def __save_absorption_spec(self):
        if self.saves[WHOLE_IMAGE_SAVE]:
            data = self.current_result.get_absorption_spec()
            self.__save_absorption_spec_graph(data, "ABSORPTION_SPEC_WHOLE_IMAGE", self.saves[ABSORPTION_SPEC_IMAGE], self.saves[ABSORPTION_SPEC_IMAGE_WO_SCALE])
        if self.saves[MASKED_IMAGE_SAVE]:
            data = self.current_result.get_absorption_spec_masked()
            self.__save_absorption_spec_graph(data, "ABSORPTION_SPEC_MASKED_IMAGE", self.saves[ABSORPTION_SPEC_IMAGE], self.saves[ABSORPTION_SPEC_IMAGE_WO_SCALE])
        if self.saves[ABSORPTION_SPEC_EXCEL]:
            data = self.current_result.get_absorption_spec()
            self.__save_data(data, "ABSORPTION_SPEC_EXCEL")

    # Saving helpers
    def __save_data(self, data, title, format=".csv"):
        output_path = self.current_output_path + "/" + title + format
        logging.debug("SAVING DATA TO " + output_path)
        np.savetxt(self.current_output_path + "/" + title + format, data, delimiter=",")

    def __save_image(self, data, title, is_image_with_scale, is_image_wo_scale,
                     format=".png", vmin=0, vmax=1):
        if is_image_with_scale:
            self.__save_image_with_scale(data, title + "_WITH_SCALE", format, vmin, vmax)
        if is_image_wo_scale:
            self.__save_image_wo_scale(data, title + "_WO_SCALE", format, vmin, vmax)

    def __save_image_with_scale(self, data, title, format=".png", vmin=0, vmax=1):
        output_path = self.current_output_path + "/" + title + format
        logging.debug("SAVING IMAGE TO " + output_path)
        plt.imshow(np.flipud(data[:, :].T), cmap='jet', vmin=vmin, vmax=vmax)
        plt.colorbar()
        plt.title(title)
        plt.savefig(output_path)
        plt.clf()

    def __save_image_wo_scale(self, data, title, format=".png", vmin=0, vmax=1):
        output_path = self.current_output_path + "/" + title + format
        logging.debug("SAVING IMAGE WO SCALE TO " + output_path)
        plt.imsave(output_path, np.flipud(data[:, :].T), cmap='jet', vmin=vmin, vmax=vmax)
        plt.clf()

    def __save_histogram_graph(self, data, title, is_hist_with_scale, is_hist_wo_scale, format=".png", min=0, max=1):
        if is_hist_with_scale:
            self.__save_histogram_with_scale(data, title + "_WITH_SCALE", format=format)
        if is_hist_wo_scale:
            self.__save_histogram_wo_scale(data, title + "_WO_SCALE", format=format)

    def __save_histogram_with_scale(self, data, title, format=".png", step_size_value=0.01):
        output_path = self.current_output_path + "/" + title + format
        logging.debug("SAVING HISTOGRAM WITH SCALE TO " + output_path)
        axes = plt.subplot(111)
        # calc bins
        start = np.min(data)
        stop = np.max(data) + step_size_value
        step = step_size_value
        bins = np.arange(start=start, stop=stop, step=step)
        # plot histogram
        axes.hist(data, bins=bins, align='left')
        median = np.median(data)
        median_text = AnchoredText("Median = " + str(median), loc=1, frameon=False)
        axes.add_artist(median_text)
        # plot boxplot
        axes2 = axes.twinx()
        axes2.boxplot(data, vert=False, sym='')
        axes2.get_yaxis().set_visible(False)
        # set axes
        axes.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        plt.title(title)
        plt.savefig(output_path)
        plt.clf()

    def __save_histogram_wo_scale(self, data, title, format=".png", step_size_value=0.01):
        output_path = self.current_output_path + "/" + title + format
        logging.debug("SAVING HISTOGRAM WO SCALE TO " + output_path)
        axes = plt.subplot(111)
        # calc bins
        start = np.min(data)
        stop = np.max(data) + step_size_value
        step = step_size_value
        bins = np.arange(start=start, stop=stop, step=step)
        # plot histogram
        axes.hist(data, bins=bins, align='left')
        median = np.median(data)
        median_text = AnchoredText("Median = " + str(median), loc=1, frameon=False)
        axes.add_artist(median_text)
        # plot boxplot
        axes2 = axes.twinx()
        axes2.boxplot(data, vert=False, sym='')
        axes2.get_yaxis().set_visible(False)
        # set axes
        axes.set_yticklabels([])
        axes.set_xticklabels([])
        plt.axis('off')
        plt.savefig(output_path)
        plt.clf()

    def __save_absorption_spec_graph(self, data, title, is_abspc_with_scale, is_abspc_wo_scale,
                         format=".png", min=0, max=1):
        if is_abspc_with_scale:
            self.__save_absorption_spec_with_scale(data, title + "_WITH_SCALE", format=format)
        if is_abspc_wo_scale:
            self.__save_absorption_spec_wo_scale(data, title + "_WO_SCALE", format=format)

    def __save_absorption_spec_with_scale(self, data, title, format=".png"):
        output_path = self.current_output_path + "/" + title + format
        logging.debug("SAVING ABSORPTION SPEC WO SCALE TO " + output_path)
        axes = plt.subplot(111)
        x_vals = np.arange(500, 1000, 5)
        # plot absorption spec
        axes.plot(x_vals, data[:, 1], '-', lw=0.5)
        axes.grid(linestyle=':', linewidth=0.5)
        plt.title(title)
        plt.savefig(output_path)
        plt.clf()

    def __save_absorption_spec_wo_scale(self, data, title, format=".png"):
        output_path = self.current_output_path + "/" + title + format
        logging.debug("SAVING ABSORPTION SPEC WO SCALE TO " + output_path)
        axes = plt.subplot(111)
        x_vals = np.arange(500, 1000, 5)
        # plot absorption spec
        axes.plot(x_vals, data[:, 1], '-', lw=0.5)
        axes.grid(linestyle=':', linewidth=0.5)
        plt.axis('off')
        plt.savefig(output_path)
        plt.clf()



