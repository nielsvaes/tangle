from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from nodes.image_node import ImageNode
import socket_types as socket_types

import numpy as np

from functools import partial

from PIL import Image, ImageQt, ImageOps, ImageEnhance, ImageFilter

class LoadTest(ImageNode):
    def __init__(self, scene, x=0, y=0):
        super(LoadTest, self).__init__(scene, x=x, y=y)
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

            # pixels = self.input_image.get_value().load()
            # width, height = self.input_image.get_value().size
            # mode = self.input_image.get_value().mode
            #
            # mask = np.zeros((height, width))

            # for y in range(0, height):
            #     for x in range(0, width):
            #         if pixels[x, y][2] > 200:
            #             mask[y][x] = 255

            # mask_image = Image.fromarray(mask).convert(mode)

            ni = np.array(self.input_image.get_value())


            reds = (ni[:,:,0] > 102) & (ni[:,:,0] < 142)
            greens = (ni[:,:,1] > 143) & (ni[:,:,1] < 183)
            blues = (ni[:,:,2] > 150) & (ni[:,:,2] < 230)
            #
            #
            # print("these are the blues")
            # print(blues)

            mask_array = np.logical_and(reds, np.logical_and(greens, blues))
            mask_array = np.invert(mask_array)

            mask_image = Image.fromarray((mask_array * 255).astype(np.uint8))


            #
            # print("mask image")
            # print(np.array(mask_image))


            self.output_image.set_value(mask_image)

            output_pixmap = ImageQt.toqpixmap(mask_image)
            self.set_pixmap(output_pixmap)

            self.get_main_window().set_pixmap(output_pixmap)
            self.set_dirty(False)
