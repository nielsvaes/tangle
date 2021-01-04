from ..base_node import BaseNode
from ...core import socket_types as socket_types

from ...core.Constants import Colors

class DivideFloat(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super().__init__(scene, title_background_color=Colors.divide_float, x=x, y=y)
        self.change_title("0.0")

        self.input_01 = self.add_input(socket_types.FloatSocketType(self), "A")
        self.input_02 = self.add_input(socket_types.FloatSocketType(self), "B")
        self.output_float = self.add_output(socket_types.FloatSocketType(self), "out")

        self.add_label("Divide")
        self.lbl_result = self.add_label("0")

        self.inputs = [self.input_01, self.input_02]

        self.set_help_text("Divides A by B")

    def compute(self, force=False):
        if self.is_dirty():
            result = 0.0

            self.input_01.fetch_connected_value()
            self.input_02.fetch_connected_value()

            if self.input_02.get_value() != 0:
                result = self.input_01.get_value() / self.input_02.get_value()
                # result = self.round_float(result)

                self.output_float.set_value(result)
                self.lbl_result.setText(str(self.output_float.get_value()))

                super().compute(force=force)
                self.set_dirty(False)

                self.title.setPlainText(str(self.output_float.get_value()))
                self.reposition_title()