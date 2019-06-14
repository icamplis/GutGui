from tkinter import *
from GutGuiModules.utility import *

class Diagram:
    def __init__(self, diagram_frame):
        self.root = diagram_frame

        self.whole_image_label = None
        self.whole_image_checkbox = None
        self.whole_image_checkbox_value = IntVar()

        self.masked_region_label = None
        self.masked_region_checkbox = None
        self.masked_region_checkbox_value = IntVar()

        self._init_widget()

    def get_whole_image_checkbox_value(self):
        return self.whole_image_checkbox_value

    def get_masked_region_checkbox_value(self):
        return self.masked_region_checkbox_value

    # Helper
    def _init_widget(self):
        self._build_whole_image()
        self._build_masked_region()

    def _build_whole_image(self):
        self.whole_image_label = make_label(self.root, "Whole Image", row=1, column=0, inner_padx=10, inner_pady=5, outer_padx=(10, 5), outer_pady=5)
        self.whole_image_checkbox = make_checkbox(self.root, "", row=1, 
            column=0, var=self.whole_image_checkbox_value, sticky=NE, 
            inner_padx=0, inner_pady=0)
        self.whole_image_checkbox.deselect()

    def _build_masked_region(self):
        self.masked_region_label = make_label(self.root, "Masked Region", row=1, column=1, inner_padx=10, inner_pady=5, outer_padx=(5, 15), outer_pady=5)
        self.masked_region_checkbox = make_checkbox(self.root, "", row=1, 
            column=1, var=self.masked_region_checkbox_value, sticky=NE,inner_padx=0, inner_pady=0, outer_padx=(0,5))
        self.masked_region_checkbox.deselect()
