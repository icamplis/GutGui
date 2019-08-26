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

    def __save_image(self, data, name, is_image_with_scale, is_image_wo_scale, cmap='jet', fmt=".png"):
        if is_image_with_scale:
            title = name[0] + '_with-scale_' + name[1]
            self.__save_image_diagram(data.T, title, True, cmap, fmt)
        if is_image_wo_scale:
            title = name[0] + '_wo-scale_' + name[1]
            self.__save_image_diagram(data.T, title, False, cmap, fmt)

    def __save_image_diagram(self, data, title, scale, cmap, fmt=".png"):
        output_path = self.current_output_path + "/" + title + fmt
        logging.debug("SAVING IMAGE TO " + output_path)
        if scale:
            plt.imshow(np.flipud(data), cmap=cmap)
            plt.colorbar()
            plt.title(title)
            plt.savefig(output_path)
        else:
            plt.imsave(output_path, np.flipud(data), cmap=cmap)
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
        # mask
        mask = None
        if self.saves[MASKED_IMAGE_SAVE]:
            mask = np.logical_not(self.listener.get_mask())
        # cmap
        cmap = 'jet'
        if self.listener.modules[ORIGINAL_COLOUR].gs:
            cmap = 'gray'
        # save
        if self.saves[OG_RGB_DATA]:
            self.__save_og_rgb_image(cmap, mask)
        if self.saves[OG_STO2_DATA]:
            self.__save_og_sto2_image(cmap, mask)
        if self.saves[OG_NIR_DATA]:
            self.__save_og_nir_image(cmap, mask)
        if self.saves[OG_THI_DATA]:
            self.__save_og_thi_image(cmap, mask)
        if self.saves[OG_TWI_DATA]:
            self.__save_og_twi_image(cmap, mask)

    def __save_og_rgb_image(self, cmap, mask):
        if self.saves[WHOLE_IMAGE_SAVE]:
            title = self.listener.get_save_og_info('RGB', image=False) + '_whole'
            data = self.current_hist_result.get_rgb_og().T
            rgb = self.__convert_original_image(data)
            self.__save_data(np.flipud(rgb), title)

            if self.saves[OG_IMAGE]:
                title = self.listener.get_save_og_info('RGB', image=True)
                if cmap == 'jet':
                    self.__save_image_diagram(data, title + '_whole', False, cmap=cmap)
                else:
                    self.__save_image_diagram(rgb, title + '_whole', False, cmap=cmap)

        if self.saves[MASKED_IMAGE_SAVE]:
            title = self.listener.get_save_og_info('RGB', image=False) + '_masked'
            data = np.ma.array(self.current_hist_result.get_rgb_og().T, mask=np.array([mask.T] * 3).T)
            rgb = self.__convert_original_image(self.current_hist_result.get_rgb_og(), mask)
            self.__save_data(np.flipud(rgb), title)

            if self.saves[OG_IMAGE]:
                title = self.listener.get_save_og_info('RGB', image=True) + '_masked'
                if cmap == 'jet':
                    self.__save_image_diagram(data, title + '_masked', False, cmap=cmap)
                else:
                    self.__save_image_diagram(rgb, title + '_masked', False, cmap=cmap)

    def __save_og_sto2_image(self, cmap, mask):
        if self.saves[WHOLE_IMAGE_SAVE]:
            title = self.listener.get_save_og_info('STO2', image=False) + '_whole'
            data = self.current_hist_result.get_sto2_og()
            sto2 = self.__convert_original_image(data)
            self.__save_data(np.flipud(sto2), title)

            if self.saves[OG_IMAGE]:
                title = self.listener.get_save_og_info('STO2', image=True)
                if cmap == 'jet':
                    self.__save_image_diagram(data, title, False, cmap=cmap) + '_whole'
                else:
                    self.__save_image_diagram(sto2, title, False, cmap=cmap) + '_whole'

        if self.saves[MASKED_IMAGE_SAVE]:
            title = self.listener.get_save_og_info('STO2', image=False) + '_masked'
            data = np.ma.array(self.current_hist_result.get_sto2_og(), mask=np.array([mask.T] * 3).T)
            sto2 = self.__convert_original_image(self.current_hist_result.get_sto2_og(), mask)
            self.__save_data(np.flipud(sto2), title)

            if self.saves[OG_IMAGE]:
                title = self.listener.get_save_og_info('STO2', image=True) + '_masked'
                if cmap == 'jet':
                    self.__save_image_diagram(data, title, False, cmap=cmap) + '_whole'
                else:
                    self.__save_image_diagram(sto2, title, False, cmap=cmap) + '_whole'

    def __save_og_nir_image(self, cmap, mask):
        if self.saves[WHOLE_IMAGE_SAVE]:
            title = self.listener.get_save_og_info('NIR', image=False) + '_whole'
            data = self.current_hist_result.get_nir_og()
            nir = self.__convert_original_image(data)
            self.__save_data(np.flipud(nir), title)

            if self.saves[OG_IMAGE]:
                title = self.listener.get_save_og_info('NIR', image=True)
                if cmap == 'jet':
                    self.__save_image_diagram(data, title, False, cmap=cmap) + '_whole'
                else:
                    self.__save_image_diagram(nir, title, False, cmap=cmap) + '_whole'

        if self.saves[MASKED_IMAGE_SAVE]:
            title = self.listener.get_save_og_info('NIR', image=False) + '_masked'
            data = np.ma.array(self.current_hist_result.get_nir_og(), mask=np.array([mask.T] * 3).T)
            nir = self.__convert_original_image(self.current_hist_result.get_nir_og(), mask)
            self.__save_data(np.flipud(nir), title)

            if self.saves[OG_IMAGE]:
                title = self.listener.get_save_og_info('NIR', image=True) + '_masked'
                if cmap == 'jet':
                    self.__save_image_diagram(data, title, False, cmap=cmap) + '_whole'
                else:
                    self.__save_image_diagram(nir, title, False, cmap=cmap) + '_whole'

    def __save_og_thi_image(self, cmap, mask):
        if self.saves[WHOLE_IMAGE_SAVE]:
            title = self.listener.get_save_og_info('THI', image=False) + '_whole'
            data = self.current_hist_result.get_thi_og()
            thi = self.__convert_original_image(data)
            self.__save_data(np.flipud(thi), title)

            if self.saves[OG_IMAGE]:
                title = self.listener.get_save_og_info('THI', image=True)
                if cmap == 'jet':
                    self.__save_image_diagram(data, title, False, cmap=cmap) + '_whole'
                else:
                    self.__save_image_diagram(thi, title, False, cmap=cmap) + '_whole'

        if self.saves[MASKED_IMAGE_SAVE]:
            title = self.listener.get_save_og_info('THI', image=False) + '_masked'
            data = np.ma.array(self.current_hist_result.get_thi_og(), mask=np.array([mask.T] * 3).T)
            thi = self.__convert_original_image(self.current_hist_result.get_thi_og(), mask)
            self.__save_data(np.flipud(thi), title)

            if self.saves[OG_IMAGE]:
                title = self.listener.get_save_og_info('THI', image=True) + '_masked'
                if cmap == 'jet':
                    self.__save_image_diagram(data, title, False, cmap=cmap) + '_whole'
                else:
                    self.__save_image_diagram(thi, title, False, cmap=cmap) + '_whole'

    def __save_og_twi_image(self, cmap, mask):
        if self.saves[WHOLE_IMAGE_SAVE]:
            title = self.listener.get_save_og_info('TWI', image=False) + '_whole'
            data = self.current_hist_result.get_twi_og()
            twi = self.__convert_original_image(data)
            self.__save_data(np.flipud(twi), title)

            if self.saves[OG_IMAGE]:
                title = self.listener.get_save_og_info('TWI', image=True)
                if cmap == 'jet':
                    self.__save_image_diagram(data, title, False, cmap=cmap) + '_whole'
                else:
                    self.__save_image_diagram(twi, title, False, cmap=cmap) + '_whole'

        if self.saves[MASKED_IMAGE_SAVE]:
            title = self.listener.get_save_og_info('TWI', image=False) + '_masked'
            data = np.ma.array(self.current_hist_result.get_twi_og(), mask=np.array([mask.T] * 3).T)
            twi = self.__convert_original_image(self.current_hist_result.get_twi_og(), mask)
            self.__save_data(np.flipud(twi), title)

            if self.saves[OG_IMAGE]:
                title = self.listener.get_save_og_info('TWI', image=True) + '_masked'
                if cmap == 'jet':
                    self.__save_image_diagram(data, title, False, cmap=cmap) + '_whole'
                else:
                    self.__save_image_diagram(twi, title, False, cmap=cmap) + '_whole'

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
        if self.saves[WHOLE_IMAGE_SAVE]:
            data = self.current_hist_result.histogram_data.flatten()
            self.__save_histogram_graph(data, self.saves[HISTOGRAM_IMAGE], self.saves[HISTOGRAM_IMAGE_WO_SCALE],
                                        masked=False)
            if self.saves[HISTOGRAM_EXCEL]:
                data = self.current_hist_result.histogram_data.flatten()
                name = self.listener.get_save_hist_info(scale=True, image=False, masked=False,
                                                        path=self.current_result_key)
                self.__save_histogram_data(data, name, masked=False)

        if self.saves[MASKED_IMAGE_SAVE]:
            data = self.current_hist_result.histogram_data.flatten()
            self.__save_histogram_graph(data, self.saves[HISTOGRAM_IMAGE], self.saves[HISTOGRAM_IMAGE_WO_SCALE],
                                        masked=True)
            if self.saves[HISTOGRAM_EXCEL]:
                data = self.current_hist_result.histogram_data_masked.flatten()
                name = self.listener.get_save_hist_info(scale=True, image=False, masked=True,
                                                        path=self.current_result_key)
                self.__save_histogram_data(data, name, masked=True)

    def __save_histogram_data(self, data, name, masked):
        stats = self.listener.generate_hist_values_for_saving(masked, self.current_result_key)
        (x_low, x_high, y_low, y_high, step) = stats
        start = x_low
        stop = x_high + step
        bins = np.arange(start=start, stop=stop, step=step)
        counts, hist_bins, _ = plt.hist(data, bins=bins)
        counts = np.clip(counts, a_min=y_low, a_max=y_high)
        hist_data = np.stack((bins[:-1], counts)).T
        self.__save_data(hist_data, name, formatting="%.2f")

    def __save_histogram_graph(self, data, is_hist_with_scale, is_hist_wo_scale, masked, fmt=".png"):
        if is_hist_with_scale:
            name = self.listener.get_save_hist_info(scale=True, image=True, masked=masked,
                                                    path=self.current_result_key)
            self.__save_histogram_diagram(data, name, True, masked, fmt=fmt)
        if is_hist_wo_scale:
            name = self.listener.get_save_hist_info(scale=False, image=True, masked=masked,
                                                    path=self.current_result_key)
            self.__save_histogram_diagram(data, name, False, masked, fmt=fmt)

    def __save_histogram_diagram(self, data, title, scale, masked, fmt=".png"):
        output_path = self.current_output_path + "/" + title + fmt
        logging.debug("SAVING HISTOGRAM TO " + output_path)
        plt.clf()
        axes = plt.subplot(111)
        stats = self.listener.generate_hist_values_for_saving(masked, self.current_result_key)
        (x_low, x_high, y_low, y_high, step) = stats
        start = np.min(data)
        stop = np.max(data) + step
        bins = np.arange(start=start, stop=stop+step, step=step)
        # plot histogram
        axes.hist(data, bins=bins, align='left')
        if self.listener.modules[HISTOGRAM].parametric:
            # plot error bar
            mean_value = np.mean(data)
            sd_value = np.std(data)
            axes2 = axes.twinx()
            axes2.plot([mean_value-sd_value, mean_value+sd_value], [1, 1], 'k-', lw=1)
            axes2.plot([mean_value-sd_value, mean_value-sd_value], [0.9, 1.1], 'k-', lw=1)
            axes2.plot([mean_value+sd_value, mean_value+sd_value], [0.9, 1.1], 'k-', lw=1)
            axes2.plot([mean_value, mean_value], [0.9, 1.1], '#F17E3A', lw=1)
            axes2.set_ylim(bottom=0, top=2)
            axes2.get_yaxis().set_visible(False)
        elif self.listener.modules[HISTOGRAM].non_parametric:
            # plot boxplot
            axes2 = axes.twinx()
            axes2.boxplot(data, vert=False, sym='')
            axes2.get_yaxis().set_visible(False)
        # set axes
        axes.set_xlim(left=x_low, right=x_high)
        axes.set_ylim(bottom=y_low, top=y_high)
        # commas and non-scientific notation
        axes.ticklabel_format(style='plain')
        axes.get_yaxis().set_major_formatter(
            matplotlib.ticker.FuncFormatter(self.listener.modules[HISTOGRAM].format_axis))
        axes.get_xaxis().set_major_formatter(
            matplotlib.ticker.FuncFormatter(self.listener.modules[HISTOGRAM].format_axis))
        if scale:
            plt.title(title)
        else:
            plt.axis('off')
        plt.savefig(output_path)
        plt.clf()

    # ------------------------------------------------ ABSORPTION SPEC -----------------------------------------------

    def __save_absorption_spec(self):
        x_low = self.listener.modules[ABSORPTION_SPEC].x_lower_scale_value
        x_high = self.listener.modules[ABSORPTION_SPEC].x_upper_scale_value
        y_low = self.listener.modules[ABSORPTION_SPEC].y_lower_scale_value
        y_high = self.listener.modules[ABSORPTION_SPEC].y_upper_scale_value
        if self.saves[WHOLE_IMAGE_SAVE]:
            data = self.current_abs_result.absorption_roi[:, 1]
            self.__save_absorption_spec_graph(data, self.saves[ABSORPTION_SPEC_IMAGE],
                                              self.saves[ABSORPTION_SPEC_IMAGE_WO_SCALE], masked='_whole')
            if self.saves[ABSORPTION_SPEC_EXCEL]:
                data1 = np.arange(x_low//5 * 5, x_high//5 * 5 + 5, 5)
                data2 = self.current_abs_result.absorption_roi[:, 1][int((x_low-500)/5):int((x_high-500)/5) + 1]
                data2 = np.clip(data2, a_min=y_low, a_max=y_high)
                data = np.asarray([data1, data2]).T
                name = self.listener.get_save_abs_info(scale=True, image=False) + '_whole'
                self.__save_data(data, name, formatting="%.5f")
        if self.saves[MASKED_IMAGE_SAVE]:
            data = self.current_abs_result.absorption_roi_masked[:, 1]
            self.__save_absorption_spec_graph(data, self.saves[ABSORPTION_SPEC_IMAGE],
                                              self.saves[ABSORPTION_SPEC_IMAGE_WO_SCALE], masked='_masked')
            if self.saves[ABSORPTION_SPEC_EXCEL]:
                data1 = np.arange(x_low//5 * 5, x_high//5 * 5 + 5, 5)
                data2 = self.current_abs_result.absorption_roi[:, 1]
                data2 = np.clip(data2, a_min=y_low, a_max=y_high)
                data = np.asarray([data1, data2]).T
                name = self.listener.get_save_abs_info(scale=True, image=False) + '_masked'
                self.__save_data(data, name, formatting="%.5f")

    def __save_absorption_spec_graph(self, data, is_abspc_with_scale, is_abspc_wo_scale, masked, fmt=".png"):
        if is_abspc_with_scale:
            name = self.listener.get_save_abs_info(scale=True, image=True) + masked
            self.__save_absorption_spec_diagram(data, name, True, fmt=fmt)
        if is_abspc_wo_scale:
            name = self.listener.get_save_abs_info(scale=False, image=True) + masked
            self.__save_absorption_spec_diagram(data, name, False, fmt=fmt)

    def __save_absorption_spec_diagram(self, data, title, scale, fmt=".png"):
        output_path = self.current_output_path + "/" + title + fmt
        logging.debug("SAVING ABSORPTION SPEC" + output_path)
        plt.clf()
        axes = plt.subplot(111)
        x_vals = np.arange(500, 1000, 5)
        x_low = self.listener.modules[ABSORPTION_SPEC].x_lower_scale_value
        x_high = self.listener.modules[ABSORPTION_SPEC].x_upper_scale_value
        y_low = self.listener.modules[ABSORPTION_SPEC].y_lower_scale_value
        y_high = self.listener.modules[ABSORPTION_SPEC].y_upper_scale_value
        # plot absorption spec
        axes.plot(x_vals, data, '-', lw=0.5)
        axes.grid(linestyle=':', linewidth=0.5)
        axes.set_xlim(left=x_low, right=x_high)
        axes.set_ylim(bottom=y_low, top=y_high)
        axes.ticklabel_format(style='plain')
        axes.get_yaxis().set_major_formatter(
            matplotlib.ticker.FuncFormatter(self.listener.modules[ABSORPTION_SPEC].format_axis))
        axes.get_xaxis().set_major_formatter(
            matplotlib.ticker.FuncFormatter(self.listener.modules[ABSORPTION_SPEC].format_axis))
        if scale:
            plt.title(title)
        else:
            plt.axis('off')
        plt.savefig(output_path)
        plt.clf()

    # ------------------------------------------------ RECREATED IMAGE -----------------------------------------------

    def __save_recreated_image(self):
        # greyscale or original
        cmap = 'jet'
        if self.listener.modules[RECREATED_COLOUR].gs:
            cmap = 'gray'

        if self.saves[STO2_DATA]:
            self.__save_sto2_data_and_image(cmap)
        if self.saves[NIR_DATA]:
            self.__save_nir_data_and_image(cmap)
        if self.saves[THI_DATA]:
            self.__save_thi_data_and_image(cmap)
        if self.saves[TWI_DATA]:
            self.__save_twi_data_and_image(cmap)

    def __save_sto2_data_and_image(self, cmap):
        data_name = self.listener.get_save_rec_info('STO2', image=False)
        image_name = self.listener.get_save_rec_info('STO2', image=True)
        whole_image_name = (image_name[0], image_name[1] + '_whole')
        masked_image_name = (image_name[0], image_name[1] + '_masked')
        if self.saves[WHOLE_IMAGE_SAVE]:
            self.__save_data(self.current_rec_result.sto2, data_name)
            self.__save_image(self.current_rec_result.sto2, whole_image_name, self.saves[REC_IMAGE],
                              self.saves[REC_IMAGE_WO_SCALE], cmap=cmap)
        if self.saves[MASKED_IMAGE_SAVE]:
            self.__save_data(self.current_rec_result.sto2_masked, data_name + '_masked')
            self.__save_image(self.current_rec_result.sto2_masked, masked_image_name, self.saves[REC_IMAGE],
                              self.saves[REC_IMAGE_WO_SCALE], cmap=cmap)

    def __save_nir_data_and_image(self, cmap):
        data_name = self.listener.get_save_rec_info('NIR', image=False)
        image_name = self.listener.get_save_rec_info('NIR', image=True)
        whole_image_name = (image_name[0], image_name[1] + '_whole')
        masked_image_name = (image_name[0], image_name[1] + '_masked')
        if self.saves[WHOLE_IMAGE_SAVE]:
            self.__save_data(self.current_rec_result.nir, data_name)
            self.__save_image(self.current_rec_result.nir, whole_image_name, self.saves[REC_IMAGE],
                              self.saves[REC_IMAGE_WO_SCALE], cmap=cmap)
        if self.saves[MASKED_IMAGE_SAVE]:
            self.__save_data(self.current_rec_result.nir_masked, data_name + '_masked')
            self.__save_image(self.current_rec_result.nir_masked, masked_image_name,
                              self.saves[REC_IMAGE], self.saves[REC_IMAGE_WO_SCALE], cmap=cmap)

    def __save_twi_data_and_image(self, cmap):
        data_name = self.listener.get_save_rec_info('TWI', image=False)
        image_name = self.listener.get_save_rec_info('TWI', image=True)
        whole_image_name = (image_name[0], image_name[1] + '_whole')
        masked_image_name = (image_name[0], image_name[1] + '_masked')
        if self.saves[WHOLE_IMAGE_SAVE]:
            self.__save_data(self.current_rec_result.twi, data_name)
            self.__save_image(self.current_rec_result.twi, whole_image_name, self.saves[REC_IMAGE],
                              self.saves[REC_IMAGE_WO_SCALE], cmap=cmap)
        if self.saves[MASKED_IMAGE_SAVE]:
            self.__save_data(self.current_rec_result.twi_masked, data_name + '_masked')
            self.__save_image(self.current_rec_result.twi_masked, masked_image_name,
                              self.saves[REC_IMAGE], self.saves[REC_IMAGE_WO_SCALE], cmap=cmap)

    def __save_thi_data_and_image(self, cmap):
        data_name = self.listener.get_save_rec_info('THI', image=False)
        image_name = self.listener.get_save_rec_info('THI', image=True)
        whole_image_name = (image_name[0], image_name[1] + '_whole')
        masked_image_name = (image_name[0], image_name[1] + '_masked')
        if self.saves[WHOLE_IMAGE_SAVE]:
            self.__save_data(self.current_rec_result.thi, data_name)
            self.__save_image(self.current_rec_result.thi, whole_image_name, self.saves[REC_IMAGE],
                              self.saves[REC_IMAGE_WO_SCALE], cmap=cmap)
        if self.saves[MASKED_IMAGE_SAVE]:
            self.__save_data(self.current_rec_result.thi_masked, data_name + '_masked')
            self.__save_image(self.current_rec_result.thi_masked, masked_image_name,
                              self.saves[REC_IMAGE], self.saves[REC_IMAGE_WO_SCALE], cmap=cmap)

    # ---------------------------------------------------- NEW IMAGE -------------------------------------------------

    def __save_new_image(self):
        # greyscale or original
        cmap = 'jet'
        if self.listener.modules[NEW_COLOUR].gs:
            cmap = 'gray'

        if self.saves[WL_DATA]:
            self.__save_wl_data_and_image(cmap)
        if self.saves[IDX_DATA]:
            self.__save_idx_data_and_image(cmap)

    def __save_wl_data_and_image(self, cmap):
        data_name = self.listener.get_save_new_info('WL', image=False)
        image_name = self.listener.get_save_new_info('WL', image=True)
        whole_image_name = (image_name[0], image_name[1] + '_whole')
        masked_image_name = (image_name[0], image_name[1] + '_masked')
        if self.saves[WHOLE_IMAGE_SAVE]:
            self.__save_data(self.current_new_result.get_wl_data(), data_name)
            self.__save_image(self.current_new_result.get_wl_data(), whole_image_name, self.saves[NEW_IMAGE],
                              self.saves[NEW_IMAGE_WO_SCALE], cmap=cmap)
        if self.saves[MASKED_IMAGE_SAVE]:
            self.__save_data(self.current_new_result.get_wl_data_masked(), data_name + '_masked')
            self.__save_image(self.current_new_result.get_wl_data_masked(), masked_image_name,  self.saves[NEW_IMAGE],
                              self.saves[NEW_IMAGE_WO_SCALE], cmap=cmap)

    def __save_idx_data_and_image(self, cmap):
        data_name = self.listener.get_save_new_info('IDX', image=False)
        image_name = self.listener.get_save_new_info('IDX', image=True)
        whole_image_name = (image_name[0], image_name[1] + '_whole')
        masked_image_name = (image_name[0], image_name[1] + '_masked')
        if self.saves[WHOLE_IMAGE_SAVE]:
            self.__save_data(self.current_new_result.index, data_name)
            self.__save_image(self.current_new_result.index, whole_image_name, self.saves[NEW_IMAGE],
                              self.saves[NEW_IMAGE_WO_SCALE], cmap=cmap)
        if self.saves[MASKED_IMAGE_SAVE]:
            self.__save_data(self.current_new_result.index_masked, data_name + '_masked')
            self.__save_image(self.current_new_result.index_masked, masked_image_name, self.saves[NEW_IMAGE],
                              self.saves[NEW_IMAGE_WO_SCALE], cmap=cmap)
