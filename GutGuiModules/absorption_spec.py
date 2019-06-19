from GutGuiModules.utility import *

class AbsorptionSpec:
    def __init__(self, absorption_spec_frame):
        self.root = absorption_spec_frame
        self.x_vals = [1, 3, 3, 4, 5, 7, 7, 9] # x_vals
        self.y_vals = [43, 6, 34, 6, 9, 31, 3, 21] # y_vals

        self.x_upper_scale_text = None
        self.y_upper_scale_text = None
        self.x_lower_scale_text = None
        self.y_lower_scale_text = None
        self.x_upper_scale_input = None
        self.y_upper_scale_input = None
        self.x_lower_scale_input = None
        self.y_lower_scale_input = None
        self.x_upper_scale_value = 10
        self.y_upper_scale_value = 10
        self.x_lower_scale_value = 0
        self.y_lower_scale_value = 0

        self.save_label = None
        self.save_checkbox = None
        self.save_checkbox_value = None
        self.save_wo_scale_label = None
        self.save_wo_scale_checkbox = None
        self.save_wo_scale_checkbox_value = None
        self.save_as_excel_label = None
        self.save_as_excel_checkbox = None
        self.save_as_excel_checkbox_value = None

        self.interactive_absorption_spec = None

        self.maximum_text = None
        self.maximum_input = None
        self.minimum_text = None
        self.maximum_input = None
        self.selected_text = None
        self.selected_input = None

        self._init_widgets()

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
        self.maximum_input = make_entry(self.root, row=1, column=4, width=5, pady=(0, 10), padx=(0, 15),
                                        columnspan=1, command=self.__update_maximum)

        # minimum
        self.minimum_text = make_text(self.root, content="Minimum: ", 
            bg=tkcolour_from_rgb(PASTEL_PINK_RGB), column=3, row=2, width=9, columnspan=1, pady=(0, 10))
        self.minimum_input = make_entry(self.root, row=2, column=4, width=5, pady=(0, 10), padx=(0, 15),
                                        columnspan=1, command=self.__update_minimum)

        # selection
        self.selection_text = make_text(self.root, content="Selection: ", 
            bg=tkcolour_from_rgb(PASTEL_PINK_RGB), column=3, row=3, width=11, columnspan=1, pady=(0, 10))
        self.selection_input = make_entry(self.root, row=3, column=4, width=5, pady=(0, 10), padx=(0, 15),
                                          columnspan=1, command=self.__update_selected)

        # x upper
        self.x_upper_scale_text = make_text(self.root, content="Max x val: ", bg=tkcolour_from_rgb(PASTEL_PINK_RGB),
                                            column=3, row=4, width=11, columnspan=1, pady=(0, 10))
        self.x_upper_scale_input = make_entry(self.root, row=4, column=4, width=5, pady=(0, 10), padx=(0, 15),
                                              columnspan=1, command=self.__update_scale_x_upper)
        self.x_upper_scale_input.bind('<Return>', self.__update_scale_x_upper)

        # x lower
        self.x_lower_scale_text = make_text(self.root, content="Min x val: ", bg=tkcolour_from_rgb(PASTEL_PINK_RGB),
                                            column=3, row=5, width=11, columnspan=1, pady=(0, 10))
        self.x_lower_scale_input = make_entry(self.root, row=5, column=4, width=5, pady=(0, 10), padx=(0, 15),
                                              columnspan=1, command=self.__update_scale_x_lower)
        self.x_lower_scale_input.bind('<Return>', self.__update_scale_x_lower)

        # y upper
        self.y_upper_scale_text = make_text(self.root, content="Max y val: ", bg=tkcolour_from_rgb(PASTEL_PINK_RGB),
                                            column=3, row=6, width=11, columnspan=1, pady=(0, 10))
        self.y_upper_scale_input = make_entry(self.root, row=6, column=4, width=5, pady=(0, 10), padx=(0, 15),
                                              columnspan=1, command=self.__update_scale_y_upper)
        self.y_upper_scale_input.bind('<Return>', self.__update_scale_y_upper)

        # y lower
        self.y_lower_scale_text = make_text(self.root, content="Min y val: ", bg=tkcolour_from_rgb(PASTEL_PINK_RGB),
                                            column=3, row=7, width=11, columnspan=1, pady=(0, 15))
        self.y_lower_scale_input = make_entry(self.root, row=7, column=4, width=5, pady=(0, 15), padx=(0, 15),
                                              columnspan=1, command=self.__update_scale_y_lower)
        self.y_lower_scale_input.bind('<Return>', self.__update_scale_y_lower)

    def _build_interactive_absorption_spec(self):
        self.interactive_absorption_spec = make_graph(master=self.root, x_vals=self.x_vals, y_vals=self.y_vals,
                                                      x_upper=self.x_upper_scale_value, x_lower=self.x_lower_scale_value,
                                                      y_upper=self.y_upper_scale_value, y_lower=self.y_lower_scale_value,
                                                      row=1, column=0, x_size=3.5, y_size=2.5, colour=PASTEL_PINK_RGB,
                                                      inner_pady=5, rowspan=6, columnspan=3)

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

    def __update_interactive_absorption_spec(self):
        pass