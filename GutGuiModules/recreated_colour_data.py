from GutGuiModules.utility import *
import logging

class RecreatedColourData:
    def __init__(self, recreated_color_data_frame, listener):
        self.root = recreated_color_data_frame

        # Listener
        self.listener = listener

        self.data = None
        self.stats_data = None

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

        self.info_label = None

        self._init_widget()

    def update_recreated_image_data(self, recreated_colour_image_data):
        data = recreated_colour_image_data.flatten()
        self.stats_data = [i for i in data if i != '--']
        self._calc_data()
        self._build_data()

    # Helper
    def _init_widget(self):
        self._build_data()
        self._build_info_label()

    def _calc_data(self):
        self.mean_value = np.round(np.ma.mean(self.stats_data), 3)
        self.sd_value = np.round(np.ma.std(self.stats_data), 3)
        self.median_value = np.round(np.ma.median(self.stats_data), 3)
        self.iqr_value = (np.round(np.quantile(self.stats_data, 0.25), 3), round(np.quantile(self.stats_data, 0.75), 3))
        self.min_value = np.round(np.min(self.stats_data), 3)
        self.max_value = np.round(np.max(self.stats_data), 3)

    def _build_data(self):
        # mean
        self.mean_text = make_text(self.root, content="Mean = " + str(self.mean_value), bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB), column=0, row=1, width=13, columnspan=1, padx=(15, 15), state=NORMAL)
        # standard deviation
        self.sd_text = make_text(self.root, content="SD = " + str(self.sd_value), bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB), column=0, row=2, width=11, columnspan=1, padx=0, state=NORMAL)
        # median
        self.median_text = make_text(self.root, content="Median = " + str(self.median_value), bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB), column=0, row=3, width=15, columnspan=1, padx=(15, 15), state=NORMAL)
        # IQR
        self.iqr_text = make_text(self.root, content="IQR = " + str(self.iqr_value), bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB), column=0, row=4, width=6+len(str(self.iqr_value)), columnspan=1, padx=(15, 15), state=NORMAL)
        # min
        self.min_text = make_text(self.root, content="Min = " + str(self.min_value), bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB), column=0, row=5, width=12, columnspan=1, padx=(15, 15), state=NORMAL)
        # max
        self.max_text = make_text(self.root, content="Max = " + str(self.max_value), bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB), column=0, row=6, width=12, columnspan=1, padx=(15, 15), pady=(0, 15), state=NORMAL)

    def _build_info_label(self):
        self.info_label = make_label_button(self.root, text='Recreated Colour Data', command=None, width=16)
