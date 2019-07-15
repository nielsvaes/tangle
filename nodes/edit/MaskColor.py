from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from nodes.image_node import ImageNode
import socket_types as socket_types

import numpy as np

from core.Constants import Colors

from PIL import Image, ImageQt

class MaskColor(ImageNode):
    def __init__(self, scene, x=0, y=0):
        super(MaskColor, self).__init__(scene, title_background_color=Colors.mask_color, x=x, y=y)
        self.change_title("mask_color")

        # self.input_image = self.add_input(socket_types.PictureSocketType(self), "in")
        # self.output_image = self.add_output(socket_types.PictureSocketType(self), "mask")

        self.input_image, self.output_image = self.add_input_output(socket_types.PictureSocketType(self), "image")

        self.output_image.override_color(Colors.black)

        self.add_label("Spread")
        self.sld_spread_amount = self.add_slider(0, 255, 0, changed_function=self.slider_changed, released_function=self.slider_released)

        self.add_button("Pick color", self.pick_color)

        self.picked_r = 0
        self.picked_g = 0
        self.picked_b = 0

        self.set_auto_compute_on_connect(True)

    def pick_color(self):
        color_dialog = QColorDialog()
        color = color_dialog.getColor()

        if color is not None:
            self.picked_r = color.red()
            self.picked_g = color.green()
            self.picked_b = color.blue()

            self.compute()

    def slider_changed(self):
        self.compute()
        self.set_dirty(True)

    def slider_released(self):
        self.scene.refresh_network()

    def clamp(self, min_val, max_val, value):
        if value <= min_val:
            return min_val
        if value >= max_val:
            return max_val
        return value

    def compute(self):
        if self.input_image.is_connected():
            self.input_image.fetch_connected_value()

            spread = self.clamp(0, 255, self.sld_spread_amount.value())

            r_max = self.clamp(0, 255, self.picked_r + spread)
            g_max = self.clamp(0, 255, self.picked_g + spread)
            b_max = self.clamp(0, 255, self.picked_b + spread)

            r_min = self.clamp(0, 255, self.picked_r - spread)
            g_min = self.clamp(0, 255, self.picked_g - spread)
            b_min = self.clamp(0, 255, self.picked_b - spread)

            image_array = np.array(self.input_image.get_value())

            reds = (image_array[:,:,0] > r_min) & (image_array[:,:,0] < r_max)
            greens = (image_array[:,:,1] > g_min) & (image_array[:,:,1] < g_max)
            blues = (image_array[:,:,2] > b_min) & (image_array[:,:,2] < b_max)

            mask_array = np.logical_and(reds, np.logical_and(greens, blues))
            # mask_array = np.invert(mask_array)

            mask_image = Image.fromarray((mask_array * 255).astype(np.uint8))

            self.output_image.set_value(mask_image)

            output_pixmap = ImageQt.toqpixmap(mask_image)
            self.set_pixmap(output_pixmap)

            self.get_main_window().set_pixmap(output_pixmap)
            self.set_dirty(False)
