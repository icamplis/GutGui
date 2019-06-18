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
        self.save_specific_button = make_button(self.root, text="Save Selected", command=self._save_specific, row=1, column=0, outer_pady=0, outer_padx=2, width=10)

    def _build_save_all_button(self):
        self.save_all_button = make_button(self.root, text='Save All', command=self._save_all, row=1, column=2, outer_pady=0, outer_padx=5, width=10)

    def _save_specific(self):
        print('save for specific placeholder')
        #     TODO

    def _save_all(self):
        print('save for all placeholder')
        #     TODO