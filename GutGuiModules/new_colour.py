from GutGuiModules.utility import *

class NewColour:
    def __init__(self, new_color_frame):
        self.root = new_color_frame

        self.wl_button = None
        self.wl_checkbox = None
        self.wl_checkbox_value = IntVar()

        self.idx_button = None
        self.idx_checkbox = None
        self.idx_checkbox_value = IntVar()

        self.save_label = None
        self.save_checkbox = None
        self.save_checkbox_value = IntVar()

        self.save_wo_scale_label = None
        self.save_wo_scale_checkbox = None
        self.save_wo_scale_checkbox_value = IntVar()

        self.upper_scale_text = None
        self.lower_scale_text = None
        self.upper_scale_input = None
        self.lower_scale_input = None

        self.displayed_image_mode = WL

        self.new_image = None

        self._init_widget()

    def get_wl_checkbox_value(self):
        return self.wl_checkbox_value

    def get_idx_checkbox_value(self):
        return self.idx_checkbox_value

    def get_save_checkbox_value(self):
        return self.save_checkbox_value

    def get_save_wo_scale_checkbox_value(self):
        return self.save_wo_scale_checkbox_value

    def get_upper_scale_input(self):
        return self.upper_scale_input.get()

    # Helper
    def _init_widget(self):
        self._build_wl()
        self._build_idx()
        self._build_save()
        self._build_save_wo_scale()
        self._build_upper_scale()
        self._build_lower_scale()
        self._build_new_image()

    def _build_wl(self):
        self.wl_button = make_button(self.root, text="WL", row=1, column=0, columnspan=2, command=self.__update_to_wl,
                                     inner_padx=10, inner_pady=2, width=10)
        self.wl_checkbox = make_checkbox(self.root, "", row=1, column=0, columnspan=2,
                                           var=self.wl_checkbox_value, sticky=E, inner_padx=0, inner_pady=0)
        self.wl_checkbox.deselect()

    def _build_idx(self):
        self.idx_button = make_button(self.root, text="IDX", row=1, column=2,columnspan=2, command=self.__update_to_idx,
                                      inner_padx=10, inner_pady=2, width=10)
        self.idx_checkbox = make_checkbox(self.root, "", row=1, column=2, columnspan=2,
                                           var=self.idx_checkbox_value, sticky=E, inner_padx=0, inner_pady=0)
        self.idx_checkbox.deselect()

    def _build_save(self):
        self.save_label = make_label(self.root, "Save", row=4, column=4)
        self.save_checkbox = make_checkbox(self.root, text="", row=4, column=4,
                                           var=self.save_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0)

    def _build_save_wo_scale(self):
        self.save_wo_scale_label = make_label(self.root, "Save W/O Scale", row=5, column=4, columnspan=3, wraplength=40)
        self.save_wo_scale_checkbox = make_checkbox(self.root, text="", row=5, column=4,
                                                    var=self.save_wo_scale_checkbox_value,
                                                    sticky=NE, inner_padx=0, inner_pady=0)

    def _build_upper_scale(self):
        self.upper_scale_text = make_label(self.root, "Upper Scale End", row=6, column=0, columnspan=3,
                                           inner_padx=30, inner_pady=10, outer_pady=5, outer_padx=15)
        self.upper_scale_input = make_entry(self.root, row=6, column=3, width=5)

    def _build_lower_scale(self):
        self.lower_scale_text = make_label(self.root, "Lower Scale End", row=7, column=0, columnspan=3,
                                           inner_padx=30, inner_pady=10, outer_pady=5, outer_padx=15)
        self.lower_scale_input = make_entry(self.root, row=7, column=3, width=5)

    def _build_new_image(self):
        self.new_image = make_label(self.root, "        new image placeholder",
                                          row=2, column=0, rowspan=4, columnspan=4,
                                          inner_pady=50, inner_padx=50, outer_padx=2)

    # Commands (Callbacks)
    def __update_to_wl(self):
        self.wl_button.config(foreground="red")
        self.idx_button.config(foreground="black")
        self.displayed_image_mode = WL

    def __update_to_idx(self):
        self.wl_button.config(foreground="black")
        self.idx_button.config(foreground="red")
        self.displayed_image_mode = IDX

    def __update_scale_upper(self):
        pass

    def __update_scale_lower(self):
        pass

    def __update_new_image(self):
        pass