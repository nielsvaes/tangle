from nodes.base_node import BaseNode
import socket_types as socket_types

from core.Constants import Colors
from PIL import ImageQt, ImageOps

class AddFloat(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super(AddFloat, self).__init__(scene, title_background_color=Colors.float, x=x, y=y)
        self.change_title("float")

        self.input_01, self.output_float = self.add_input_output(socket_types.FloatSocketType(self), "A")
        self.input_02 = self.add_input(socket_types.FloatSocketType(self), "B")

        self.result_label = self.add_label("0")

        self.set_auto_compute_on_connect(True)

    def compute(self):
        self.input_01.fetch_connected_value()
        self.input_02.fetch_connected_value()

        try:
            result = self.input_01.get_value() + self.input_02.get_value()
        except Exception as err:
            result = 0.0

        self.output_float.set_value(result)
        self.result_label.setText(str(result))

        self.set_dirty(False)