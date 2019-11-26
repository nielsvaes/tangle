from nodes.base_node import BaseNode
from core import socket_types as socket_types

from core.Constants import Colors


class BreakVector3(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super().__init__(scene, title_background_color=Colors.vector3, x=x, y=y)
        self.change_title("[0.0, 0.0, 0.0]")

        self.input_vector = self.add_input(socket_types.Vector3SocketType(self), "vec3")
        self.output_x = self.add_output(socket_types.FloatSocketType(self), "x")
        self.output_y = self.add_output(socket_types.FloatSocketType(self), "y")
        self.output_y = self.add_output(socket_types.FloatSocketType(self), "z")

    def compute(self):
        if self.input_vector.is_connected():
            self.input_vector.fetch_connected_value()

            print(self.input_vector.get_value())

            x_value = self.input_vector.get_value()[0]
            y_value = self.input_vector.get_value()[1]
            z_value = self.input_vector.get_value()[2]

            self.output_x.set_value(x_value)
            self.output_y.set_value(y_value)
            self.output_y.set_value(z_value)

            self.change_title(str(self.input_vector.get_value()))
            self.compute_connected_nodes()

            super().compute()
