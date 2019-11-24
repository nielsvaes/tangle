from PyQt5.QtWidgets import *

import logging
logging.basicConfig(level=logging.DEBUG)

from nodes.image_node import ImageNode
from core import socket_types as socket_types

from core.Constants import Colors
from PIL import ImageQt


class SaveImage(ImageNode):
    def __init__(self, scene, x=0, y=0):
        super(SaveImage, self).__init__(scene, title_background_color=Colors.save_image, x=x, y=y)
        self.change_title("save")

        self.input_image = self.add_input(socket_types.PictureSocketType(self), "in")

        self.txt_line = self.add_label_text_button("File path", "Browse...", self.browse)[1]
        self.btn_save = self.add_button("Save", self.save)

        # self.add_label("Please click the button")
        # self.add_button("Save image", self.save_image)

    def browse(self):
        file_path = QFileDialog.getSaveFileName(caption="Save image", filter="Image files (*.jpg *.png)")[0]
        if file_path != "":
            self.txt_line.setText(file_path)

    def save(self):
        if self.input_image.is_connected():
            self.input_image.fetch_connected_value()
            pixmap = ImageQt.toqpixmap(self.input_image.get_value())
            self.set_pixmap(pixmap)
            pixmap.save(self.txt_line.text())

    def compute(self):
        pass


