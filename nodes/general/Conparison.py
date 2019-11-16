from nodes.base_node import BaseNode
import socket_types as socket_types

from core.Constants import Colors

class Conparison(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super(Conparison, self).__init__(scene, title_background_color=Colors.subtract_float, x=x, y=y)
        self.change_title("comparison")

        self.input_01, self.output_true = self.add_input_output(socket_types.DebugSocketType(self), "true")
        self.input_02, self.output_false = self.add_input_output(socket_types.DebugSocketType(self), "false")

        self.cb_operation = self.add_combobox(["equal to", "not equal to", "bigger than", "smaller than"], changed_function=self.operation_changed)

        self.set_auto_compute_on_connect(True)

    def operation_changed(self):
        self.set_dirty(True)
        self.compute()

    def compute(self):
        if self.is_dirty():
            operation = self.cb_operation.currentText()
            print("computing")
            if self.input_01.is_connected() and self.input_02.is_connected():
                print("both are connected")

                self.input_01.fetch_connected_value()
                self.input_02.fetch_connected_value()

                if not type(self.input_01.socket_type) == type(self.input_02.socket_type):
                    return

                self.output_true.change_socket_type(self.input_01.socket_type, self.input_01.get_connected_sockets()[0].color)
                self.output_false.change_socket_type(self.input_01.socket_type, self.input_01.get_connected_sockets()[0].color)

                result = False

                if operation == "equal to":
                    result = True if self.input_01.get_value() == self.input_02.get_value() else False
                if operation == "not equal to":
                    result = True if self.input_01.get_value() != self.input_02.get_value() else False
                if operation == "bigger than":
                    result = True if self.input_01.get_value() > self.input_02.get_value() else False
                if operation == "smaller than":
                    result = True if self.input_01.get_value() < self.input_02.get_value() else False

                # self.output.set_value(result)
                print("setting result")

                if result:
                    self.compute_connected_nodes(output_socket=self.output_true)
                else:
                    self.compute_connected_nodes(output_socket=self.output_true)
                self.set_dirty(False)

