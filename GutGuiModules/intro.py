from GutGuiModules.utility import *
from tkinter import *


class Introduction:
    def __init__(self, introduction_frame):
        self.root = introduction_frame

        self.number = 1
        self.prev_button = None
        self.next_button = None

        self.text_box = None
        self.text_text_1 = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut" \
                           " labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco " \
                           "laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in " \
                           "voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat " \
                           "cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

        self.text_text_2 = "At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium " \
                           "voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati "

        self.text_text_3 = "cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id " \
                           "est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam " \
                           "libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod " \
                           "maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. " \
                           "Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet " \
                           "ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic " \
                           "tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut " \
                           "perferendis doloribus asperiores repellat."

        self.text_text_4 = "tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut " \
                           "perferendis doloribus asperiores repellat."

        self.text_text_5 = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut" \
                           " labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco " \
                           "laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in " \
                           "voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat "

        self.text_text_6 = "At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium " \
                           "voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati "

        self.text_text_7 = "est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam " \
                           "libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod " \
                           "maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. " \
                           "Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet " \
                           "ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic " \
                           "tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut " \
                           "perferendis doloribus asperiores repellat."

        self.text_text_8 = "est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam " \
                           "libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod " \
                           "maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. "

        self.text_texts = [self.text_text_1, self.text_text_2, self.text_text_3, self.text_text_4,
                           self.text_text_5, self.text_text_6, self.text_text_7, self.text_text_8]

        self.image_box = None
        self.images = []

        self.image1 = None
        self.image2 = None
        self.image3 = None
        self.image4 = None
        self.image5 = None
        self.image6 = None
        self.image7 = None
        self.image8 = None

        self.parse_images()
        self._build_text_box()
        self._build_image_box()
        self._build_prev_next()

    # --------------------------------------------------- BUILDERS ---------------------------------------------------

    def parse_images(self):
        self.images.append(image_to_array('./image1.png'))
        for i in range(2, 9):
            self.images.append(image_to_array('./image' + str(i) + '.jpg'))

    def _build_text_box(self):
        self.text_box = Text(self.root, height=10, width=70, wrap=WORD, highlightthickness=0)
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
            self._build_text_box()
            self._build_image_box()

    def __next(self):
        if self.number == 8:
            pass
        else:
            self.number += 1
            self._build_text_box()
            self._build_image_box()

