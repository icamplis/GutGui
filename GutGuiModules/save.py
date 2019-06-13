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

    def _build_save_specific_button(self):
        self.save_specific_button = make_button(self.root, text="Save for specifically selected data cube", command=self._save_specific, 
            row=1, column=0, outer_pady=(20, 0), outer_padx=20, width=30)

    def _build_save_all_button(self):
        self.save_all_button = make_button(self.root, text='Save for all selected data cubes', command=self._save_all, row=2, column=0, outer_pady=20, outer_padx=20, width=30)

    def _save_specific(self):
        print('save for specific placeholder')
        #     TODO

    def _save_all(self):
        print('save for all placeholder')
        #     TODO