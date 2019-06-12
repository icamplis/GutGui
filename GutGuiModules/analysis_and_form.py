from GutGuiModules.utility import *

class AnalysisAndForm:
    def __init__(self, analysis_and_form_frame):
        self.root = analysis_and_form_frame

        self.normalisation_button = None
        self.original_button = None
        self.OR_text = None

        self._init_widget()

    def _init_widget(self):
        self.build_normalisation_button()
        self.build_original_button()
        self.build_OR_text()

    def build_normalisation_button(self):
        self.normalisation_button = Button(self.root, text='Normalisation', command=self.normal, highlightthickness=0)
        self.normalisation_button.grid(row=1, column=1, pady=10, padx=(30, 0))

    def build_original_button(self):
        self.original_button = Button(self.root, text='Original', command=self.original, highlightthickness=0)
        self.original_button.grid(row=2, column=1, pady=10, padx=(0, 10))

    def build_OR_text(self):
        self.OR_text = Text(self.root, bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB), height=1, width=2,
             highlightthickness=0)
        self.OR_text.insert(END, "OR")
        self.OR_text.grid(row=3, column=1, padx=10, pady=10)

    def normal(self):
        print('normal placeholder')

    def original(self):
        print('original placeholder')