from GutGuiModules.utility import *
from tkinter import *


class Introduction:
    def __init__(self, introduction_frame):
        self.root = introduction_frame

        self.number = 1
        self.prev_button = None
        self.next_button = None

        self.title_1 = "Introduction to Hyperspectral Imaging"
        self.title_2 = "The Hyperspectral Camera System"
        self.title_3a = "TIVITA® Tissue Camera Operation"
        self.title_3b = "Data Requirements"
        self.title_4 = "TIVITA® Tissue System Image Calculation"
        self.title_5 = "Purpose of this Software"
        self.title_6 = "HyperGUI© (Hyperspectral Graphical User Interface) Disclaimer"

        self.text_text_1 = "HyperGUI© is a freeware Python tool for the extensive analysis and evaluation of " \
                           "hyperspectral data cubes from the TIVITA® Suite software version 1.4.1.5 from the TIVITA® " \
                           "Tissue Hyperspectral Camera from Diaspective Vision GmbH in Germany." \
                           "\n\nwww.diaspective-vision.com" \
                           "\noffice@diaspective-vision.com " \
                           "\n\nSpectral imaging is a method that has already been extensively used in other industries " \
                           "such as the food industry, geology, oil & gas industry and agriculture; however, it is " \
                           "relatively new to the field of medicine. It is based on the physical principle that " \
                           "different molecules have different characteristic absorbance and reflectance properties " \
                           "much like a spectral “fingerprint” (Figure 1)." \
                           "\n\nWhen measuring the absorbance or reflectance values of only a few specific wavelengths " \
                           "of the electromagnetic spectrum of every pixel within a two dimensional image this is " \
                           "called multispectral imaging. When measuring these values of several specific wavelengths " \
                           "or even continuously over the electromagnetic spectrum this is called hyperspectral " \
                           "imaging." \
                           "\n\nConsequently, when recording an image with a hyperspectral camera, the data received " \
                           "will be in the form of a three dimensional data cube in which every pixel of the two " \
                           "dimensional grid will be associated with a specific optical spectrum (Figure 2) that can " \
                           "then be analysed."

        self.text_text_2 = "The hyperspectral camera system that this software has been designed for is the TIVITA® " \
                           "Suite software version 1.4.1.5 from the TIVITA® Tissue Hyperspectral Camera from " \
                           "Diaspective Vision GmbH in Germany (Figure 3). The software will be regularly updated for " \
                           "subsequent TIVITA® Tissue versions."

        self.text_text_3a = "The hyperspectral camera works as a line-scanner in the way that the image is scanned in " \
                            "a linear fashion several times while the holographic transmission grating changes over " \
                            "time allowing different wavelengths to pass through the spectral filter (Figure 4)."

        self.text_text_3b = "This software is optimized for Python on Apple Mac. " \
                            "\nIt can be downloaded from https://github.com/icamplis/GutGui." \
                            "\nIn order to be able to use this software the primary data created by the camera" \
                            " system must not be manipulated and in its original form exemplarily displayed on the" \
                            " right (Figure 5)."

        self.text_text_4 = "The software of the camera system creates four different index pictures that are " \
                           "calculated from specific wavelength areas as depicted on the right (Figure 6):" \
                           "\n- StO2: HSI Tissue Oxygen Saturation		        570-590 nm & 740-780 nm" \
                           "\n- NIR: HSI Tissue Perfusion (Near-Infrared)		 655-735 nm & 825-925 nm" \
                           "\n- THI: HSI Tissue Haemoglobin Index		         530-590 nm & 785-825 nm" \
                           "\n- TWI: HSI Tissue Water Index			              880-900 nm & 955-980 nm" \
                           "\n\nThe formulas used are displayed on the right (Figure 7). The parameters represented " \
                           "by the letter variables are part of the corporate secret and cannot be provided."

        self.text_text_5 = "The purpose of this software is the facilitation of an extensive analysation of the " \
                           "hyperspectral datacube." \
                           "\nEvery analysis can be exported either as .png if it is a graphical result or as .csv " \
                           "if it is a numerical result. " \
                           "\nThis software is particularly suited to analyze the application of dyes, identify " \
                           "limitations and influencing factors of the method, classify tissue and find new " \
                           "formulas for new tissue characteristics."

        self.text_text_6 = "HyperGUI© is a freeware Python tool for the extensive analysis and evaluation of " \
                           "hyperspectral data cubes from the TIVITA® Suite software version 1.4.1.5 from the " \
                           "TIVITA® Tissue Hyperspectral Camera from Diaspective Vision GmbH in Germany." \
                           "\nwww.diaspective-vision.com" \
                           "\noffice@diaspective-vision.com " \
                           "\n\nVersion 1.1.0" \
                           "\nOpen source hyperspectral data processing and analysis software." \
                           "\n\nThis is not a certified medical product and cannot be used for clinical diagnostics. " \
                           "]nThe creators cannot be held liable for faulty indications and their consequences, " \
                           "neither assume any juridical responsibility nor any liability." \
                           "\n\n\nCand. med. Alexander Studier-Fischer" \
                           "\nUniversity Hospital of Heidelberg" \
                           "\nDepartment of General, Visceral- and Transplantation Surgery" \
                           "\nIm Neuenheimer Feld 110" \
                           "\n69120 Heidelberg, Germany" \
                           "\nalexander@studier-fischer.de" \
                           "\n\nIsabella Camplisson" \
                           "\nCalifornia Institute of Technology" \
                           "\nDepartment of Engineering and Applied Science" \
                           "\n1200 E California Boulevard MSC 161, CA, USA 91125" \
                           "\n\nGuanyue Wu" \
                           "\nUniversity of British Columbia, Faculty of Science" \
                           "\nICICS Computer Science" \
                           "\n2366 Main Mall, Vancouver, BC V6T 1Z4, Canada" \
                           "\n\nPD Dr. med. Felix Nickel, MME" \
                           "\nUniversity Hospital of Heidelberg" \
                           "\nDepartment of General, Visceral- and Transplantation Surgery" \
                           "\nIm Neuenheimer Feld 110" \
                           "\n69120 Heidelberg, Germany" \
                           "\n\nThis software is made available by the provider 'as is' and 'with all faults.' The " \
                           "provider makes no representations or warranties of any kind concerning the safety, " \
                           "suitability or inaccuracies. You are solely responsible for determining whether this " \
                           "graphical user interface is compatible with your equipment and other software installed " \
                           "on your equipment. The provider will not be liable for any damages you may suffer in " \
                           "connection with using, modifying, or distributing this software."

        self.image_box = None
        self.images = []

        self._init_widget()

    # ------------------------------------------------ INITIALIZATION ------------------------------------------------

    def _init_widget(self):
        self.parse_images()
        self._build_prev_next()
        self._build_page(self.number)

    # --------------------------------------------------- BUILDERS ---------------------------------------------------

    def parse_images(self):
        self.images.append(image_to_array('./image1.png'))
        for i in range(2, 9):
            self.images.append(image_to_array('./image' + str(i) + '.jpg'))

    def _build_page(self, page_num):
        if page_num == 1:
            self._build_page1()
        if page_num == 2:
            self._build_page2()
        if page_num == 3:
            self._build_page3()
        if page_num == 4:
            self._build_page4()
        if page_num == 5:
            self._build_page5()
        if page_num == 6:
            self._build_page6()

    def _build_page1(self):
        pass


    def _build_text_box(self):
        self.text_box = Text(self.root, height=47, width=70, wrap=WORD, highlightthickness=0)
        self.text_box.insert(END, self.text_texts[self.number-1])
        self.text_box.config(state="disabled", bg=tkcolour_from_rgb(WHITE))
        self.text_box.grid(padx=25, pady=15, row=0, column=0)

    def _build_image_box(self):
        self.image_box = make_image(self.root, self.images[self.number-1], column=1, rowspan=1, lower_scale_value=None,
                                    upper_scale_value=None, color_rgb=WHITE, figwidth=8, figheight=7.2, original=True,
                                    row=0, columnspan=1)[1]
        self.image_box.get_tk_widget().grid(padx=15, pady=15)

    def _build_prev_next(self):
        self.prev_button = make_button(self.root, text='Previous', width=9, command=self.__previous, row=1, column=0,
                                       columnspan=2, inner_pady=5, outer_padx=(0, 130), outer_pady=15)
        self.next_button = make_button(self.root, text='Next', width=9, command=self.__next, row=1, column=0,
                                       columnspan=2, inner_pady=5, outer_padx=(130, 0), outer_pady=15)

    # -------------------------------------------------- CALLBACKS ---------------------------------------------------

    def __previous(self):
        if self.number == 1:
            pass
        else:
            self.number -= 1
            self._build_page(self.number)

    def __next(self):
        if self.number == 6:
            pass
        else:
            self.number += 1
            self._build_page(self.number)

