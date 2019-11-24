from nodes.base_node import BaseNode
import socket_types as socket_types

from core.Constants import Colors
from PIL import ImageQt, ImageOps

class Float(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super(Float, self).__init__(scene, title_background_color=Colors.float, x=x, y=y)
        self.change_title("0.0")

        self.output_float = self.add_output(socket_types.FloatSocketType(self), "float")
        _, self.txt_number = self.add_label_float("number: ", number_changed_function=self.number_changed)

    def number_changed(self):
        if self.txt_number.text() == "":
            self.txt_number.setText("0.0")
        self.output_float.set_value(float(self.txt_number.text()))

        self.compute_connected_nodes()

        self.set_dirty(True)
        self.compute()

    def compute(self):
        if self.is_dirty():
            self.change_title(str(self.txt_number.text()))
            self.set_dirty(False)

