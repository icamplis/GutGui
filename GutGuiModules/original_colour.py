from GutGuiModules.utility import *
from GutGuiModules.constants import *
from skimage.draw import line_aa
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw
import numpy as np
import logging
import csv

class OGColour:
    def __init__(self, original_color_frame, listener):
        self.root = original_color_frame

        # Listener
        self.listener = listener

        self.rgb_button = None
        self.rgb_checkbox = None
        self.rgb_checkbox_value = IntVar()

        self.sto2_button = None
        self.sto2_checkbox = None
        self.sto2_checkbox_value = IntVar()

        self.nir_button = None
        self.nir_checkbox = None
        self.nir_checkbox_value = IntVar()

        self.thi_button = None
        self.thi_checkbox = None
        self.thi_checkbox_value = IntVar()

        self.twi_button = None
        self.twi_checkbox = None
        self.twi_checkbox_value = IntVar()

        self.pt1_label = None
        self.pt1_remove = None
        self.pt1_checkbox = None
        self.pt1_checkbox_value = IntVar()

        self.pt2_label = None
        self.pt2_remove = None
        self.pt2_checkbox = None
        self.pt2_checkbox_value = IntVar()

        self.pt3_label = None
        self.pt3_remove = None
        self.pt3_checkbox = None
        self.pt3_checkbox_value = IntVar()

        self.pt4_label = None
        self.pt4_remove = None
        self.pt4_checkbox = None
        self.pt4_checkbox_value = IntVar()

        self.pt5_label = None
        self.pt5_remove = None
        self.pt5_checkbox = None
        self.pt5_checkbox_value = IntVar()

        self.pt6_label = None
        self.pt6_remove = None
        self.pt6_checkbox = None
        self.pt6_checkbox_value = IntVar()

        self.pt7_label = None
        self.pt7_remove = None
        self.pt7_checkbox = None
        self.pt7_checkbox_value = IntVar()

        self.pt8_label = None
        self.pt8_remove = None
        self.pt8_checkbox = None
        self.pt8_checkbox_value = IntVar()

        self.pt9_label = None
        self.pt9_remove = None
        self.pt9_checkbox = None
        self.pt9_checkbox_value = IntVar()

        self.pt10_label = None
        self.pt10_remove = None
        self.pt10_checkbox = None
        self.pt10_checkbox_value = IntVar()

        self.all_points_remove = None
        self.all_points_checkbox = None
        self.all_points_checkbox_value = IntVar()

        self.use_mask_button = None
        self.instant_save_button = None
        self.input_coords_button = None
        self.upload_mask_button = None

        self.coords_window = None
        self.input_points_title = None
        self.go_button = None

        self.input_pt1_title = None
        self.input_pt1_title_x = None
        self.input_pt1_x = None
        self.input_pt1_title_y = None
        self.input_pt1_y = None

        self.input_pt2_title = None
        self.input_pt2_title_x = None
        self.input_pt2_x = None
        self.input_pt2_title_y = None
        self.input_pt2_y = None

        self.input_pt3_title = None
        self.input_pt3_title_x = None
        self.input_pt3_x = None
        self.input_pt3_title_y = None
        self.input_pt3_y = None

        self.input_pt4_title = None
        self.input_pt4_title_x = None
        self.input_pt4_x = None
        self.input_pt4_title_y = None
        self.input_pt4_y = None

        self.input_pt5_title = None
        self.input_pt5_title_x = None
        self.input_pt5_x = None
        self.input_pt5_title_y = None
        self.input_pt5_y = None

        self.input_pt6_title = None
        self.input_pt6_title_x = None
        self.input_pt6_x = None
        self.input_pt6_title_y = None
        self.input_pt6_y = None

        self.input_pt7_title = None
        self.input_pt7_title_x = None
        self.input_pt7_x = None
        self.input_pt7_title_y = None
        self.input_pt7_y = None

        self.input_pt8_title = None
        self.input_pt8_title_x = None
        self.input_pt8_x = None
        self.input_pt8_title_y = None
        self.input_pt8_y = None

        self.input_pt9_title = None
        self.input_pt9_title_x = None
        self.input_pt9_x = None
        self.input_pt9_title_y = None
        self.input_pt9_y = None

        self.input_pt10_title = None
        self.input_pt10_title_x = None
        self.input_pt10_x = None
        self.input_pt10_title_y = None
        self.input_pt10_y = None

        self.original_image_graph = None
        self.original_image_data = None
        self.original_image = None
        self.image_array = None

        self.pop_up_graph = None
        self.pop_up_window = None
        self.pop_up_image = None
        self.pop_up = False

        self.info_label = None

        # coords in dimensions of image, i.e. xrange=[0, 640], yrange=[0, 480]
        self.coords_list = [(None, None) for i in range(10)]
        self.mask_raw = None

        self._init_widget()

        self.displayed_image_mode = RGB  # RGB by default
        self.rgb_button.config(foreground="red")

    def get_mask(self):
        return self.mask_raw

    def get_coords(self):
        return self.coords_list

    def get_bools(self):
        return [self.get_pt1_checkbox_value(), 
        self.get_pt2_checkbox_value(), self.get_pt3_checkbox_value(), 
        self.get_pt4_checkbox_value(), self.get_pt5_checkbox_value(), 
        self.get_pt6_checkbox_value(), self.get_pt7_checkbox_value(), 
        self.get_pt8_checkbox_value(), self.get_pt9_checkbox_value(), 
        self.get_pt10_checkbox_value()]

    def get_current_data(self):
        return self.original_image_data

    def update_original_image(self, original_image_data):
        self.original_image_data = original_image_data
        self._draw_points()

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

    def get_all_points_checkbox_value(self):
        return not bool(self.all_points_checkbox_value.get())

    def get_pt1_checkbox_value(self):
        return not bool(self.pt1_checkbox_value.get())

    def get_pt2_checkbox_value(self):
        return not bool(self.pt2_checkbox_value.get())

    def get_pt3_checkbox_value(self):
        return not bool(self.pt3_checkbox_value.get())

    def get_pt4_checkbox_value(self):
        return not bool(self.pt4_checkbox_value.get())

    def get_pt5_checkbox_value(self):
        return not bool(self.pt5_checkbox_value.get())

    def get_pt6_checkbox_value(self):
        return not bool(self.pt6_checkbox_value.get())

    def get_pt7_checkbox_value(self):
        return not bool(self.pt7_checkbox_value.get())
        
    def get_pt8_checkbox_value(self):
        return not bool(self.pt8_checkbox_value.get())

    def get_pt9_checkbox_value(self):
        return not bool(self.pt7_checkbox_value.get())
        
    def get_pt10_checkbox_value(self):
        return not bool(self.pt8_checkbox_value.get())

    # Helper
    def _init_widget(self):
        self._build_rgb()
        self._build_sto2()
        self._build_nir()
        self._build_thi()
        self._build_twi()
        self._build_pt1()
        self._build_pt2()
        self._build_pt3()
        self._build_pt4()
        self._build_pt5()
        self._build_pt6()
        self._build_pt7()
        self._build_pt8()
        self._build_pt9()
        self._build_pt10()
        self._build_all_points()
        self._build_use_mask_button()
        self._build_instant_save_button()
        self._build_edit_coords_button()
        self._build_upload_mask_button()
        self._build_info_label()
        self._build_original_image(self.original_image_data)

    def _build_rgb(self):
        self.rgb_button = make_button(self.root, text='RGB', width=3, command=self.__update_to_rgb, row=1, column=0, columnspan=1, inner_pady=5, outer_padx=(15, 10))

    def _build_sto2(self):
        self.sto2_button = make_button(self.root, text='StO2', width=4, command=self.__update_to_sto2, row=1, column=1, columnspan=1, inner_pady=5, outer_padx=(0, 10))

    def _build_nir(self):
        self.nir_button = make_button(self.root, text='NIR', width=3, command=self.__update_to_nir, row=1, column=2, columnspan=1, inner_pady=5, outer_padx=(0, 10))

    def _build_thi(self):
        self.thi_button = make_button(self.root, text='THI', width=3, command=self.__update_to_thi, row=1, column=3, columnspan=1, inner_pady=5, outer_padx=(0, 10))

    def _build_twi(self):
        self.twi_button = make_button(self.root, text='TWI', width=3, command=self.__update_to_twi, row=1, column=4, columnspan=1, inner_pady=5, outer_padx=0)

    def _build_all_points(self):
        # remove
        self.all_points_remove = make_button(self.root, text='x', width=1, command=lambda:self.__remove_pt('all'), row=1, column=6, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10, highlightthickness=0)
        # checkbox
        self.all_points_checkbox = make_checkbox(self.root, "", row=1, column=7, columnspan=1, var=self.all_points_checkbox_value, inner_padx=0, inner_pady=0, outer_padx=(0, 15), sticky=W)
        self.all_points_checkbox.deselect()
        self.all_points_checkbox.bind('<Button-1>', self.__update_all_points_checked)

    def _build_pt1(self):
        # text
        # displat points on interval [1, max] because ??????
        if self.coords_list[0] == (None, None):
            self.pt1_label = make_text(self.root, content="Pt 0: " + str(self.coords_list[0]), bg=tkcolour_from_rgb(BACKGROUND), column=5, row=2, width=18, columnspan=1, padx=0, state=NORMAL)
        else:
            self.pt1_label = make_text(self.root, content="Pt 0: " + str(tuple(x+1 for x in self.coords_list[0])), bg=tkcolour_from_rgb(BACKGROUND), column=5, row=2, width=18, columnspan=1, padx=0, state=NORMAL)
        # remove
        self.pt1_remove = make_button(self.root, text='x', width=1, command=lambda:self.__remove_pt(1), row=2, column=6, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10, highlightthickness=0)
        # checkbox
        self.pt1_checkbox = make_checkbox(self.root, "", row=2, column=7, columnspan=1, var=self.pt1_checkbox_value, inner_padx=0, inner_pady=0, outer_padx=(0, 15), sticky=W)
        self.pt1_checkbox.deselect()
        self.pt1_checkbox.bind('<Button-1>', self.__update_pt1_checked)

    def _build_pt2(self):
        # text
        if self.coords_list[1] == (None, None):
            self.pt2_label = make_text(self.root, content="Pt 1: " + str(self.coords_list[1]), bg=tkcolour_from_rgb(BACKGROUND), column=5, row=3, width=18, columnspan=1, padx=0, state=NORMAL)
        else:
            self.pt2_label = make_text(self.root, content="Pt 1: " + str(tuple(x+1 for x in self.coords_list[1])), bg=tkcolour_from_rgb(BACKGROUND), column=5, row=3, width=18, columnspan=1, padx=0, state=NORMAL)
        # remove
        self.pt2_remove = make_button(self.root, text='x', width=1, command=lambda:self.__remove_pt(2), row=3, column=6, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10, highlightthickness=0)
        # checkbox
        self.pt2_checkbox = make_checkbox(self.root, "", row=3, column=7, columnspan=1, var=self.pt2_checkbox_value, inner_padx=0, inner_pady=0, outer_padx=(0, 15), sticky=W)
        self.pt2_checkbox.deselect()
        self.pt2_checkbox.bind('<Button-1>', self.__update_pt2_checked)

    def _build_pt3(self):
        # text
        if self.coords_list[2] == (None, None):
            self.pt3_label = make_text(self.root, content="Pt 2: " + str(self.coords_list[2]), bg=tkcolour_from_rgb(BACKGROUND), column=5, row=4, width=18, columnspan=1, padx=0, state=NORMAL)
        else:
            self.pt3_label = make_text(self.root, content="Pt 2: " + str(tuple(x+1 for x in self.coords_list[2])), bg=tkcolour_from_rgb(BACKGROUND), column=5, row=4, width=18, columnspan=1, padx=0, state=NORMAL)
        # remove
        self.pt3_remove = make_button(self.root, text='x', width=1, command=lambda:self.__remove_pt(3), row=4, column=6, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10, highlightthickness=0)
        # checkbox
        self.pt3_checkbox = make_checkbox(self.root, "", row=4, column=7, columnspan=1, var=self.pt3_checkbox_value, inner_padx=0, inner_pady=0, outer_padx=(0, 15), sticky=W)
        self.pt3_checkbox.deselect()
        self.pt3_checkbox.bind('<Button-1>', self.__update_pt3_checked)

    def _build_pt4(self):
        # text
        if self.coords_list[3] == (None, None):
            self.pt4_label = make_text(self.root, content="Pt 3: " + str(self.coords_list[3]), bg=tkcolour_from_rgb(BACKGROUND), column=5, row=5, width=18, columnspan=1, padx=0, state=NORMAL)
        else:
            self.pt4_label = make_text(self.root, content="Pt 3: " + str(tuple(x+1 for x in self.coords_list[3])), bg=tkcolour_from_rgb(BACKGROUND), column=5, row=5, width=18, columnspan=1, padx=0, state=NORMAL)
        # remove
        self.pt4_remove = make_button(self.root, text='x', width=1, command=lambda:self.__remove_pt(4), row=5, column=6, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10, highlightthickness=0)
        # checkbox
        self.pt4_checkbox = make_checkbox(self.root, "", row=5, column=7, columnspan=1, var=self.pt4_checkbox_value, inner_padx=0, inner_pady=0, outer_padx=(0, 15), sticky=W)
        self.pt4_checkbox.deselect()
        self.pt4_checkbox.bind('<Button-1>', self.__update_pt4_checked)

    def _build_pt5(self):
        # text
        if self.coords_list[4] == (None, None):
            self.pt5_label = make_text(self.root, content="Pt 4: " + str(self.coords_list[4]), bg=tkcolour_from_rgb(BACKGROUND), column=5, row=6, width=18, columnspan=1, padx=0, state=NORMAL)
        else:
            self.pt5_label = make_text(self.root, content="Pt 4: " + str(tuple(x+1 for x in self.coords_list[4])), bg=tkcolour_from_rgb(BACKGROUND), column=5, row=6, width=18, columnspan=1, padx=0, state=NORMAL)
        # remove
        self.pt5_remove = make_button(self.root, text='x', width=1, command=lambda:self.__remove_pt(5), row=6, column=6, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10, highlightthickness=0)
        # checkbox
        self.pt5_checkbox = make_checkbox(self.root, "", row=6, column=7, columnspan=1, var=self.pt5_checkbox_value, inner_padx=0, inner_pady=0, outer_padx=(0, 15), sticky=W)
        self.pt5_checkbox.deselect()
        self.pt5_checkbox.bind('<Button-1>', self.__update_pt5_checked)

    def _build_pt6(self):
        # text
        if self.coords_list[5] == (None, None):
            self.pt6_label = make_text(self.root, content="Pt 5: " + str(self.coords_list[5]), bg=tkcolour_from_rgb(BACKGROUND), column=5, row=7, width=18, columnspan=1, padx=0, state=NORMAL)
        else:
            self.pt6_label = make_text(self.root, content="Pt 5: " + str(tuple(x+1 for x in self.coords_list[5])), bg=tkcolour_from_rgb(BACKGROUND), column=5, row=7, width=18, columnspan=1, padx=0, state=NORMAL)
        # remove
        self.pt6_remove = make_button(self.root, text='x', width=1, command=lambda:self.__remove_pt(6), row=7, column=6, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10, highlightthickness=0)
        # checkbox
        self.pt6_checkbox = make_checkbox(self.root, "", row=7, column=7, columnspan=1, var=self.pt6_checkbox_value, inner_padx=0, inner_pady=0, outer_padx=(0, 15), sticky=W)
        self.pt6_checkbox.deselect()
        self.pt6_checkbox.bind('<Button-1>', self.__update_pt6_checked)

    def _build_pt7(self):
        # text
        if self.coords_list[6] == (None, None):
            self.pt7_label = make_text(self.root, content="Pt 6: " + str(self.coords_list[6]), bg=tkcolour_from_rgb(BACKGROUND), column=5, row=8, width=18, columnspan=1, padx=0, state=NORMAL)
        else:
            self.pt7_label = make_text(self.root, content="Pt 6: " + str(tuple(x+1 for x in self.coords_list[6])), bg=tkcolour_from_rgb(BACKGROUND), column=5, row=8, width=18, columnspan=1, padx=0, state=NORMAL)
        # remove
        self.pt7_remove = make_button(self.root, text='x', width=1, command=lambda:self.__remove_pt(7), row=8, column=6, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10, highlightthickness=0)
        # checkbox
        self.pt7_checkbox = make_checkbox(self.root, "", row=8, column=7, columnspan=1, var=self.pt7_checkbox_value, inner_padx=0, inner_pady=0, outer_padx=(0, 15), sticky=W)
        self.pt7_checkbox.deselect()
        self.pt7_checkbox.bind('<Button-1>', self.__update_pt7_checked)

    def _build_pt8(self):
        # text
        if self.coords_list[7] == (None, None):
            self.pt8_label = make_text(self.root, content="Pt 7: " + str(self.coords_list[7]), bg=tkcolour_from_rgb(BACKGROUND), column=5, row=9, width=18, columnspan=1, padx=0, state=NORMAL)
        else:
            self.pt8_label = make_text(self.root, content="Pt 7: " + str(tuple(x+1 for x in self.coords_list[7])), bg=tkcolour_from_rgb(BACKGROUND), column=5, row=9, width=18, columnspan=1, padx=0, state=NORMAL)
        # remove
        self.pt8_remove = make_button(self.root, text='x', width=1, command=lambda:self.__remove_pt(8), row=9, column=6, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10, highlightthickness=0)
        # checkbox
        self.pt8_checkbox = make_checkbox(self.root, "", row=9, column=7, columnspan=1, var=self.pt8_checkbox_value, inner_padx=0, inner_pady=0, outer_padx=(0, 15), sticky=W)
        self.pt8_checkbox.deselect()
        self.pt8_checkbox.bind('<Button-1>', self.__update_pt8_checked)

    def _build_pt9(self):
        # text
        if self.coords_list[8] == (None, None):
            self.pt9_label = make_text(self.root, content="Pt 8: " + str(self.coords_list[8]), bg=tkcolour_from_rgb(BACKGROUND), column=5, row=10, width=18, columnspan=1, padx=0, state=NORMAL)
        else:
            self.pt9_label = make_text(self.root, content="Pt 8: " + str(tuple(x+1 for x in self.coords_list[8])), bg=tkcolour_from_rgb(BACKGROUND), column=5, row=10, width=18, columnspan=1, padx=0, state=NORMAL)
        # remove
        self.pt9_remove = make_button(self.root, text='x', width=1, command=lambda:self.__remove_pt(9), row=10, column=6, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10, highlightthickness=0)
        # checkbox
        self.pt9_checkbox = make_checkbox(self.root, "", row=10, column=7, columnspan=1, var=self.pt9_checkbox_value, inner_padx=0, inner_pady=0, outer_padx=(0, 15), sticky=W)
        self.pt9_checkbox.deselect()
        self.pt9_checkbox.bind('<Button-1>', self.__update_pt9_checked)

    def _build_pt10(self):
        # text
        if self.coords_list[9] == (None, None):
            self.pt10_label = make_text(self.root, content="Pt 9: " + str(self.coords_list[9]), bg=tkcolour_from_rgb(BACKGROUND), column=5, row=11, width=18, columnspan=1, padx=0, state=NORMAL)
        else:
            self.pt10_label = make_text(self.root, content="Pt 9: " + str(tuple(x+1 for x in self.coords_list[9])), bg=tkcolour_from_rgb(BACKGROUND), column=5, row=11, width=18, columnspan=1, padx=0, state=NORMAL)
        # remove
        self.pt10_remove = make_button(self.root, text='x', width=1, command=lambda:self.__remove_pt(10), row=11, column=6, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10, highlightthickness=0)
        # checkbox
        self.pt10_checkbox = make_checkbox(self.root, "", row=11, column=7, columnspan=1, var=self.pt10_checkbox_value, inner_padx=0, inner_pady=0, outer_padx=(0, 15), sticky=W)
        self.pt10_checkbox.deselect()
        self.pt10_checkbox.bind('<Button-1>', self.__update_pt10_checked)

    def _build_use_mask_button(self):
        self.use_mask_button = make_button(self.root, text='Use mask', width=8, command=self.__use_coords, row=12, column=5, columnspan=3, inner_pady=5, outer_padx=(100, 15), outer_pady=(10, 15))

    def _build_instant_save_button(self):
        self.instant_save_button = make_button(self.root, text='Save coords', width=11, command=self.__save_coords, row=12, column=2, columnspan=2, inner_pady=5, outer_padx=(0, 15), outer_pady=(10, 15))

    def _build_edit_coords_button(self):
        self.input_coords_button = make_button(self.root, text='Edit coords', width=12, command=self.__input_coords, row=12, column=4, columnspan=2, inner_pady=5, outer_padx=(0, 45), outer_pady=(10, 15))

    def _build_upload_mask_button(self):
        self.upload_mask_button = make_button(self.root, text='Upload mask', width=11, command=self.__upload_mask, row=12, column=0, columnspan=2, inner_pady=5, outer_padx=15, outer_pady=(10, 15))

    def _build_info_label(self):
        self.info_label = make_label_button(self.root, text='Original Image', command=self.__info, width=12)
        self.info_label.grid(columnspan=2)

    def _build_original_image(self, data):
        if data is None:
            # Placeholder
            self.original_image = make_label(self.root, "original image placeholder", row=2, column=0, rowspan=10, columnspan=5, inner_pady=80, inner_padx=120, outer_padx=(15, 10), outer_pady=(15, 10))
        else:
            logging.debug("BUILDING ORIGINAL COLOUR IMAGE...")
            (self.original_image_graph, self.original_image, self.image_array) = make_image(self.root, data, row=2, column=0, columnspan=5, rowspan=10, lower_scale_value=None, upper_scale_value=None, color_rgb=BACKGROUND, original=True, figheight=2.5, figwidth=3.5)
            self.original_image.get_tk_widget().bind('<Button-2>', self.__pop_up_image)
            self.original_image.get_tk_widget().bind('<Button-1>', self.__get_coords)
            if self.pop_up == True:
                self.pop_up_graph = self.original_image_graph
                self.pop_up_graph.set_size_inches(8, 8)
                self.pop_up_image = FigureCanvasTkAgg(self.pop_up_graph, master=self.pop_up_window)
                self.pop_up_image.draw()
                self.pop_up_image.get_tk_widget().grid(column=0, row=0)
                self.pop_up_image.get_tk_widget().bind('<Button-1>', self.__get_coords)

    def _draw_points(self):
        copy_data = self.original_image_data.copy()
        not_none = [i for i in self.coords_list if i != (None, None)]
        for point in not_none:
            y = int(point[0])
            x = int(point[1])
            for xi in range(-4, 5):
                 copy_data[(x+xi)%480, y, :] = BRIGHT_GREEN_RGB
            for yi in range(-4, 5):
                copy_data[x, (y+yi)%640, :] = BRIGHT_GREEN_RGB
            idx = not_none.index(point)
            self._draw_a_line(not_none[idx-1], not_none[idx], copy_data)    
        self._build_original_image(copy_data)

    def _draw_a_line(self, point1, point2, image):
        r0, c0 = point1
        r1, c1 = point2
        rr, cc, val = line_aa(c0, r0, c1, r1)
        for i in range(len(rr)):
            image[rr[i]%480, cc[i]%640] = (int(113*val[i]), int(255*val[i]), int(66*val[i]))
        return image

    def _build_points(self):
        self._build_pt1()
        self._build_pt2()
        self._build_pt3()
        self._build_pt4()
        self._build_pt5()
        self._build_pt6()
        self._build_pt7()
        self._build_pt8()
        self._build_pt9()
        self._build_pt10()

    # Commands (Callbacks)
    def __info(self):
        info = self.listener.get_original_info()
        title = "Original Image Information"
        make_info(title=title, info=info)

    def __use_coords(self):
        # produces a 640x480 8-bit mask
        polygon = [point for point in self.coords_list if point != (None, None)]
        img = Image.new('L', (640, 480), 0)
        ImageDraw.Draw(img).polygon(polygon, outline=1, fill=1)
        self.mask_raw = np.array(img)
        self.mask_raw = np.fliplr((self.mask_raw).T)
        self.listener.submit_mask(self.mask_raw)

    def __save_coords(self):
        self.listener.instant_save_points()

    def __upload_mask(self):
        mask_dir_path = filedialog.askopenfilename(parent=self.root, title="Please select a .csv file containing the coordinates of a mask.")
        if mask_dir_path[-4:] != ".csv":
            messagebox.showerror("Error", "That's not a .csv file!")
        else:
            self.__load_mask(mask_dir_path)

    def __load_mask(self, path):
        coords = []
        with open(path) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                coords.append((int(float(row[0]-1)), (int(float(row[1]-1)))))
        for i in range(10-len(coords)):
            coords.append((None, None))
        self.coords_list = coords
        self._build_points()
        self._draw_points()

    def __remove_pt(self, index):
        if index == 'all':
            self.coords_list = [(None, None) for i in range(10)]
        else:
            self.coords_list[index-1] = (None, None)
        self._build_points()
        self._draw_points()

    def __add_pt(self, pt):
        if self.coords_list.count((None, None)) != 0:
            index = self.coords_list.index((None, None))
            self.coords_list[index] = pt
            self._build_points()
            self._draw_points()

    def __get_coords(self, eventorigin):
        if not self.pop_up:
            x = int((eventorigin.x - 30)*640/296)
            y = int((eventorigin.y - 18)*480/221)
            if 0 <= x < 640 and 0 <= y < 480:
                self.__add_pt((x, y))
        else:
            x = int(((eventorigin.x) - 17)*640/770)
            y = int(((eventorigin.y) - 114)*480/578)
            if 0 <= x < 640 and 0 <= y < 480:
                self.__add_pt((x, y))

    def __pop_up_image(self, event):
        (self.pop_up_window, self.pop_up_image) = make_popup_image(self.original_image_graph, interactive=True)
        self.pop_up = True
        self.pop_up_image.get_tk_widget().bind('<Button-1>', self.__get_coords)
        self.pop_up_window.protocol("WM_DELETE_WINDOW", func=self.__close_pop_up)
        self.pop_up_window.attributes("-topmost", True)

    def __close_pop_up(self):
        self.pop_up = False
        self.pop_up_window.destroy()

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

    def __update_all(self, value):
        for point in [PT1, PT2, PT3, PT4, PT5, PT6, PT7, PT8, PT9, PT10]:
            self.listener.update_saved(point, value)

    def __update_all_points_checked(self, event):
        value = self.get_all_points_checkbox_value()
        if value == True:
            self.pt1_checkbox.select()
            self.pt2_checkbox.select()
            self.pt3_checkbox.select()
            self.pt4_checkbox.select()
            self.pt5_checkbox.select()
            self.pt6_checkbox.select()
            self.pt7_checkbox.select()
            self.pt8_checkbox.select()
            self.pt9_checkbox.select()
            self.pt10_checkbox.select()
        else:
            self.pt1_checkbox.deselect()
            self.pt2_checkbox.deselect()
            self.pt3_checkbox.deselect()
            self.pt4_checkbox.deselect()
            self.pt5_checkbox.deselect()
            self.pt6_checkbox.deselect()
            self.pt7_checkbox.deselect()
            self.pt8_checkbox.deselect()
            self.pt9_checkbox.deselect()
            self.pt10_checkbox.deselect()
        self.__update_all(value)

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

    def __update_pt9_checked(self, event):
        value = self.get_pt9_checkbox_value()
        self.listener.update_saved(PT9, value)

    def __update_pt10_checked(self, event):
        value = self.get_pt10_checkbox_value()
        self.listener.update_saved(PT10, value)

    def __input_coords(self):
        self.coords_window  = Toplevel()
        self.coords_window.geometry("+0+0")
        self.coords_window.configure(bg=tkcolour_from_rgb(BACKGROUND))
        # title
        self.input_points_title = make_label_button(self.coords_window, text='Coordinate Input', command=self.__input_info, width=14)
        self.input_points_title.grid(columnspan=3)

        # point 1
        self.input_pt1_title = make_text(self.coords_window, content="Pt 0: ", bg=tkcolour_from_rgb(BACKGROUND), column=0, row=1, width=6, pady=(0, 3), padx=(15, 0))
        self.input_pt1_title_x = make_text(self.coords_window, content="x = ", bg=tkcolour_from_rgb(BACKGROUND), column=1, row=1, width=4, pady=(0, 3))
        self.input_pt1_x = make_entry(self.coords_window, row=1, column=2, width=5, columnspan=1, pady=(0, 3))
        self.input_pt1_title_y = make_text(self.coords_window, content="y = ", bg=tkcolour_from_rgb(BACKGROUND), column=3, row=1, width=4, pady=(0, 3), padx=(5, 0))
        self.input_pt1_y = make_entry(self.coords_window, row=1, column=4, width=5, columnspan=1, padx=(0, 15), pady=(0, 3))
        if self.coords_list[0] != (None, None):
            self.input_pt1_x.insert(END, str(self.coords_list[0][0]+1))
            self.input_pt1_y.insert(END, str(self.coords_list[0][1]+1))

        # point 2
        self.input_pt2_title = make_text(self.coords_window, content="Pt 1: ", bg=tkcolour_from_rgb(BACKGROUND), column=0, row=2, width=6, pady=(0, 3), padx=(15, 0))
        self.input_pt2_title_x = make_text(self.coords_window, content="x = ", bg=tkcolour_from_rgb(BACKGROUND), column=1, row=2, width=4, pady=(0, 3))
        self.input_pt2_x = make_entry(self.coords_window, row=2, column=2, width=5, columnspan=1, pady=(0, 3))
        self.input_pt2_title_y = make_text(self.coords_window, content="y = ", bg=tkcolour_from_rgb(BACKGROUND), column=3, row=2, width=4, pady=(0, 3), padx=(5, 0))
        self.input_pt2_y = make_entry(self.coords_window, row=2, column=4, width=5, columnspan=1, padx=(0, 15), pady=(0, 3))
        if self.coords_list[1] != (None, None):
            self.input_pt2_x.insert(END, str(self.coords_list[1][0]+1))
            self.input_pt2_y.insert(END, str(self.coords_list[1][1]+1))

        # point 3
        self.input_pt3_title = make_text(self.coords_window, content="Pt 2: ", bg=tkcolour_from_rgb(BACKGROUND), column=0, row=3, width=6, pady=(0, 3), padx=(15, 0))
        self.input_pt3_title_x = make_text(self.coords_window, content="x = ", bg=tkcolour_from_rgb(BACKGROUND), column=1, row=3, width=4, pady=(0, 3))
        self.input_pt3_x = make_entry(self.coords_window, row=3, column=2, width=5, columnspan=1, pady=(0, 3))
        self.input_pt3_title_y = make_text(self.coords_window, content="y = ", bg=tkcolour_from_rgb(BACKGROUND), column=3, row=3, width=4, pady=(0, 3), padx=(5, 0))
        self.input_pt3_y = make_entry(self.coords_window, row=3, column=4, width=5, columnspan=1, padx=(0, 15), pady=(0, 3))
        if self.coords_list[2] != (None, None):
            self.input_pt3_x.insert(END, str(self.coords_list[2][0]+1))
            self.input_pt3_y.insert(END, str(self.coords_list[2][1]+1))

        # point 4
        self.input_pt4_title = make_text(self.coords_window, content="Pt 3: ", bg=tkcolour_from_rgb(BACKGROUND), column=0, row=4, width=6, pady=(0, 3), padx=(15, 0))
        self.input_pt4_title_x = make_text(self.coords_window, content="x = ", bg=tkcolour_from_rgb(BACKGROUND), column=1, row=4, width=4, pady=(0, 3))
        self.input_pt4_x = make_entry(self.coords_window, row=4, column=2, width=5, columnspan=1, pady=(0, 3))
        self.input_pt4_title_y = make_text(self.coords_window, content="y = ", bg=tkcolour_from_rgb(BACKGROUND), column=3, row=4, width=4, pady=(0, 3), padx=(5, 0))
        self.input_pt4_y = make_entry(self.coords_window, row=4, column=4, width=5, columnspan=1, padx=(0, 15), pady=(0, 3))
        if self.coords_list[3] != (None, None):
            self.input_pt4_x.insert(END, str(self.coords_list[3][0]+1))
            self.input_pt4_y.insert(END, str(self.coords_list[3][1]+1))

        # point 5
        self.input_pt5_title = make_text(self.coords_window, content="Pt 4: ", bg=tkcolour_from_rgb(BACKGROUND), column=0, row=5, width=6, pady=(0, 3), padx=(15, 0))
        self.input_pt5_title_x = make_text(self.coords_window, content="x = ", bg=tkcolour_from_rgb(BACKGROUND), column=1, row=5, width=4, pady=(0, 3))
        self.input_pt5_x = make_entry(self.coords_window, row=5, column=2, width=5, columnspan=1, pady=(0, 3))
        self.input_pt5_title_y = make_text(self.coords_window, content="y = ", bg=tkcolour_from_rgb(BACKGROUND), column=3, row=5, width=4, pady=(0, 3), padx=(5, 0))
        self.input_pt5_y = make_entry(self.coords_window, row=5, column=4, width=5, columnspan=1, padx=(0, 15), pady=(0, 3))
        if self.coords_list[4] != (None, None):
            self.input_pt5_x.insert(END, str(self.coords_list[4][0]+1))
            self.input_pt5_y.insert(END, str(self.coords_list[4][1]+1))

        # point 6
        self.input_pt6_title = make_text(self.coords_window, content="Pt 5: ", bg=tkcolour_from_rgb(BACKGROUND), column=0, row=6, width=6, pady=(0, 3), padx=(15, 0))
        self.input_pt6_title_x = make_text(self.coords_window, content="x = ", bg=tkcolour_from_rgb(BACKGROUND), column=1, row=6, width=4, pady=(0, 3))
        self.input_pt6_x = make_entry(self.coords_window, row=6, column=2, width=5, columnspan=1, pady=(0, 3))
        self.input_pt6_title_y = make_text(self.coords_window, content="y = ", bg=tkcolour_from_rgb(BACKGROUND), column=3, row=6, width=4, pady=(0, 3), padx=(5, 0))
        self.input_pt6_y = make_entry(self.coords_window, row=6, column=4, width=5, columnspan=1, padx=(0, 15), pady=(0, 3))
        if self.coords_list[5] != (None, None):
            self.input_pt6_x.insert(END, str(self.coords_list[5][0]+1))
            self.input_pt6_y.insert(END, str(self.coords_list[5][1]+1))

        # point 7
        self.input_pt7_title = make_text(self.coords_window, content="Pt 6: ", bg=tkcolour_from_rgb(BACKGROUND), column=0, row=7, width=6, pady=(0, 3), padx=(15, 0))
        self.input_pt7_title_x = make_text(self.coords_window, content="x = ", bg=tkcolour_from_rgb(BACKGROUND), column=1, row=7, width=4, pady=(0, 3))
        self.input_pt7_x = make_entry(self.coords_window, row=7, column=2, width=5, columnspan=1, pady=(0, 3))
        self.input_pt7_title_y = make_text(self.coords_window, content="y = ", bg=tkcolour_from_rgb(BACKGROUND), column=3, row=7, width=4, pady=(0, 3), padx=(5, 0))
        self.input_pt7_y = make_entry(self.coords_window, row=7, column=4, width=5, columnspan=1, padx=(0, 15), pady=(0, 3))
        if self.coords_list[6] != (None, None):
            self.input_pt7_x.insert(END, str(self.coords_list[6][0]+1))
            self.input_pt7_y.insert(END, str(self.coords_list[6][1]+1))

        # point 8
        self.input_pt8_title = make_text(self.coords_window, content="Pt 7: ", bg=tkcolour_from_rgb(BACKGROUND), column=0, row=8, width=6, pady=(0, 3), padx=(15, 0))
        self.input_pt8_title_x = make_text(self.coords_window, content="x = ", bg=tkcolour_from_rgb(BACKGROUND), column=1, row=8, width=4, pady=(0, 3))
        self.input_pt8_x = make_entry(self.coords_window, row=8, column=2, width=5, columnspan=1, pady=(0, 3))
        self.input_pt8_title_y = make_text(self.coords_window, content="y = ", bg=tkcolour_from_rgb(BACKGROUND), column=3, row=8, width=4, pady=(0, 3), padx=(5, 0))
        self.input_pt8_y = make_entry(self.coords_window, row=8, column=4, width=5, columnspan=1, padx=(0, 15), pady=(0, 3))
        if self.coords_list[7] != (None, None):
            self.input_pt8_x.insert(END, str(self.coords_list[7][0]+1))
            self.input_pt8_y.insert(END, str(self.coords_list[7][1]+1))

        # point 9
        self.input_pt9_title = make_text(self.coords_window, content="Pt 8: ", bg=tkcolour_from_rgb(BACKGROUND), column=0, row=9, width=6, pady=(0, 3), padx=(15, 0))
        self.input_pt9_title_x = make_text(self.coords_window, content="x = ", bg=tkcolour_from_rgb(BACKGROUND), column=1, row=9, width=4, pady=(0, 3))
        self.input_pt9_x = make_entry(self.coords_window, row=9, column=2, width=5, columnspan=1, pady=(0, 3))
        self.input_pt9_title_y = make_text(self.coords_window, content="y = ", bg=tkcolour_from_rgb(BACKGROUND), column=3, row=9, width=4, pady=(0, 3), padx=(5, 0))
        self.input_pt9_y = make_entry(self.coords_window, row=9, column=4, width=5, columnspan=1, padx=(0, 15), pady=(0, 3))
        if self.coords_list[8] != (None, None):
            self.input_pt9_x.insert(END, str(self.coords_list[8][0]+1))
            self.input_pt9_y.insert(END, str(self.coords_list[8][1]+1))

        # point 10
        self.input_pt10_title = make_text(self.coords_window, content="Pt 9: ", bg=tkcolour_from_rgb(BACKGROUND), column=0, row=10, width=6, pady=(0, 3), padx=(15, 0))
        self.input_pt10_title_x = make_text(self.coords_window, content="x = ", bg=tkcolour_from_rgb(BACKGROUND), column=1, row=10, width=4, pady=(0, 3))
        self.input_pt10_x = make_entry(self.coords_window, row=10, column=2, width=5, columnspan=1, pady=(0, 3))
        self.input_pt10_title_y = make_text(self.coords_window, content="y = ", bg=tkcolour_from_rgb(BACKGROUND), column=3, row=10, width=4, pady=(0, 3), padx=(5, 0))
        self.input_pt10_y = make_entry(self.coords_window, row=10, column=4, width=5, columnspan=1, padx=(0, 15), pady=(0, 3))
        if self.coords_list[9] != (None, None):
            self.input_pt10_x.insert(END, str(self.coords_list[9][0]+1))
            self.input_pt10_y.insert(END, str(self.coords_list[9][1]+1))

        # go button
        self.go_button = make_button(self.coords_window, text='Go', width=2, command=self.__use_inputted_coords, row=11, column=0, columnspan=5, inner_pady=5, outer_padx=(15, 15), outer_pady=(7, 15))

    def __input_info(self):
        info = self.listener.get_input_info()
        title = "Coordinate Input Information"
        make_info(title=title, info=info)

    def __use_inputted_coords(self):
        coords = [(self.input_pt1_x.get(), self.input_pt1_y.get()),
        (self.input_pt2_x.get(), self.input_pt2_y.get()), 
        (self.input_pt3_x.get(), self.input_pt3_y.get()), 
        (self.input_pt4_x.get(), self.input_pt4_y.get()), 
        (self.input_pt5_x.get(), self.input_pt5_y.get()), 
        (self.input_pt6_x.get(), self.input_pt6_y.get()), 
        (self.input_pt7_x.get(), self.input_pt7_y.get()), 
        (self.input_pt8_x.get(), self.input_pt8_y.get()), 
        (self.input_pt9_x.get(), self.input_pt9_y.get()), 
        (self.input_pt10_x.get(), self.input_pt10_y.get())]
        coords = [(int(i[0])-1, int(i[1])-1) for i in coords if i[0] != '' and i[1] != '']
        if len(coords) > 0:
            xs = [i[0] for i in coords]
            ys = [i[1] for i in coords]
            for i in range(10-len(coords)):
                coords.append((None, None))
            if min(xs) >= 0 and max(xs) < 640 and min(ys) >= 0 and max(ys) < 480:
                self.coords_list = coords
                self._build_points()
                self._draw_points()
            else:
                messagebox.showerror("Error", "x values must be on the interval [1, 640] and y values must be on the interval \n[1, 480].")
        self.coords_window.destroy()
        
