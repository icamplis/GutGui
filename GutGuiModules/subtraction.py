from GutGuiModules.utility import *
from matplotlib.pyplot import cm
import matplotlib
from tkinter import filedialog, messagebox
import csv
matplotlib.use("TkAgg")


class Subtraction:
    def __init__(self, subtraction, listener):
        self.root = subtraction

        # Listener
        self.listener = listener

        self.hist1_button = None
        self.hist2_button = None
        self.calc_button = None

        self.data1 = None
        self.data2 = None
        self.subtracted_data = None

        self.bins = None
        self.contents = None
        self.graph = None
        self.axes = None

        self.info_label = None

        self._init_widget()

    # ------------------------------------------------ INITIALIZATION ------------------------------------------------

    def _init_widget(self):
        self._build_buttons()
        self._build_histogram()
        self._build_info_label()

    # --------------------------------------------------- BUILDERS ---------------------------------------------------

    def _build_buttons(self):
        self.hist1_button = make_button(self.root, text="Choose Primary Histogram",
                                        command=self.__update_data1, row=1, column=0, outer_pady=(0, 5),
                                        outer_padx=15, width=13, wraplength=120, height=2)
        self.hist2_button = make_button(self.root, text="Choose Secondary Histogram",
                                        command=self.__update_data2, row=1, column=1, outer_pady=(0, 5),
                                        outer_padx=15, width=13, wraplength=120, height=2)
        self.calc_button = make_button(self.root, text="Calculate Histogram",
                                       command=self.__calculate, row=1, column=2, outer_pady=(0, 5),
                                       outer_padx=15, width=13, wraplength=120, height=2)

    def _build_histogram(self):
        # create canvas
        self.graph = Figure(figsize=(5, 5))
        self.axes = self.graph.add_subplot(111)
        self.graph.patch.set_facecolor(rgb_to_rgba(BACKGROUND))
        if self.contents is not None:
            # plot histogram
            self.axes.hist(self.contents, bins=self.bins)
            self.axes.hist(self.data1[1], bins=self.data1[0])
            self.axes.hist(self.data2[1], bins=self.data2[0])
            self.axes.legend(['Subtracted Histogram', 'Primary Histogram', 'Secondary Histogram'])
            # set axes
            self.graph.set_tight_layout(True)
            # commas and non-scientific notation
            self.axes.ticklabel_format(style='plain')
            self.axes.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(self.format_axis))
            self.axes.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(self.format_axis))

        # draw figure
        self.interactive_histogram = FigureCanvasTkAgg(self.graph, master=self.root)
        self.interactive_histogram.draw()
        self.interactive_histogram.get_tk_widget().grid(column=0, row=2, columnspan=3, rowspan=7, ipady=5, ipadx=0,
                                                        pady=0)

    def _build_info_label(self):
        self.info_label = make_label_button(self.root, text='Histogram Subtraction', command=self.__info, width=16)

    # -------------------------------------------------- CALLBACKS ---------------------------------------------------

    def __calculate(self):
        if self.data1 is None or self.data2 is None:
            messagebox.showerror("Error", "Please select two csv files.")
        if self.data1_bin_width != self.data2_bin_width:
            messagebox.showerror("Error", "Please ensure your files have the same bin width. Currently your primary"
                                          "csv file has a bin width of " + str(self.data1_bin_width) + " while your"
                                          "second csv file has a bin width of " + str(self.data2_bin_width) + ".")
        else:
            min_len = min(len(self.data1[1]), len(self.data2[1]))
            self.bins = self.data1[0][:min_len]
            self.data1[1] = self.data1[1][:min_len]
            self.data2[1] = self.data2[1][:min_len]
            self.contents = np.asarray(self.data1[1]) - np.asarray(self.data2[1])
        self._build_histogram()

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
            self.data1_bin_width, self.data1 = self.__load_data(data1_path)

    def __update_data2(self):
        data2_path = filedialog.askopenfilename(parent=self.root, title="Please select a .csv file containing histogram"
                                                                        "data.")
        if data2_path == '' or data2_path is None:
            return None
        if data2_path[-4:] != ".csv":
            messagebox.showerror("Error", "That's not a .csv file!")
        else:
            self.data2_bin_width, self.data2 = self.__load_data(data2_path)

    @staticmethod
    def __load_data(path):
        bins = []
        contents = []
        with open(path) as csvfile:
            read_csv = csv.reader(csvfile, delimiter=',')
            for row in read_csv:
                bins.append(float(row[0]))
                contents.append(int(float(row[1])))
        bin_width = round(np.abs(bins[1] - bins[2]), 7)
        data = [bins, contents]
        return bin_width, data

    def __info(self):
        info = self.listener.modules[INFO].colour_info
        title = "Histogram Subtraction Information"
        make_info(title=title, info='')
