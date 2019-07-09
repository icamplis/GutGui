from GutGuiModules.utility import *

class AnalysisAndForm:
    def __init__(self, analysis_and_form_frame, listener):
        self.root = analysis_and_form_frame

        # Listener
        self.listener = listener

        self.normalisation_button = None
        self.original_button = None
        self.reflection_button = None
        self.absorbance_button = None

        self.OR_text = None

        self.upper_wavelength_text = None
        self.lower_wavelength_text = None
        self.wavelength_entry = None
        self.wavelength_value = None
        self.wavelength_upper_text = None
        self.wavelength_upper_entry = None
        self.wavelength_upper_value = None
        self.wavelength_lower_text = None
        self.wavelength_lower_entry = None
        self.wavelength_lower_value = None

        self.idx_title = None
        self.idx1_button = None
        self.idx2_button = None
        self.idx3_button = None
        self.idx4_button = None
        self.idx5_button = None
        self.idx6_button = None
        self.idx7_button = None
        self.idx8_button = None
        # self.stO2_text = None
        # self.stO2_entry = None
        # self.perf_text = None
        # self.perf_entry = None
        # self.hemo_text = None
        # self.hemo = None
        # self.tissue_text = None
        # self.tissue_entry = None

        # State vars
        self.normal = True  # True by default
        self.absorbance = True

        self._init_widget()

    def get_normal(self):
        return self.normal

    def get_absorbance(self):
        return self.absorbance

    def get_wavelength_upper(self):
        return int(self.wavelength_upper_entry.get())

    def get_wavelength_lower(self):
        return int(self.wavelength_lower_entry.get())

    def get_wavelength(self):
        return (self.get_wavelength_lower(), self.get_wavelength_upper())

    def get_index(self):
        return self.index_selected

    # Helpers
    def _init_widget(self):
        self._build_idx_title()
        self._build_idxs()
        self._build_normalisation_button()
        self._build_OR_text(height=1, width=2, row=1, column=3, columnspan=2, pady=0)
        self._build_original_button()
        self._build_reflection_button()
        self._build_OR_text(height=1, width=2, row=2, column=3, columnspan=2, pady=5)
        self._build_absorbance_button()
        self._build_wavelength_text()
        # self._build_wavelength_entry()
        self._build_wavelength_upper_entry()
        self._build_wavelength_lower_entry()
        # self._build_stO2_text()
        # self._build_stO2()
        # self._build_perf_text()
        # self._build_perf()
        # self._build_hemo_text()
        # self._build_hemo()
        # self._build_tissue_text()
        # self._build_tissue()

    def _build_normalisation_button(self):
        self.normalisation_button = make_button(self.root, text='Normalisation',
                                                command=self.__normal, row=1, column=0, outer_pady=(0,5),
                                                outer_padx=(15, 0), columnspan=3)
        self.normalisation_button.config(foreground="red")

    def _build_original_button(self):
        self.original_button = make_button(self.root, text='Original',
            command=self.__original, row=1, column=5, outer_pady=(0,5),
            outer_padx=(0, 15), columnspan=3)

    def _build_reflection_button(self):
        self.reflection_button = make_button(self.root, text='Reflectance',
                                             command=self.__reflect, row=2, column=0, outer_pady=(0,5),
            outer_padx=(15, 0), columnspan=3)

    def _build_absorbance_button(self):
        self.absorbance_button = make_button(self.root, text='Absorbance',
            command=self.__absorb,row=2, column=5, outer_pady=(0,5),
            outer_padx=(0, 15), columnspan=3)
        self.absorbance_button.config(foreground="red")

    def _build_OR_text(self, height, width, row, column, columnspan, padx=0, pady=10):
        self.OR_text = make_text(self.root, content="OR",
            bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB), height=height, width=width, row=row, column=column, padx=padx, pady=pady, columnspan=columnspan)

    def _build_wavelength_text(self):
        self.lower_wavelength_text = make_text(self.root, content="Lower Wavelength: ", bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB), column=0, row=3, width=19, columnspan=4, pady=(10, 0))
        self.upper_wavelength_text = make_text(self.root, content="Upper Wavelength: ", bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB), column=0, row=4, width=19, columnspan=4, pady=(10, 0))

    def _build_wavelength_upper_entry(self):
        self.wavelength_upper_entry = make_entry(self.root, row=3, column=4, width=15, pady=(10, 0), columnspan=4)
        self.wavelength_upper_entry.insert(0, str(64))
        self.wavelength_upper_entry.bind('<Return>', self.__update_wavelength)

    def _build_wavelength_lower_entry(self):
        self.wavelength_lower_entry = make_entry(self.root, row=4, column=4, width=15, pady=(10, 0), columnspan=4)
        self.wavelength_lower_entry.insert(0, str(64))
        self.wavelength_lower_entry.bind('<Return>', self.__update_wavelength)

    def _build_idx_title(self):
        self.idx_title = make_text(self.root, content="Individual Index:",
                                   bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB), column=0, row=5, width=17, columnspan=8, pady=(10, 0))

    def _build_idxs(self):
        self.idx1_button = make_button(self.root, text='1', command=lambda:self.__idxn(1),
                                       row=6, column=0, outer_pady=(5, 15), outer_padx=(15, 5), width=1)
        self.idx2_button = make_button(self.root, text='2', command=lambda:self.__idxn(2),
                                       row=6, column=1, outer_pady=(5, 15), outer_padx=5, width=1)
        self.idx3_button = make_button(self.root, text='3', command=lambda:self.__idxn(3),
                                       row=6, column=2, outer_pady=(5, 15), outer_padx=5, width=1)
        self.idx4_button = make_button(self.root, text='4', command=lambda:self.__idxn(4),
                                       row=6, column=3, outer_pady=(5, 15), outer_padx=5, width=1)
        self.idx5_button = make_button(self.root, text='5', command=lambda:self.__idxn(5),
                                       row=6, column=4, outer_pady=(5, 15), outer_padx=5, width=1)
        self.idx6_button = make_button(self.root, text='6', command=lambda:self.__idxn(6),
                                       row=6, column=5, outer_pady=(5, 15), outer_padx=5, width=1)
        self.idx7_button = make_button(self.root, text='7', command=lambda:self.__idxn(7),
                                       row=6, column=6, outer_pady=(5, 15), outer_padx=5, width=1)
        self.idx8_button = make_button(self.root, text='8', command=lambda:self.__idxn(8),
                                       row=6, column=7, outer_pady=(5, 15), outer_padx=(5, 15), width=1)
        self.idx1_button.config(foreground="red")
        self.index_selected = 1  # Use index no.1 by default

    # def _build_stO2_text(self):
    #     self.stO2_text = make_text(self.root, content="Saturation index: ", 
    #         bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB), column=0, row=6, width=18, columnspan=4, pady=(5,0))

    # def _build_stO2(self):
    #     self.stO2_entry = make_entry(self.root, row=6, column=4, width=15, pady=(5,0), padx=(0, 20), columnspan=4, command=self.__update_st02)

    # def _build_perf_text(self):
    #     self.perf_text = make_text(self.root, content="Perfusion index: ", 
    #         bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB), column=0, row=7, width=17, columnspan=4, pady=(5,0))

    # def _build_perf(self):
    #     self.perf_entry = make_entry(self.root, row=7, column=4, width=15, pady=(5,0), padx=(0, 20), columnspan=4, command=self.__update_perf)

    # def _build_hemo_text(self):
    #     self.hemo_text = make_text(self.root, content="Hemoglobin index: ", 
    #         bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB), column=0, row=8, width=18, columnspan=4, pady=(5,0))

    # def _build_hemo(self):
    #     self.hemo = make_entry(self.root, row=8, column=4, width=15, pady=(5,0), padx=(0, 20), columnspan=4, command=self.__update_hemo)

    # def _build_tissue_text(self):
    #     self.tissue_text = make_text(self.root, content="Tissue water index: ",
    #         bg=tkcolour_from_rgb(PASTEL_ORANGE_RGB), column=0, row=9, width=20, columnspan=4, pady=(5, 15))

    # def _build_tissue(self):
    #     self.tissue_entry = make_entry(self.root, row=9, column=4, width=15, pady=(5, 15), padx=(0, 20), columnspan=4, command=self.__update_tissue)

    # Commands (Callbacks)
    def __normal(self):
        self.normalisation_button.config(foreground="red")
        self.original_button.config(foreground="black")
        self.normal = True
        self.listener.submit_normal(self.normal)

    def __original(self):
        self.original_button.config(foreground="red")
        self.normalisation_button.config(foreground="black")
        self.normal = False
        self.listener.submit_normal(self.normal)

    def __absorb(self):
        self.absorbance_button.config(foreground="red")
        self.reflection_button.config(foreground="black")
        self.absorbance = True
        self.listener.submit_absorbance(self.absorbance)

    def __reflect(self):
        self.reflection_button.config(foreground="red")
        self.absorbance_button.config(foreground="black")
        self.absorbance = False
        self.listener.submit_absorbance(self.absorbance)

    def __idxn(self, n):
        self.listener.submit_index(n)
        buttons = [self.idx1_button, self.idx2_button, self.idx3_button, self.idx4_button,
                   self.idx5_button, self.idx6_button, self.idx7_button, self.idx8_button]
        for i in range(len(buttons)):
            if i+1 == n:
                buttons[i].config(foreground="red")
            else:
                buttons[i].config(foreground="black")

    def __update_wavelength(self, event):
        (wav1, wav2) = self.get_wavelength()
        wavelength = tuple((wav1, wav2))
        self.listener.submit_wavelength(wavelength)
