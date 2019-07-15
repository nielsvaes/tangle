from nodes.image_node import ImageNode
import socket_types as socket_types

import numpy as np
from core.Constants import Colors
from PIL import Image, ImageQt, ImageOps

class Invert(ImageNode):
    def __init__(self, scene, x=0, y=0):
        super(Invert, self).__init__(scene, title_background_color=Colors.invert, x=x, y=y)
        self.change_title("invert")

        self.input_image, self.output_image = self.add_input_output(socket_types.PictureSocketType(self), "image")

        self.set_auto_compute_on_connect(True)

    def compute(self):
        if self.input_image.is_connected():
            self.input_image.fetch_connected_value()

            inverted_image = ImageOps.invert(self.input_image.get_value())

            self.output_image.set_value(inverted_image)

            output_pixmap = ImageQt.toqpixmap(inverted_image)
            self.set_pixmap(output_pixmap)

            self.get_main_window().set_pixmap(output_pixmap)
            self.set_dirty(False)


