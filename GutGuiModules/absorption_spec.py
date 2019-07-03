from GutGuiModules.utility import *
import numpy as np

class AbsorptionSpec:
    def __init__(self, absorption_spec_frame, listener):
        self.root = absorption_spec_frame

        # Listener
        self.listener = listener

        self.x_vals = np.arange(500, 1000, 5) # [500, 505, 510, ... , 995, 1000]
        self.absorption_spec = []  # PLACEHOLDER before actual data is gained

        self.local_maximum_title = None
        self.local_maximum_text = None
        self.local_maximum_value = None
        self.local_minimum_title = None
        self.local_minimum_text = None
        self.local_minimum_value = None

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

        self.save_label = None
        self.save_checkbox = None
        self.save_checkbox_value = None
        self.save_wo_scale_label = None
        self.save_wo_scale_checkbox = None
        self.save_wo_scale_checkbox_value = None
        self.save_as_excel_label = None
        self.save_as_excel_checkbox = None
        self.save_as_excel_checkbox_value = None

        self.interactive_absorption_spec_graph = None
        self.axes = None
        self.interactive_absorption_spec = None

        self.upper_text = None
        self.upper_input = None
        self.upper_value = 995
        self.lower_text = None
        self.lower_input = None
        self.lower_value = 500

        self._init_widgets()

    def update_absorption_spec(self, absorption_spec_data):
        self.absorption_spec = absorption_spec_data[:, 1]
        self._build_interactive_absorption_spec()
        self._calc_extrema()

    # Helper
    def _init_widgets(self):
        self._build_scale()
        self._build_save()
        self._build_save_wo_scale()
        self._build_save_as_excel()
        self._build_interactive_absorption_spec()
        self._build_extrema()

    def _build_save(self):
        self.save_label = make_label(self.root, "Save", row=8, column=0, inner_padx=10, inner_pady=5, outer_padx=15, outer_pady=(0, 15))
        self.save_checkbox = make_checkbox(self.root, "", row=8, column=0, var=self.save_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0, outer_padx=(0, 13))
        self.save_checkbox.deselect()

    def _build_save_wo_scale(self):
        self.save_wo_scale_label = make_label(self.root, "Save W/O Scale", row=8, column=1, inner_padx=10, inner_pady=5, outer_padx=(5, 16), outer_pady=(0, 15), columnspan=2)
        self.save_wo_scale_checkbox = make_checkbox(self.root, "", row=8, column=2, var=self.save_wo_scale_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0, outer_padx=(0,25))
        self.save_wo_scale_checkbox.deselect()

    def _build_save_as_excel(self):
        self.save_as_excel_label = make_label(self.root, "Save as Excel", row=8, column=3,inner_padx=10, inner_pady=5, outer_padx=(5, 15), outer_pady=(0, 15))
        self.save_as_excel_checkbox = make_checkbox(self.root, "", row=8, column=3,var=self.save_as_excel_checkbox_value, sticky=NE,inner_padx=0, inner_pady=0, outer_padx=(0, 7))
        self.save_as_excel_checkbox.deselect()

    def _build_extrema(self):
        self.local_maximum_title = make_text(self.root, content="Local Max: ", bg=tkcolour_from_rgb(PASTEL_PINK_RGB), column=0, row=1, width=11, columnspan=1, pady=(0, 5), padx=(15, 5))
        self.local_maximum_text = make_text(self.root, content=str(self.local_maximum_value), bg=tkcolour_from_rgb(PASTEL_PINK_RGB), column=1, row=1, width=12, columnspan=1, pady=(0, 5), padx=(15,5), state=NORMAL)

        self.local_minimum_title= make_text(self.root, content="Local Min: ", bg=tkcolour_from_rgb(PASTEL_PINK_RGB), column=2, row=1, width=11, columnspan=1, pady=(0, 5), padx=5)
        self.local_minimum_text = make_text(self.root, content=str(self.local_minimum_value), bg=tkcolour_from_rgb(PASTEL_PINK_RGB), column=3, row=1, width=12, columnspan=1, pady=(0, 5), padx=5, state=NORMAL)

    def _build_scale(self):

        # lower
        self.lower_text = make_text(self.root, content="Lower: ", 
            bg=tkcolour_from_rgb(PASTEL_PINK_RGB), column=4, row=1, width=7, columnspan=1, pady=(0, 10))
        self.lower_input = make_entry(self.root, row=1, column=5, width=5, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.lower_input.bind('<Return>', self.__update_lower)
        self.lower_input.insert(END, self.lower_value)

        # upper
        self.upper_text = make_text(self.root, content="Upper: ", 
            bg=tkcolour_from_rgb(PASTEL_PINK_RGB), column=4, row=2, width=7, columnspan=1, pady=(0, 10))
        self.upper_input = make_entry(self.root, row=2, column=5, width=5, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.upper_input.bind('<Return>', self.__update_upper)
        self.upper_input.insert(END, self.upper_value)

        # x lower
        self.x_lower_scale_text = make_text(self.root, content="Min x val: ", bg=tkcolour_from_rgb(PASTEL_PINK_RGB), column=4, row=3, width=11, columnspan=1, pady=(0, 10))
        self.x_lower_scale_input = make_entry(self.root, row=3, column=5, width=5, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.x_lower_scale_input.bind('<Return>', self.__update_scale_x_lower)

        # x upper
        self.x_upper_scale_text = make_text(self.root, content="Max x val: ", bg=tkcolour_from_rgb(PASTEL_PINK_RGB), column=4, row=4, width=11, columnspan=1, pady=(0, 10))
        self.x_upper_scale_input = make_entry(self.root, row=4, column=5, width=5, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.x_upper_scale_input.bind('<Return>', self.__update_scale_x_upper)

        # y lower
        self.y_lower_scale_text = make_text(self.root, content="Min y val: ", bg=tkcolour_from_rgb(PASTEL_PINK_RGB), column=4, row=5, width=11, columnspan=1, pady=(0, 20))
        self.y_lower_scale_input = make_entry(self.root, row=5, column=5, width=5, pady=(0, 20), padx=(0, 15), columnspan=1, command=self.__update_scale_y_lower)
        self.y_lower_scale_input.bind('<Return>', self.__update_scale_y_lower)

        # y upper
        self.y_upper_scale_text = make_text(self.root, content="Max y val: ", bg=tkcolour_from_rgb(PASTEL_PINK_RGB), column=4, row=6, width=11, columnspan=1, pady=(0, 10))
        self.y_upper_scale_input = make_entry(self.root, row=6, column=5, width=5, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.y_upper_scale_input.bind('<Return>', self.__update_scale_y_upper)

    def _build_interactive_absorption_spec(self):
        # create canvas
        self.interactive_absorption_spec_graph = Figure(figsize=(3.5, 2))
        self.axes = self.interactive_absorption_spec_graph.add_subplot(111)
        self.interactive_absorption_spec_graph.patch.set_facecolor(rgb_to_rgba(PASTEL_PINK_RGB))
        # plot absorption spec
        # TODO: Need to build absorption spec according to notebook
        if len(self.absorption_spec) != 0:
            self.axes.plot(self.x_vals, self.absorption_spec, '-', lw=0.5)
            self.axes.grid(linestyle=':', linewidth='0.5')
        # set axes
        self.interactive_absorption_spec_graph.set_tight_layout(True)
        self.axes.set_xlim(left=self.x_lower_scale_value, right=self.x_upper_scale_value)
        self.axes.set_ylim(bottom=self.y_lower_scale_value, top=self.y_upper_scale_value)
        # draw figure
        self.interactive_absorption_spec = FigureCanvasTkAgg(self.interactive_absorption_spec_graph, master=self.root)
        self.interactive_absorption_spec.draw()
        self.interactive_absorption_spec.get_tk_widget().grid(column=0, row=2, columnspan=4, rowspan=6, ipady=5, ipadx=0)
        self.interactive_absorption_spec.get_tk_widget().bind('<Double-Button-1>', self.__pop_up_image)

    def _calc_extrema(self):
        abs_spec_list = self.absorption_spec.tolist()
        abs_range = abs_spec_list[int((self.lower_value-500)/5):int((self.upper_value-500)/5)]
        maximum = max(abs_range)
        maximum_x = abs_spec_list.index(maximum) * 5 + 500
        self.local_maximum_value = (maximum_x, round(maximum, 3))
        minimum = min(abs_range)
        minimum_x = abs_spec_list.index(minimum) * 5 + 500
        self.local_minimum_value = (minimum_x, round(minimum, 3))
        self._build_extrema()

    # Commands (Callbacks)
    def __update_upper(self, event):
        self.upper_value = int(self.upper_input.get())
        print(self.upper_value)
        self._calc_extrema()

    def __update_lower(self, event):
        self.lower_value = int(self.lower_input.get())
        print(self.lower_value)
        self._calc_extrema()

    def __update_scale_x_upper(self, event):
        self.x_upper_scale_value = float(self.x_upper_scale_input.get())
        self._build_interactive_absorption_spec()

    def __update_scale_y_upper(self, event):
        self.y_upper_scale_value = float(self.y_upper_scale_input.get())
        self._build_interactive_absorption_spec()

    def __update_scale_x_lower(self, event):
        self.x_lower_scale_value = float(self.x_lower_scale_input.get())
        self._build_interactive_absorption_spec()

    def __update_scale_y_lower(self, event):
        self.y_lower_scale_value = float(self.y_lower_scale_input.get())
        self._build_interactive_absorption_spec()

    def __pop_up_image(self, event):
        make_popup_image(self.interactive_absorption_spec_graph)
