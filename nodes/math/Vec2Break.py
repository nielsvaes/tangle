import logging

from nv_NodeEditor.nodes.base_node import BaseNode
import nv_NodeEditor.socket_types as socket_types
from nv_NodeEditor.core.Constants import ss


class Vec2Break(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super(Vec2Break, self).__init__(scene, x=x, y=y)

        self.change_title("break_vec2")

        self.x = self.add_output(socket_types.FloatSocketType(self, "x output"), "x output")
        self.x.set_initial_value(0)
        self.y = self.add_output(socket_types.FloatSocketType(self, "y output"), "y output")
        self.y.set_initial_value(0)


        self.input_vector = self.add_input(socket_types.Vector2SocketType(self),"input")
        self.input_vector.set_initial_value([0.0, 0.0])

        self.set_auto_compute(False)

    def compute(self):
        x = self.input_vector.get_value()[0]
        y = self.input_vector.get_value()[1]

        try:
            self.x.set_value(x)
            self.y.set_value(y)
        except StandardError, err:
            self.error("Can't set result value!")
