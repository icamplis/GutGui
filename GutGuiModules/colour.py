import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.colorbar import ColorbarBase
from GutGuiModules.utility import *
from matplotlib import colors
from matplotlib.pyplot import cm

class Colour:
    def __init__(self, colour_frame, listener):
        self.root = colour_frame

        # Listener
        self.listener = listener

        self.colourbar = None

        self._init_widget()

    # Helper
    def _init_widget(self):
        self._make_colourbar()

    def _make_colourbar(self):
        colour_fig = Figure(figsize=(2, 1))
        axes = colour_fig.add_subplot(111)

        cmap = cm.get_cmap('jet')
        self.colourbar = cmap(np.arange(cmap.N))

        axes.imshow([self.colourbar], extent=[0, 255, 0, 100])
        axes.get_yaxis().set_visible(False)
        axes.get_xaxis().set_visible(False)
        colour_fig.patch.set_facecolor(rgb_to_rgba(PASTEL_PINK_RGB))
        colour_fig.set_tight_layout('True')
        image = FigureCanvasTkAgg(colour_fig, master=self.root)
        image.draw()
        image.get_tk_widget().grid(column=0, row=1, pady=(15,0))