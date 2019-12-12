import logging
logging.basicConfig(level=logging.DEBUG)

from nodes.image_node import ImageNode
from core import socket_types as socket_types
from core.Constants import Colors

from PIL import ImageQt


class SplitChannels(ImageNode):
    def __init__(self, scene, x=0, y=0):
        super(SplitChannels, self).__init__(scene, title_background_color=Colors.split_channel, x=x, y=y)
        self.change_title("split")

        self.input_image = self.add_input(socket_types.PictureSocketType(self), "image")
        self.output_r = self.add_output(socket_types.PictureSocketType(self), "R")
        self.output_g = self.add_output(socket_types.PictureSocketType(self), "G")
        self.output_b = self.add_output(socket_types.PictureSocketType(self), "B")
        self.output_a = self.add_output(socket_types.PictureSocketType(self), "A")

        self.output_r.override_color(Colors.red)
        self.output_g.override_color(Colors.green)
        self.output_b.override_color(Colors.blue)
        self.output_a.override_color(Colors.gray)


    def compute(self):
        if self.input_image.is_connected():
            self.input_image.fetch_connected_value()

            channels = self.input_image.get_value().split()
            self.output_r.set_value(channels[0])
            self.output_g.set_value(channels[1])
            self.output_b.set_value(channels[2])
            if len(channels) > 3:
                self.output_a.set_value(channels[3])

            self.set_pixmap(ImageQt.toqpixmap(self.input_image.get_value()))

            super().compute()
            self.set_dirty(False)

