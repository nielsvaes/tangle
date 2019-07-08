from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from nodes.image_node import ImageNode
import socket_types as socket_types

from functools import partial

import PIL
from PIL import Image, ImageQt, ImageOps, ImageEnhance, ImageFilter

class Rotate(ImageNode):
    def __init__(self, scene, x=0, y=0):
        super(Rotate, self).__init__(scene, x=x, y=y)
        self.change_title("rotate")

        self.input_image = self.add_input(socket_types.PictureSocketType(self), "in")
        self.output_image = self.add_output(socket_types.PictureSocketType(self), "out")

        self.chk_counter_clockwise = self.add_checkbox("Counter clockwise", change_checked_function=self.value_changed)
        self.cb_percentage = self.add_label_combobox("Rotate by degrees", ["90", "180", "270"],
                                                     changed_function=self.value_changed)
    def value_changed(self):
        self.set_dirty(True)
        self.scene.refresh_network()

    def compute(self):
        if self.input_image.is_connected():
            self.input_image.fetch_connected_value()

            rotated = self.input_image.get_value()

            degrees_to_rotate = int(self.cb_percentage.currentText())
            if not self.chk_counter_clockwise.isChecked():
                degrees_to_rotate = degrees_to_rotate * -1

            rotated = rotated.rotate(degrees_to_rotate, expand=True)

            self.output_image.set_value(rotated)

            rotated_pixmap = ImageQt.toqpixmap(rotated)
            self.set_pixmap(rotated_pixmap)

            self.set_dirty(False)