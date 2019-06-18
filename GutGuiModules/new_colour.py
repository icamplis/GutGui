from GutGuiModules.utility import *

class NewColour:
    def __init__(self, new_color_frame):
        self.root = new_color_frame

        self.wl_button = None
        self.wl_checkbox = None
        self.wl_checkbox_value = None

        self.idx_button = None
        self.idx_checkbox = None
        self.idx_checkbox_value = None

        self.save_label = None
        self.save_checkbox = None
        self.save_checkbox_value = None

        self.save_wo_scale_label = None
        self.save_wo_scale_checkbox = None
        self.save_wo_scale_checkbox_value = None

        self.upper_scale_text = None
        self.lower_scale_text = None
        self.upper_scale_input = None
        self.lower_scale_input = None

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
                                     inner_padx=10, inner_pady=2, width=14)
        self.wl_checkbox = make_checkbox(self.root, "", row=1, column=0, columnspan=2,
                                           var=self.wl_checkbox_value, sticky=E, inner_padx=0, inner_pady=0)
        self.wl_checkbox.deselect()

    def _build_idx(self):
        self.idx_button = make_button(self.root, text="IDX", row=1, column=2,columnspan=2, command=self.__update_to_idx,
                                      inner_padx=10, inner_pady=2, width=14)
        self.idx_checkbox = make_checkbox(self.root, "", row=1, column=2, columnspan=2,
                                           var=self.idx_checkbox_value, sticky=E, inner_padx=0, inner_pady=0)
        self.idx_checkbox.deselect()

    def _build_save(self):
        pass

    def _build_save_wo_scale(self):
        pass

    def _build_upper_scale(self):
        pass

    def _build_lower_scale(self):
        pass

    def _build_new_image(self):
        pass

    # Commands (Callbacks)
    def __update_to_wl(self):
        pass

    def __update_to_idx(self):
        pass

    def __update_scale_upper(self):
        pass

    def __update_scale_lower(self):
        pass

    def __update_new_image(self):
        pass