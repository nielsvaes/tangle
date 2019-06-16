import logging

from nv_NodeEditor.nodes.base_node import BaseNode
import nv_NodeEditor.socket_types as socket_types
import math

class FloatOperation(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super(FloatOperation, self).__init__(scene, x=x, y=y)

        self.change_title("operation")

        # self.add_execution_input()
        # self.add_execution_output()
        operations = ["add", "subtract", "multiply", "divide", "power", "square root"]
        self.operation = self.add_input(socket_types.EnumSocketType(self, operations), "operation")

        self.value_1 = self.add_input(socket_types.FloatSocketType(self, "value_1"), "value_1")
        self.value_1.set_initial_value(0)
        self.value_2 = self.add_input(socket_types.FloatSocketType(self, "value_2"), "value_2")
        self.value_2.set_initial_value(0)

        self.result = self.add_output(socket_types.FloatSocketType(self, "result"), "result")
        self.result.set_initial_value(0)

        self.set_auto_compute(True)

    def compute(self):
        operation = self.operation.socket_type.get_choice()
        if operation == "add":
            result = self.value_1.get_value() + self.value_2.get_value()
        elif operation == "subtract":
            result = self.value_1.get_value() - self.value_2.get_value()
        elif operation == "multiply":
            result = self.value_1.get_value() * self.value_2.get_value()
        elif operation == "divide":
            try:
                result = self.value_1.get_value() / self.value_2.get_value()
            except StandardError, err:
                logging.error("Can't divide by %s", self.value_2.get_value())
        elif operation == "power":
            result = self.value_1.get_value() ** self.value_2.get_value()
        elif operation == "square root":
            result = math.sqrt(self.value_1.get_value())

        result = round(result, 3)

        try:
            self.result.set_value(result)
            self.change_title("(%s) %s" % (operation, result))
        except StandardError, err:
            self.error(self.result, "Can't set result value!")

