from nodes.base_node import BaseNode
from core import socket_types as socket_types

from core.Constants import Colors

class AddFloat(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super().__init__(scene, title_background_color=Colors.add_float, x=x, y=y)
        self.change_title("0.0")

        self.input_01, self.output_float = self.add_input_output(socket_types.FloatSocketType(self), "A")
        self.input_02 = self.add_input(socket_types.FloatSocketType(self), "B")

        self.add_label("Add")
        self.lbl_result = self.add_label("0")
        self.btn_add_input = self.add_button("Add input", clicked_function=self.add_new_input)

        self.inputs = [self.input_01, self.input_02]


    def add_new_input(self):
        next_letter = chr(ord(self.inputs[-1].name) + 1)
        input = self.add_input(socket_types.FloatSocketType(self), next_letter)
        self.inputs.append(input)

    def compute(self):
        if self.is_dirty():
            result = 0.0

            for each in self.inputs:
                each.fetch_connected_value()
                input_value = each.get_value()

                result += input_value

            self.output_float.set_value(result)
            self.lbl_result.setText(str(result))

            self.set_dirty(False)

            self.title.setPlainText(str(result))
            self.reposition_title()
            super().compute()
