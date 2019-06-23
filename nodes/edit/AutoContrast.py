from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from nodes.base_node import BaseNode
import socket_types as socket_types

from functools import partial

import PIL
from PIL import Image, ImageQt, ImageOps, ImageEnhance, ImageFilter

class AutoContrast(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super(AutoContrast, self).__init__(scene, x=x, y=y)
        self.change_title("autocontrast")

        self.input_image = self.add_input(socket_types.PictureSocketType(self), "in")
        self.output_image = self.add_output(socket_types.PictureSocketType(self), "out")

        self.add_label("Contrast amount")
        self.sld_contrast_amount = self.add_slider(0, 50, 20, self.slider_changed)

    def slider_changed(self):
        self.set_dirty(True)

    def compute(self):
        if self.input_image.is_connected():
            self.input_image.fetch_connected_value()

            contrasted = self.input_image.get_value()

            contrasted = ImageOps.autocontrast(contrasted, cutoff = self.sld_contrast_amount.value())

            self.output_image.set_value(contrasted)

            contrasted_pixmap = ImageQt.toqpixmap(contrasted)
            self.set_pixmap(contrasted_pixmap)

            self.set_dirty(False)