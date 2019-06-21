from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import logging
logging.basicConfig(level=logging.DEBUG)

from nodes.base_node import BaseNode
import socket_types as socket_types

class SaveImage(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super(SaveImage, self).__init__(scene, x=x, y=y)
        self.change_title("*PICTURE*")

        self.input_image = self.add_input(socket_types.PictureSocketType(self), "input_image")

        self.add_label("Please click the button")
        self.add_button("Save image", self.save_image)

    def save_image(self):
        file_path = QFileDialog.getSaveFileName(caption="Save image", filter="Image files (*.jpg *.png)")[0]
        if file_path != "":
            self.get_pixmap().save(file_path)

    def compute(self):
        logging.debug("Computing %s - %s" % (self.title, self.uuid))
        for node in self.get_connected_input_nodes():
            self.set_pixmap(node.get_pixmap())


