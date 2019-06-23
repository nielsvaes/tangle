from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import PIL
from PIL import Image, ImageQt, ImageOps, ImageEnhance

from nodes.base_node import BaseNode
import socket_types as socket_types

from utils import image as im_utils

class LoadImage(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super(LoadImage, self).__init__(scene, x=x, y=y)
        self.change_title("load_image")

        self.output_image = self.add_output(socket_types.PictureSocketType(self), "out")

        self.scene = scene

        self.add_button("Load image", self.load_image)

    def load_image(self):
        file_path = QFileDialog.getOpenFileName(caption="Open image", filter="Image files (*.jpg *.png)")[0]

        if file_path != "":
            pil_img = Image.open(file_path)

            pixmap = ImageQt.toqpixmap(pil_img)
            self.set_pixmap(pixmap)
            self.output_image.set_value(pil_img)

        self.scene.get_main_window().load_values_ui()
        self.set_dirty(True)

    def compute(self):
        if self.is_dirty():
            self.set_dirty(False)

