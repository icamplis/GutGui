from GutGuiModules.utility import *
import logging

class OGColourData:
    def __init__(self, original_color_data_frame, listener):
        self.root = original_color_data_frame

        # Listener
        self.listener = listener

        self.data = None

        self.mean_text = None
        self.mean_value = None
        self.sd_text = None
        self.sd_value = None
        self.median_text = None
        self.median_value = None
        self.iqr_text = None
        self.iqr_value = None
        self.min_text = None
        self.min_value = None
        self.max_text = None
        self.max_value = None

        self._init_widget()

    def update_original_image_data(self, original_colour_image_data):
        self.data = original_colour_image_data
        self._build_data()

    # Helper
    def _init_widget(self):
        self._build_data()

    def _build_data(self):
        # mean
        pass
