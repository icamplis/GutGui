from GutGuiModules.utility import *
import numpy as np

class AbsorptionSpec:
    def __init__(self, absorption_spec_frame, listener):
        self.root = absorption_spec_frame

        # Listener
        self.listener = listener

        self.x_vals = np.arange(500, 1000, 5) # [500, 505, 510, ... , 995, 1000]
        self.absorption_spec = range(100)  # PLACEHOLDER before actual data is gained

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
        self.interactve_absorption_spec = None

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

    def update_absorption_spec(self, absorption_spec_data):
        self.absorption_spec = absorption_spec_data[:, 1]
        self._build_interactive_absorption_spec()

    # Helper
    def _init_widgets(self):
        self._build_scale()
        self._build_save()
        self._build_save_wo_scale()
        self._build_save_as_excel()
        self._build_interactive_absorption_spec()

    def _build_save(self):
        self.save_label = make_label(self.root, "Save", row=7, column=0,
                                     inner_padx=10, inner_pady=5, outer_padx=15, outer_pady=(0, 15))
        self.save_checkbox = make_checkbox(self.root, "", row=7, column=0, var=self.save_checkbox_value, sticky=NE,
                                           inner_padx=0, inner_pady=0, outer_padx=(16, 10))
        self.save_checkbox.deselect()

    def _build_save_wo_scale(self):
        self.save_wo_scale_label = make_label(self.root, "Save W/O Scale", row=7, column=1, inner_padx=10, inner_pady=5,
                                              outer_padx=(5, 16), outer_pady=(0, 15))
        self.save_wo_scale_checkbox = make_checkbox(self.root, "", row=7, column=1,
                                                    var=self.save_wo_scale_checkbox_value, sticky=NE,
                                                    inner_padx=0, inner_pady=0, outer_padx=(0,11))
        self.save_wo_scale_checkbox.deselect()

    def _build_save_as_excel(self):
        self.save_as_excel_label = make_label(self.root, "Save as Excel", row=7, column=2,
                                              inner_padx=10, inner_pady=5, outer_padx=(5, 15), outer_pady=(0, 15))
        self.save_as_excel_checkbox = make_checkbox(self.root, "", row=7, column=2,
                                                    var=self.save_as_excel_checkbox_value, sticky=NE,
                                                    inner_padx=0, inner_pady=0, outer_padx=(0, 10))
        self.save_as_excel_checkbox.deselect()

    def _build_scale(self):
        # maximum
        self.maximum_text = make_text(self.root, content="Maximum: ", 
            bg=tkcolour_from_rgb(PASTEL_PINK_RGB), column=3, row=1, width=9, columnspan=1, pady=(0, 10))

        self.maximum_input = make_entry(self.root, row=1, column=4, width=5, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.maximum_input.bind('<Return>', self.__update_maximum)

        # minimum
        self.minimum_text = make_text(self.root, content="Minimum: ", 
            bg=tkcolour_from_rgb(PASTEL_PINK_RGB), column=3, row=2, width=9, columnspan=1, pady=(0, 10))

        self.minimum_input = make_entry(self.root, row=2, column=4, width=5, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.minimum_input.bind('<Return>', self.__update_minimum)

        # selection
        self.selection_text = make_text(self.root, content="Selection: ", 
            bg=tkcolour_from_rgb(PASTEL_PINK_RGB), column=3, row=3, width=11, columnspan=1, pady=(0, 10))

        self.selection_input = make_entry(self.root, row=3, column=4, width=5, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.selection_input.bind('<Return>', self.__update_selected)

        # x upper
        self.x_upper_scale_text = make_text(self.root, content="Max x val: ", bg=tkcolour_from_rgb(PASTEL_PINK_RGB), column=3, row=4, width=11, columnspan=1, pady=(0, 10))
        self.x_upper_scale_input = make_entry(self.root, row=4, column=4, width=5, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.x_upper_scale_input.bind('<Return>', self.__update_scale_x_upper)

        # x lower
        self.x_lower_scale_text = make_text(self.root, content="Min x val: ", bg=tkcolour_from_rgb(PASTEL_PINK_RGB), column=3, row=5, width=11, columnspan=1, pady=(0, 10))
        self.x_lower_scale_input = make_entry(self.root, row=5, column=4, width=5, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.x_lower_scale_input.bind('<Return>', self.__update_scale_x_lower)

        # y upper
        self.y_upper_scale_text = make_text(self.root, content="Max y val: ", bg=tkcolour_from_rgb(PASTEL_PINK_RGB), column=3, row=6, width=11, columnspan=1, pady=(0, 10))
        self.y_upper_scale_input = make_entry(self.root, row=6, column=4, width=5, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.y_upper_scale_input.bind('<Return>', self.__update_scale_y_upper)

        # y lower
        self.y_lower_scale_text = make_text(self.root, content="Min y val: ", bg=tkcolour_from_rgb(PASTEL_PINK_RGB), column=3, row=7, width=11, columnspan=1, pady=(0, 20))
        self.y_lower_scale_input = make_entry(self.root, row=7, column=4, width=5, pady=(0, 20), padx=(0, 15), columnspan=1, command=self.__update_scale_y_lower)
        self.y_lower_scale_input.bind('<Return>', self.__update_scale_y_lower)

    def _build_interactive_absorption_spec(self):
        # TODO: Need to build absorption spec according to notebook
        self.interactive_absorption_spec_graph = Figure(figsize=(3.5, 2.5))
        self.axes = self.interactive_absorption_spec_graph.add_subplot(111)
        self.axes.plot(self.x_vals, self.absorption_spec, '-', lw=0.5)
        self.interactive_absorption_spec_graph.patch.set_facecolor(rgb_to_rgba(PASTEL_PINK_RGB))
        self.interactive_absorption_spec_graph.set_tight_layout(True)
        self.axes.set_xlim(left=self.x_lower_scale_value, right=self.x_upper_scale_value)
        self.axes.set_ylim(bottom=self.y_lower_scale_value, top=self.y_upper_scale_value)
        self.interactve_absorption_spec = FigureCanvasTkAgg(self.interactive_absorption_spec_graph, master=self.root)
        self.interactve_absorption_spec.draw()
        self.interactve_absorption_spec.get_tk_widget().grid(column=0, row=1, columnspan=3, rowspan=6, ipady=5, ipadx=0)
        self.interactve_absorption_spec.get_tk_widget().bind('<Button-1>', self.__pop_up_image)

    # Commands (Callbacks)
    def __update_maximum(self):
        self.maximum_value = float(self.maximum_input.get())

    def __update_minimum(self, event):
        self.minimum_value = float(self.minimum_input.get())

    def __update_selected(self, event):
        self.selected_value = float(self.selected_input.get())

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
