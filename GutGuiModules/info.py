from GutGuiModules.utility import *


class Info:
    def __init__(self, info_frame, listener):
        self.root = info_frame
        self.listener = listener
        self.info_button = None
        self.info_text = None

        # INFORMATION
        self.info = "This is filler text\nWrite whatever you want here\n\n:)"

        self.source_output_info = "This window allows to select the source datacubes for the analysis. The source data " \
                                  "has to be provided in its original file structure the way it is saved by the TIVITA® " \
                                  "Tissue Hyperspectral Camera (that means stored in a folder that contains the " \
                                  "Datacube (.dat) as well as the 5 PNGs: RGB-Image.png, Oxygenation.png, " \
                                  "NIR-Perfusion.png, THI.png and TWI.png as depicted in Figure 5 of the introduction)." \
                                  "\n\nDepending on one’s preference the folder containing these 6 elements can be " \
                                  "selected individually via 'Select Data Directory'. Alternatively - for the purpose " \
                                  "of analyzing several datacubes in the same fashion at the same time - a separate " \
                                  "folder can be created previously that contains a number of primary data folders " \
                                  "and then be selected with the option 'Select Data Superdirectory'. Single primary " \
                                  "data folders can then be removed by 'Remove Data Cube'." \
                                  "\n\nAfter your datacube(s) is displayed in the white box you have to select it for " \
                                  "rendering before you continue with 'Images and Diagrams'."
        self.analysis_form_info = "In this window the analysis settings for the “New Image” can be specified. In case" \
                                  " that only a certain area of the spectrum is interesting, this area can be specified" \
                                  " in the text boxes for lower and upper wavelength (between 500 - 995 nm). In case" \
                                  " one not only wants to visualize simple wavelength areas, but also wants to perform" \
                                  " mathematical operations - much like the original mathematical formulas for StO2," \
                                  " NIR, THI and TWI - there are placeholders for 8 formulas that can be chosen. " \
                                  "\n\nThese formulas can be created and modified depending on the need or " \
                                  "scientific deliberations by encoding them in the module Index in the folder " \
                                  "AnalysisModules/Indices within the GUI directory."
        self.csv_info = "This window allows to save all of the numerical information in .csv files with 480 rows" \
                        " and 640 columns in accordance to the pixel distribution of 480 x 640 in the original" \
                        " recordings."
        self.save_info = "This window allows to save all of the features of the 'Images and Diagrams' window that" \
                         " have a tick in the blue boxes. These features can either be saved for the selected" \
                         " datacube in the 'Source and Output' window by 'Save for Selected Data Cube Only'." \
                         " Alternatively, these features can be saved for all of the datacubes - in case that" \
                         " several data cubes were uploaded - by 'Save for All Data Cubes'."
        self.parameter_info = "In this window, the letter variables for the formulas depicted in Figure 7 of the" \
                              " introduction that are used for the creation of the index pictures can be specified." \
                              " For research purposes these can be enquired from Diaspective Vision."
        self.original_info = "This window uploads the original pngs and allows to mask a specific area of interest" \
                             " with a 9-point freehand selection tool for further analysis. After having marked" \
                             " the specific area, the button 'Use mask' has to be selected in order for the further" \
                             " analysis steps to work. \n\nRight click maximizes the image."
        self.input_info = "Here you can input coordinates manually. Make sure that your values are integers " \
                          "(they will be rounded if not), and that your x values are in the interval [0, 640] " \
                          "and your y values are in the interval [0, 480]. Press 'Go' when you are ready to upload " \
                          "your coordinates."
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

    # ------------------------------------------------ INITIALIZATION ------------------------------------------------

    def _init_widget(self):
        self._build_info_button()
        self._build_info_text()

    # --------------------------------------------------- BUILDERS ---------------------------------------------------

    def _build_info_button(self):
        self.info_label = make_label_button(self.root, text='App Info', command=self.__info, width=8)
        self.info_label.grid(padx=(0, 40))

    def _build_info_text(self):
        text = "*click on the section titles to find further information about that specific widget"
        self.info_text = Text(self.root, height=6, width=19, highlightthickness=0, wrap=WORD,
                              bg=tkcolour_from_rgb(BACKGROUND))
        self.info_text.insert(END, text)
        self.info_text.config(state="disabled")
        self.info_text.grid(row=1, column=0, padx=15)

    # -------------------------------------------------- CALLBACKS ---------------------------------------------------

    def __info(self):
        make_info(title="App Information", info=self.info)
