from nodes.base_node import BaseNode
from core import socket_types as socket_types

from core.Constants import Colors

class Percentage(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super().__init__(scene, title_background_color=Colors.add_float, x=x, y=y)
        self.change_title("0.0")

        self.input_01, self.output_float = self.add_input_output(socket_types.FloatSocketType(self), "number")
        self.input_percentage = self.add_input(socket_types.FloatSocketType(self), "percent")

        self.add_label("Percentage")
        self.lbl_result = self.add_label("0.0")


        self.set_auto_compute_on_connect(True)

    def compute(self):
        if self.is_dirty():
            result = 0.0

            for input in self.get_all_input_sockets():
                input.fetch_connected_value()

            result = (self.input_01.get_value() * self.input_percentage.get_value()) / 100

            self.output_float.set_value(result)
            self.lbl_result.setText(str(result))

            self.set_dirty(False)

            self.title.setPlainText(str(result))
            self.reposition_title()
            super().compute()