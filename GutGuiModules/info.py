from GutGuiModules.utility import *
from tkinter import messagebox

class Info:
    def __init__(self, info_frame, listener):
        self.root = info_frame
        self.listener = listener
        self.info_button = None
        self.info_text = None

        # INFORMATION
        self.info = "This is filler text\nWrite whatever you want here\n\n:)"

        self.source_output_info = "Source & Output Information"
        self.analysis_form_info = "Analysis Settings Information"
        self.csv_info = "Data to CSV Information"
        self.save_info = "Save Information"
        self.param_info = "Parameter Specification Information"
        self.original_info = "Original Image Information"
        self.input_info = "Here you can input coordinates manually. Make sure that your values are integers (they will be rounded if not), and that your x values are in the interval [0, 640] and your y values are in the interval [0, 480]. Press 'Go' when you are ready to upload your coordinates."
        self.original_data_info = "Original Data Information"
        self.recreated_info = "Recreated Image Information"
        self.recreated_data_info = "Recreated Data Information"
        self.new_info = "New Image Information"
        self.new_data_info = "New Data Information"
        self.diagram_info = "Area Information"
        self.hist_info = "Histogram Information"
        self.abspec_info = "Optical Spectrum Information"
        self.colour_info = "Colour Information"

        self._init_widget()

    def get_source_output_info(self):
        return self.source_output_info

    def get_analysis_form_info(self):
        return self.analysis_form_info

    def get_csv_info(self):
        return self.csv_info

    def get_save_info(self):
        return self.save_info

    def get_parameter_info(self):
        return self.param_info

    def get_original_info(self):
        return self.original_info

    def get_input_info(self):
        return self.input_info  

    def get_original_data_info(self):
        return self.original_data_info      

    def get_recreated_info(self):
        return self.recreated_info   

    def get_recreated_data_info(self):
        return self.recreated_data_info

    def get_new_info(self):
        return self.new_info

    def get_new_data_info(self):
        return self.new_data_info

    def get_diagram_info(self):
        return self.diagram_info

    def get_hist_info(self):
        return self.hist_info

    def get_abspec_info(self):
        return self.abspec_info

    def get_colour_info(self):
        return self.colour_info

    # Helper
    def _init_widget(self):
        self._make_info_button()
        self._make_info_text()

    def _make_info_button(self):
        self.info_label = make_label_button(self.root, text='App Info', command=self._info, width=8)
        self.info_label.grid(padx=(0, 40))

    def _make_info_text(self):
        text = "*click on the section titles to find further information about that specific widget"
        self.info_text = Text(self.root, height=6, width=19, highlightthickness=0, wrap=WORD, bg=tkcolour_from_rgb(BACKGROUND))
        self.info_text.insert(END, text)
        self.info_text.config(state="disabled")
        self.info_text.grid(row=1, column=0, padx=15)

    def _info(self):
        make_info(title="App Information", info=self.info)
