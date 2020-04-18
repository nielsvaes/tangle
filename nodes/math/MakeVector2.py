from nodes.base_node import BaseNode
from core import socket_types as socket_types

from core.Constants import Colors


class MakeVector2(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super().__init__(scene, title_background_color=Colors.vector2, x=x, y=y)
        self.change_title("[0.0, 0.0]")

        self.input_x = self.add_input(socket_types.FloatSocketType(self), "x")
        self.input_y = self.add_input(socket_types.FloatSocketType(self), "y")
        self.output_vector = self.add_output(socket_types.Vector2SocketType(self), "vec2")

    def compute(self, force=False):
        if self.is_dirty():
            self.input_x.fetch_connected_value()
            self.input_y.fetch_connected_value()
            output_value = [self.input_x.get_value(), self.input_y.get_value()]
            self.output_vector.set_value(output_value)

            self.change_title(str(output_value))
            super().compute(force=force)
            self.set_dirty(False)

