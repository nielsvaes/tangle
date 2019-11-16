from nodes.base_node import BaseNode
import socket_types as socket_types

from core.Constants import Colors

class Condition(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super(Condition, self).__init__(scene, title_background_color=Colors.subtract_float, x=x, y=y)
        self.change_title("comparison")

        self.input_01 = self.add_input(socket_types.BooleanSocketType(self), "A")

        self.output_true = self.add_output(socket_types.DebugSocketType(self), "true")
        self.output_false = self.add_output(socket_types.DebugSocketType(self), "false")

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
                    print(self.input_01.socket_type)
                    print(self.input_02.socket_type)
                    return

                self.output.change_socket_type(self.input_01.socket_type, self.input_01.get_connected_sockets()[0].color)

                result = False

                if operation == "equal to":
                    result = True if self.input_01.get_value() == self.input_02.get_value() else False
                if operation == "not equal to":
                    result = True if self.input_01.get_value() != self.input_02.get_value() else False
                if operation == "bigger than":
                    result = True if self.input_01.get_value() > self.input_02.get_value() else False
                if operation == "smaller than":
                    result = True if self.input_01.get_value() < self.input_02.get_value() else False

                self.output.set_value(result)
                print("setting result")

                self.compute_connected_nodes()
                self.set_dirty(False)

