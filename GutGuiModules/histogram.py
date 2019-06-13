class Histogram:
    def __init__(self, absorption_spec_frame):
        self.root = absorption_spec_frame

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
        self.step_size_value = None

        self.save_label = None
        self.save_checkbox = None
        self.save_checkbox_value = None
        self.save_wo_scale_label = None
        self.save_wo_scale_checkbox = None
        self.save_wo_scale_checkbox_value = None
        self.save_as_excel_label = None
        self.save_as_excel_checkbox = None
        self.save_as_excel_checkbox_value = None

        self.interactive_histogram = None

    #   TODO: IS THIS INTERACTIVE?
        self.maximum_box = None
        self.minimum_box = None
        self.selected_box = None

    # Helper
    def _init_widget(self):
        pass

    def _build_scale(self):
        pass

    def _build_step_size(self):
        pass

    def _build_save(self):
        pass

    def _build_save_wo_scale(self):
        pass

    def _build_save_as_excel(self):
        pass

    def _build_interactive_histogram(self):
        pass

    # Commands (Callbacks)
    def __update_scale_x_upper(self):
        pass

    def __update_scale_y_upper(self):
        pass

    def __update_scale_x_lower(self):
        pass

    def __update_scale_y_lower(self):
        pass

    def __update_save_checked(self):
        pass

    def __update_save_wo_scale_checked(self):
        pass

    def __update_save_as_excel_checked(self):
        pass

    def __update_interactive_histogram(self):
        pass