from GutGuiModules.utility import *
import tkinter as tk
import numpy as np
from matplotlib.offsetbox import AnchoredText

class Histogram:
    def __init__(self, histogram_frame, listener):
        self.root = histogram_frame
        self.listener = listener

        self.flattened_data = None

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
        self.step_size_value = 1 # TODO: find a good starting stepsize value

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
        self.median = None
        self.median_text = None

        self.maximum_text = None
        self.maximum_input = None
        self.maximum_value = StringVar()
        self.minimum_text = None
        self.minimum_input = None
        self.minimum_value = StringVar()
        self.selected_text = None
        self.selected_input = None
        self.selectd_value = StringVar()

        self._init_widgets()

    def update_histogram(self, data):
        self.flattened_data = data.flatten()
        self._build_interactive_histogram()

    # Helper
    def _init_widgets(self):
        self._build_scale()
        self._build_step_size()
        self._build_save()
        self._build_save_wo_scale()
        self._build_save_as_excel()
        self._build_interactive_histogram()

    def _build_save(self):
        self.save_label = make_label(self.root, "Save", row=8, column=0,inner_padx=10, inner_pady=5, outer_padx=(15, 10), outer_pady=(0, 20))
        self.save_checkbox = make_checkbox(self.root, "", row=8, column=0, var=self.save_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0, outer_padx=(0, 5))
        self.save_checkbox.deselect()

    def _build_save_wo_scale(self):
        self.save_wo_scale_label = make_label(self.root, "Save W/O Scale", row=8, column=1, inner_padx=10, inner_pady=5, outer_padx=(10, 16), outer_pady=(0, 20))
        self.save_wo_scale_checkbox = make_checkbox(self.root, "", row=8, column=1, var=self.save_wo_scale_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0, outer_padx=(0,12))
        self.save_wo_scale_checkbox.deselect()

    def _build_save_as_excel(self):
        self.save_as_excel_label = make_label(self.root, "Save as Excel", row=8, column=2,inner_padx=10, inner_pady=5, outer_padx=(5, 15), outer_pady=(0, 20))
        self.save_as_excel_checkbox = make_checkbox(self.root, "", row=8, column=2,var=self.save_as_excel_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0, outer_padx=(0, 9))
        self.save_as_excel_checkbox.deselect()

    def _build_scale(self):
        # maximum
        self.maximum_text = make_text(self.root, content="Maximum: ", 
            bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), column=3, row=2, width=9, columnspan=1, pady=(0, 10))
        self.maximum_input = make_entry(self.root, row=2, column=4, width=5, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.maximum_input.bind('<Return>', self.__update_maximum)

        # minimum
        self.minimum_text = make_text(self.root, content="Minimum: ", 
            bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), column=3, row=3, width=9, columnspan=1, pady=(0, 10))
        self.minimum_input = make_entry(self.root, row=3, column=4, width=5, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.minimum_input.bind('<Return>', self.__update_minimum)

        # selection
        self.selection_text = make_text(self.root, content="Selection: ", 
            bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), column=3, row=4, width=11, columnspan=1, pady=(0, 10))
        self.selection_input = make_entry(self.root, row=4, column=4, width=5, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.selection_input.bind('<Return>', self.__update_selected)

        # x upper
        self.x_upper_scale_text = make_text(self.root, content="Max x val: ", bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), column=3, row=5, width=11, columnspan=1, pady=(0, 10))
        self.x_upper_scale_input = make_entry(self.root, row=5, column=4, width=5, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.x_upper_scale_input.bind('<Return>', self.__update_scale_x_upper)

        # x lower
        self.x_lower_scale_text = make_text(self.root, content="Min x val: ", bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), column=3, row=6, width=11, columnspan=1, pady=(0, 10))
        self.x_lower_scale_input = make_entry(self.root, row=6, column=4, width=5, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.x_lower_scale_input.bind('<Return>', self.__update_scale_x_lower)

        # y upper
        self.y_upper_scale_text = make_text(self.root, content="Max y val: ", bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), column=3, row=7, width=11, columnspan=1, pady=(0, 10))
        self.y_upper_scale_input = make_entry(self.root, row=7, column=4, width=5, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.y_upper_scale_input.bind('<Return>', self.__update_scale_y_upper)

        # y lower
        self.y_lower_scale_text = make_text(self.root, content="Min y val: ", bg=tkcolour_from_rgb(PASTEL_BLUE_RGB),column=3, row=8, width=11, columnspan=1, pady=(0, 20))
        self.y_lower_scale_input = make_entry(self.root, row=8, column=4, width=5, pady=(0, 20), padx=(0, 15),columnspan=1, command=self.__update_scale_y_lower)
        self.y_lower_scale_input.bind('<Return>', self.__update_scale_y_lower)

    def _build_step_size(self):
        self.step_size_text = make_text(self.root, content="Stepsize: ", 
            bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), column=3, row=1, width=10, columnspan=1, pady=(0, 10))
        self.step_size_input = make_entry(self.root, row=1, column=4, width=5, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.step_size_input.bind('<Return>', self.__update_step_size)

    def _build_interactive_histogram(self):
        # create canvas
        self.interactive_histogram_graph = Figure(figsize=(3.5, 2.5))
        self.axes = self.interactive_histogram_graph.add_subplot(111)
        self.interactive_histogram_graph.patch.set_facecolor(rgb_to_rgba(PASTEL_BLUE_RGB))
        if self.flattened_data != None:
            # calc bins
            bins = bins=range(min(self.flattened_data), max(self.flattened_data) + self.step_size_value, self.step_size_value)
            # plot histogram
            self.axes.hist(self.flattened_data, bins=bins, align='left')
            self.median = np.median(self.flattened_data)
            self.median_text = AnchoredText("Median = " + str(self.median), loc=1, frameon=False)
            self.axes.add_artist(self.median_text)
            # plot boxplot
            self.axes2 = self.axes.twinx()
            self.axes2.boxplot(self.flattened_data, vert=False, sym='')
            self.axes2.get_yaxis().set_visible(False)
            # set axes
            self.interactive_histogram_graph.set_tight_layout(True)
            self.axes.set_xlim(left=self.x_lower_scale_value, right=self.x_upper_scale_value)
            self.axes.set_ylim(bottom=self.y_lower_scale_value, top=self.y_upper_scale_value)
        # draw figure
        self.interactive_histogram = FigureCanvasTkAgg(self.interactive_histogram_graph, master=self.root)
        self.interactive_histogram.draw()
        self.interactive_histogram.get_tk_widget().grid(column=0, row=1, columnspan=3, rowspan=7, ipady=5, ipadx=0)
        self.interactive_histogram.get_tk_widget().bind('<Button-1>', self.__pop_up_image)

    # Commands (Callbacks)
    def __update_maximum(self):
        self.maximum_value = float(self.maximum_input.get())

    def __update_minimum(self, event):
        self.minimum_value = float(self.minimum_input.get())

    def __update_selected(self, event):
        self.selected_value = float(self.selected_input.get())

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
        self.step_size_value = int(self.step_size_input.get())
        self._build_interactive_histogram()

    def __pop_up_image(self, event):
        make_popup_image(self.interactive_histogram_graph)