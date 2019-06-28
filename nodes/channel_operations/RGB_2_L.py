from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import logging
logging.basicConfig(level=logging.DEBUG)

from nodes.base_node import BaseNode
import socket_types as socket_types
from core.Constants import Colors

import PIL
from PIL import Image, ImageQt, ImageOps, ImageEnhance, ImageFilter

class RGB_2_L(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super(RGB_2_L, self).__init__(scene, x=x, y=y)
        self.change_title("rgb_2_l")

        self.input_image = self.add_input(socket_types.PictureSocketType(self), "RGB in")
        self.output_image = self.add_output(socket_types.PictureSocketType(self), "L out")
        self.output_image.override_color(Colors.gray)

        self.set_auto_compute_on_connect(True)


    def compute(self):
        if self.input_image.is_connected():
            print("computing rgb 2 l")
            self.input_image.fetch_connected_value()

            converted = self.input_image.get_value().convert("L")

            self.output_image.set_value(converted)

            pixmap = ImageQt.toqpixmap(converted)
            self.set_pixmap(pixmap)

            self.set_dirty(False)

