from HyperGuiModules.utility import *
import matplotlib.pyplot as plt
import matplotlib
from tkinter import filedialog, messagebox
import csv
import logging
matplotlib.use("TkAgg")


class HistCalculation:
    def __init__(self, hist_calculation, listener):
        self.root = hist_calculation

        # Listener
        self.listener = listener

        self.output_path = None

        self.math = '-'

        self.hist1_button = None
        self.hist2_button = None
        self.calc_button = None

        self.data1_stats = [None, None, None, None]
        self.data2_stats = [None, None, None, None]
        self.data3_stats = [None, None, None, None]

        self.data1 = None
        self.data2 = None
        self.data3 = None

        self.drop_down_var = StringVar()
        self.choices = ['-', '+', 'x', '/']

        self.bins = None
        self.contents = None
        self.graph = None
        self.axes = None

        self.info_label = None

        self._init_widget()

    # ------------------------------------------------ INITIALIZATION ------------------------------------------------

    def _init_widget(self):
        self._build_buttons()
        self._build_reset_buttons()
        self._build_save_buttons()
        self._build_drop_down()
        self._build_equals()
        self._build_hist(None, None, 0, self.data1_stats)
        self._build_hist(None, None, 2, self.data2_stats)
        self._build_hist(None, None, 4, self.data3_stats)
        self._build_scale(self.data1_stats, 0)
        self._build_scale(self.data2_stats, 5)
        self._build_scale(self.data3_stats, 10)
        self._build_info_label()

    # --------------------------------------------------- BUILDERS ---------------------------------------------------

    def _build_buttons(self):
        self.hist1_button = make_button(self.root, text="Choose First Histogram",
                                        command=self.__update_data1, row=1, column=0, outer_pady=(0, 5),
                                        outer_padx=15, width=23, height=1, columnspan=4)
        self.hist2_button = make_button(self.root, text="Choose Second Histogram",
                                        command=self.__update_data2, row=1, column=5, outer_pady=(0, 5),
                                        outer_padx=15, width=23, height=1, columnspan=4)
        self.calc_button = make_button(self.root, text="Calculate Histogram",
                                       command=self.__calculate, row=1, column=10, outer_pady=(0, 5),
                                       outer_padx=15, width=23, height=1, columnspan=4)

    def _build_reset_buttons(self):
        make_button(self.root, text="Reset", command=self.__reset_data1, row=7, column=0, outer_padx=15,
                    width=6, height=1, columnspan=4, outer_pady=15)
        make_button(self.root, text="Reset", command=self.__reset_data2, row=7, column=5, outer_padx=15,
                    width=6, height=1, columnspan=4, outer_pady=15)
        make_button(self.root, text="Reset", command=self.__reset_data3, row=7, column=10, outer_padx=15,
                    width=6, height=1, columnspan=4, outer_pady=15)

    def _build_save_buttons(self):
        make_button(self.root, text="Select Output Folder", command=self.__select_output, row=2, column=14,
                    outer_padx=15, width=15, height=1, columnspan=1, outer_pady=(35, 5), inner_pady=5)
        make_button(self.root, text="Save as CSV", command=self.__save_as_csv, row=3, column=14, outer_padx=15,
                    width=15, height=1, columnspan=1, outer_pady=(0, 5), inner_pady=5)
        make_button(self.root, text="Save as Image", command=self.__save_as_image, row=4, column=14, outer_padx=15,
                    width=15, height=1, columnspan=1, outer_pady=(0, 55), inner_pady=5)

    def _build_drop_down(self):
        self.drop_down_var.set(self.choices[0])
        self.drop_down_menu = OptionMenu(self.root, self.drop_down_var, *self.choices, command=self.__update_math)
        self.drop_down_menu.configure(highlightthickness=0, width=1, anchor='w', padx=15)
        self.drop_down_menu.grid(column=4, row=2, columnspan=1, padx=0, rowspan=3)

    def _build_scale(self, stats, col):
        if col == 0:
            (self.data1_minx, self.data1_maxx, self.data1_miny, self.data1_maxy) = self._build_scale_helper(stats, col)
        elif col == 5:
            (self.data2_minx, self.data2_maxx, self.data2_miny, self.data2_maxy) = self._build_scale_helper(stats, col)
        elif col == 10:
            (self.data3_minx, self.data3_maxx, self.data3_miny, self.data3_maxy) = self._build_scale_helper(stats, col)

    def _build_scale_helper(self, stats, col):
        bg = tkcolour_from_rgb(BACKGROUND)
        print(stats)
        # min x
        make_text(self.root, content="Min x: ", bg=bg, column=col, row=5, width=7, pady=(0, 10), padx=(25, 5))
        min_x_input = make_entry(self.root, row=5, column=col+1, width=7, pady=(0, 10), padx=(0, 30))
        min_x_input.bind('<Return>', lambda x: self.__update_scales(col))
        min_x_input.insert(END, str(stats[0]))
        # max x
        make_text(self.root, content="Max x: ", bg=bg, column=col+2, row=5, width=7, pady=(0, 10), padx=(0, 5))
        max_x_input = make_entry(self.root, row=5, column=col+3, width=7, pady=(0, 10), padx=(0, 25))
        max_x_input.bind('<Return>', lambda x: self.__update_scales(col))
        max_x_input.insert(END, str(stats[1]))
        # min y
        make_text(self.root, content="Min y: ", bg=bg, column=col, row=6, width=7, pady=(0, 10), padx=(25, 5))
        min_y_input = make_entry(self.root, row=6, column=col+1, width=7, pady=(0, 10), padx=(0, 30))
        min_y_input.bind('<Return>', lambda x: self.__update_scales(col))
        min_y_input.insert(END, str(stats[2]))
        # max x
        make_text(self.root, content="Max y: ", bg=bg, column=col+2, row=6, width=7, pady=(0, 10), padx=(0, 5))
        max_y_input = make_entry(self.root, row=6, column=col+3, width=7, pady=(0, 10), padx=(0, 25))
        max_y_input.bind('<Return>', lambda x: self.__update_scales(col))
        max_y_input.insert(END, str(stats[3]))
        return min_x_input, max_x_input, min_y_input, max_y_input

    def _build_equals(self):
        equals = make_text(self.root, content="=",  bg=tkcolour_from_rgb(BACKGROUND), column=9, row=2, width=3,
                           columnspan=1, padx=0, rowspan=3)
        equals.config(font=("Courier", 44))

    def _build_hist(self, bins, contents, column, stats):
        # create canvas
        self.graph = Figure(figsize=(3, 2))
        self.axes = self.graph.add_subplot(111)
        self.graph.patch.set_facecolor(rgb_to_rgba(BACKGROUND))
        if contents is not None:
            # plot histogram
            # print(contents, bins)
            self.axes.hist(contents, bins=bins)
            # set axes
            self.graph.set_tight_layout(True)
            self.axes.set_xlim(left=stats[0], right=stats[1])
            self.axes.set_ylim(bottom=stats[2], top=stats[3])
            # commas and non-scientific notation
            self.axes.ticklabel_format(style='plain')
            self.axes.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(self.format_axis))
            self.axes.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(self.format_axis))

        # draw figure
        self.interactive_histogram = FigureCanvasTkAgg(self.graph, master=self.root)
        self.interactive_histogram.draw()
        self.interactive_histogram.get_tk_widget().grid(column=int(2.5*column), row=2, columnspan=4, rowspan=3, ipady=5,
                                                        ipadx=0, pady=(0, 20), padx=0)
        self.interactive_histogram.get_tk_widget().bind('<Button-2>', self.__pop_up_image)

    def _build_info_label(self):
        self.info_label = make_label_button(self.root, text='Histogram Calculation', command=self.__info, width=16)
        self.info_label.grid(columnspan=2, pady=(25, 30))

    # -------------------------------------------------- CALLBACKS ---------------------------------------------------

    def __calculate(self):
        if self.data1 is None or self.data2 is None:
            messagebox.showerror("Error", "Please select two csv files.")
        elif self.data1_bin_width != self.data2_bin_width:
            messagebox.showerror("Error", "Please ensure your files have the same bin width. Currently your first "
                                          "csv file has a bin width of " + str(self.data1_bin_width) + " while your "
                                          "second csv file has a bin width of " + str(self.data2_bin_width) + ".")
        elif self.data1[0][0] != self.data2[0][0] and self.data1[0][-1] != self.data2[0][-1]:
            messagebox.showerror("Error", "Please ensure your start and end with the same bin. Currently your first "
                                          "csv file begins with a bin at " + str(self.data1[0][0]) + " and ends with a "
                                          "bin at " + str(self.data1[0][-1]) + " while your second csv file begins "
                                          "with a bin at " + str(self.data2[0][0]) + " and ends with a bin at " +
                                          str(self.data2[0][-1]) + ".")
        else:
            self.bins = self.data1[0]
            if self.math == '-':
                data = np.asarray(self.data1[2]) - np.asarray(self.data2[2])
            elif self.math == '+':
                data = np.asarray(self.data1[2]) + np.asarray(self.data2[2])
            elif self.math == 'x':
                data = np.asarray(self.data1[2]) * np.asarray(self.data2[2])
            elif self.math == '/':
                contents = np.asarray(self.data1[2]) / np.asarray(self.data2[2])
                data = [int(i) for i in contents]
            self.contents = []
            for i in range(len(data)):
                self.contents += [self.bins[i] for _ in range(data[i])]
            self.data3_stats = [np.min(self.bins), np.max(self.bins), 0, np.max(data)]
            self.data3 = [self.bins, self.contents, data]
            self.initial_data3 = [self.bins, self.contents, data]
            self.initial_stats3 = self.data3_stats
        self._build_hist(self.data3[0], self.data3[1], 4, self.data3_stats)
        self._build_scale(self.data3_stats, 10)


    @staticmethod
    def format_axis(x, p):
        if x % 1 == 0:
            return format(int(x), ',')
        else:
            return format(round(x, 2))

    def __update_data1(self):
        data1_path = filedialog.askopenfilename(parent=self.root, title="Please select a .csv file containing histogram"
                                                                        "data.")
        if data1_path == '' or data1_path is None:
            return None
        if data1_path[-4:] != ".csv":
            messagebox.showerror("Error", "That's not a .csv file!")
        else:
            self.data1_bin_width, self.data1, self.data1_stats = self.__load_data(data1_path)
            self._build_hist(self.data1[0], self.data1[1], 0, self.data1_stats)
            self._build_scale(self.data1_stats, 0)
            self.initial_data1 = self.data1
            self.initial_stats1 = self.data1_stats

    def __update_data2(self):
        data2_path = filedialog.askopenfilename(parent=self.root, title="Please select a .csv file containing histogram"
                                                                        "data.")
        if data2_path == '' or data2_path is None:
            return None
        if data2_path[-4:] != ".csv":
            messagebox.showerror("Error", "That's not a .csv file!")
        else:
            self.data2_bin_width, self.data2, self.data2_stats = self.__load_data(data2_path)
            self._build_hist(self.data2[0], self.data2[1], 2, self.data2_stats)
            self._build_scale(self.data2_stats, 5)
            self.initial_data2 = self.data2
            self.initial_stats2 = self.data2_stats

    @staticmethod
    def __load_data(path):
        bins = []
        contents = []
        with open(path) as csvfile:
            read_csv = csv.reader(csvfile, delimiter=',')
            for row in read_csv:
                bins.append(float(row[0]))
                contents.append(int(float(row[1])))
        cont = []
        for i in range(len(contents)):
            cont += [bins[i] for _ in range(contents[i])]
        bin_width = round(np.abs(bins[1] - bins[2]), 7)
        data = [bins, cont, contents]
        stats = [np.min(bins), np.max(bins), np.min(contents), np.max(contents)]
        print(stats)
        return bin_width, data, stats

    def __update_scales(self, col):
        if col == 0:
            print('updating')
            minx = float(self.data1_minx.get())
            maxx = float(self.data1_maxx.get())
            miny = float(self.data1_miny.get())
            maxy = float(self.data1_maxy.get())
            self.data1_stats = [minx, maxx, miny, maxy]
            self._build_hist(self.data1[0], self.data1[1], 0, self.data1_stats)
        elif col == 5:
            minx = float(self.data2_minx.get())
            maxx = float(self.data2_maxx.get())
            miny = float(self.data2_miny.get())
            maxy = float(self.data2_maxy.get())
            self.data2_stats = [minx, maxx, miny, maxy]
            self._build_hist(self.data2[0], self.data2[1], 2, self.data2_stats)
        elif col == 10:
            minx = float(self.data3_minx.get())
            maxx = float(self.data3_maxx.get())
            miny = float(self.data3_miny.get())
            maxy = float(self.data3_maxy.get())
            self.data3_stats = [minx, maxx, miny, maxy]
            self._build_hist(self.data3[0], self.data3[1], 4, self.data3_stats)

    def __reset_data1(self):
        print('resetting')
        self.data1_stats = self.initial_stats1
        self.data1 = self.initial_data1
        self._build_hist(self.data1[0], self.data1[1], 0, self.data1_stats)
        self._build_scale(self.data1_stats, 0)

    def __reset_data2(self):
        self.data2_stats = self.initial_stats2
        self.data2 = self.initial_data2
        self._build_hist(self.data2[0], self.data2[1], 2, self.data2_stats)
        self._build_scale(self.data2_stats, 5)

    def __reset_data3(self):
        self.data3_stats = self.initial_stats3
        self.data3 = self.initial_data3
        self._build_hist(self.data3[0], self.data3[1], 4, self.data3_stats)
        self._build_scale(self.data3_stats, 10)

    def __update_math(self, event):
        self.math = self.drop_down_var.get()
        self.__calculate()

    def __info(self):
        info = self.listener.modules[INFO].hist_calc_info
        title = "Histogram Calculation Information"
        make_info(title=title, info=info)

    def __pop_up_image(self, event):
        make_popup_image(self.graph)

    def __select_output(self):
        title = "Please select an output folder."
        self.output_path = filedialog.askdirectory(parent=self.root, title=title)

    def __save_as_csv(self):
        if self.output_path is None:
            messagebox.showerror("Error", "Please select an output folder before saving data.")
        if self.data3 is None:
            messagebox.showerror("Error", "Please generate a histogram to save.")
        else:
            (x_low, x_high, y_low, y_high) = self.data3_stats

            step = self.data1_bin_width
            start = x_low
            stop = x_high + step + step
            bins = np.arange(start=start, stop=stop, step=step)

            bin_heights = self.data3[2]
            index1 = np.where(self.bins == x_low)[0][0]
            index2 = np.where(self.bins == x_high)[0][0]
            print(index1)
            print(index2)
            bin_heights = bin_heights[index1:index2+1]

            bin_heights = np.clip(bin_heights, a_min=y_low, a_max=y_high)
            hist_data = np.stack((bins[:-1], bin_heights)).T
            output_path = self.output_path + "/histogram_calculation.csv"
            logging.debug("SAVING DATA TO " + output_path)
            np.savetxt(output_path, hist_data, delimiter=",", fmt="%.2f")

    def __save_as_image(self):
        if self.output_path is None:
            messagebox.showerror("Error", "Please select an output folder before saving data.")
        if self.data3 is None:
            messagebox.showerror("Error", "Please generate a histogram to save.")
        else:
            output_path = self.output_path + "/histogram_calculation.png"
            logging.debug("SAVING HISTOGRAM TO " + output_path)
            bins = self.data3[0]
            contents = self.data3[1]
            stats = self.data3_stats
            plt.clf()
            axes = plt.subplot(111)
            axes.hist(contents, bins=bins)
            axes.set_xlim(left=stats[0], right=stats[1])
            axes.set_ylim(bottom=stats[2], top=stats[3])
            axes.ticklabel_format(style='plain')
            axes.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(self.format_axis))
            axes.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(self.format_axis))
            plt.savefig(output_path)
            plt.clf()
