from GutGuiModules.utility import *

class Diagram:
    def __init__(self, diagram_frame, listener):
        self.root = diagram_frame

        # Listener
        self.listener = listener

        self.whole_image_button = None
        self.whole_image_checkbox = None
        self.whole_image_checkbox_value = IntVar()

        self.masked_region_button = None
        self.masked_region_checkbox = None
        self.masked_region_checkbox_value = IntVar()

        self.is_masked = False

        self._init_widget()

    def get_is_masked(self):
        return self.is_masked

    def get_whole_image_checkbox_value(self):
        return self.whole_image_checkbox_value

    def get_masked_region_checkbox_value(self):
        return self.masked_region_checkbox_value

    # Helper
    def _init_widget(self):
        self._build_whole_image()
        self._build_masked_region()

    def _build_whole_image(self):
        self.whole_image_button = make_button(self.root, "Whole Image", row=1, column=0, command=self.__use_whole_image, inner_padx=15, inner_pady=5, outer_padx=15, outer_pady=(0, 10))
        self.whole_image_checkbox = make_checkbox(self.root, "", row=1, column=0,var=self.whole_image_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0, outer_padx=(0, 5))
        self.whole_image_checkbox.deselect()
        self.whole_image_button.config(foreground="red")

    def _build_masked_region(self):
        self.masked_region_button = make_button(self.root, "Masked Region", row=2, column=0, command=self.__use_masked_image, inner_padx=15, inner_pady=5, outer_padx=15, outer_pady=(0, 15))
        self.masked_region_checkbox = make_checkbox(self.root, "", row=2, column=0, var=self.masked_region_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0, outer_padx=(0, 5))
        self.masked_region_checkbox.deselect()

    def __use_whole_image(self):
        self.is_masked = False
        self.whole_image_button.config(foreground="red")
        self.masked_region_button.config(foreground="black")
        self.listener.submit_is_masked(self.is_masked)

    def __use_masked_image(self):
        self.is_masked = True
        self.masked_region_button.config(foreground="red")
        self.whole_image_button.config(foreground="black")
        self.listener.submit_is_masked(self.is_masked)