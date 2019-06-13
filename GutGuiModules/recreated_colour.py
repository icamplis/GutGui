class RecColour:
    def __init__(self, recreated_color_frame):
        self.root = recreated_color_frame

        self.sto2_label = None
        self.sto2_checkbox = None
        self.sto2_checkbox_value = None

        self.nir_label = None
        self.nir_checkbox = None
        self.nir_checkbox_value = None

        self.thi_label = None
        self.thi_checkbox = None
        self.thi_checkbox_value = None

        self.twi_label = None
        self.twi_checkbox = None
        self.twi_checkbox_value = None

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
        self.upper_scale_value = None
        self.lower_scale_value = None

        self.recreated_image = None

    # Helper
    def _init_widget(self):
        pass

    def _build_sto2(self):
        pass

    def _build_nir(self):
        pass

    def _build_twi(self):
        pass

    def _build_thi(self):
        pass

    def _build_save(self):
        pass

    def _build_save_wo_scale(self):
        pass

    def _build_upper_scale(self):
        pass

    def _build_lower_scale(self):
        pass

    def _build_recreated_image(self):
        pass

    # Commands (Callbacks)
    def __update_sto2_checked(self):
        pass

    def __update_nir_checked(self):
        pass

    def __update_thi_checked(self):
        pass

    def __update_twi_checked(self):
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

    def __update_recreated_image(self):
        pass

