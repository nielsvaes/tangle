from nodes.image_node import ImageNode
import socket_types as socket_types

from core.Constants import Colors
from PIL import ImageQt, ImageOps

class Combine(ImageNode):
    def __init__(self, scene, x=0, y=0):
        super(Combine, self).__init__(scene, title_background_color=Colors.combine, x=x, y=y)
        self.change_title("combine")

        self.background_input, self.output_image = self.add_input_output(socket_types.PictureSocketType(self), "image")
        self.foreground_input = self.add_input(socket_types.PictureSocketType(self), "fg")

        self.input_mask = self.add_input(socket_types.PictureSocketType(self), "mask")

        self.input_mask.override_color(Colors.black)

        self.set_auto_compute_on_connect(True)

    def compute(self):
        if self.background_input.is_connected() and self.foreground_input.is_connected():
            self.background_input.fetch_connected_value()
            self.foreground_input.fetch_connected_value()
            self.input_mask.fetch_connected_value()

            combined = self.background_input.get_value().copy()

            if self.input_mask.get_value() is None:
                print("mask is none")
                combined.paste(self.foreground_input.get_value(), (0,0))
                print(combined)
            else:
                combined.paste(self.foreground_input.get_value(), (0, 0), self.input_mask.get_value())

            # combined = combined.paste(self.foreground_input.get_value(), (0, 0), self.input_mask.get_value())

            self.output_image.set_value(combined)

            combined_pixmap = ImageQt.toqpixmap(combined)
            self.set_pixmap(combined_pixmap)

            self.get_main_window().set_pixmap(combined_pixmap)
            self.set_dirty(False)
