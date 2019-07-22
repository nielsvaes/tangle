from nodes.base_node import BaseNode
import socket_types as socket_types

from core.Constants import Colors

class SubtractFloat(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super(SubtractFloat, self).__init__(scene, title_background_color=Colors.subtract_float, x=x, y=y)
        self.change_title("0.0")

        self.input_01, self.output_float = self.add_input_output(socket_types.FloatSocketType(self), "A")
        self.input_02 = self.add_input(socket_types.FloatSocketType(self), "B")

        self.add_label("Subtract")
        self.lbl_result = self.add_label("0")
        self.btn_add_input = self.add_button("Add input", clicked_function=self.add_new_input)

        self.inputs = [self.input_02]

        self.set_auto_compute_on_connect(True)

    def add_new_input(self):
        next_letter = chr(ord(self.inputs[-1].name) + 1)
        input = self.add_input(socket_types.FloatSocketType(self), next_letter)
        self.inputs.append(input)


    def compute(self):
        if self.is_dirty():
            self.input_01.fetch_connected_value()
            result = self.input_01.get_value()

            for each in self.inputs:
                each.fetch_connected_value()
                input_value = each.get_value()

                result -= input_value

            self.output_float.set_value(result)
            self.lbl_result.setText(str(result))

            self.compute_connected_nodes()
            self.set_dirty(False)

            self.title.setPlainText(str(result))
            self.reposition_title()