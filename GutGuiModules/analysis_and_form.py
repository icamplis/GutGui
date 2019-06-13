from GutGuiModules.utility import *

class AnalysisAndForm:
    def __init__(self, analysis_and_form_frame):
        self.root = analysis_and_form_frame

        self.normalisation_button = None
        self.original_button = None
        self.OR_text = None

        self._init_widget()

    # Helpers
    def _init_widget(self):
        self._build_normalisation_button()
        self._build_original_button()
        self._build_OR_text(height=1, width=2, row=3, column=1)

    def _build_normalisation_button(self):
        self.normalisation_button = make_button(self.root, text='Normalisation', command=self.__normal,
                                                row=1, column=1, outer_pady=10, outer_padx=(30, 0))

    def _build_original_button(self):
        self.original_button = make_button(self.root, text='Original', command=self.__original,
                                           row=2, column=1, outer_pady=10, outer_padx=(0, 10))

    def _build_OR_text(self, height, width, row, column, padx=10, pady=10):
        self.OR_text = make_text(self.root, content="OR", bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB),
                                 height=height, width=width, row=row, column=column, padx=padx, pady=pady)

    # Commands (Callbacks)
    def __normal(self):
        print('normal placeholder')
        #     TODO

    def __original(self):
        print('original placeholder')
        #     TODO