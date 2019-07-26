from tkinter import *
from tkinter.ttk import Notebook, Style
from tkinter.ttk import Button as TButton
from GutGuiModules.constants import *
import numpy as np
from PIL import Image
from matplotlib import cm
import imageio
from math import atan, pi

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

def frame(window, colour, row, column, rowspan, columnspan,  wraplength=140):
    frame = Frame(window, bg=tkcolour_from_rgb(colour), highlightbackground=tkcolour_from_rgb(BORDER), highlightcolor=tkcolour_from_rgb(BORDER), highlightthickness=2)
    frame.grid(row=row, rowspan=rowspan, column=column, columnspan=columnspan, sticky=W+E+N+S)
    return frame

def make_button(window, text, command, row, column, height=1, width=10, 
    inner_padx=10, inner_pady=10, outer_padx=0, outer_pady=0, columnspan=1, rowspan=1, highlightthickness=1, wraplength=0):
    button = Button(window, text=text, command=command, padx=inner_padx, pady=inner_pady, height=height, width=width, highlightthickness=highlightthickness, wraplength=wraplength)
    button.grid(row=row, column=column, padx=outer_padx, pady=outer_pady, columnspan=columnspan, rowspan=rowspan)
    return button

def make_label_button(window, text, command, width):
    button = TButton(window, text=text, width=width, command=command)
    Style().configure("TButton", relief="solid", background=tkcolour_from_rgb((255, 255, 255)), bordercolor=tkcolour_from_rgb((0, 0, 0)), borderwidth=2)
    Style().theme_use('default')
    button.grid(row=0, column=0, padx=(15, 0), pady=15)
    return button

def make_label(window, text, row, column, borderwidth=2, inner_padx=1, inner_pady=1, outer_padx=0, outer_pady=15, relief="solid", rowspan=1, columnspan=1, wraplength=140):
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
    listbox = Listbox(window, width=16, highlightthickness=highlightthickness, selectmode=EXTENDED, height=7)
    listbox.grid(row=row, column=column, padx=padx, pady=pady, rowspan=rowspan, columnspan=columnspan)
    return listbox

def make_entry(window, row, column, width, columnspan=1, pady=0, 
    padx=0, highlightthickness=0):
    entry = Entry(window, width=width, highlightthickness=highlightthickness, textvariable=StringVar())
    entry.grid(row=row, column=column, columnspan=columnspan, padx=padx, pady=pady)
    return entry

def make_checkbox(window, text, row, column, var, columnspan=1,
                  inner_padx=1, inner_pady=1, outer_padx=0, outer_pady=0, bg=tkcolour_from_rgb(CHECKBOX), sticky=W+N+S+E):
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
    text.config(state="disabled")
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
            print(update[val%4] + ' ' + str(round((val+1)/total *100, 2)) + '%', end="\r", flush=True)
        else:
            print(update[val%4] + ' ' + str(round((val+1)/total *100, 2)) + '%')

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def rgb_to_angle(rgb):
    if rgb[0] == rgb[1] == rgb[2] == 0 or rgb[0] == rgb[1] == rgb[2] == 255:
        return 0
    
    a = rgb[0]-0.5
    b = 0.5-rgb[1]

    if a < 0:
        if b > 0:
            if atan(a/b)*180/pi >= 45:
                red = 0
            else:
                red = atan(a/b)*180/pi
        elif b == 0:
            red = 360 - 270
        else:
            red = 360 - (atan(a/b)*180/pi + 180)
    else:
        if b > 0:
            red = 360 - atan(a/b)*180/pi
        elif b == 0:
            red = 360 - 90
        else:
            red = 360 - (atan(a/b)*180/pi + 180)
            
    a = rgb[2]-0.5
    b = rgb[1]-0.5

    if a < 0:
        if b > 0:
            blue = 180-atan(a/b)*180/pi
        elif b == 0:
            blue = 270
        else:
            blue = 360-atan(a/b)*180/pi
    else:
        if b > 0:
            blue = 180 - atan(a/b)*180/pi
        elif b == 0:
            blue = 90
        else:
            blue = atan(-a/b)*180/pi
    
    if red == 0:
        return blue
    elif blue == 315:
        return red
    else:
        return (red+blue)/2


boi = cm.jet(np.arange(256))
jet_angles = [rgb_to_angle(i) for i in boi]

def angle_to_jet(angle):
    index = find_nearest(jet_angles, angle)
    return int(index)

def rgb_image_to_jet_array(img_array):
    array = []
    for i in range(len(img_array)):
        progress(i, len(img_array))
        for j in range(len(img_array[i])):
            zero = img_array[i][j][0]/255
            one = img_array[i][j][1]/255
            two = img_array[i][j][2]/255
            array.append(angle_to_jet(rgb_to_angle((zero, one, two))))
    return array

