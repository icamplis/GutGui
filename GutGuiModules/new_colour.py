from GutGuiModules.utility import *

class NewColour:
    def __init__(self, new_color_frame):
        self.root = new_color_frame

        self.wl_label = None
        self.wl_checkbox = None
        self.wl_checkbox_value = IntVar()

        self.idx_label = None
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
        self.upper_scale_value = None
        self.lower_scale_value = None

        self.new_image = None

    # Helper
    def _init_widget(self):
        pass

    def _build_wl(self):
        pass

    def _build_idx(self):
        pass

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
    def __update_wl_checked(self):
        pass

    def __update_idx_checked(self):
        pass

    def __update_save_wo_scale_checked(self):
        pass

    def __update_save_as_excel_checked(self):
        pass

    def __update_save_checked(self):
        pass

    def __update_scale_upper(self):
        pass

    def __update_scale_lower(self):
        pass

    def __update_new_image(self):
        pass