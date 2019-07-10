import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.colorbar import ColorbarBase
from GutGuiModules.utility import *
from matplotlib import colors

class Colour:
    def __init__(self, colour_frame, listener):
        self.root = colour_frame

        # Listener
        self.listener = listener

        self.colourbar = None

        self._init_widget()

    def get_is_masked(self):
        return self.is_masked

    def get_whole_image_checkbox_value(self):
        return not bool(self.whole_image_checkbox_value.get())

    def get_masked_region_checkbox_value(self):
        return not bool(self.masked_region_checkbox_value.get())

    # Helper
    def _init_widget(self):
        self._make_colourbar()

    def _make_colourbar(self):
        colour_fig = Figure(figsize=(2, 1))
        axes = colour_fig.add_subplot(111)
        self.colourbar = ColorbarBase(axes, orientation='horizontal', norm=colors.NoNorm(vmin=0, vmax=255))
        self.colourbar.set_ticks([0, 255])
        colour_fig.patch.set_facecolor(rgb_to_rgba(PASTEL_PINK_RGB))
        colour_fig.set_tight_layout('True')
        image = FigureCanvasTkAgg(colour_fig, master=self.root)
        image.draw()
        image.get_tk_widget().grid(column=0, row=1, pady=(15,0))
