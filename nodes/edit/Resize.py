from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from nodes.base_node import BaseNode
import socket_types as socket_types

from functools import partial

import PIL
from PIL import Image, ImageQt, ImageOps, ImageEnhance, ImageFilter

class Resize(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super(Resize, self).__init__(scene, x=x, y=y)
        self.change_title("resize")

        self.input_image = self.add_input(socket_types.PictureSocketType(self), "in")
        self.output_image = self.add_output(socket_types.PictureSocketType(self), "out")

        #self.keep_aspect = self.add_checkbox("Keep aspect ratio")
        self.txt_width = self.add_label_text("New width", txt_text=0, text_changed_function=self.value_changed)[1]
        self.txt_height = self.add_label_text("New height", txt_text=0, text_changed_function=self.value_changed)[1]

        self.txt_width.setValidator(QIntValidator())
        self.txt_width.setValidator(QIntValidator())

    def set_width_height(self, caller):
        # width = self.input_image.get_value()
        # if self.keep_aspect.isChecked():
        #     if caller == "width":
        #         width = int(self.txt_width.text())
        #         new_height =
        #     else:
        #         widget_to_change = self.txt_width
        pass

    def value_changed(self):
        self.set_dirty(True)


    def compute(self):
        if self.input_image.is_connected():
            self.input_image.fetch_connected_value()

            height = int(self.txt_height.text())
            width = int(self.txt_width.text())

            resized = self.input_image.get_value().resize((width, height), Image.ANTIALIAS)
            self.output_image.set_value(resized)

            resized_pixmap = ImageQt.toqpixmap(resized)
            self.set_pixmap(resized_pixmap)

            self.set_dirty(False)