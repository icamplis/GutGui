from tkinter import *
from utility import *
from constants import *

global window
root = Tk()
root.resizable(width=False, height=False)
root.title(WINDOW_TITLE)
root.geometry("+0+0")
window = Frame(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
window.pack()

def frame_and_label(name, colour, width, height, row, column, rowspan, columnspan):
    '''Returns a frame and its label, with the name "name", frame colour (in rbg)'''
    global window
    frame = Frame(window, bg=tkcolour_from_rgb(colour))
    frame.grid(row=row, rowspan=rowspan, column=column, columnspan=columnspan, sticky=W+E+N+S,
              ipadx=width, ipady=height)
    label = Label(frame, text=name, borderwidth=2, relief="solid")
    label.grid(row=0, column=0)
    return (frame, label)

def main():
    global window
    
    # source and output
    (source_and_output_frame, sno_label) = frame_and_label("Source & Output", 
                    PASTEL_BLUE_RGB, SMALL_W, SMALL_H, 0, 0, 1, 1)
    
    # analysis and form
    (analysis_and_form_frame, anf_label) = frame_and_label("Analysis & Form", 
                    PASTEL_ORANGE_RGB, SMALL_W, BIG_H, 1, 0, 2, 1)
    
    # save
    (save_frame, s_label) = frame_and_label("Save", 
                    PASTEL_PINK_RGB, SMALL_W, SMALL_H, 3, 0, 1, 1)
    
    # original colour
    (og_color_frame, ogc_label) = frame_and_label("Original Colour-Coded Image", 
                    PASTEL_PINK_RGB, BIG_W, BIG_H, 0, 1, 2, 2)
    
    # recreated colour
    (recreated_color_frame, recreated_color_label) = frame_and_label("Recreated Color-Coded Image", 
                    PASTEL_BLUE_RGB, SMALL_W, BIG_H, 2, 1, 2, 1)
    
    # new colour
    (new_color_frame, new_color_label) = frame_and_label("New Color-Coded Image", 
                    PASTEL_ORANGE_RGB, SMALL_W, BIG_H, 2, 2, 2, 1)
    
    # diagram
    (diagram_frame, diagram_label) = frame_and_label("Diagram Image", 
                    PASTEL_ORANGE_RGB, BIG_W, SMALL_H, 0, 3, 1, 2)
    
    # histogram
    (histogram_frame, histogram_label) = frame_and_label("Histogram", 
                    PASTEL_BLUE_RGB, BIG_W, BIG_H, 1, 3, 1, 2)
    
    # absorption
    (absorption_spec_frame, absorption_spec_label) = frame_and_label("Absorption Spectrum", 
                    PASTEL_PINK_RGB, BIG_W, BIG_H, 2, 3, 2, 2)

    window.mainloop()

if __name__ == '__main__':
    main()