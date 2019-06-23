from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from nodes.base_node import BaseNode
import socket_types as socket_types
import utils.image as im_utils

import PIL
from PIL import Image, ImageQt, ImageOps, ImageEnhance, ImageFilter

class Sharpen(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super(Sharpen, self).__init__(scene, x=x, y=y)
        self.change_title("*SHARPEN*")

        self.input_image = self.add_input(socket_types.PictureSocketType(self), "in")
        self.output_image = self.add_output(socket_types.PictureSocketType(self), "out")

        self.sld_sharpen_amount = self.add_slider(0, 10, 0, self.slider_changed)

    def slider_changed(self):
        self.set_dirty(True)

    def compute(self):
        if self.input_image.is_connected():
            self.input_image.fetch_connected_value()

            sharpen = self.input_image.get_value()
            for i in range(0, self.sld_sharpen_amount.value()):
                sharpen = sharpen.filter(ImageFilter.SHARPEN)

            self.output_image.set_value(sharpen)

            sharpen_pixmap = ImageQt.toqpixmap(sharpen)
            self.set_pixmap(sharpen_pixmap)

            self.set_dirty(False)
