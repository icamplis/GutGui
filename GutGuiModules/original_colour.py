from GutGuiModules.utility import *
import logging

class OGColour:
    def __init__(self, original_color_frame, listener):
        self.root = original_color_frame

        # Listener
        self.listener = listener

        self.coords_list = [None for i in range(8)]

        self.rgb_button = None
        self.rgb_checkbox = None
        self.rgb_checkbox_value = None

        self.sto2_button = None
        self.sto2_checkbox = None
        self.sto2_checkbox_value = None

        self.nir_button = None
        self.nir_checkbox = None
        self.nir_checkbox_value = None

        self.thi_button = None
        self.thi_checkbox = None
        self.thi_checkbox_value = None

        self.twi_button = None
        self.twi_checkbox = None
        self.twi_checkbox_value = None

        self.save_coords_label = None
        self.save_coords_checkbox = None
        self.save_coords_checkbox_value = None

        self.pt1_label = None
        self.pt1_value = None
        self.pt1_remove = None
        self.pt1_checkbox = None
        self.pt1_checkbox_value = None

        self.pt2_label = None
        self.pt2_value = None
        self.pt2_remove = None
        self.pt2_checkbox = None
        self.pt2_checkbox_value = None

        self.pt3_label = None
        self.pt3_value = None
        self.pt3_remove = None
        self.pt3_checkbox = None
        self.pt3_checkbox_value = None

        self.pt4_label = None
        self.pt4_value = None
        self.pt4_remove = None
        self.pt4_checkbox = None
        self.pt4_checkbox_value = None

        self.pt5_label = None
        self.pt5_value = None
        self.pt5_remove = None
        self.pt5_checkbox = None
        self.pt5_checkbox_value = None

        self.pt6_label = None
        self.pt6_value = None
        self.pt6_remove = None
        self.pt6_checkbox = None
        self.pt6_checkbox_value = None

        self.pt7_label = None
        self.pt7_value = None
        self.pt7_remove = None
        self.pt7_checkbox = None
        self.pt7_checkbox_value = None

        self.pt8_label = None
        self.pt8_value = None
        self.pt8_remove = None
        self.pt8_checkbox = None
        self.pt8_checkbox_value = None

        self.original_image_graph = None
        self.original_image_data = None
        self.original_image = None

        self._init_widget()

        self.displayed_image_mode = RGB  # RGB by default
        self.rgb_button.config(foreground="red")

    def get_mask(self):
        return None

    def update_original_image(self, original_image_data):
        self.original_image_data = original_image_data
        self._build_original_image()

    def get_displayed_image_mode(self):
        return self.displayed_image_mode

    def get_rgb_checkbox_value(self):
        return not bool(self.rgb_checkbox_value.get())

    def get_sto2_checkbox_value(self):
        return not bool(self.sto2_checkbox_value.get())

    def get_nir_checkbox_value(self):
        return not bool(self.nir_checkbox_value.get())

    def get_thi_checkbox_value(self):
        return not bool(self.thi_checkbox_value.get())

    def get_twi_checkbox_value(self):
        return not bool(self.twi_checkbox_value.get())

    def get_save_coords_checkbox_value(self):
        return not bool(self.save_coords_checkbox_value.get())

    def get_pt1_checkbox_value():
        return not bool(self.pt1_checkbox_value.get())

    def get_pt2_checkbox_value():
        return not bool(self.pt2_checkbox_value.get())

    def get_pt3_checkbox_value():
        return not bool(self.pt3_checkbox_value.get())

    def get_pt4_checkbox_value():
        return not bool(self.pt4_checkbox_value.get())

    def get_pt5_checkbox_value():
        return not bool(self.pt5_checkbox_value.get())

    def get_pt6_checkbox_value():
        return not bool(self.pt6_checkbox_value.get())

    def get_pt7_checkbox_value():
        return not bool(self.pt7_checkbox_value.get())
        
    def get_pt8_checkbox_value():
        return not bool(self.pt8_checkbox_value.get())

    # Helper
    def _init_widget(self):
        self._build_rgb()
        self._build_sto2()
        self._build_nir()
        self._build_thi()
        self._build_twi()
        self._build_original_image()
        self._build_pt1()
        self._build_pt2()
        self._build_pt3()
        self._build_pt4()
        self._build_pt5()
        self._build_pt6()
        self._build_pt7()
        self._build_pt8()
        self._build_save_coords()


    def _build_rgb(self):
        self.rgb_button = make_button(self.root, text='RGB', width=3, command=self.__update_to_rgb, row=1, column=0, columnspan=1, inner_pady=5, outer_padx=(15, 10))
        # self.rgb_checkbox = make_checkbox(self.root, "", row=1, column=0, columnspan=1, var=self.rgb_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0)
        # self.rgb_checkbox.deselect()
        # self.rgb_checkbox.bind('<Button-1>', self.__update_rgb_checked)

    def _build_sto2(self):
        self.sto2_button = make_button(self.root, text='StO2', width=4, command=self.__update_to_sto2, row=1, column=1, columnspan=1, inner_pady=5, outer_padx=(0, 10))
        # self.sto2_checkbox = make_checkbox(self.root, "", row=1, column=1, columnspan=1, var=self.sto2_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0)
        # self.sto2_checkbox.deselect()
        # self.sto2_checkbox.bind('<Button-1>', self.__update_sto2_checked)

    def _build_nir(self):
        self.nir_button = make_button(self.root, text='NIR', width=3, command=self.__update_to_nir, row=1, column=2, columnspan=1, inner_pady=5, outer_padx=(0, 10))
        # self.nir_checkbox = make_checkbox(self.root, "", row=1, column=2, columnspan=1, var=self.nir_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0)
        # self.nir_checkbox.deselect()
        # self.nir_checkbox.bind('<Button-1>', self.__update_nir_checked)

    def _build_thi(self):
        self.thi_button = make_button(self.root, text='THI', width=3, command=self.__update_to_thi, row=1, column=3, columnspan=1, inner_pady=5, outer_padx=(0, 10))
        # self.thi_checkbox = make_checkbox(self.root, "", row=1, column=3, columnspan=1, var=self.thi_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0)
        # self.thi_checkbox.deselect()
        # self.thi_checkbox.bind('<Button-1>', self.__update_thi_checked)

    def _build_twi(self):
        self.twi_button = make_button(self.root, text='TWI', width=3, command=self.__update_to_twi, row=1, column=4, columnspan=1, inner_pady=5, outer_padx=0)
        # self.twi_checkbox = make_checkbox(self.root, "", row=1, column=4, columnspan=1, var=self.twi_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0)
        # self.twi_checkbox.deselect()
        # self.twi_checkbox.bind('<Button-1>', self.__update_twi_checked)

    def _build_save_coords(self):
        self.save_coords_label = make_label(self.root, "Save Coordinates of Freehand Selection", row=10, column=0, columnspan=5, outer_padx=(15, 0), outer_pady=(0, 15), inner_padx=5, inner_pady=5, wraplength=300)
        self.save_coords_checkbox = make_checkbox(self.root, text="", row=10, column=0, var=self.save_coords_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0, outer_pady=(0, 15), outer_padx=(0, 25), columnspan=5)
        self.save_coords_checkbox.bind('<Button-1>', self.__update_save_coords_checked)

    def _build_pt1(self):
        # text
        self.pt1_label = make_text(self.root, content="Pt 1: " + str(self.pt1_value), bg=tkcolour_from_rgb(PASTEL_PINK_RGB), column=5, row=2, width=16, columnspan=1, padx=0, state=NORMAL)
        # remove
        self.pt1_remove = make_button(self.root, text='x', width=1, command=lambda:self.__remove_pt(1), row=2, column=6, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10, highlightthickness=0)
        # checkbox
        self.pt1_checkbox = make_checkbox(self.root, "", row=2, column=7, columnspan=1, var=self.pt1_checkbox_value, inner_padx=0, inner_pady=0, outer_padx=(0, 15), sticky=W)
        self.pt1_checkbox.deselect()
        self.pt1_checkbox.bind('<Button-1>', self.__update_pt1_checked)

    def _build_pt2(self):
        # text
        self.pt2_label = make_text(self.root, content="Pt 2: " + str(self.pt2_value), bg=tkcolour_from_rgb(PASTEL_PINK_RGB), column=5, row=3, width=16, columnspan=1, padx=0, state=NORMAL)
        # remove
        self.pt2_remove = make_button(self.root, text='x', width=1, command=lambda:self.__remove_pt(2), row=3, column=6, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10, highlightthickness=0)
        # checkbox
        self.pt2_checkbox = make_checkbox(self.root, "", row=3, column=7, columnspan=1, var=self.pt2_checkbox_value, inner_padx=0, inner_pady=0, outer_padx=(0, 15), sticky=W)
        self.pt2_checkbox.deselect()
        self.pt2_checkbox.bind('<Button-1>', self.__update_pt2_checked)

    def _build_pt3(self):
        # text
        self.pt3_label = make_text(self.root, content="Pt 3: " + str(self.pt3_value), bg=tkcolour_from_rgb(PASTEL_PINK_RGB), column=5, row=4, width=16, columnspan=1, padx=0, state=NORMAL)
        # remove
        self.pt3_remove = make_button(self.root, text='x', width=1, command=lambda:self.__remove_pt(3), row=4, column=6, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10, highlightthickness=0)
        # checkbox
        self.pt3_checkbox = make_checkbox(self.root, "", row=4, column=7, columnspan=1, var=self.pt3_checkbox_value, inner_padx=0, inner_pady=0, outer_padx=(0, 15), sticky=W)
        self.pt3_checkbox.deselect()
        self.pt3_checkbox.bind('<Button-1>', self.__update_pt3_checked)

    def _build_pt4(self):
        # text
        self.pt4_label = make_text(self.root, content="Pt 4: " + str(self.pt4_value), bg=tkcolour_from_rgb(PASTEL_PINK_RGB), column=5, row=5, width=16, columnspan=1, padx=0, state=NORMAL)
        # remove
        self.pt4_remove = make_button(self.root, text='x', width=1, command=lambda:self.__remove_pt(4), row=5, column=6, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10, highlightthickness=0)
        # checkbox
        self.pt4_checkbox = make_checkbox(self.root, "", row=5, column=7, columnspan=1, var=self.pt4_checkbox_value, inner_padx=0, inner_pady=0, outer_padx=(0, 15), sticky=W)
        self.pt4_checkbox.deselect()
        self.pt4_checkbox.bind('<Button-1>', self.__update_pt4_checked)

    def _build_pt5(self):
        # text
        self.pt5_label = make_text(self.root, content="Pt 5: " + str(self.pt5_value), bg=tkcolour_from_rgb(PASTEL_PINK_RGB), column=5, row=6, width=16, columnspan=1, padx=0, state=NORMAL)
        # remove
        self.pt5_remove = make_button(self.root, text='x', width=1, command=lambda:self.__remove_pt(5), row=6, column=6, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10, highlightthickness=0)
        # checkbox
        self.pt5_checkbox = make_checkbox(self.root, "", row=6, column=7, columnspan=1, var=self.pt5_checkbox_value, inner_padx=0, inner_pady=0, outer_padx=(0, 15), sticky=W)
        self.pt5_checkbox.deselect()
        self.pt5_checkbox.bind('<Button-1>', self.__update_pt5_checked)

    def _build_pt6(self):
        # text
        self.pt6_label = make_text(self.root, content="Pt 6: " + str(self.pt6_value), bg=tkcolour_from_rgb(PASTEL_PINK_RGB), column=5, row=7, width=16, columnspan=1, padx=0, state=NORMAL)
        # remove
        self.pt6_remove = make_button(self.root, text='x', width=1, command=lambda:self.__remove_pt(6), row=7, column=6, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10, highlightthickness=0)
        # checkbox
        self.pt6_checkbox = make_checkbox(self.root, "", row=7, column=7, columnspan=1, var=self.pt6_checkbox_value, inner_padx=0, inner_pady=0, outer_padx=(0, 15), sticky=W)
        self.pt6_checkbox.deselect()
        self.pt6_checkbox.bind('<Button-1>', self.__update_pt6_checked)

    def _build_pt7(self):
        # text
        self.pt7_label = make_text(self.root, content="Pt 7: " + str(self.pt7_value), bg=tkcolour_from_rgb(PASTEL_PINK_RGB), column=5, row=8, width=16, columnspan=1, padx=0, state=NORMAL)
        # remove
        self.pt7_remove = make_button(self.root, text='x', width=1, command=lambda:self.__remove_pt(7), row=8, column=6, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10, highlightthickness=0)
        # checkbox
        self.pt7_checkbox = make_checkbox(self.root, "", row=8, column=7, columnspan=1, var=self.pt7_checkbox_value, inner_padx=0, inner_pady=0, outer_padx=(0, 15), sticky=W)
        self.pt7_checkbox.deselect()
        self.pt7_checkbox.bind('<Button-1>', self.__update_pt7_checked)

    def _build_pt8(self):
        # text
        self.pt8_label = make_text(self.root, content="Pt 8: " + str(self.pt8_value), bg=tkcolour_from_rgb(PASTEL_PINK_RGB), column=5, row=9, width=16, columnspan=1, padx=0, state=NORMAL)
        # remove
        self.pt8_remove = make_button(self.root, text='x', width=1, command=lambda:self.__remove_pt(8), row=9, column=6, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10, highlightthickness=0)
        # checkbox
        self.pt8_checkbox = make_checkbox(self.root, "", row=9, column=7, columnspan=1, var=self.pt8_checkbox_value, inner_padx=0, inner_pady=0, outer_padx=(0, 15), sticky=W)
        self.pt8_checkbox.deselect()
        self.pt8_checkbox.bind('<Button-1>', self.__update_pt8_checked)

    def _build_original_image(self):
        if self.original_image_data is None:
            # Placeholder
            self.original_image = make_label(self.root, "original image placeholder", row=2, column=0, rowspan=8, columnspan=5, inner_pady=100, inner_padx=120, outer_padx=(15, 10), outer_pady=(15, 10))
        else:
            logging.debug("BUILDING ORIGINAL COLOUR IMAGE...")
            (self.original_image_graph, self.original_image) = make_image(self.root, self.original_image_data,row=2, column=0,columnspan=5, rowspan=8, lower_scale_value=None, upper_scale_value=None, color_rgb=PASTEL_PINK_RGB, original=True, figheight=2.5, figwidth=3.5)
            self.original_image.get_tk_widget().bind('<Double-Button-1>', self.__pop_up_image)

    def _draw_points(self):
        # for i in range(len(self.coords_list)-1):
        #     draw point between self.coords_list[i] and self.coords_list[i+1]
        pass

    # Commands (Callbacks)
    def __remove_pt(self, index):
        print('remove ' + str(index))
        self.coords_list[index-1] = None

    def __add_pt(self, pt):
        index = self.coords_list.index(None)
        self.coords_list[index] = pt
        _draw_points()

    def __pop_up_image(self, event):
        make_popup_image(self.original_image_graph)

    def __update_to_rgb(self):
        self.rgb_button.config(foreground="red")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="black")
        self.displayed_image_mode = RGB
        self.listener.render_original_image_data()

    def __update_to_sto2(self):
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="red")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="black")
        self.displayed_image_mode = STO2
        self.listener.render_original_image_data()

    def __update_to_nir(self):
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="red")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="black")
        self.displayed_image_mode = NIR
        self.listener.render_original_image_data()

    def __update_to_thi(self):
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="red")
        self.twi_button.config(foreground="black")
        self.displayed_image_mode = THI
        self.listener.render_original_image_data()

    def __update_to_twi(self):
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="red")
        self.displayed_image_mode = TWI
        self.listener.render_original_image_data()

    def __update_save_coords_checked(self, event):
        value = self.get_save_coords_checkbox_value()
        self.listener.update_saved(OG_IMAGE, value)

    def __update_pt1_checked(self, event):
        value = self.get_pt1_checkbox_value()
        self.listener.update_saved(PT1, value)

    def __update_pt2_checked(self, event):
        value = self.get_pt2_checkbox_value()
        self.listener.update_saved(PT2, value)

    def __update_pt3_checked(self, event):
        value = self.get_pt3_checkbox_value()
        self.listener.update_saved(PT3, value)

    def __update_pt4_checked(self, event):
        value = self.get_pt4_checkbox_value()
        self.listener.update_saved(PT4, value)

    def __update_pt5_checked(self, event):
        value = self.get_pt5_checkbox_value()
        self.listener.update_saved(PT5, value)

    def __update_pt6_checked(self, event):
        value = self.get_pt6_checkbox_value()
        self.listener.update_saved(PT6, value)

    def __update_pt7_checked(self, event):
        value = self.get_pt7_checkbox_value()
        self.listener.update_saved(PT7, value)

    def __update_pt8_checked(self, event):
        value = self.get_pt8_checkbox_value()
        self.listener.update_saved(PT8, value)
