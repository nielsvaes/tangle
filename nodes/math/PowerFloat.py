from nodes.base_node import BaseNode
from core import socket_types as socket_types

from core.Constants import Colors

class PowerFloat(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super().__init__(scene, title_background_color=Colors.power_float, x=x, y=y)
        self.change_title("0.0")

        self.input_01, self.output_float = self.add_input_output(socket_types.FloatSocketType(self), "A")
        self.input_02 = self.add_input(socket_types.FloatSocketType(self), "B")

        self.input_01.set_initial_value(0.0)
        self.input_02.set_initial_value(0.0)

        self.add_label("Power")
        self.lbl_result = self.add_label("0")

        self.inputs = [self.input_01, self.input_02]



    def compute(self, force=False):
        if self.is_dirty():
            self.input_01.fetch_connected_value()
            self.input_02.fetch_connected_value()

            result = self.input_01.get_value() ** self.input_02.get_value()

            self.output_float.set_value(result)
            self.lbl_result.setText(str(result))

            super().compute(force=force)
            self.set_dirty(False)

            self.title.setPlainText(str(result))
            self.reposition_title()