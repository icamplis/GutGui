from GutGuiModules.utility import *

class AnalysisAndForm:
    def __init__(self, analysis_and_form_frame):
        self.root = analysis_and_form_frame
        self.root.grid_columnconfigure(7, weight=1)

        self.normalisation_button = None
        self.original_button = None
        self.reflection_button = None
        self.absorbance_button = None
        self.OR_text = ''
        self.wavelength_text = ''
        self.wavelength = None
        self.idx = ''
        self.idx1 = None
        self.idx2 = None
        self.idx3 = None
        self.idx4 = None
        self.idx5 = None
        self.idx6 = None
        self.idx7 = None
        self.idx8 = None
        self.stO2_text = ''
        self.stO2 = None
        self.perf_text = ''
        self.perf = None
        self.hemo_text = ''
        self.hemo = None
        self.tissue_text = ''
        self.tissue = None

        self._init_widget()

    # Helpers
    def _init_widget(self):
        self._build_idx_title()
        self._build_idxs()
        self._build_normalisation_button() 
        self._build_OR_text(height=1, width=2, row=1, column=3, columnspan=1)
        self._build_original_button()
        self._build_reflection_button()
        self._build_OR_text(height=1, width=2, row=2, column=3, columnspan=1)
        self._build_absorbance_button()
        self._build_wavelength_text()
        self._build_wavelength()
        self._build_stO2_text()
        self._build_stO2()
        self._build_perf_text()
        self._build_perf()
        self._build_hemo_text()
        self._build_hemo()
        self._build_tissue_text()
        self._build_tissue()

    def _build_normalisation_button(self):
        self.normalisation_button = make_button(self.root, text='Normalisation', command=self.__normal, row=1, column=0, outer_pady=10, 
            outer_padx=(30, 0), columnspan=3)

    def _build_original_button(self):
        self.original_button = make_button(self.root, text='Original', 
            command=self.__original, row=1, column=5, outer_pady=10, 
            outer_padx=(0, 10), columnspan=3)

    def _build_reflection_button(self):
        self.reflection_button = make_button(self.root, text='Reflection', command=self.__reflect, row=2, column=0, outer_pady=10, 
            outer_padx=(30, 0), columnspan=3)

    def _build_absorbance_button(self):
        self.absorbance_button = make_button(self.root, text='Absorbance', 
            command=self.__absorb,row=2, column=5, outer_pady=10, 
            outer_padx=(0, 10), columnspan=3)

    def _build_OR_text(self, height, width, row, column, columnspan, padx=10, pady=10):
        self.OR_text = make_text(self.root, content="OR", 
            bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB), height=height, width=width, row=row, column=column, padx=padx, pady=pady, columnspan=columnspan)

    def _build_wavelength_text(self):
        self.wavelength_text = make_text(self.root, content="Wavelength: ", 
            bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB), column=0, row=3, width=12, columnspan=4, pady=(10, 0))

    def _build_wavelength(self):
        self.wavelength = make_entry(self.root, row=3, column=4, width=20, pady=(10,0), padx=(0, 30), columnspan=4)

    def _build_idx_title(self):
        self.idx = make_text(self.root, content="Individual Index", 
            bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB), column=0, row=4, width=16, columnspan=8, pady=(10, 0))
    def _build_idxs(self):
        self.idx1 = make_button(self.root, text='1', command=lambda:self.__idxn(1), row=5, column=0, outer_pady=5, outer_padx=5, width=1)
        self.idx2 = make_button(self.root, text='2', command=lambda:self.__idxn(2), row=5, column=1, outer_pady=5, outer_padx=5, width=1)
        self.idx3 = make_button(self.root, text='3', command=lambda:self.__idxn(3), row=5, column=2, outer_pady=5, outer_padx=5, width=1)
        self.idx4 = make_button(self.root, text='4', command=lambda:self.__idxn(4), row=5, column=3, outer_pady=5, outer_padx=5, width=1)
        self.idx5 = make_button(self.root, text='5', command=lambda:self.__idxn(5), row=5, column=4, outer_pady=5, outer_padx=5, width=1)
        self.idx6 = make_button(self.root, text='6', command=lambda:self.__idxn(6), row=5, column=5, outer_pady=5, outer_padx=5, width=1)
        self.idx7 = make_button(self.root, text='7', command=lambda:self.__idxn(7), row=5, column=6, outer_pady=5, outer_padx=5, width=1)
        self.idx8 = make_button(self.root, text='8', command=lambda:self.__idxn(8), row=5, column=7, outer_pady=5, outer_padx=5, width=1)

    def _build_stO2_text(self):
        self.stO2_text = make_text(self.root, content="Saturation index: ", 
            bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB), column=0, row=6, width=18, columnspan=4, pady=0)

    def _build_stO2(self):
        self.stO2 = make_entry(self.root, row=6, column=4, width=20, pady=(5,0), padx=(0, 30), columnspan=4)

    def _build_perf_text(self):
        self.perf_text = make_text(self.root, content="Perfusion index: ", 
            bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB), column=0, row=7, width=17, columnspan=4, pady=0)

    def _build_perf(self):
        self.perf = make_entry(self.root, row=7, column=4, width=20, pady=(5,0), padx=(0, 30), columnspan=4)


    def _build_hemo_text(self):
        self.hemo_text = make_text(self.root, content="Hemoglobin index: ", 
            bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB), column=0, row=8, width=18, columnspan=4, pady=0)

    def _build_hemo(self):
        self.hemo = make_entry(self.root, row=8, column=4, width=20, pady=(5,0), padx=(0, 30), columnspan=4)

    def _build_tissue_text(self):
        self.stO2_text = make_text(self.root, content="Tissue water index: ", 
            bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB), column=0, row=9, width=20, columnspan=4, pady=0)

    def _build_tissue(self):
        self.stO2 = make_entry(self.root, row=9, column=4, width=20, pady=5, padx=(0, 30), columnspan=4)

    # Commands (Callbacks)
    def __normal(self):
        print('normal placeholder')
        #     TODO

    def __original(self):
        print('original placeholder')
        #     TODO

    def __reflect(self):
        print('reflect placeholder')
        #     TODO

    def __absorb(self):
        print('absorb placeholder')
        #     TODO

    def __idxn(self, n):
        print('idxn placeholder')
        #     TODO