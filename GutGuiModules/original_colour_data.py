from GutGuiModules.utility import *
import logging

class OGColourData:
    def __init__(self, original_color_data_frame, listener):
        self.root = original_color_data_frame

        # Listener
        self.listener = listener

        self.stats_data = None

        # self.calc_button = None
        self.c1_button = None
        self.c2_button = None
        self.c1 = False
        self.c2 = False

        self.mean_text = None
        self.mean_value = ''
        self.sd_text = None
        self.sd_value = ''
        self.median_text = None
        self.median_value = ''
        self.iqr_text = None
        self.iqr_value = ''
        self.min_text = None
        self.min_value = ''
        self.max_text = None
        self.max_value = ''

        self.info_label = None

        self._init_widget()

    def update_calc(self):
        self.stats_data = self.listener.get_current_original_data()
        if self.c1:
            logging.debug("CONVERTING IMAGE TO JET...")
            self.stats_data = rgb_image_to_jet_array(self.stats_data)
        elif self.c2:
            logging.debug("CONVERTING IMAGE TO HSI...")
            self.stats_data = rgb_image_to_hsi_array(self.stats_data)
        logging.debug("CALCULATING IMAGE STATS...")
        self._calc_data()
        self._build_data()
        logging.debug("DONE W STATS...")

    # Helper
    def _init_widget(self):
        self._build_data()
        self._build_info_label()
        self._build_calc_button()

    def _calc_data(self):
        self.mean_value = np.round(np.ma.mean(self.stats_data), 3)
        self.sd_value = np.round(np.ma.std(self.stats_data), 3)
        self.median_value = np.round(np.ma.median(self.stats_data), 3)
        self.iqr_value = (np.round(np.quantile(self.stats_data, 0.25), 3), round(np.quantile(self.stats_data, 0.75), 3))
        self.min_value = np.round(np.ma.min(self.stats_data), 3)
        self.max_value = np.round(np.ma.max(self.stats_data), 3)

    def _build_data(self):
        # mean
        self.mean_text = make_text(self.root, content="Mean = " + str(self.mean_value), bg=tkcolour_from_rgb(BACKGROUND), column=0, row=1, width=22, columnspan=3, padx=(10, 15), state=NORMAL)
        # standard deviation
        self.sd_text = make_text(self.root, content="SD = " + str(self.sd_value), bg=tkcolour_from_rgb(BACKGROUND), column=0, row=2, width=22, columnspan=3, padx=(10, 15), state=NORMAL)
        # median
        self.median_text = make_text(self.root, content="Median = " + str(self.median_value), bg=tkcolour_from_rgb(BACKGROUND), column=0, row=3, width=22, columnspan=3, padx=(10, 15), state=NORMAL)
        # IQR
        self.iqr_text = make_text(self.root, content="IQR = " + str(self.iqr_value), bg=tkcolour_from_rgb(BACKGROUND), column=0, row=4, width=22, columnspan=3, padx=(10, 15), state=NORMAL)
        # min
        self.min_text = make_text(self.root, content="Min = " + str(self.min_value), bg=tkcolour_from_rgb(BACKGROUND), column=0, row=5, width=22, columnspan=3, padx=(10, 15), state=NORMAL)
        # max
        self.max_text = make_text(self.root, content="Max = " + str(self.max_value), bg=tkcolour_from_rgb(BACKGROUND), column=0, row=6, width=22, columnspan=3, padx=(10, 15), pady=(0, 15), state=NORMAL)

    def _build_calc_button(self):
        self.c1_button = make_button(self.root, text="C1", row=0, column=1, columnspan=1, command=self._update_c1, inner_padx=3, inner_pady=0, outer_padx=(10, 5), outer_pady=15, width=2)
        self.c2_button = make_button(self.root, text="C2", row=0, column=2, columnspan=1, command=self._update_c2, inner_padx=3, inner_pady=0, outer_padx=(0, 15), outer_pady=15, width=2)
        # self.calc_button = make_button(self.root, text="CALC", row=0, column=1, columnspan=1, command=self.update_calc, inner_padx=3, inner_pady=0, outer_padx=(10, 15), outer_pady=15, width=5)

    def _build_info_label(self):
        self.info_label = make_label_button(self.root, text='Original Data', command=self.__info, width=11)

    def _update_c1(self):
        self.c1 = True
        self.c2 = False
        self.update_calc()

    def _update_c2(self):
        self.c1 = False
        self.c2 = True
        self.update_calc()

    def __info(self):
        info = self.listener.get_original_data_info()
        title = "Original Data Information"
        make_info(title=title, info=info)
