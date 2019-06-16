import logging

from nv_NodeEditor.nodes.base_node import BaseNode
import nv_NodeEditor.socket_types as socket_types
from nv_NodeEditor.core.Constants import ss


class Vec2Make(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super(Vec2Make, self).__init__(scene, x=x, y=y)

        self.change_title("make_vec2")

        # self.add_execution_input()
        # self.add_execution_output()

        self.x = self.add_input(socket_types.FloatSocketType(self, "x input"), "x input")
        self.x.set_initial_value(0)
        self.y = self.add_input(socket_types.FloatSocketType(self, "y input"), "y input")
        self.y.set_initial_value(0)


        self.result_vector = self.add_output(socket_types.Vector2SocketType(self), "result")
        self.result_vector.set_initial_value([0.0, 0.0])

        self.set_auto_compute(False)

    def compute(self):
        result = [self.x.get_value(), self.y.get_value()]
        try:
            self.result_vector.set_value(result)
        except StandardError, err:
            self.error(self.result_vector, "Can't set result value!")


        if self.x.is_connected():
            self.result_vector.socket_type.x_spin.setStyleSheet(ss.socket_ui_connected)
            self.result_vector.socket_type.x_spin.setEnabled(False)
        else:
            self.result_vector.socket_type.x_spin.setStyleSheet("")
            self.result_vector.socket_type.x_spin.setEnabled(True)

        if self.y.is_connected():
            self.result_vector.socket_type.y_spin.setStyleSheet(ss.socket_ui_connected)
            self.result_vector.socket_type.y_spin.setEnabled(False)
        else:
            self.result_vector.socket_type.y_spin.setStyleSheet("")
            self.result_vector.socket_type.y_spin.setEnabled(True)
