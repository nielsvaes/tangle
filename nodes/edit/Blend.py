from nodes.base_node import BaseNode
import socket_types as socket_types

class Blend(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super(Blend, self).__init__(scene, x=x, y=y)
        self.change_title("Blend")

        self.foreground_image = self.add_input(socket_types.PictureSocketType(self), "foreground_image")
        self.background_image = self.add_input(socket_types.PictureSocketType(self), "background_image")
        self.output_image = self.add_output(socket_types.PictureSocketType(self), "output_image")

        self.add_label("Blend")
        self.add_slider(self.change_blend)

    def change_blend(self):
        pass

    def compute(self):
        pass

