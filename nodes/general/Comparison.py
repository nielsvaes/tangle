from nodes.base_node import BaseNode
from core import socket_types as socket_types
from functools import partial

from core.Constants import Colors

class Comparison(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super(Comparison, self).__init__(scene, title_background_color=Colors.subtract_float, x=x, y=y)
        self.change_title("comparison")

        self.input_01 = self.add_input(socket_types.DebugSocketType(self), "value 1")
        self.input_02 = self.add_input(socket_types.DebugSocketType(self), "value 2")

        self.value_if_true = self.add_input(socket_types.DebugSocketType(self), "value true")
        self.value_if_false = self.add_input(socket_types.DebugSocketType(self), "value false")

        self.output = self.add_output(socket_types.DebugSocketType(self), "output")

        for socket in [self.input_01, self.input_02, self.value_if_true, self.value_if_false]:
            socket.got_connected.signal.connect(partial(self.change_type, socket))
            socket.got_disconnected.signal.connect(partial(self.change_type, socket, socket_types.DebugSocketType(self)))

        self.cb_operation = self.add_combobox(["equal to", "not equal to", "bigger than", "smaller than"], changed_function=self.operation_changed)

        self.set_auto_compute_on_connect(True)

    def change_type(self, socket, new_socket_type=None):
        if new_socket_type is None:
            new_socket_type = socket.get_connected_sockets()[0].socket_type
        socket.change_socket_type(new_socket_type)


    def operation_changed(self):
        self.set_dirty(True)
        self.compute()

    def compute(self):
        if self.is_dirty():
            operation = self.cb_operation.currentText()
            if self.value_if_true.is_connected() and self.value_if_false.is_connected():

                self.value_if_true.fetch_connected_value()
                self.value_if_false.fetch_connected_value()

                if self.input_01.is_connected() and self.input_02.is_connected():
                    self.input_01.fetch_connected_value()
                    self.input_02.fetch_connected_value()

                    if not type(self.input_01.socket_type) == type(self.input_02.socket_type):
                        return

                    result = False

                    try:
                        if operation == "equal to":
                            result = True if self.input_01.get_value() == self.input_02.get_value() else False
                        if operation == "not equal to":
                            result = True if self.input_01.get_value() != self.input_02.get_value() else False
                        if operation == "bigger than":
                            result = True if self.input_01.get_value() > self.input_02.get_value() else False
                        if operation == "smaller than":
                            result = True if self.input_01.get_value() < self.input_02.get_value() else False
                    except TypeError as err:
                        pass

                    self.change_title(str(result))

                    if result:
                        print(self.value_if_true.get_value())
                        self.output.change_socket_type(self.value_if_true.socket_type)
                        self.output.set_value(self.value_if_true.get_value())
                        print(self.value_if_true.get_value())
                    else:
                        self.output.change_socket_type(self.value_if_false.socket_type)
                        self.output.set_value(self.value_if_false.get_value())

                    self.compute_connected_nodes()
                    self.set_dirty(False)
            else:
                self.change_title("comparison")

