from nodes.base_node import BaseNode
import socket_types as socket_types

from core.Constants import Colors
from PIL import ImageQt, ImageOps

class Float(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super(Float, self).__init__(scene, title_background_color=Colors.float, x=x, y=y)
        self.change_title("0.0")

        self.output_float = self.add_output(socket_types.FloatSocketType(self), "float")
        self.spin_number = self.add_spinbox(changed_function=self.spin_value_entered)

    def spin_value_entered(self):
        self.output_float.set_value(self.spin_number.value())

        self.compute_connected_nodes()

        self.set_dirty(True)

        self.title.setPlainText(str(self.spin_number.value()))
        self.reposition_title()

    def compute(self):
        if self.is_dirty():
            self.set_dirty(False)