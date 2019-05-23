from constants import *

def initialize_window(window):
    window.title(WINDOW_TITLE)
    window.geometry(WINDOW_SIZE)
    window.resizable(width=False, height=False)

def tkcolour_from_rgb(rgb):
    # translates an rgb tuple of int to a tkinter friendly color code
    return "#%02x%02x%02x" % rgb