from PyQt5.QtWidgets import *

from functools import partial

from PIL import Image, ImageQt

from core.Constants import Colors
from nodes.image_node import ImageNode
from core import socket_types as socket_types


class LoadImage(ImageNode):
    def __init__(self, scene, x=0, y=0):
        super(LoadImage, self).__init__(scene, title_background_color=Colors.load_image, x=x, y=y)
        self.change_title("load_image")

        self.output_image = self.add_output(socket_types.PictureSocketType(self), "out")
        self.size = self.add_output(socket_types.TupleSocketType(self), "size")

        self.scene = scene

        self.add_button("Load image", self.load_image)
        self.load_image()

    def load_image(self):
        file_path = QFileDialog.getOpenFileName(caption="Open image", filter="Image files (*.jpg *.png *.tga)")[0]

        if file_path != "":
            pil_img = Image.open(file_path)

            pixmap = ImageQt.toqpixmap(pil_img)
            self.set_pixmap(pixmap)
            self.output_image.set_value(pil_img)

            self.size.set_value(pil_img.size)

        self.scene.get_main_window().load_values_ui()

        self.compute_connected_nodes()

    def compute(self):
        if self.is_dirty():
            self.set_dirty(False)

