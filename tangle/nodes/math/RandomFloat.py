import random

from ..base_node import BaseNode
from ...core import socket_types as socket_types

from ...core.Constants import Colors

class RandomFloat(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super().__init__(scene, title_background_color=Colors.add_float, x=x, y=y)
        self.change_title("0.0")

        self.input_min = self.add_input(socket_types.FloatSocketType(self), "min")
        self.output_float = self.add_output(socket_types.FloatSocketType(self), "out")
        self.input_max = self.add_input(socket_types.FloatSocketType(self), "max")

        self.add_label("Random")
        self.btn_random = self.add_button("Get new value", clicked_function=self.get_new_value)

        self.lbl_result = self.add_label("0")

        self.set_help_text("Generates a single float value between Min and Max values")

    def get_new_value(self):
        self.set_dirty(True)
        self.compute()

    def compute(self, force=False):
        if self.is_dirty():
            self.input_min.fetch_connected_value()
            self.input_max.fetch_connected_value()

            result = random.uniform(self.input_min.get_value(), self.input_max.get_value())

            self.output_float.set_value(result)
            self.lbl_result.setText(str(self.output_float.get_value()))

            self.set_dirty(False)

            self.title.setPlainText(str(self.output_float.get_value()))
            self.reposition_title()
            super().compute(force=force)

    # def save(self):
    #     node_dict = super().save()
    #
    # def load(self, node_dict, x=None, y=None):
    #     super().load(node_dict, x=x, y=y)
