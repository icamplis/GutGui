from GutGuiModules.utility import *
import numpy as np
import matplotlib.pyplot as plt
import skimage.color
import os
import logging


class Save:
    def __init__(self, save_frame, listener):
        self.root = save_frame

        # Listener
        self.listener = listener

        self.save_specific_button = None
        self.save_all_button = None

        self.info_label = None

        # Saves
        # by default, nothing is saved
        self.saves = {
            WHOLE_IMAGE_SAVE: False,
            MASKED_IMAGE_SAVE: False,
            GS_ORIGINAL: False,
            GS_RECREATED: False,
            GS_NEW: False,
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
        self.current_result_list = None  # for readability
        self.current_hist_result = None
        self.current_abs_result = None
        self.current_rec_result = None
        self.current_new_result = None
        # The current path to save to
        # i.e the current result key's dirname
        self.current_output_path = ""

        self._init_widgets()

    def update_saves(self, key, value):
        assert type(value) == bool
        self.saves[key] = value
        # print(self.saves)

    def instant_save_points(self, data, title):
        for path, _ in self.listener.get_results().items():
            selected_paths = self.listener.get_selected_paths()
            if path in selected_paths:
                output_path = os.path.dirname(path) + "/" + title + '.csv'
                logging.debug("SAVING DATA TO " + output_path)
                np.savetxt(output_path, data, delimiter=",", fmt="%.2f")

    def _init_widgets(self):
        self._build_save_specific_button()
        self._build_save_all_button()
        self._build_info_label()

    def _build_save_specific_button(self):
        self.save_specific_button = make_button(self.root, text="Save for Selected Data Cube Only",
                                                command=self._save_specific, row=1, column=0, outer_pady=(0, 5),
                                                outer_padx=15, width=13, wraplength=120, height=2)

    def _build_save_all_button(self):
        self.save_all_button = make_button(self.root, text='Save for All Data Cubes', command=self._save_all, row=2,
                                           column=0, outer_pady=(0, 15), outer_padx=15, width=13, wraplength=120,
                                           height=2)

    def _build_info_label(self):
        self.info_label = make_label_button(self.root, text='Save', command=self.__info, width=4)
        self.info_label.grid(padx=(0, 90))

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
        for path, _ in self.listener.get_results().items():
            self._save_to_path(path)

    # Callback helper
    def _save_to_path(self, path):
        self.current_result_key = path
        self.current_result_list = self.listener.get_result(self.current_result_key)

        self.current_hist_result = self.current_result_list[0]
        self.current_abs_result = self.current_result_list[1]
        self.current_rec_result = self.current_result_list[2]
        self.current_new_result = self.current_result_list[3]

        self.current_output_path = os.path.dirname(path)

        if self.saves[GS_ORIGINAL]:
            self.__save_gs_original_image()

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
        point_bools = [self.saves[PT1], self.saves[PT2], self.saves[PT3], self.saves[PT4], self.saves[PT5],
                       self.saves[PT6], self.saves[PT7], self.saves[PT8], self.saves[PT9], self.saves[PT10]]
        data = self.listener.get_coords(point_bools)
        self.__save_data(data, title="MASK_COORDINATES")

    def __convert_original_image(self, array, mask=None):
        if mask is None:
            mask = []
        if len(mask) == 0:
            return np.flipud(np.asarray(rgb_image_to_hsi_array(array)).reshape((480, 640))).T
        else:
            return np.ma.array(np.flipud(skimage.color.rgb2gray(array)).T, mask=mask)

    def __save_gs_original_image(self):
        if self.saves[GS_ORIGINAL]:
            if self.saves[WHOLE_IMAGE_SAVE]:
                rgb = self.__convert_original_image(self.current_hist_result.get_rgb_og())
                self.__save_image_diagram(rgb, "RGB_GREYSCALE", False, cmap='gray')
                sto2 = self.__convert_original_image(self.current_hist_result.get_sto2_og())
                self.__save_image_diagram(sto2, "STO2_GREYSCALE", False, cmap='gray')
                nir = self.__convert_original_image(self.current_hist_result.get_nir_og())
                self.__save_image_diagram(nir, "NIR_GREYSCALE", False, cmap='gray')
                thi = self.__convert_original_image(self.current_hist_result.get_thi_og())
                self.__save_image_diagram(thi, "THI_GREYSCALE", False, cmap='gray')
                twi = self.__convert_original_image(self.current_hist_result.get_twi_og())
                self.__save_image_diagram(twi, "TWI_GREYSCALE", False, cmap='gray')
            if self.saves[MASKED_IMAGE_SAVE]:
                mask = np.logical_not(self.listener.get_mask())
                rgb = self.__convert_original_image(self.current_hist_result.get_rgb_og(), mask)
                self.__save_image_diagram(rgb, "RGB_GREYSCALE_MASKED", False, cmap='gray')
                sto2 = self.__convert_original_image(self.current_hist_result.get_sto2_og(), mask)
                self.__save_image_diagram(sto2, "STO2_GREYSCALE_MASKED", False, cmap='gray')
                nir = self.__convert_original_image(self.current_hist_result.get_nir_og(), mask)
                self.__save_image_diagram(nir, "NIR_GREYSCALE_MASKED", False, cmap='gray')
                thi = self.__convert_original_image(self.current_hist_result.get_thi_og(), mask)
                self.__save_image_diagram(thi, "THI_GREYSCALE_MASKED", False, cmap='gray')
                twi = self.__convert_original_image(self.current_hist_result.get_twi_og(), mask)
                self.__save_image_diagram(twi, "TWI_GREYSCALE_MASKED", False, cmap='gray')

    def __save_sto2_data_and_image(self):
        name = self.listener.get_current_rec_info(saves=True)
        if self.saves[STO2_DATA]:
            if self.saves[WHOLE_IMAGE_SAVE]:
                self.__save_data(self.current_rec_result.get_sto2(), "STO2_DATA" + name)
                self.__save_image(self.current_rec_result.get_sto2(), "STO2_WHOLE_IMAGE" + name, self.saves[REC_IMAGE],
                                  self.saves[REC_IMAGE_WO_SCALE])
                if self.saves[GS_RECREATED]:
                    self.__save_image(self.current_rec_result.get_sto2(), "STO2_WHOLE_IMAGE_GREYSCALE" + name,
                                      self.saves[REC_IMAGE], self.saves[REC_IMAGE_WO_SCALE], cmap='gray')
            if self.saves[MASKED_IMAGE_SAVE]:
                self.__save_data(self.current_rec_result.get_sto2_masked(), "STO2_DATA_MASKED" + name)
                self.__save_image(self.current_rec_result.get_sto2_masked(), "STO2_MASKED_IMAGE" + name,
                                  self.saves[REC_IMAGE], self.saves[REC_IMAGE_WO_SCALE])
                if self.saves[GS_RECREATED]:
                    self.__save_image(self.current_rec_result.get_sto2_masked(), "STO2_MASKED_IMAGE_GREYSCALE" + name,
                                      self.saves[REC_IMAGE], self.saves[REC_IMAGE_WO_SCALE], cmap='gray')

    def __save_nir_data_and_image(self):
        name = self.listener.get_current_rec_info(saves=True)
        if self.saves[NIR_DATA]:
            if self.saves[WHOLE_IMAGE_SAVE]:
                self.__save_data(self.current_rec_result.get_nir(), "NIR_DATA" + name)
                self.__save_image(self.current_rec_result.get_nir(), "NIR_WHOLE_IMAGE" + name, self.saves[REC_IMAGE],
                                  self.saves[REC_IMAGE_WO_SCALE])
                if self.saves[GS_RECREATED]:
                    self.__save_image(self.current_rec_result.get_nir(), "NIR_WHOLE_IMAGE_GREYSCALE" + name,
                                      self.saves[REC_IMAGE], self.saves[REC_IMAGE_WO_SCALE], cmap='gray')
            if self.saves[MASKED_IMAGE_SAVE]:
                self.__save_data(self.current_rec_result.get_nir_masked(), "NIR_DATA_MASKED" + name)
                self.__save_image(self.current_rec_result.get_nir_masked(), "NIR_MASKED_IMAGE" + name,
                                  self.saves[REC_IMAGE], self.saves[REC_IMAGE_WO_SCALE])
                if self.saves[GS_RECREATED]:
                    self.__save_image(self.current_rec_result.get_nir_masked(), "NIR_MASKED_IMAGE_GREYSCALE" + name,
                                      self.saves[REC_IMAGE], self.saves[REC_IMAGE_WO_SCALE], cmap='gray')

    def __save_twi_data_and_image(self):
        name = self.listener.get_current_rec_info(saves=True)
        if self.saves[TWI_DATA]:
            if self.saves[WHOLE_IMAGE_SAVE]:
                self.__save_data(self.current_rec_result.get_twi(), "TWI_DATA" + name)
                self.__save_image(self.current_rec_result.get_twi(), "TWI_WHOLE_IMAGE" + name, self.saves[REC_IMAGE],
                                  self.saves[REC_IMAGE_WO_SCALE])
                if self.saves[GS_RECREATED]:
                    self.__save_image(self.current_rec_result.get_twi(), "TWI_WHOLE_IMAGE_GREYSCALE" + name,
                                      self.saves[REC_IMAGE], self.saves[REC_IMAGE_WO_SCALE], cmap='gray')
            if self.saves[MASKED_IMAGE_SAVE]:
                self.__save_data(self.current_rec_result.get_twi_masked(), "TWI_DATA_MASKED" + name)
                self.__save_image(self.current_rec_result.get_twi_masked(), "TWI_MASKED_IMAGE" + name,
                                  self.saves[REC_IMAGE], self.saves[REC_IMAGE_WO_SCALE])
                if self.saves[GS_RECREATED]:
                    self.__save_image(self.current_rec_result.get_twi_masked(), "TWI_MASKED_IMAGE_GREYSCALE" + name,
                                      self.saves[REC_IMAGE], self.saves[REC_IMAGE_WO_SCALE], cmap='gray')

    def __save_thi_data_and_image(self):
        name = self.listener.get_current_rec_info(saves=True)
        if self.saves[THI_DATA]:
            if self.saves[WHOLE_IMAGE_SAVE]:
                self.__save_data(self.current_rec_result.get_thi(), "THI_DATA" + name)
                self.__save_image(self.current_rec_result.get_thi(), "THI_WHOLE_IMAGE" + name, self.saves[REC_IMAGE],
                                  self.saves[REC_IMAGE_WO_SCALE])
                if self.saves[GS_RECREATED]:
                    self.__save_image(self.current_rec_result.get_thi(), "THI_WHOLE_IMAGE_GREYSCALE" + name,
                                      self.saves[REC_IMAGE], self.saves[REC_IMAGE_WO_SCALE], cmap='gray')
            if self.saves[MASKED_IMAGE_SAVE]:
                self.__save_data(self.current_rec_result.get_thi_masked(), "THI_DATA_MASKED" + name)
                self.__save_image(self.current_rec_result.get_thi_masked(), "THI_MASKED_IMAGE" + name,
                                  self.saves[REC_IMAGE], self.saves[REC_IMAGE_WO_SCALE])
                if self.saves[GS_RECREATED]:
                    self.__save_image(self.current_rec_result.get_thi_masked(), "THI_MASKED_IMAGE_GREYSCALE" + name,
                                      self.saves[REC_IMAGE], self.saves[REC_IMAGE_WO_SCALE], cmap='gray')

    def __save_wl_data_and_image(self):
        name = self.listener.get_current_new_info(mode='WL')
        if self.saves[WL_DATA]:
            if self.saves[WHOLE_IMAGE_SAVE]:
                self.__save_data(self.current_new_result.get_wl_data(), "WL_DATA" + name)
                self.__save_image(self.current_new_result.get_wl_data(), "WL_WHOLE_IMAGE" + name, self.saves[NEW_IMAGE],
                                  self.saves[NEW_IMAGE_WO_SCALE])
                if self.saves[GS_NEW]:
                    self.__save_image(self.current_new_result.get_wl_data(), "WL_WHOLE_IMAGE_GREYSCALE" + name,
                                      self.saves[NEW_IMAGE], self.saves[NEW_IMAGE_WO_SCALE], cmap='gray')
            if self.saves[MASKED_IMAGE_SAVE]:
                self.__save_data(self.current_new_result.get_wl_data_masked(), "WL_DATA_MASKED" + name)
                self.__save_image(self.current_new_result.get_wl_data_masked(), "WL_MASKED_IMAGE" + name,
                                  self.saves[NEW_IMAGE], self.saves[NEW_IMAGE_WO_SCALE])
                if self.saves[GS_NEW]:
                    self.__save_image(self.current_new_result.get_wl_data_masked(), "WL_MASKED_IMAGE_GREYSCALE" + name,
                                      self.saves[NEW_IMAGE], self.saves[NEW_IMAGE_WO_SCALE], cmap='gray')

    def __save_idx_data_and_image(self):
        name = self.listener.get_current_new_info(mode='IDX')
        if self.saves[IDX_DATA]:
            if self.saves[WHOLE_IMAGE_SAVE]:
                self.__save_data(self.current_new_result.get_index(), "INDEX_DATA" + name)
                self.__save_image(self.current_new_result.get_index(), "INDEX_WHOLE_IMAGE" + name,
                                  self.saves[NEW_IMAGE],
                                  self.saves[NEW_IMAGE_WO_SCALE])
                if self.saves[GS_NEW]:
                    self.__save_image(self.current_new_result.get_index(), "INDEX_WHOLE_IMAGE_GREYSCALE" + name,
                                      self.saves[NEW_IMAGE], self.saves[NEW_IMAGE_WO_SCALE], cmap='gray')
            if self.saves[MASKED_IMAGE_SAVE]:
                self.__save_data(self.current_new_result.get_index_masked(), "INDEX_DATA_MASKED" + name)
                self.__save_image(self.current_new_result.get_index_masked(), "INDEX_MASKED_IMAGE" + name,
                                  self.saves[NEW_IMAGE], self.saves[NEW_IMAGE_WO_SCALE])
                if self.saves[GS_NEW]:
                    self.__save_image(self.current_new_result.get_index_masked(), "INDEX_MASKED_IMAGE_GREYSCALE" + name,
                                      self.saves[NEW_IMAGE], self.saves[NEW_IMAGE_WO_SCALE], cmap='gray')

    def __save_histogram(self):
        name = self.listener.get_current_hist_info()
        if self.saves[WHOLE_IMAGE_SAVE]:
            data = self.current_hist_result.get_histogram_data(is_masked=False).flatten()
            self.__save_histogram_graph(data, "HISTOGRAM_WHOLE_IMAGE" + name, self.saves[HISTOGRAM_IMAGE],
                                        self.saves[HISTOGRAM_IMAGE_WO_SCALE])
        if self.saves[MASKED_IMAGE_SAVE]:
            data = self.current_hist_result.get_histogram_data(is_masked=True).flatten()
            self.__save_histogram_graph(data, "HISTOGRAM_MASKED_IMAGE" + name, self.saves[HISTOGRAM_IMAGE],
                                        self.saves[HISTOGRAM_IMAGE_WO_SCALE])
        if self.saves[HISTOGRAM_EXCEL]:
            data = self.current_hist_result.get_histogram_data(self.saves[MASKED_IMAGE_SAVE]).flatten()
            start = np.min(data)
            step = self.listener.modules[HISTOGRAM].get_step_size()
            stop = np.max(data) + step
            bins = np.arange(start=start, stop=stop, step=step)
            counts, _, _ = plt.hist(data, bins=bins)
            hist_data = np.stack((bins[1:], counts)).T
            self.__save_data(hist_data, "HISTOGRAM_EXCEL" + name, fmt="%.2f")  # too slow to save it as an actual xlsx

    def __save_absorption_spec(self):
        name = self.listener.get_current_abs_info()
        if self.saves[WHOLE_IMAGE_SAVE]:
            data = self.current_abs_result.get_absorption_spec()
            self.__save_absorption_spec_graph(data, "ABSORPTION_SPEC_WHOLE_IMAGE" + name,
                                              self.saves[ABSORPTION_SPEC_IMAGE],
                                              self.saves[ABSORPTION_SPEC_IMAGE_WO_SCALE])
        if self.saves[MASKED_IMAGE_SAVE]:
            data = self.current_abs_result.get_absorption_spec_masked()
            self.__save_absorption_spec_graph(data, "ABSORPTION_SPEC_MASKED_IMAGE" + name,
                                              self.saves[ABSORPTION_SPEC_IMAGE],
                                              self.saves[ABSORPTION_SPEC_IMAGE_WO_SCALE])
        if self.saves[ABSORPTION_SPEC_EXCEL]:
            data = self.current_abs_result.get_absorption_spec()
            self.__save_data(data, "ABSORPTION_SPEC_EXCEL" + name, fmt="%.5f")

    # Saving helpers
    def __save_data(self, data, title, fmt=".csv", formatting="%.2f"):
        output_path = self.current_output_path + "/" + title + fmt
        logging.debug("SAVING DATA TO " + output_path)
        np.savetxt(self.current_output_path + "/" + title + fmt, data, delimiter=",", fmt=formatting)

    def __save_image(self, data, title, is_image_with_scale, is_image_wo_scale, cmap='jet', fmt=".png", vmin=0,
                     vmax=1):
        if is_image_with_scale:
            self.__save_image_diagram(data, title, True, cmap, fmt, vmin, vmax)
        if is_image_wo_scale:
            self.__save_image_diagram(data, title, False, cmap, fmt, vmin, vmax)

    def __save_image_diagram(self, data, title, scale, cmap, fmt=".png", vmin=None, vmax=None):
        if scale:
            title += '_WITH_SCALE'
        else:
            title += '_WO_SCALE'
        output_path = self.current_output_path + "/" + title + fmt
        logging.debug("SAVING IMAGE TO " + output_path)
        if scale:
            plt.imshow(np.flipud(data[:, :].T), cmap=cmap, vmin=vmin, vmax=vmax)
            plt.colorbar()
            plt.title(title)
            plt.savefig(output_path)
        else:
            plt.imsave(output_path, np.flipud(data[:, :].T), cmap=cmap, vmin=vmin, vmax=vmax)
        plt.clf()

    def __save_histogram_graph(self, data, title, is_hist_with_scale, is_hist_wo_scale, fmt=".png", min_val=0,
                               max_val=1):
        step_size = self.listener.modules[HISTOGRAM].get_step_size()
        if is_hist_with_scale:
            self.__save_histogram_diagram(data, title + "_WITH_SCALE", True, fmt=fmt, step_size_value=step_size)
        if is_hist_wo_scale:
            self.__save_histogram_diagram(data, title + "_WO_SCALE", False, fmt=fmt, step_size_value=step_size)

    def __save_histogram_diagram(self, data, title, scale, fmt=".png", step_size_value=0.01):
        if scale:
            title += '_WITH_SCALE'
        else:
            title += '_WO_SCALE'
        output_path = self.current_output_path + "/" + title + fmt
        logging.debug("SAVING HISTOGRAM TO " + output_path)
        plt.clf()
        axes = plt.subplot(111)
        # calc bins
        start = np.min(data)
        stop = np.max(data) + step_size_value
        step = step_size_value
        bins = np.arange(start=start, stop=stop, step=step)
        # plot histogram
        axes.hist(data, bins=bins, align='left')
        # plot boxplot
        axes2 = axes.twinx()
        axes2.boxplot(data, vert=False, sym='')
        axes2.get_yaxis().set_visible(False)
        # set axes
        if scale:
            axes.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
            plt.title(title)
        else:
            axes.set_yticklabels([])
            axes.set_xticklabels([])
            plt.axis('off')
        plt.savefig(output_path)
        plt.clf()

    def __save_absorption_spec_graph(self, data, title, is_abspc_with_scale, is_abspc_wo_scale,
                                     fmt=".png", min_val=0, max_val=1):
        if is_abspc_with_scale:
            self.__save_absorption_spec_diagram(data, title, True, fmt=fmt)
        if is_abspc_wo_scale:
            self.__save_absorption_spec_diagram(data, title, False, fmt=fmt)

    def __save_absorption_spec_diagram(self, data, title, scale, fmt=".png"):
        if scale:
            title += '_WITH_SCALE'
        else:
            title += '_WO_SCALE'
        output_path = self.current_output_path + "/" + title + fmt
        logging.debug("SAVING ABSORPTION SPEC" + output_path)
        plt.clf()
        axes = plt.subplot(111)
        x_vals = np.arange(500, 1000, 5)
        # plot absorption spec
        axes.plot(x_vals, data, '-', lw=0.5)
        axes.grid(linestyle=':', linewidth=0.5)
        if scale:
            plt.title(title)
        else:
            plt.axis('off')
        plt.savefig(output_path)
        plt.clf()
