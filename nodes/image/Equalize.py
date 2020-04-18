from nodes.image_node import ImageNode
from core import socket_types as socket_types

from core.Constants import Colors
from PIL import ImageQt, ImageOps

class Equalize(ImageNode):
    def __init__(self, scene, x=0, y=0):
        super(Equalize, self).__init__(scene, title_background_color=Colors.equalize, x=x, y=y)
        self.change_title("equalize")

        self.input_image, self.output_image = self.add_input_output(socket_types.PictureSocketType(self), "image")
        self.input_mask = self.add_input(socket_types.PictureSocketType(self), "mask")

        self.input_mask.override_color(Colors.black)


    def compute(self, force=False):
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
            self.refresh()
            super().compute(force=force)
            self.set_dirty(False)
