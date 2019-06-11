from tkinter import *
from utility import *
from constants import *
from init import *

def main():
    window = Tk()

    init_window(window)

    source_and_output_frame = init_source_and_output(window)

    analysis_and_form_frame = init_analysis_and_form(window)

    save_frame = init_save(window)

    og_color_frame = init_og_color(window)

    diagram_frame = init_diagram(window)

    histogram_frame = init_histogram(window)

    recreated_color_frame = init_recreated_color(window)

    new_color_frame = init_new_color(window)

    absorption_spec_frame = init_absorption_spec(window)

    window.mainloop()

if __name__ == '__main__':
    main()