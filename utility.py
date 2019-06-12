from tkinter import *
from constants import *

def init():
    root = Tk()
    root.resizable(width=False, height=False)
    root.title(WINDOW_TITLE)
    root.geometry("+0+0")
    window = Frame(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
    window.pack()
    return window

def tkcolour_from_rgb(rgb):
    # translates an rgb tuple of int to a tkinter friendly color code
    return "#%02x%02x%02x" % rgb

def frame_and_label(window, name, colour, width, height, row, column, rowspan, columnspan):
    '''Returns a frame and its label, with the name "name", frame colour (in rbg)'''
    frame = Frame(window, bg=tkcolour_from_rgb(colour))
    frame.grid(row=row, rowspan=rowspan, column=column, columnspan=columnspan, sticky=W+E+N+S,
              ipadx=width, ipady=height)
    label = Label(frame, text=name, borderwidth=2, relief="solid")
    label.grid(row=0, column=0)
    return (frame, label)

def make_button(window, text, command, padx, pady, row, column):
    button = Button(window, text=text, command=command, padx=padx, pady=pady)
    button.grid(row=row, column=column)
    return button
