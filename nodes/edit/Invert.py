from nodes.image_node import ImageNode
import socket_types as socket_types

import numpy as np

from PIL import Image, ImageQt

class Invert(ImageNode):
    def __init__(self, scene, x=0, y=0):
        super(Invert, self).__init__(scene, x=x, y=y)
        self.change_title("invert")

        self.input_image = self.add_input(socket_types.PictureSocketType(self), "in")
        self.output_image = self.add_output(socket_types.PictureSocketType(self), "out")

        self.set_auto_compute_on_connect(True)

    def compute(self):
        if self.input_image.is_connected():
            self.input_image.fetch_connected_value()

            print(self.input_image.get_value())

            image_array = np.array(self.input_image.get_value())
            mask_array = np.invert(image_array)

            mask_image = Image.fromarray((mask_array * 255).astype(np.uint8))

            self.output_image.set_value(mask_image)

            output_pixmap = ImageQt.toqpixmap(mask_image)
            self.set_pixmap(output_pixmap)

            self.get_main_window().set_pixmap(output_pixmap)
            self.set_dirty(False)


