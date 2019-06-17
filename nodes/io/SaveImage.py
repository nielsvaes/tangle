from nodes.base_node import BaseNode
import socket_types as socket_types

class SaveImage(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super(SaveImage, self).__init__(scene, x=x, y=y)
        self.change_title("*PICTURE*")

        self.output_image = self.add_input(socket_types.PictureSocketType(self), "output_image")

        self.add_label("Please click the button")
        self.add_button("Save image", self.load_image)

    def load_image(self):
        print("Saving image!")

    def compute(self):
        pass

