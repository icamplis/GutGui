from GutGuiModules.utility import *
from tkinter import messagebox

class Info:
    def __init__(self, info_frame, listener):
        self.root = info_frame

        # Listener
        self.listener = listener

        self.info_button = None

        # if you want a newline, type \n
        self.info = "This is filler text\nWrite whatever you want here\n\n:)"

        self._init_widget()

    # Helper
    def _init_widget(self):
        self._make_info_button()

    def _make_info_button(self):
        self.info_button = make_button(self.root, text="App Info", command=self._info, row=0, column=0, outer_pady=15, outer_padx=15, width=10)

    def _info(self):
        window = Toplevel()
        window.title("App Information")
        window.geometry("+0+0")
        text = Text(window, height=20, width=50, wrap=WORD, highlightthickness=0) 
        text.insert(END, self.info)
        text.grid(padx=5, pady=5)
        window.resizable(width=False, height=False)