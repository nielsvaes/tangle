from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from nodes.image_node import ImageNode
import socket_types as socket_types

from functools import partial

from PIL import Image, ImageQt, ImageOps, ImageEnhance, ImageFilter

class PointTest(ImageNode):
    def __init__(self, scene, x=0, y=0):
        super(PointTest, self).__init__(scene, x=x, y=y)
        self.change_title("saturation")

        self.input_image = self.add_input(socket_types.PictureSocketType(self), "in")
        self.output_image = self.add_output(socket_types.PictureSocketType(self), "out")

        # self.add_label("Saturation amount")
        # self.sld_contrast_amount = self.add_slider(0, 800, 100, changed_function=self.slider_changed, released_function=self.slider_released)

        self.add_button("Compute", self.compute)

        self.set_auto_compute_on_connect(True)

    # def slider_changed(self):
    #     self.compute()
    #     self.set_dirty(True)
    #
    # def slider_released(self):
    #     self.scene.refresh_network()

    def compute(self):
        if self.input_image.is_connected():
            self.input_image.fetch_connected_value()

            source = self.input_image.get_value().split()
            R, G, B = 0, 1, 2

            # select regions where red is less than 100
            mask = source[R].point(lambda i: i < 100 and 255)

            # process the green band
            out = source[G].point(lambda i: i * 0.7)

            # paste the processed band back, but only where red was < 100
            source[G].paste(out, None, mask)

            output = Image.merge(self.input_image.get_value().mode, source)

            self.output_image.set_value(output)

            output_pixmap = ImageQt.toqpixmap(output)
            self.set_pixmap(output_pixmap)

            self.get_main_window().set_pixmap(output_pixmap)
            self.set_dirty(False)
