from GutGuiModules.utility import *

class NewColour:
    def __init__(self, new_color_frame, listener):
        self.root = new_color_frame

        # Listener
        self.listener = listener

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

        self.new_image = None

        self._init_widget()

        self.displayed_image_mode = WL
        self.wl_button.config(foreground="red")

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
        self.wl_button = make_button(self.root, text='WL', width=3, command=self.__update_to_wl, row=1, column=0, columnspan=2, inner_pady=5, outer_padx=(35, 0))
        self.wl_checkbox = make_checkbox(self.root, "", row=1, column=0, columnspan=2, var=self.wl_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0)
        self.wl_checkbox.deselect()

    def _build_idx(self):
        self.idx_button = make_button(self.root, text="IDX", width=3, row=1, column=2, columnspan=2, command=self.__update_to_idx, inner_pady=5)
        self.idx_checkbox = make_checkbox(self.root, "", row=1, column=2, columnspan=2,var=self.idx_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0, outer_padx=(0, 40))
        self.idx_checkbox.deselect()

    def _build_save(self):
        self.save_label = make_label(self.root, "Save", row=8, column=0, rowspan=2, outer_padx=(10, 0), outer_pady=(10, 0), inner_padx=10, inner_pady=5)
        self.save_checkbox = make_checkbox(self.root, text="", row=8, column=0,var=self.save_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0, outer_pady=(10, 0), outer_padx=(0, 5))

    def _build_save_wo_scale(self):
        self.save_wo_scale_label = make_label(self.root, "Save W/O Scale", row=8, column=2, columnspan=2, outer_padx=(0, 15), outer_pady=(10, 0), inner_padx=10, inner_pady=5)
        self.save_wo_scale_checkbox = make_checkbox(self.root, text="", row=8, column=3, var=self.save_wo_scale_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0, outer_pady=(10, 0), outer_padx=(0, 10))

    def _build_upper_scale(self):
        self.upper_scale_text = make_text(self.root, content="Upper Scale End: ", row=6, column=0, columnspan=3, width=17, bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB), pady=(5, 0), padx=(15, 0))
        self.upper_scale_input = make_entry(self.root, row=6, column=3, width=9, pady=(5,0), padx=(0,15))
        self.upper_scale_input.bind('<Return>', self.__update_scale_upper)

    def _build_lower_scale(self):
        self.lower_scale_text = make_text(self.root, content="Lower Scale End: ", row=7, column=0, columnspan=3, width=17, bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB), pady=5, padx=(15, 0))
        self.lower_scale_input = make_entry(self.root, row=7, column=3, width=9, pady=5, padx=(0,15))
        self.lower_scale_input.bind('<Return>', self.__update_scale_lower)

    def _build_new_image(self):
        self.new_image = make_label(self.root, "new image placeholder",row=2, column=0, rowspan=4, columnspan=4, inner_pady=50, inner_padx=50, outer_padx=15, outer_pady=(15, 10))

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
        # todo
        self._build_new_image()

    def __update_scale_lower(self):
        # todo
        self._build_new_image()
