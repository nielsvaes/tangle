from nodes.image_node import ImageNode
from core import socket_types as socket_types

from core.Constants import Colors
from PIL import ImageQt, ImageOps

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
            super().compute()
            self.set_dirty(False)


