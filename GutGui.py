from tkinter import *
from utility import *
from constants import *

def main():
    window = Tk()

    # to rename the title of the window
    initialize_window(window)

    # input_frame = Frame(window, bg=tkcolour_from_rgb(PASTEL_BLUE_RGB),
    #                       width=WINDOW_WIDTH/5, height = WINDOW_HEIGHT)
    # output_frame = Frame(window, bg=tkcolour_from_rgb(PASTEL_PINK_RGB),
    #                        width=WINDOW_WIDTH/5*4, height=WINDOW_HEIGHT)
    #
    # input_frame.grid(row=0, column=0)  # don't use pack and grid in same program
    # output_frame.grid(row=0, column=1)

    source_and_output_frame = Frame(window, bg=tkcolour_from_rgb(PASTEL_BLUE_RGB),
                                    width=WINDOW_WIDTH/5, height = WINDOW_HEIGHT/4)
    source_and_output_frame.grid(row=0, column=0)

    analysis_and_form_frame = Frame(window, bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB),
                                    width=WINDOW_WIDTH / 5, height =WINDOW_HEIGHT / 4 * 2)
    analysis_and_form_frame.grid(row=1, rowspan=2, column=0)

    save_frame = Frame(window, bg=tkcolour_from_rgb(PASTEL_PINK_RGB),
                       width=WINDOW_WIDTH / 5, height =WINDOW_HEIGHT / 4)
    save_frame.grid(row=3, column=0)

    og_color_frame = Frame(window, bg=tkcolour_from_rgb(PASTEL_PINK_RGB),
                           width=WINDOW_WIDTH / 5 * 2, height =WINDOW_HEIGHT / 4 * 2)
    og_color_frame.grid(row=0, rowspan=2, column=1, columnspan=2)

    diagram_frame = Frame(window, bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB),
                          width=WINDOW_WIDTH / 5 * 2, height =WINDOW_HEIGHT / 4)
    diagram_frame.grid(row=0, column=3, columnspan=2)

    histogram_frame = Frame(window, bg=tkcolour_from_rgb(PASTEL_BLUE_RGB),
                            width=WINDOW_WIDTH / 5 * 2, height = WINDOW_HEIGHT/4)
    histogram_frame.grid(row=1, column=3, columnspan=2)

    recreated_color_frame = Frame(window, bg=tkcolour_from_rgb(PASTEL_BLUE_RGB),
                                  width=WINDOW_WIDTH / 5, height = WINDOW_HEIGHT / 4 * 2)
    recreated_color_frame.grid(row=2, rowspan=2, column=1)

    new_color_frame = Frame(window, bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB),
                            width=WINDOW_WIDTH / 5, height =WINDOW_HEIGHT / 4 * 2)
    new_color_frame.grid(row=2, rowspan=2, column=2)

    absorption_spec_frame = Frame(window, bg=tkcolour_from_rgb(PASTEL_PINK_RGB),
                                  width=WINDOW_WIDTH / 5 * 2, height =WINDOW_HEIGHT / 4 * 2)
    absorption_spec_frame.grid(row=2, rowspan=2, column=3, columnspan=2)

    window.mainloop()

if __name__ == '__main__':
    main()