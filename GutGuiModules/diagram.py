class Diagram:
    def __init__(self):
        self.whole_image_label = None
        self.whole_image_checkbox = None
        self.whole_image_checkbox_value = None

        self.masked_region_label = None
        self.masked_region_checkbox = None
        self.masked_region_checkbox_value = None

    # Helper
    def _init_widget(self):
        pass

    def _build_whole_image(self):
        pass

    def _build_masked_region(self):
        pass

    # Commands (Callbacks)
    def __update_whole_image_checked(self):
        pass

    def __update_masked_region_checked(self):
        pass