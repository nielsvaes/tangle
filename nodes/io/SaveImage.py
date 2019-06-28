from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import logging
logging.basicConfig(level=logging.DEBUG)

from nodes.base_node import BaseNode
import socket_types as socket_types

import PIL
from PIL import Image, ImageQt, ImageOps, ImageEnhance, ImageFilter

class SaveImage(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super(SaveImage, self).__init__(scene, x=x, y=y)
        self.change_title("save")

        self.input_image = self.add_input(socket_types.PictureSocketType(self), "in")

        self.txt_line = self.add_label_text_button("File path", "Browse...", self.browse)[1]

        # self.add_label("Please click the button")
        # self.add_button("Save image", self.save_image)

    def browse(self):
        file_path = QFileDialog.getSaveFileName(caption="Save image", filter="Image files (*.jpg *.png)")[0]
        if file_path != "":
            self.txt_line.setText(file_path)

    def compute(self):
        if self.input_image.is_connected():
            self.input_image.fetch_connected_value()
            pixmap = ImageQt.toqpixmap(self.input_image.get_value())
            self.set_pixmap(pixmap)
            pixmap.save(self.txt_line.text())
        else:
            self.set_pixmap(self.input_image.get_initial_value())

            self.set_dirty(False)

