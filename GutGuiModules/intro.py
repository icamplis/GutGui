from GutGuiModules.utility import *

class Introduction:
    def __init__(self, introduction_frame):
        self.root = introduction_frame

        self.image1 = None
        self.image2 = None
        self.image3 = None
        self.image4 = None
        self.image5 = None
        self.image6 = None
        self.image7 = None
        self.image8 = None
        self.image9 = None
        self.image10 = None
        self.image11 = None
        self.image12 = None
        self.image13 = None
        self.text = None

        self.load_images()

    def load_images(self):
        # image 1
        self.text = make_text(self.root, content='hello!', row=0, column=0, padx=0, pady=0, height=1, width=6, highlightthickness=0, bg="white", columnspan=1,  rowspan=1, state=DISABLED)