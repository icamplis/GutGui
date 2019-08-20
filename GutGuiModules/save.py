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
            STO2_DATA: False,
            NIR_DATA: False,
            TWI_DATA: False,
            THI_DATA: False,
            OG_IMAGE: False,
            OG_RGB_DATA: False,
            OG_STO2_DATA: False,
            OG_NIR_DATA: False,
            OG_TWI_DATA: False,
            OG_THI_DATA: False,
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

    # ------------------------------------------------ INITIALIZATION ------------------------------------------------

    def update_saves(self, key, value):
        assert type(value) == bool
        self.saves[key] = value
        # print(self.saves)

    def _init_widgets(self):
        self._build_save_specific_button()
        self._build_save_all_button()
        self._build_info_label()

    # --------------------------------------------------- BUILDERS ---------------------------------------------------

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

    # --------------------------------------------------- CALLBACKS --------------------------------------------------

    def __info(self):
        info = self.listener.modules[INFO].save_info
        title = "Save Information"
        make_info(title=title, info=info)

    # ------------------------------------------------ SAVING CALLBACKS ----------------------------------------------

    def _save_specific(self):
        for path, _ in self.listener.results.items():
            selected_paths = self.listener.selected_paths
            if path in selected_paths:
                self._save_to_path(path)

    def _save_all(self):
        for path, _ in self.listener.results.items():
            self._save_to_path(path)

    def _save_to_path(self, path):
        self.current_result_key = path
        self.current_result_list = self.listener.get_result(self.current_result_key)

        self.current_hist_result = self.current_result_list[0]
        self.current_abs_result = self.current_result_list[1]
        self.current_rec_result = self.current_result_list[2]
        self.current_new_result = self.current_result_list[3]

        self.current_output_path = os.path.dirname(path)

        if self.saves[PT1] or self.saves[PT2] or self.saves[PT3] or \
                self.saves[PT4] or self.saves[PT5] or self.saves[PT6] or \
                self.saves[PT7] or self.saves[PT8] or self.saves[PT9] or \
                self.saves[PT10]:
            self.__save_points()

        if self.saves[OG_RGB_DATA] or self.saves[OG_STO2_DATA] or \
                self.saves[OG_NIR_DATA] or self.saves[OG_THI_DATA] or \
                self.saves[OG_TWI_DATA]:
            self.__save_original_image()

        if self.saves[HISTOGRAM_IMAGE] or \
                self.saves[HISTOGRAM_IMAGE_WO_SCALE] or \
                self.saves[HISTOGRAM_EXCEL]:
            self.__save_histogram()

        if self.saves[ABSORPTION_SPEC_IMAGE] or \
                self.saves[ABSORPTION_SPEC_IMAGE_WO_SCALE] or \
                self.saves[ABSORPTION_SPEC_EXCEL]:
            self.__save_absorption_spec()

        if self.saves[STO2_DATA] or self.saves[NIR_DATA] or \
                self.saves[TWI_DATA] or self.saves[THI_DATA]:
            self.__save_recreated_image()

        if self.saves[WL_DATA] or self.saves[IDX_DATA]:
            self.__save_new_image()

    # ------------------------------------------------- SAVING HELPERS -----------------------------------------------

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

    # ------------------------------------------------- ORIGINAL IMAGE -----------------------------------------------

    def __save_points(self):
        point_bools = [self.saves[PT1], self.saves[PT2], self.saves[PT3], self.saves[PT4], self.saves[PT5],
                       self.saves[PT6], self.saves[PT7], self.saves[PT8], self.saves[PT9], self.saves[PT10]]
        data = self.listener.get_coords(point_bools)
        self.__save_data(data, title="MASK_COORDINATES")

    def instant_save_points(self, data, title):
        for path, _ in self.listener.results.items():
            selected_paths = self.listener.selected_paths
            if path in selected_paths:
                output_path = os.path.dirname(path) + "/" + title + '.csv'
                logging.debug("SAVING DATA TO " + output_path)
                np.savetxt(output_path, data, delimiter=",", fmt="%.2f")

    def __save_original_image(self):
        # greyscale or original
        if self.listener.modules[ORIGINAL_COLOUR].gs:
            title = "_GS"
            cmap = 'gray'
        else:
            title = '_CS'
            cmap = 'jet'
        # mask
        mask = None
        if self.saves[MASKED_IMAGE_SAVE]:
            mask = np.logical_not(self.listener.get_mask())

        if self.saves[OG_RGB_DATA]:
            self.__save_og_rgb_image(title, cmap, mask)
        if self.saves[OG_STO2_DATA]:
            self.__save_og_sto2_image(title, cmap, mask)
        if self.saves[OG_NIR_DATA]:
            self.__save_og_nir_image(title, cmap, mask)
        if self.saves[OG_THI_DATA]:
            self.__save_og_thi_image(title, cmap, mask)
        if self.saves[OG_TWI_DATA]:
            self.__save_og_twi_image(title, cmap, mask)

    def __save_og_rgb_image(self, title, cmap, mask):
        if self.saves[WHOLE_IMAGE_SAVE]:
            rgb = self.__convert_original_image(self.current_hist_result.get_rgb_og())
            self.__save_data(np.flipud(rgb), "OG_RGB_DATA" + title)
            if self.saves[OG_IMAGE]:
                self.__save_image_diagram(rgb, "OG_RGB" + title, False, cmap=cmap)
        if self.saves[MASKED_IMAGE_SAVE]:
            rgb = self.__convert_original_image(self.current_hist_result.get_rgb_og(), mask)
            self.__save_data(np.flipud(rgb), "OG_RGB_DATA_MASKED" + title)
            if self.saves[OG_IMAGE]:
                self.__save_image_diagram(rgb, "OG_RGB" + title + "_MASKED", False, cmap=cmap)

    def __save_og_sto2_image(self, title, cmap, mask):
        if self.saves[WHOLE_IMAGE_SAVE]:
            sto2 = self.__convert_original_image(self.current_hist_result.get_sto2_og())
            self.__save_data(np.flipud(sto2), "OG_STO2_DATA" + title)
            if self.saves[OG_IMAGE]:
                self.__save_image_diagram(sto2, "STO2" + title, False, cmap=cmap)
        if self.saves[MASKED_IMAGE_SAVE]:
            sto2 = self.__convert_original_image(self.current_hist_result.get_sto2_og(), mask)
            self.__save_data(np.flipud(sto2), "OG_STO2_DATA_MASKED" + title)
            if self.saves[OG_IMAGE]:
                self.__save_image_diagram(sto2, "STO2" + title + "_MASKED", False, cmap=cmap)

    def __save_og_nir_image(self, title, cmap, mask):
        if self.saves[WHOLE_IMAGE_SAVE]:
            nir = self.__convert_original_image(self.current_hist_result.get_nir_og())
            self.__save_data(np.flipud(nir), "OG_NIR_DATA" + title)
            if self.saves[OG_IMAGE]:
                self.__save_image_diagram(nir, "NIR" + title, False, cmap=cmap)
        if self.saves[MASKED_IMAGE_SAVE]:
            nir = self.__convert_original_image(self.current_hist_result.get_nir_og(), mask)
            self.__save_data(np.flipud(nir), "OG_NIR_DATA_MASKED" + title)
            if self.saves[OG_IMAGE]:
                self.__save_image_diagram(nir, "NIR" + title + "_MASKED", False, cmap=cmap)

    def __save_og_thi_image(self, title, cmap, mask):
        if self.saves[WHOLE_IMAGE_SAVE]:
            thi = self.__convert_original_image(self.current_hist_result.get_thi_og())
            self.__save_data(np.flipud(thi), "OG_THI_DATA" + title)
            if self.saves[OG_IMAGE]:
                self.__save_image_diagram(thi, "THI" + title, False, cmap=cmap)
        if self.saves[MASKED_IMAGE_SAVE]:
            thi = self.__convert_original_image(self.current_hist_result.get_thi_og(), mask)
            self.__save_data(np.flipud(thi), "OG_THI_DATA_MASKED" + title)
            if self.saves[OG_IMAGE]:
                self.__save_image_diagram(thi, "THI" + title + "_MASKED", False, cmap=cmap)

    def __save_og_twi_image(self, title, cmap, mask):
        if self.saves[WHOLE_IMAGE_SAVE]:
            twi = self.__convert_original_image(self.current_hist_result.get_twi_og())
            self.__save_data(np.flipud(twi), "OG_TWI_DATA" + title)
            if self.saves[OG_IMAGE]:
                self.__save_image_diagram(twi, "TWI" + title, False, cmap=cmap)
        if self.saves[MASKED_IMAGE_SAVE]:
            twi = self.__convert_original_image(self.current_hist_result.get_twi_og(), mask)
            self.__save_data(np.flipud(twi), "OG_TWI_DATA_MASKED" + title)
            if self.saves[OG_IMAGE]:
                self.__save_image_diagram(twi, "TWI" + title + "_MASKED", False, cmap=cmap)

    @staticmethod
    def __convert_original_image(array, mask=None):
        if mask is None:
            mask = []
        if len(mask) == 0:
            return np.flipud(np.asarray(rgb_image_to_hsi_array(array)).reshape((480, 640))).T
        else:
            return np.ma.array(np.flipud(skimage.color.rgb2gray(array)).T, mask=mask)

    # ---------------------------------------------------- HISTOGRAM -------------------------------------------------

    def __save_histogram(self):
        name = self.listener.get_current_hist_abs_info(hist_or_abs='hist')
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
            step = self.listener.modules[HISTOGRAM].step_size_value
            stop = np.max(data) + step
            bins = np.arange(start=start, stop=stop, step=step)
            counts, _, _ = plt.hist(data, bins=bins)
            hist_data = np.stack((bins[1:], counts)).T
            self.__save_data(hist_data, "HISTOGRAM_EXCEL" + name, fmt="%.2f")  # too slow to save it as an actual xlsx

    def __save_histogram_graph(self, data, title, is_hist_with_scale, is_hist_wo_scale, fmt=".png", min_val=0,
                               max_val=1):
        step_size = self.listener.modules[HISTOGRAM].step_size_value
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

    # ------------------------------------------------ ABSORPTION SPEC -----------------------------------------------

    def __save_absorption_spec(self):
        name = self.listener.get_current_hist_abs_info(hist_or_abs='abs')
        if self.saves[WHOLE_IMAGE_SAVE]:
            data = self.current_abs_result.absorption_roi[:, 1]
            self.__save_absorption_spec_graph(data, "ABSORPTION_SPEC_WHOLE_IMAGE" + name,
                                              self.saves[ABSORPTION_SPEC_IMAGE],
                                              self.saves[ABSORPTION_SPEC_IMAGE_WO_SCALE])
        if self.saves[MASKED_IMAGE_SAVE]:
            data = self.current_abs_result.absorption_roi_masked[:, 1]
            self.__save_absorption_spec_graph(data, "ABSORPTION_SPEC_MASKED_IMAGE" + name,
                                              self.saves[ABSORPTION_SPEC_IMAGE],
                                              self.saves[ABSORPTION_SPEC_IMAGE_WO_SCALE])
        if self.saves[ABSORPTION_SPEC_EXCEL]:
            data = self.current_abs_result.absorption_roi[:, 1]
            self.__save_data(data, "ABSORPTION_SPEC_EXCEL" + name, fmt="%.5f")

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

    # ------------------------------------------------ RECREATED IMAGE -----------------------------------------------

    def __save_recreated_image(self):
        # greyscale or original
        if self.listener.modules[RECREATED_COLOUR].gs:
            title = "_GS"
            cmap = 'gray'
        else:
            title = '_CS'
            cmap = 'jet'
        title += self.listener.get_current_rec_info(saves=True)

        if self.saves[STO2_DATA]:
            self.__save_sto2_data_and_image(title, cmap)
        if self.saves[NIR_DATA]:
            self.__save_nir_data_and_image(title, cmap)
        if self.saves[THI_DATA]:
            self.__save_thi_data_and_image(title, cmap)
        if self.saves[TWI_DATA]:
            self.__save_twi_data_and_image(title, cmap)

    def __save_sto2_data_and_image(self, title, cmap):
        if self.saves[WHOLE_IMAGE_SAVE]:
            self.__save_data(self.current_rec_result.sto2, "STO2_DATA" + title)
            self.__save_image(self.current_rec_result.sto2, "STO2_WHOLE_IMAGE" + title, self.saves[REC_IMAGE],
                              self.saves[REC_IMAGE_WO_SCALE], cmap=cmap)
        if self.saves[MASKED_IMAGE_SAVE]:
            self.__save_data(self.current_rec_result.sto2_masked, "STO2_DATA_MASKED" + title)
            self.__save_image(self.current_rec_result.sto2_masked, "STO2_MASKED_IMAGE" + title,
                              self.saves[REC_IMAGE], self.saves[REC_IMAGE_WO_SCALE], cmap=cmap)

    def __save_nir_data_and_image(self, title, cmap):
        if self.saves[WHOLE_IMAGE_SAVE]:
            self.__save_data(self.current_rec_result.nir, "NIR_DATA" + title)
            self.__save_image(self.current_rec_result.nir, "NIR_WHOLE_IMAGE" + title, self.saves[REC_IMAGE],
                              self.saves[REC_IMAGE_WO_SCALE], cmap=cmap)
        if self.saves[MASKED_IMAGE_SAVE]:
            self.__save_data(self.current_rec_result.nir_masked, "NIR_DATA_MASKED" + title)
            self.__save_image(self.current_rec_result.nir_masked, "NIR_MASKED_IMAGE" + title,
                              self.saves[REC_IMAGE], self.saves[REC_IMAGE_WO_SCALE], cmap=cmap)

    def __save_twi_data_and_image(self, title, cmap):
        if self.saves[WHOLE_IMAGE_SAVE]:
            self.__save_data(self.current_rec_result.twi, "TWI_DATA" + title)
            self.__save_image(self.current_rec_result.twi, "TWI_WHOLE_IMAGE" + title, self.saves[REC_IMAGE],
                              self.saves[REC_IMAGE_WO_SCALE], cmap=cmap)
        if self.saves[MASKED_IMAGE_SAVE]:
            self.__save_data(self.current_rec_result.twi_masked, "TWI_DATA_MASKED" + title)
            self.__save_image(self.current_rec_result.twi_masked, "TWI_MASKED_IMAGE" + title,
                              self.saves[REC_IMAGE], self.saves[REC_IMAGE_WO_SCALE], cmap=cmap)

    def __save_thi_data_and_image(self, title, cmap):
        if self.saves[WHOLE_IMAGE_SAVE]:
            self.__save_data(self.current_rec_result.thi, "THI_DATA" + title)
            self.__save_image(self.current_rec_result.thi, "THI_WHOLE_IMAGE" + title, self.saves[REC_IMAGE],
                              self.saves[REC_IMAGE_WO_SCALE], cmap=cmap)
        if self.saves[MASKED_IMAGE_SAVE]:
            self.__save_data(self.current_rec_result.thi_masked, "THI_DATA_MASKED" + title)
            self.__save_image(self.current_rec_result.thi_masked, "THI_MASKED_IMAGE" + title,
                              self.saves[REC_IMAGE], self.saves[REC_IMAGE_WO_SCALE], cmap=cmap)

    # ---------------------------------------------------- NEW IMAGE -------------------------------------------------

    def __save_new_image(self):
        # greyscale or original
        if self.listener.modules[NEW_COLOUR].gs:
            title = "_GS"
            cmap = 'gray'
        else:
            title = '_CS'
            cmap = 'jet'

        if self.saves[WL_DATA]:
            self.__save_wl_data_and_image(title, cmap)
        if self.saves[IDX_DATA]:
            self.__save_idx_data_and_image(title, cmap)

    def __save_wl_data_and_image(self, title, cmap):
        name = self.listener.get_current_new_info(mode='WL')
        if self.saves[WHOLE_IMAGE_SAVE]:
            self.__save_data(self.current_new_result.get_wl_data(), "WL_DATA" + title + name)
            self.__save_image(self.current_new_result.get_wl_data(), "WL_WHOLE_IMAGE" + title + name,
                              self.saves[NEW_IMAGE], self.saves[NEW_IMAGE_WO_SCALE], cmap=cmap)
        if self.saves[MASKED_IMAGE_SAVE]:
            self.__save_data(self.current_new_result.get_wl_data_masked(), "WL_DATA_MASKED" + title + name)
            self.__save_image(self.current_new_result.get_wl_data_masked(), "WL_MASKED_IMAGE" + title + name,
                              self.saves[NEW_IMAGE], self.saves[NEW_IMAGE_WO_SCALE], cmap=cmap)

    def __save_idx_data_and_image(self, title, cmap):
        name = self.listener.get_current_new_info(mode='IDX')
        if self.saves[WHOLE_IMAGE_SAVE]:
            self.__save_data(self.current_new_result.index, "IDX_DATA" + title + name)
            self.__save_image(self.current_new_result.index, "IDX_WHOLE_IMAGE" + title + name,
                              self.saves[NEW_IMAGE], self.saves[NEW_IMAGE_WO_SCALE], cmap=cmap)
        if self.saves[MASKED_IMAGE_SAVE]:
            self.__save_data(self.current_new_result.index_masked, "IDX_DATA_MASKED" + title + name)
            self.__save_image(self.current_new_result.index_masked, "IDX_MASKED_IMAGE" + title + name,
                              self.saves[NEW_IMAGE], self.saves[NEW_IMAGE_WO_SCALE], cmap=cmap)
