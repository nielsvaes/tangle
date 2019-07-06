from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from nodes.image_node import ImageNode
import socket_types as socket_types
import utils.image as im_utils

import PIL
from PIL import Image, ImageQt, ImageOps, ImageEnhance, ImageFilter

class Blur(ImageNode):
    def __init__(self, scene, x=0, y=0):
        super(Blur, self).__init__(scene, x=x, y=y)
        self.change_title("blur")

        self.input_image = self.add_input(socket_types.PictureSocketType(self), "in")
        self.output_image = self.add_output(socket_types.PictureSocketType(self), "out")

        self.sld_blur_amount = self.add_slider(0, 50, 0, self.slider_changed)

        self.set_auto_compute_on_connect(True)

    def slider_changed(self):
        self.set_dirty(True)
        self.scene.refresh_network()

    def compute(self):
        if self.input_image.is_connected():
            self.input_image.fetch_connected_value()

            blurred = self.input_image.get_value().filter(ImageFilter.GaussianBlur(radius=self.sld_blur_amount.value()))
            self.output_image.set_value(blurred)

            blurred_pixmap = ImageQt.toqpixmap(blurred)
            self.set_pixmap(blurred_pixmap)

            self.get_main_window().set_pixmap(blurred_pixmap)
            self.set_dirty(False)
