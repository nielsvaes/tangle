from nodes.base_node import BaseNode
import socket_types as socket_types

class BlackAndWhite(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super(BlackAndWhite, self).__init__(scene, x=x, y=y)
        self.change_title("BlackWhite")

        self.input_image = self.add_input(socket_types.PictureSocketType(self), "input_image")
        self.output_image = self.add_output(socket_types.PictureSocketType(self), "output_image")

    def compute(self):
        pass

