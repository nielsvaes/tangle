from ..image_node import ImageNode
from ...core import socket_types as socket_types

from ...core.Constants import Colors
from PIL import ImageQt, ImageOps

class Invert(ImageNode):
    def __init__(self, scene, x=0, y=0):
        super(Invert, self).__init__(scene, title_background_color=Colors.invert, x=x, y=y)
        self.change_title("invert")

        self.input_image, self.output_image = self.add_input_output(socket_types.PictureSocketType(self), "image")


    def compute(self, force=False):
        if self.input_image.is_connected():
            self.input_image.fetch_connected_value()
            input_image = self.input_image.get_value()
            if input_image.mode == "RGBA":
                input_image = input_image.convert("RGB")

            inverted_image = ImageOps.invert(input_image)

            self.output_image.set_value(inverted_image)

            output_pixmap = ImageQt.toqpixmap(inverted_image)
            self.set_pixmap(output_pixmap)
            super().compute(force=force)
            self.set_dirty(False)


