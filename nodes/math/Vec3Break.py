import logging

from nv_NodeEditor.nodes.base_node import BaseNode
import nv_NodeEditor.socket_types as socket_types
from nv_NodeEditor.core.Constants import ss


class Vec3Break(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super(Vec3Break, self).__init__(scene, x=x, y=y)

        self.change_title("break_vec3")

        self.x = self.add_output(socket_types.FloatSocketType(self, "x output"), "x output")
        self.x.set_initial_value(0)
        self.y = self.add_output(socket_types.FloatSocketType(self, "y output"), "y output")
        self.y.set_initial_value(0)
        self.z = self.add_output(socket_types.FloatSocketType(self, "z output"), "z output")
        self.z.set_initial_value(0)

        self.input_vector = self.add_input(socket_types.Vector3SocketType(self),"input")
        self.input_vector.set_initial_value([0.0, 0.0, 0.0])

        self.set_auto_compute(False)

    def compute(self):
        x = self.input_vector.get_value()[0]
        y = self.input_vector.get_value()[1]
        z = self.input_vector.get_value()[2]

        try:
            self.x.set_value(x)
            self.y.set_value(y)
            self.z.set_value(z)
        except StandardError, err:
            self.error("Can't set result value!")
        #
        # if self.x.is_connected():
        #     self.result_vector.socket_type.ui_widget.x_spin.setStyleSheet(ss.node_result_calculated)
        #     self.result_vector.socket_type.ui_widget.x_spin.setEnabled(False)
        # else:
        #     self.result_vector.socket_type.ui_widget.x_spin.setStyleSheet("")
        #     self.result_vector.socket_type.ui_widget.x_spin.setEnabled(True)
        #
        # if self.y.is_connected():
        #     self.result_vector.socket_type.ui_widget.y_spin.setStyleSheet(ss.node_result_calculated)
        #     self.result_vector.socket_type.ui_widget.y_spin.setEnabled(False)
        # else:
        #     self.result_vector.socket_type.ui_widget.y_spin.setStyleSheet("")
        #     self.result_vector.socket_type.ui_widget.y_spin.setEnabled(True)
        #
        # if self.z.is_connected():
        #     self.result_vector.socket_type.ui_widget.z_spin.setStyleSheet(ss.node_result_calculated)
        #     self.result_vector.socket_type.ui_widget.z_spin.setEnabled(False)
        # else:
        #     self.result_vector.socket_type.ui_widget.z_spin.setStyleSheet("")
        #     self.result_vector.socket_type.ui_widget.z_spin.setEnabled(True)


