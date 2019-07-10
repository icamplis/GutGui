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

        self.use_mask_button = None

        self.upload_mask_button = None

        self.original_image_graph = None
        self.original_image_data = None
        self.original_image = None
        self.image_array = None

        self.pop_up_graph = None
        self.pop_up_window = None
        self.pop_up_image = None
        self.pop_up = False

        # coords in dimensions of image, i.e. xrange=[0, 640], yrange=[0, 480]
        self.coords_list = [(None, None) for i in range(8)]
        self.mask_raw = None

        self._init_widget()

        self.displayed_image_mode = RGB  # RGB by default
        self.rgb_button.config(foreground="red")

    def get_mask(self):
        return self.mask_raw

    def get_coords(self):
        return self.coords_list

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
        self._build_use_mask_button()
        self._build_upload_mask_button()
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

    def _build_pt1(self):
        # text
        self.pt1_label = make_text(self.root, content="Pt 1: " + str(self.coords_list[0]), bg=tkcolour_from_rgb(PASTEL_PINK_RGB), column=5, row=2, width=18, columnspan=1, padx=0, state=NORMAL)
        # remove
        self.pt1_remove = make_button(self.root, text='x', width=1, command=lambda:self.__remove_pt(1), row=2, column=6, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10, highlightthickness=0)
        # checkbox
        self.pt1_checkbox = make_checkbox(self.root, "", row=2, column=7, columnspan=1, var=self.pt1_checkbox_value, inner_padx=0, inner_pady=0, outer_padx=(0, 15), sticky=W)
        self.pt1_checkbox.deselect()
        self.pt1_checkbox.bind('<Button-1>', self.__update_pt1_checked)

    def _build_pt2(self):
        # text
        self.pt2_label = make_text(self.root, content="Pt 2: " + str(self.coords_list[1]), bg=tkcolour_from_rgb(PASTEL_PINK_RGB), column=5, row=3, width=18, columnspan=1, padx=0, state=NORMAL)
        # remove
        self.pt2_remove = make_button(self.root, text='x', width=1, command=lambda:self.__remove_pt(2), row=3, column=6, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10, highlightthickness=0)
        # checkbox
        self.pt2_checkbox = make_checkbox(self.root, "", row=3, column=7, columnspan=1, var=self.pt2_checkbox_value, inner_padx=0, inner_pady=0, outer_padx=(0, 15), sticky=W)
        self.pt2_checkbox.deselect()
        self.pt2_checkbox.bind('<Button-1>', self.__update_pt2_checked)

    def _build_pt3(self):
        # text
        self.pt3_label = make_text(self.root, content="Pt 3: " + str(self.coords_list[2]), bg=tkcolour_from_rgb(PASTEL_PINK_RGB), column=5, row=4, width=18, columnspan=1, padx=0, state=NORMAL)
        # remove
        self.pt3_remove = make_button(self.root, text='x', width=1, command=lambda:self.__remove_pt(3), row=4, column=6, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10, highlightthickness=0)
        # checkbox
        self.pt3_checkbox = make_checkbox(self.root, "", row=4, column=7, columnspan=1, var=self.pt3_checkbox_value, inner_padx=0, inner_pady=0, outer_padx=(0, 15), sticky=W)
        self.pt3_checkbox.deselect()
        self.pt3_checkbox.bind('<Button-1>', self.__update_pt3_checked)

    def _build_pt4(self):
        # text
        self.pt4_label = make_text(self.root, content="Pt 4: " + str(self.coords_list[3]), bg=tkcolour_from_rgb(PASTEL_PINK_RGB), column=5, row=5, width=18, columnspan=1, padx=0, state=NORMAL)
        # remove
        self.pt4_remove = make_button(self.root, text='x', width=1, command=lambda:self.__remove_pt(4), row=5, column=6, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10, highlightthickness=0)
        # checkbox
        self.pt4_checkbox = make_checkbox(self.root, "", row=5, column=7, columnspan=1, var=self.pt4_checkbox_value, inner_padx=0, inner_pady=0, outer_padx=(0, 15), sticky=W)
        self.pt4_checkbox.deselect()
        self.pt4_checkbox.bind('<Button-1>', self.__update_pt4_checked)

    def _build_pt5(self):
        # text
        self.pt5_label = make_text(self.root, content="Pt 5: " + str(self.coords_list[4]), bg=tkcolour_from_rgb(PASTEL_PINK_RGB), column=5, row=6, width=18, columnspan=1, padx=0, state=NORMAL)
        # remove
        self.pt5_remove = make_button(self.root, text='x', width=1, command=lambda:self.__remove_pt(5), row=6, column=6, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10, highlightthickness=0)
        # checkbox
        self.pt5_checkbox = make_checkbox(self.root, "", row=6, column=7, columnspan=1, var=self.pt5_checkbox_value, inner_padx=0, inner_pady=0, outer_padx=(0, 15), sticky=W)
        self.pt5_checkbox.deselect()
        self.pt5_checkbox.bind('<Button-1>', self.__update_pt5_checked)

    def _build_pt6(self):
        # text
        self.pt6_label = make_text(self.root, content="Pt 6: " + str(self.coords_list[5]), bg=tkcolour_from_rgb(PASTEL_PINK_RGB), column=5, row=7, width=18, columnspan=1, padx=0, state=NORMAL)
        # remove
        self.pt6_remove = make_button(self.root, text='x', width=1, command=lambda:self.__remove_pt(6), row=7, column=6, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10, highlightthickness=0)
        # checkbox
        self.pt6_checkbox = make_checkbox(self.root, "", row=7, column=7, columnspan=1, var=self.pt6_checkbox_value, inner_padx=0, inner_pady=0, outer_padx=(0, 15), sticky=W)
        self.pt6_checkbox.deselect()
        self.pt6_checkbox.bind('<Button-1>', self.__update_pt6_checked)

    def _build_pt7(self):
        # text
        self.pt7_label = make_text(self.root, content="Pt 7: " + str(self.coords_list[6]), bg=tkcolour_from_rgb(PASTEL_PINK_RGB), column=5, row=8, width=18, columnspan=1, padx=0, state=NORMAL)
        # remove
        self.pt7_remove = make_button(self.root, text='x', width=1, command=lambda:self.__remove_pt(7), row=8, column=6, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10, highlightthickness=0)
        # checkbox
        self.pt7_checkbox = make_checkbox(self.root, "", row=8, column=7, columnspan=1, var=self.pt7_checkbox_value, inner_padx=0, inner_pady=0, outer_padx=(0, 15), sticky=W)
        self.pt7_checkbox.deselect()
        self.pt7_checkbox.bind('<Button-1>', self.__update_pt7_checked)

    def _build_pt8(self):
        # text
        self.pt8_label = make_text(self.root, content="Pt 8: " + str(self.coords_list[7]), bg=tkcolour_from_rgb(PASTEL_PINK_RGB), column=5, row=9, width=18, columnspan=1, padx=0, state=NORMAL)
        # remove
        self.pt8_remove = make_button(self.root, text='x', width=1, command=lambda:self.__remove_pt(8), row=9, column=6, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10, highlightthickness=0)
        # checkbox
        self.pt8_checkbox = make_checkbox(self.root, "", row=9, column=7, columnspan=1, var=self.pt8_checkbox_value, inner_padx=0, inner_pady=0, outer_padx=(0, 15), sticky=W)
        self.pt8_checkbox.deselect()
        self.pt8_checkbox.bind('<Button-1>', self.__update_pt8_checked)

    def _build_use_mask_button(self):
        self.use_mask_button = make_button(self.root, text='Use this mask', width=13, command=self.__use_coords, row=10, column=5, columnspan=3, inner_pady=5, outer_padx=(0, 15), outer_pady=(10, 15))

    def _build_upload_mask_button(self):
        self.upload_mask_button = make_button(self.root, text='Upload .csv mask', width=16, command=self.__upload_mask, row=10, column=0, columnspan=5, inner_pady=5, outer_padx=15, outer_pady=(10, 15))

    def _build_original_image(self, data):
        if data is None:
            # Placeholder
            self.original_image = make_label(self.root, "original image placeholder", row=2, column=0, rowspan=8, columnspan=5, inner_pady=80, inner_padx=120, outer_padx=(15, 10), outer_pady=(15, 10))
        else:
            logging.debug("BUILDING ORIGINAL COLOUR IMAGE...")
            (self.original_image_graph, self.original_image, self.image_array) = make_image(self.root, data, row=2, column=0, columnspan=5, rowspan=8, lower_scale_value=None, upper_scale_value=None, color_rgb=PASTEL_PINK_RGB, original=True, figheight=2.5, figwidth=3.5)
            self.listener._image_array_to_og_data(self.image_array)
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
                for yi in range(-4, 5):
                    copy_data[(x+xi)%480, (y+yi)%640, :] = BRIGHT_GREEN_RGB
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

    # Commands (Callbacks)
    def __use_coords(self):
        # produces a 640x480 8-bit mask
        polygon = [point for point in self.coords_list if point != (None, None)]
        img = Image.new('L', (640, 480), 0)
        ImageDraw.Draw(img).polygon(polygon, outline=1, fill=1)
        self.mask_raw = np.array(img)
        mask = self.__process_mask(self.mask_raw)
        self.listener.submit_mask(mask) # re-transpose the mask - original data is transposed

    def __process_mask(self, mask_raw):
        mask = np.logical_not(mask_raw)
        mask = np.fliplr(mask.T)
        return mask

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
                coords.append((int(float(row[0])), (int(float(row[1])))))
        for i in range(8-len(coords)):
            coords.append((None, None))
        self.coords_list = coords
        self._build_points()
        self._draw_points()

    def __remove_pt(self, index):
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
            x = int((eventorigin.x - 54)*640/260)
            y = int((eventorigin.y - 18)*480/192)
            if 0 <= x < 640 and 0 <= y < 640:
                self.__add_pt((x, y))
        else:
            x = int(((eventorigin.x) - 53)*640/734)
            y = int(((eventorigin.y) - 128)*480/550)
            if 0 <= x < 640 and 0 <= y < 640:
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
