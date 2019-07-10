from GutGuiModules.utility import *
import logging

class NewColourData:
    def __init__(self, new_color_data_frame, listener):
        self.root = new_color_data_frame

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

    def update_new_image_data(self, new_colour_image_data):
        self.data = new_colour_image_data
        self._calc_data()
        self._build_data()

    # Helper
    def _init_widget(self):
        self._build_data()

    def _calc_data(self):
        self.mean_value = None
        self.sd_value = None
        self.median_value = None
        self.iqr_value = None
        self.min_value = None
        self.max_value = None

    def _build_data(self):
        # mean
        self.mean_text = make_text(self.root, content="Mean = " + str(self.mean_value), bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), column=0, row=1, width=12, columnspan=1, padx=0, state=NORMAL)
        # standard deviation
        self.sd_text = make_text(self.root, content="SD = " + str(self.sd_value), bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), column=0, row=2, width=10, columnspan=1, padx=0, state=NORMAL)
        # median
        self.median_text = make_text(self.root, content="Median = " + str(self.median_value), bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), column=0, row=3, width=14, columnspan=1, padx=0, state=NORMAL)
        # IQR
        self.iqr_text = make_text(self.root, content="IQR = " + str(self.iqr_value), bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), column=0, row=4, width=20, columnspan=1, padx=0, state=NORMAL)
        # min
        self.min_text = make_text(self.root, content="Min = " + str(self.min_value), bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), column=0, row=5, width=11, columnspan=1, padx=0, state=NORMAL)
        # max
        self.max_text = make_text(self.root, content="Max = " + str(self.max_value), bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), column=0, row=6, width=11, columnspan=1, padx=0, pady=(0, 15), state=NORMAL)
