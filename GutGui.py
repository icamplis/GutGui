from tkinter import *
from utility import *
from constants import *
from init import *

def main():
    window = Tk()

    init_window(window)

    init_source_and_output(window)

    init_analysis_and_form(window)

    init_save(window)

    init_og_color(window)

    init_diagram(window)

    init_histogram(window)

    init_recreated_color(window)

    init_new_color(window)

    init_absorption_spec(window)

    window.mainloop()

if __name__ == '__main__':
    main()