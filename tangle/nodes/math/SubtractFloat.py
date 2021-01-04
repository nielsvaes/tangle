from ..base_node import BaseNode
from ...core import socket_types as socket_types

from ...core.Constants import Colors

class SubtractFloat(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super().__init__(scene, title_background_color=Colors.subtract_float, x=x, y=y)
        self.change_title("0.0")

        self.input_01 = self.add_input(socket_types.FloatSocketType(self), "A")
        self.input_02 = self.add_input(socket_types.FloatSocketType(self), "B")
        self.output_float = self.add_output(socket_types.FloatSocketType(self), "out")

        self.add_label("Subtract")
        self.lbl_result = self.add_label("0")
        self.btn_add_input = self.add_button("Add input", clicked_function=self.add_new_input)

        self.inputs = [self.input_02]
        
        self.set_help_text("Subtracts all inputs from the first input (A)")

    def add_new_input(self):
        next_letter = chr(ord(self.inputs[-1].name) + 1)
        input = self.add_input(socket_types.FloatSocketType(self), next_letter)
        self.inputs.append(input)

        self.set_help_text("Subtracts all inputs from the first input (A)")

    def compute(self, force=False):
        if self.is_dirty():
            self.input_01.fetch_connected_value()
            result = self.input_01.get_value()

            for each in self.inputs:
                each.fetch_connected_value()
                input_value = each.get_value()

                result -= input_value

            self.output_float.set_value(result)
            self.lbl_result.setText(str(result))

            super().compute(force=force)
            self.set_dirty(False)

            self.title.setPlainText(str(result))
            self.reposition_title()