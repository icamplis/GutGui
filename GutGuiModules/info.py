from GutGuiModules.utility import *
from tkinter import messagebox

class Info:
    def __init__(self, info_frame, listener):
        self.root = info_frame
        self.listener = listener
        self.info_button = None

        # INFORMATION
        self.info = "This is filler text\nWrite whatever you want here\n\n:)"

        self.source_output_info = "Source & Output Information"
        self.analysis_form_info = "Analysis & Form Information"
        self.csv_info = "Data to CSV Information"
        self.save_info = "Save Information"
        self.original_info = "Original Image Information"
        self.recreated_info = "Recreated Image Information"
        self.new_info = "New Image Information"
        self.diagram_info = "Diagram Information"
        self.hist_info = "Histogram Information"
        self.abspec_info = "Absorption Spec Information"

        self._init_widget()

    def get_source_output_info(self):
        return self.source_output_info

    def get_analysis_form_info(self):
        return self.analysis_form_info

    def get_csv_info(self):
        return self.csv_info

    def get_save_info(self):
        return self.save_info

    def get_original_info(self):
        return self.original_info

    def get_recreated_info(self):
        return self.recreated_info

    def get_new_info(self):
        return self.new_info

    def get_diagram_info(self):
        return self.diagram_info

    def get_hist_info(self):
        return self.hist_info

    def get_abspec_info(self):
        return self.abspec_info

    # Helper
    def _init_widget(self):
        self._make_info_button()

    def _make_info_button(self):
        self.info_button = make_button(self.root, text="App Info", command=self._info, row=0, column=0, outer_pady=15, outer_padx=(120,0), width=10, columnspan=8)

    def _info(self):
        make_info(title="App Information", info=self.info)
