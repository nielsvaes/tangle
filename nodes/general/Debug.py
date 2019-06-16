from nodes.base_node import BaseNode
import socket_types as socket_types

class Debug(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super(Debug, self).__init__(scene, x=x, y=y)
        self.change_title("*DEBUG*")

        self.debug_value = self.add_input(socket_types.DebugSocketType(self), "debug value")
        self.enum_debug = self.add_input(socket_types.EnumSocketType(self), "enum value")

        self.test_value = self.add_output(socket_types.DebugSocketType(self), "output test")

    def compute(self):
        print(self.debug_value.get_value())