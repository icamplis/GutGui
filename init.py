from constants import *
from tkinter import *
from utility import *

def init_window(window):
    window.title(WINDOW_TITLE)  # set window title
    window.geometry(WINDOW_SIZE)  # set window size
    window.resizable(width=False, height=False)

def init_histogram(window):
    histogram_frame = Frame(window, bg=tkcolour_from_rgb(PASTEL_BLUE_RGB),
                            width=WINDOW_WIDTH / 5 * 2, height=WINDOW_HEIGHT / 4)
    histogram_frame.grid(row=1, column=3, columnspan=2, sticky=W + E + N + S)
    # histogram_label = Label(histogram_frame, text="Histogram                                                                                                                    ", borderwidth=2, relief="solid")
    # histogram_label.grid(row=0, column=0)


def init_diagram(window):
    diagram_frame = Frame(window, bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB),
                          width=WINDOW_WIDTH / 5 * 2, height=WINDOW_HEIGHT / 4)
    diagram_frame.grid(row=0, column=3, columnspan=2, sticky=W + E + N + S)
    # diagram_label = Label(diagram_frame, text="Diagram Image                                                                                                             ", borderwidth=2, relief="solid")
    # diagram_label.grid(row=0, column=0)


def init_og_color(window):
    og_color_frame = Frame(window, bg=tkcolour_from_rgb(PASTEL_PINK_RGB),
                           width=WINDOW_WIDTH / 5 * 2, height=WINDOW_HEIGHT / 4 * 2)
    og_color_frame.grid(row=0, rowspan=2, column=1, columnspan=2, sticky=W + E + N + S)
    ogc_label = Label(og_color_frame,
                      text="Original Colour-Coded Image                                                                             ",
                      borderwidth=2, relief="solid")
    ogc_label.grid(row=0, column=0)


def init_save(window):
    save_frame = Frame(window, bg=tkcolour_from_rgb(PASTEL_PINK_RGB),
                       width=WINDOW_WIDTH / 5, height=WINDOW_HEIGHT / 4)
    save_frame.grid(row=3, column=0, sticky=W + E + N + S)
    s_label = Label(save_frame, text="Save                                                 ",
                    borderwidth=2, relief="solid")
    s_label.grid(row=0, column=0)


def init_analysis_and_form(window):
    analysis_and_form_frame = Frame(window, bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB),
                                    width=WINDOW_WIDTH / 5, height=WINDOW_HEIGHT / 4 * 2)
    analysis_and_form_frame.grid(row=1, rowspan=2, column=0, sticky=W + E + N + S)
    anf_label = Label(analysis_and_form_frame, text="Analysis & Form                                ",
                      borderwidth=2, relief="solid")
    anf_label.grid(row=0, column=0)


def init_source_and_output(window):
    source_and_output_frame = Frame(window, bg=tkcolour_from_rgb(PASTEL_BLUE_RGB),
                                    width=WINDOW_WIDTH / 5, height=WINDOW_HEIGHT / 4)
    source_and_output_frame.grid(row=0, column=0, sticky=W + E + N + S)
    sno_label = Label(source_and_output_frame, text="Source & Output                              ",
                      borderwidth=2, relief="solid")
    sno_label.grid(row=0, column=0)

def init_recreated_color(window):
    recreated_color_frame = Frame(window, bg=tkcolour_from_rgb(PASTEL_BLUE_RGB),
                                  width=WINDOW_WIDTH / 5, height=WINDOW_HEIGHT / 4 * 2)
    recreated_color_frame.grid(row=2, rowspan=2, column=1, sticky=W + E + N + S)
    recreated_color_label = Label(recreated_color_frame, text="Recreated Color-Coded Image            ",
                                  borderwidth=2, relief="solid")
    recreated_color_label.grid(row=0, column=0)


def init_new_color(window):
    new_color_frame = Frame(window, bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB),
                            width=WINDOW_WIDTH / 5, height=WINDOW_HEIGHT / 4 * 2)
    new_color_frame.grid(row=2, rowspan=2, column=2, sticky=W + E + N + S)
    new_color_label = Label(new_color_frame, text="New Color-Coded Image                  ",
                            borderwidth=2, relief="solid")
    new_color_label.grid(row=0, column=0)


def init_absorption_spec(window):
    absorption_spec_frame = Frame(window, bg=tkcolour_from_rgb(PASTEL_PINK_RGB),
                                  width=WINDOW_WIDTH / 5 * 2, height=WINDOW_HEIGHT / 4 * 2)
    absorption_spec_frame.grid(row=2, rowspan=2, column=3, columnspan=2, sticky=W + E + N + S)
    # absorption_spec_label = Label(absorption_spec_frame, text="Absorption Spectrum                                        "
    #                                                           "                                                           ",
    #                               borderwidth=2, relief="solid")
    # absorption_spec_label.grid(row=0, column=0)
