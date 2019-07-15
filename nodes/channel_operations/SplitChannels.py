from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import logging
logging.basicConfig(level=logging.DEBUG)

from nodes.image_node import ImageNode
import socket_types as socket_types
from core.Constants import Colors

import PIL
from PIL import Image, ImageQt, ImageOps, ImageEnhance, ImageFilter

class SplitChannels(ImageNode):
    def __init__(self, scene, x=0, y=0):
        super(SplitChannels, self).__init__(scene, title_background_color=Colors.split_channel, x=x, y=y)
        self.change_title("split")

        self.input_image = self.add_input(socket_types.PictureSocketType(self), "RGB(A) in")
        self.output_r = self.add_output(socket_types.PictureSocketType(self), "out R")
        self.output_g = self.add_output(socket_types.PictureSocketType(self), "out G")
        self.output_b = self.add_output(socket_types.PictureSocketType(self), "out B")
        self.output_a = self.add_output(socket_types.PictureSocketType(self), "out A")

        self.output_r.override_color(Colors.red)
        self.output_g.override_color(Colors.green)
        self.output_b.override_color(Colors.blue)
        self.output_a.override_color(Colors.gray)

        self.set_auto_compute_on_connect(True)


    def compute(self):
        if self.input_image.is_connected():
            print("computing split")
            self.input_image.fetch_connected_value()

            channels = self.input_image.get_value().split()
            self.output_r.set_value(channels[0])
            self.output_g.set_value(channels[1])
            self.output_b.set_value(channels[2])
            if len(channels) > 3:
                self.output_a.set_value(channels[3])

            self.set_pixmap(ImageQt.toqpixmap(self.input_image.get_value()))

            self.set_dirty(False)

