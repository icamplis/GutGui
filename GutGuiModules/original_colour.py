class OGColour:
    def __init__(self, original_color_frame, listener):
        self.root = original_color_frame

        # Listener
        self.listener = listener

        self.rgb_label = None
        self.rgb_checkbox = None
        self.rgb_checkbox_value = None

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

        self.save_coords_label = None
        self.save_coords_checkbox = None
        self.save_coords_checkbox_value = None

        self.pt1_label = None
        self.pt1_checkbox = None
        self.pt1_checkbox_value = None

        self.pt2_label = None
        self.pt2_checkbox = None
        self.pt2_checkbox_value = None

        self.pt2_label = None
        self.pt2_checkbox = None
        self.pt2_checkbox_value = None

        self.pt3_label = None
        self.pt3_checkbox = None
        self.pt3_checkbox_value = None

        self.pt4_label = None
        self.pt4_checkbox = None
        self.pt4_checkbox_value = None

        self.pt5_label = None
        self.pt5_checkbox = None
        self.pt5_checkbox_value = None

        self.pt6_label = None
        self.pt6_checkbox = None
        self.pt6_checkbox_value = None

        self.pt7_label = None
        self.pt7_checkbox = None
        self.pt7_checkbox_value = None

        self.pt8_label = None
        self.pt8_checkbox = None
        self.pt8_checkbox_value = None

        self.original_image = None

    # Helper
    def _init_widget(self):
        pass

    def _build_rgb(self):
        pass

    def _build_sto2(self):
        pass

    def _build_nir(self):
        pass

    def _build_twi(self):
        pass

    def _build_thi(self):
        pass

    def _build_save_coords(self):
        pass

    def _build_pt1(self):
        pass

    def _build_pt2(self):
        pass

    def _build_pt3(self):
        pass

    def _build_pt4(self):
        pass

    def _build_pt5(self):
        pass

    def _build_pt6(self):
        pass

    def _build_pt7(self):
        pass

    def _build_pt8(self):
        pass

    def _build_recreated_image(self):
        pass

    # Commands (Callbacks)
    def __update_rgb_checked(self):
        pass

    def __update_sto2_checked(self):
        pass

    def __update_nir_checked(self):
        pass

    def __update_thi_checked(self):
        pass

    def __update_twi_checked(self):
        pass

    def __update_save_coords_checked(self):
        pass

    def __update_pt1_checked(self):
        pass

    def __update_pt2_checked(self):
        pass

    def __update_pt3_checked(self):
        pass

    def __update_pt4_checked(self):
        pass

    def __update_pt5_checked(self):
        pass

    def __update_pt6_checked(self):
        pass

    def __update_pt7_checked(self):
        pass

    def __update_pt8_checked(self):
        pass

    def __update_origina_image(self):
        pass