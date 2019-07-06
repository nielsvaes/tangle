from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from nodes.image_node import ImageNode
import socket_types as socket_types

from functools import partial

import PIL
from PIL import Image, ImageQt, ImageOps, ImageEnhance, ImageFilter

class Brightness(ImageNode):
    def __init__(self, scene, x=0, y=0):
        super(Brightness, self).__init__(scene, x=x, y=y)
        self.change_title("brightness")

        self.input_image = self.add_input(socket_types.PictureSocketType(self), "in")
        self.output_image = self.add_output(socket_types.PictureSocketType(self), "out")

        self.add_label("Brightness amount")
        self.sld_contrast_amount = self.add_slider(0, 400, 100, changed_function=self.slider_changed, released_function=self.slider_released)

        self.set_auto_compute_on_connect(True)

    def slider_changed(self):
        self.compute()
        self.set_dirty(True)

    def slider_released(self):
        self.scene.refresh_network()


    def compute(self):
        if self.input_image.is_connected():
            self.input_image.fetch_connected_value()

            factor = self.sld_contrast_amount.value()

            brightened = ImageEnhance.Brightness(self.input_image.get_value()).enhance(factor / 100)

            self.output_image.set_value(brightened)

            contrasted_pixmap = ImageQt.toqpixmap(brightened)
            self.set_pixmap(contrasted_pixmap)

            self.get_main_window().set_pixmap(contrasted_pixmap)
            self.set_dirty(False)
