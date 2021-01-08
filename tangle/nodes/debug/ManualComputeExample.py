from ..base_node import BaseNode
from ...core import socket_types as socket_types
from ez_utils.decorators import timeit

from ...core.Constants import Colors

class ManualComputeExample(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super().__init__(scene, title_background_color=Colors.add_float, x=x, y=y)
        self.change_title("0.0")

        self.input_01 = self.add_input(socket_types.FloatSocketType(self), "A")
        self.input_02 = self.add_input(socket_types.FloatSocketType(self), "B")
        self.output_float = self.add_output(socket_types.FloatSocketType(self), "Result")
        self.something_else_in, self.something_else_out = self.add_input_output(socket_types.ListSocketType(self), "Something")

        self.add_label("Manual Compute Example")
        self.lbl_result = self.add_label("0")
        self.btn_add_input = self.add_button("Add input", clicked_function=self.add_new_input)

        self.inputs = [self.input_01, self.input_02]

        self.set_auto_compute_on_connect(False)

    def add_new_input(self):
        next_letter = chr(ord(self.inputs[-1].name) + 1)
        input = self.add_input(socket_types.FloatSocketType(self), next_letter)
        self.inputs.append(input)

    @timeit
    def compute(self, force=False):
        if not self.get_auto_compute_on_connect() and force:
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
                super().compute(force=force)
