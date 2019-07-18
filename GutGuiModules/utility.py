from tkinter import *
from tkinter.ttk import Notebook
from GutGuiModules.constants import *
import numpy as np
from PIL import Image
from matplotlib import cm
import imageio

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def init():
    root = Tk()
    root.resizable(width=False, height=False)
    root.title(WINDOW_TITLE)
    root.geometry("+0+0")

    notebook = Notebook(root)

    input_output = Frame(notebook)
    input_output.pack()
    notebook.add(input_output, text="Input and Output")

    image_diagram = Frame(notebook)
    image_diagram.pack()
    notebook.add(image_diagram, text="Images and Diagrams")

    notebook.pack()

    return root, input_output, image_diagram

def tkcolour_from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code"""
    return "#%02x%02x%02x" % rgb

def frame_and_label(window, name, colour, row, column, rowspan, columnspan, labelspan=1, wraplength=140, label=True):
    frame = Frame(window, bg=tkcolour_from_rgb(colour), highlightbackground=tkcolour_from_rgb(BORDER), highlightcolor=tkcolour_from_rgb(BORDER), highlightthickness=2)
    frame.grid(row=row, rowspan=rowspan, column=column, columnspan=columnspan, sticky=W+E+N+S)
    if label:
        label = make_label(frame, text=name, row=0, column=0, borderwidth=2, columnspan=labelspan, wraplength=wraplength)
        return frame, label
    else:
        return frame
        

def make_button(window, text, command, row, column, height=1, width=10, 
    inner_padx=10, inner_pady=10, outer_padx=0, outer_pady=0, columnspan=1, rowspan=1, highlightthickness=1):
    button = Button(window, text=text, command=command, padx=inner_padx, pady=inner_pady, height=height, width=width, highlightthickness=highlightthickness)
    button.grid(row=row, column=column, padx=outer_padx, pady=outer_pady, columnspan=columnspan, rowspan=rowspan)
    return button

def make_label(window, text, row, column,
               borderwidth=2, inner_padx=1, inner_pady=1, outer_padx=0, outer_pady=15, relief="solid", rowspan=1, columnspan=1, wraplength=140):
    label = Label(window, text=text, borderwidth=borderwidth, relief=relief,
                  padx=inner_padx, pady=inner_pady, wraplength=wraplength)
    label.grid(row=row, column=column, padx=outer_padx, pady=outer_pady, columnspan=columnspan, rowspan=rowspan)
    return label

def make_text(window, content, row, column, padx=0, pady=0, height=1, width=2,
              highlightthickness=0, bg="white", columnspan=1,  rowspan=1, state=DISABLED):
    text = Text(window, bg=bg, height=height, width=width, highlightthickness=highlightthickness)
    text.insert(END, content)
    text.config(state=state)
    text.grid(row=row, column=column, padx=padx, pady=pady, columnspan=columnspan, rowspan=rowspan)
    return text

def make_listbox(window, row, column, padx=0, pady=0,
                 highlightthickness=0, columnspan=1,  rowspan=1):
    listbox = Listbox(window, width=28, highlightthickness=highlightthickness, selectmode=EXTENDED)
    listbox.grid(row=row, column=column, padx=padx, pady=pady, rowspan=rowspan, columnspan=columnspan)
    return listbox

def make_entry(window, row, column, width, columnspan=1, pady=0, 
    padx=0, highlightthickness=0):
    entry = Entry(window, width=width, highlightthickness=highlightthickness, textvariable=StringVar())
    entry.grid(row=row, column=column, columnspan=columnspan, padx=padx, pady=pady)
    return entry

def make_checkbox(window, text, row, column, var, columnspan=1,
                  inner_padx=1, inner_pady=1, outer_padx=0, outer_pady=0, bg="yellow", sticky=W+N+S+E):
    checkbox = Checkbutton(window, text=text, variable=var,padx=inner_padx, pady=inner_pady, bg=bg, width=2)
    checkbox.grid(row=row, column=column, padx=outer_padx, pady=outer_pady, sticky=sticky, columnspan=columnspan)
    return checkbox

def make_image(window, image_data, row, column, columnspan, rowspan,
               lower_scale_value, upper_scale_value, color_rgb, figwidth=3, figheight=2, original=False):
    graph = Figure(figsize=(figwidth, figheight))
    axes = graph.add_subplot(111)
    if original:
        image = axes.imshow(np.flipud(image_data[:,:,:]), origin='lower', cmap='jet')
        axes.axis('off')
        image_array = image.get_array().flatten()
    else:

        image = axes.imshow(image_data[:,:].T, origin='lower', cmap='jet',
                    vmin=float(lower_scale_value),
                    vmax=float(upper_scale_value))
        image_array = image.get_array().flatten()

    graph.patch.set_facecolor(rgb_to_rgba(color_rgb))
    graph.set_tight_layout('True')
    image = FigureCanvasTkAgg(graph, master=window)
    image.draw()
    image.get_tk_widget().grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan)
    return graph, image, image_array

def make_popup_image(graph, graphsize=(8,8), interactive = False):
    window = Toplevel()
    window.geometry("+0+0")
    graph.set_size_inches(graphsize[0], graphsize[1])
    image = FigureCanvasTkAgg(graph, master=window)
    image.draw()
    image.get_tk_widget().grid(column=0, row=0)
    if interactive == True:
        return (window, image)

def image_to_array(filename):
    return imageio.imread(filename)

def make_info(title, info):
    window = Toplevel()
    window.title(title)
    window.geometry("+0+0")
    text = Text(window, height=20, width=50, wrap=WORD, highlightthickness=0) 
    text.insert(END, info)
    text.grid(padx=5, pady=5)
    window.resizable(width=False, height=False)

def rgb_to_rgba(rgb):
    r = rgb[0]/255
    g = rgb[1]/255
    b = rgb[2]/255
    return r, g, b

def progress(val, total):
        update = ['-', '\\', '|', '/']
        if val != total-1:
            print(update[val%4] + ' ' + str(val+1) + '%', end="\r", flush=True)
        else:
            print(update[val%4] + ' ' + str(val+1) + '%')




