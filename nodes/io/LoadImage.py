from PyQt5.QtWidgets import *

from nodes.base_node import BaseNode
import socket_types as socket_types

class LoadImage(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super(LoadImage, self).__init__(scene, x=x, y=y)
        self.change_title("*PICTURE*")

        self.output_image = self.add_output(socket_types.PictureSocketType(self), "output_image")

        self.add_label("Please click the button")
        self.add_button("Load image", self.load_image)

    def load_image(self):
        file_path = QFileDialog.getOpenFileName(caption="Open image", filter="Image files (*.jpg *.png)")[0]
        if file_path != "":
            print(file_path)


    def compute(self):
        pass

