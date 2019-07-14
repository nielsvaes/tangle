from nodes.image_node import ImageNode
import socket_types as socket_types

import core.Constants as nc

from PIL import ImageQt, ImageOps

class Equalize(ImageNode):
    def __init__(self, scene, x=0, y=0):
        super(Equalize, self).__init__(scene, x=x, y=y)
        self.change_title("equalize")

        self.input_image, self.output_image = self.add_input_output(socket_types.PictureSocketType(self), "image")
        self.input_mask = self.add_input(socket_types.PictureSocketType(self), "mask")

        self.input_mask.override_color(nc.Colors.black)

        self.set_auto_compute_on_connect(True)

    def compute(self):
        if self.input_image.is_connected():
            self.input_image.fetch_connected_value()
            self.input_mask.fetch_connected_value()

            if self.input_mask.get_value() is None:
                equalize = ImageOps.equalize(self.input_image.get_value())
            else:
                equalize = ImageOps.equalize(self.input_image.get_value(), self.input_mask.get_value())

            self.output_image.set_value(equalize)

            contrasted_pixmap = ImageQt.toqpixmap(equalize)
            self.set_pixmap(contrasted_pixmap)

            self.get_main_window().set_pixmap(contrasted_pixmap)
            self.set_dirty(False)
