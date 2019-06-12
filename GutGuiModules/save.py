from GutGuiModules.utility import *

class Save:
    def __init__(self, save_frame):
        self.root = save_frame

        self.save_specific_button = None
        self.save_all_button = None

        self._init_widgets()

    def _init_widgets(self):
        self._build_save_specific_button()
        self._build_save_all_button()

    # TODO: MAKE THIS USE THE MAKE_BUTTON FUNCTION INSTEAD
    def _build_save_specific_button(self):
        self.save_specific_button = Button(self.root, text='Save for specifically selected data cube',
                                           command=self._save_specific, highlightthickness=0)
        self.save_specific_button.grid(row=1, column=0, pady=(20, 0))

    def _build_save_all_button(self):
        self.save_all_button = Button(self.root, text='Save for all selected data cubes', command=self._save_all,
                                      highlightthickness=0)
        self.save_all_button.grid(row=2, column=0, pady=20)

    def _save_specific(self):
        print('save for specific placeholder')

    def _save_all(self):
        print('save for all placeholder')