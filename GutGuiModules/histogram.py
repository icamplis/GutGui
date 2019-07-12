from GutGuiModules.utility import *
import numpy as np
from matplotlib.offsetbox import AnchoredText
import logging

class Histogram:
    def __init__(self, histogram_frame, listener):
        self.root = histogram_frame
        self.listener = listener

        self.flattened_data = None

        self.parametric_title = None
        self.mean_text = None
        self.mean_value = None
        self.sd_text = None
        self.sd_value = None
        self.non_parametric_title = None
        self.median_text = None
        self.median_value = None
        self.iqr_text = None
        self.iqr_value = None
        self.min_text = None
        self.min_bin = None
        self.min_bin_size = None
        self.max_text = None
        self.max_bin = None
        self.max_bin_size = None

        self.og_data_button = None
        self.wl_data_button = None
        self.idx_data_button = None

        self.x_upper_scale_text = None
        self.y_upper_scale_text = None
        self.x_lower_scale_text = None
        self.y_lower_scale_text = None
        self.x_upper_scale_input = None
        self.y_upper_scale_input = None
        self.x_lower_scale_input = None
        self.y_lower_scale_input = None
        self.x_upper_scale_value = None
        self.y_upper_scale_value = None
        self.x_lower_scale_value = None
        self.y_lower_scale_value = None

        self.step_size_text = None
        self.step_size_input = None
        self.step_size_value = 0.05 

        self.save_label = None
        self.save_checkbox = None
        self.save_checkbox_value = IntVar()
        self.save_wo_scale_label = None
        self.save_wo_scale_checkbox = None
        self.save_wo_scale_checkbox_value = IntVar()
        self.save_as_excel_label = None
        self.save_as_excel_checkbox = None
        self.save_as_excel_checkbox_value = IntVar()

        self.interactive_histogram_graph = None
        self.axes = None
        self.axes2 = None
        self.interactive_histogram = None

        self.upper_text = None
        self.upper_input = None
        self.upper_value = None
        self.lower_text = None
        self.lower_input = None
        self.lower_value = None

        self.info_button = None

        self._init_widgets()

    def get_save_checkbox_value(self):
        return not bool(self.save_checkbox_value.get())

    def get_save_wo_scale_checkbox_value(self):
        return not bool(self.save_wo_scale_checkbox_value.get())

    def get_save_as_excel_checkbox_value(self):
        return not bool(self.save_as_excel_checkbox_value.get())

    def update_histogram(self, data):
        logging.debug("BUILDING HISTOGRAM...")
        self.flattened_data = data.flatten()
        self.flattened_data = self.flattened_data[self.flattened_data != np.array(None)]
        self.upper_value = np.max(self.flattened_data)
        self.lower_value = np.min(self.flattened_data)
        self._calc_stats()
        self._build_scale()
        self._build_interactive_histogram()

    # Helper

    def _init_widgets(self):
        self._build_scale()
        self._build_step_size()
        self._build_save()
        self._build_save_wo_scale()
        self._build_save_as_excel()
        self._build_info_button()
        self._build_reset_button()
        self._build_data_buttons()
        self._build_interactive_histogram()
        self._build_stats()

    def _build_stats(self):
        # parametric
        self.parametric_title = make_text(self.root, content="P: ", 
            bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), column=0, row=1, width=3, columnspan=1, padx=(15, 0))
        # mean
        self.mean_text = make_text(self.root, content="Mean = " + str(self.mean_value), bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), column=1, row=1, width=12, columnspan=1, padx=0, state=NORMAL)
        # standard deviation
        self.sd_text = make_text(self.root, content="SD = " + str(self.sd_value), bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), column=2, row=1, width=10, columnspan=1, padx=0, state=NORMAL)
        # non parametric
        self.non_parametric_title = make_text(self.root, content="NP: ", bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), column=0, row=2, width=4, columnspan=1, padx=(15, 0))
        # median
        self.median_text = make_text(self.root, content="Median = " + str(self.median_value), bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), column=1, row=2, width=14, columnspan=1, padx=0, state=NORMAL)
        # IQR
        self.iqr_text = make_text(self.root, content="IQR = " + str(self.iqr_value), bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), column=2, row=2, width=20, columnspan=1, padx=(0, 10), state=NORMAL)
        # min and max
        self.min_text = make_text(self.root, content="Min bin = " + str(self.min_bin), bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), column=1, row=3, width=15, columnspan=1, padx=0, state=NORMAL)
        self.max_text = make_text(self.root, content="Max bin = " + str(self.max_bin), bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), column=2, row=3, width=15, columnspan=1, padx=0, state=NORMAL)

    def _build_data_buttons(self):
        self.og_data_button = make_button(self.root, text='Original Data', width=12, command=self.__update_to_original_data, row=1, column=3, columnspan=2, inner_padx=3, inner_pady=2, outer_pady=2, highlightthickness=0)
        self.wl_data_button = make_button(self.root, text='WL Data', width=12, command=self.__update_to_wl_data,  row=2, column=3, columnspan=2, inner_padx=3, inner_pady=2, outer_pady=2, highlightthickness=0)
        self.idx_data_button = make_button(self.root, text='IDX Data', width=12, command=self.__update_to_idx_data,  row=3, column=3, columnspan=2, inner_padx=3, inner_pady=2, outer_pady=(2, 10), highlightthickness=0)

    def _build_save(self):
        self.save_label = make_label(self.root, "Save", row=11, column=0,inner_padx=10, inner_pady=5, outer_padx=(15, 10), outer_pady=(0, 15))
        self.save_checkbox = make_checkbox(self.root, "", row=11, column=0, var=self.save_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0, outer_padx=(0, 5))
        self.save_checkbox.deselect()
        self.save_checkbox.bind('<Button-1>', self.__update_save_with_scale_check_status)

    def _build_save_wo_scale(self):
        self.save_wo_scale_label = make_label(self.root, "Save W/O Scale", row=11, column=1, inner_padx=10, inner_pady=5, outer_padx=(10, 16), outer_pady=(0, 15))
        self.save_wo_scale_checkbox = make_checkbox(self.root, "", row=11, column=1, var=self.save_wo_scale_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0, outer_padx=(0,12))
        self.save_wo_scale_checkbox.deselect()
        self.save_wo_scale_checkbox.bind('<Button-1>', self.__update_save_wo_scale_check_status)

    def _build_save_as_excel(self):
        self.save_as_excel_label = make_label(self.root, "Save as CSV", row=11, column=2, inner_padx=10, inner_pady=5, outer_padx=(5, 15), outer_pady=(0, 15))
        self.save_as_excel_checkbox = make_checkbox(self.root, "", row=11, column=2,var=self.save_as_excel_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0, outer_padx=(0, 9))
        self.save_as_excel_checkbox.deselect()
        self.save_as_excel_checkbox.bind('<Button-1>', self.__update_save_as_excel_check_status)

    def _build_reset_button(self):
        self.reset_button = make_button(self.root, "Reset", row=11, column=3, command=self.__reset, inner_padx=10, inner_pady=5, outer_padx=15, outer_pady=(0, 10), columnspan=2)

    def _build_scale(self):
        # lower
        self.lower_text = make_text(self.root, content="Lower: ", 
            bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), column=3, row=5, width=7, columnspan=1, pady=(0, 10))
        self.lower_input = make_entry(self.root, row=5, column=4, width=7, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.lower_input.bind('<Return>', self.__update_lower)
        self.lower_input.insert(END, str(self.lower_value))

        # upper
        self.upper_text = make_text(self.root, content="Upper: ", 
            bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), column=3, row=6, width=7, columnspan=1, pady=(0, 10))
        self.upper_input = make_entry(self.root, row=6, column=4, width=7, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.upper_input.bind('<Return>', self.__update_upper)
        self.upper_input.insert(END, str(self.upper_value))

        # x lower
        self.x_lower_scale_text = make_text(self.root, content="Min x: ", bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), column=3, row=7, width=7, columnspan=1, pady=(0, 10))
        self.x_lower_scale_input = make_entry(self.root, row=7, column=4, width=7, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.x_lower_scale_input.bind('<Return>', self.__update_scale_x_lower)
        self.x_lower_scale_input.insert(END, str(self.lower_value))

         # x upper
        self.x_upper_scale_text = make_text(self.root, content="Max x: ", bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), column=3, row=8, width=7, columnspan=1, pady=(0, 10))
        self.x_upper_scale_input = make_entry(self.root, row=8, column=4, width=7, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.x_upper_scale_input.bind('<Return>', self.__update_scale_x_upper)
        self.x_upper_scale_input.insert(END, str(self.upper_value))

        # y lower
        self.y_lower_scale_text = make_text(self.root, content="Min y: ", bg=tkcolour_from_rgb(PASTEL_BLUE_RGB),column=3, row=9, width=7, columnspan=1, pady=(0, 10))
        self.y_lower_scale_input = make_entry(self.root, row=9, column=4, width=7, pady=(0, 10), padx=(0, 15),columnspan=1)
        self.y_lower_scale_input.bind('<Return>', self.__update_scale_y_lower)
        self.y_lower_scale_input.insert(END, str(self.min_bin_size))

        # y upper
        self.y_upper_scale_text = make_text(self.root, content="Max y: ", bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), column=3, row=10, width=7, columnspan=1, pady=(0, 10))
        self.y_upper_scale_input = make_entry(self.root, row=10, column=4, width=7, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.y_upper_scale_input.bind('<Return>', self.__update_scale_y_upper)
        self.y_upper_scale_input.insert(END, str(self.max_bin_size))

    def _build_step_size(self):
        self.step_size_text = make_text(self.root, content="Step: ", 
            bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), column=3, row=4, width=6, columnspan=1, pady=(0, 10))
        self.step_size_input = make_entry(self.root, row=4, column=4, width=7, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.step_size_input.bind('<Return>', self.__update_step_size)
        self.step_size_input.insert(END, str(self.step_size_value))

    def _build_info_button(self):
        self.info_button = make_button(self.root, text='?', width=1, command=self.__info, row=0, column=4, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=5, outer_pady=5, highlightthickness=0)

    def _build_interactive_histogram(self):
        # create canvas
        self.interactive_histogram_graph = Figure(figsize=(3.5, 2))
        self.axes = self.interactive_histogram_graph.add_subplot(111)
        self.interactive_histogram_graph.patch.set_facecolor(rgb_to_rgba(PASTEL_BLUE_RGB))
        if self.flattened_data is not None:
            # calc bins
            bins = np.arange(start = np.min(self.flattened_data), stop = np.max(self.flattened_data) + self.step_size_value, step = self.step_size_value)
            # plot histogram
            self.axes.hist(self.flattened_data, bins=bins)
            # plot boxplot
            self.axes2 = self.axes.twinx()
            self.axes2.boxplot(self.flattened_data, vert=False, sym='')
            self.axes2.get_yaxis().set_visible(False)
            # set axes
            self.interactive_histogram_graph.set_tight_layout(True)
            self.axes.set_xlim(left=self.x_lower_scale_value, right=self.x_upper_scale_value)
            self.axes.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            self.axes.set_ylim(bottom=self.y_lower_scale_value, top=self.y_upper_scale_value)
        # draw figure
        self.interactive_histogram = FigureCanvasTkAgg(self.interactive_histogram_graph, master=self.root)
        self.interactive_histogram.draw()
        self.interactive_histogram.get_tk_widget().grid(column=0, row=4, columnspan=3, rowspan=7, ipady=5, ipadx=0, pady=(0, 15))
        self.interactive_histogram.get_tk_widget().bind('<Double-Button-1>', self.__pop_up_image)

    def _calc_stats(self):
        # construct data list in proper range
        logging.debug("CONSTRUCTING RANGED DATA...")
        data = self.flattened_data[self.lower_value <= self.flattened_data]
        data = data[data <= self.upper_value]
        # mean, sd, median, iqr
        logging.debug("CALCULATING STATS...")
        self.mean_value = np.round(np.mean(data), 3)
        self.sd_value = np.round(np.std(data), 3)
        self.median_value = np.round(np.ma.median(data), 3)
        self.iqr_value = (np.round(np.quantile(data, 0.25), 3), round(np.quantile(data, 0.75), 3))
        # generate bins
        bins = np.arange(start = self.lower_value, stop = self.upper_value + self.step_size_value, step = self.step_size_value)
        # generate numpy histogram data
        histogram_data = np.histogram(data, bins=bins)
        # determine the maximum bin size and which bin this occurs in
        self.max_bin_size = np.max(histogram_data[0])
        self.max_bin = histogram_data[1][np.where(histogram_data[0] == self.max_bin_size)[0][0]]
        # determine the minimum bin size and which bin this occurs in
        self.min_bin_size = np.min(np.histogram(data, bins=bins)[0])
        self.min_bin = histogram_data[1][np.where(histogram_data[0] == self.min_bin_size)[0][0]]
        self._build_stats()

    # Commands (Callbacks)
    def __update_to_original_data(self):
        self.listener._broadcast_to_histogram()

    def __update_to_wl_data(self):
        data = self.listener.get_wl()
        self.update_histogram(data)
        
    def __update_to_idx_data(self):
        data = self.listener.get_idx()
        self.update_histogram(data)

    def __reset(self):
        self.upper_value = np.max(self.flattened_data)
        self.lower_value = np.min(self.flattened_data)
        self._calc_stats()
        self._build_scale()
        self._build_interactive_histogram()

    def __info(self):
        info = self.listener.get_hist_info()
        title = "Histogram Information"
        make_info(title=title, info=info)

    def __update_upper(self):
        self.upper_value = float(self.upper_input.get())
        self._calc_stats()

    def __update_lower(self, event):
        self.lower_value = float(self.lower_input.get())
        self._calc_stats()

    def __update_scale_x_upper(self, event):
        self.x_upper_scale_value = float(self.x_upper_scale_input.get())
        self._build_interactive_histogram()

    def __update_scale_y_upper(self, event):
        self.y_upper_scale_value = float(self.y_upper_scale_input.get())
        self._build_interactive_histogram()

    def __update_scale_x_lower(self, event):
        self.x_lower_scale_value = float(self.x_lower_scale_input.get())
        self._build_interactive_histogram()

    def __update_scale_y_lower(self, event):
        self.y_lower_scale_value = float(self.y_lower_scale_input.get())
        self._build_interactive_histogram()

    def __update_step_size(self, event):
        self.step_size_value = float(self.step_size_input.get())
        self._build_interactive_histogram()

    def __pop_up_image(self, event):
        make_popup_image(self.interactive_histogram_graph)

    def __update_save_with_scale_check_status(self, event):
        value = self.get_save_checkbox_value()
        self.listener.update_saved(HISTOGRAM_IMAGE, value)

    def __update_save_wo_scale_check_status(self, event):
        value = self.get_save_wo_scale_checkbox_value()
        self.listener.update_saved(HISTOGRAM_IMAGE_WO_SCALE, value)

    def __update_save_as_excel_check_status(self, event):
        value = self.get_save_as_excel_checkbox_value()
        self.listener.update_saved(HISTOGRAM_EXCEL, value)