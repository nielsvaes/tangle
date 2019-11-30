from nodes.base_node import BaseNode
from core import socket_types as socket_types


class Debug(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super().__init__(scene, x=x, y=y)
        self.change_title("*DEBUG*")

        self.debug_value = self.add_input(socket_types.DebugSocketType(self), "debug")

        self.txt_debug = self.add_label_text("Debug value: ")[1]


    def compute(self):
        self.debug_value.fetch_connected_value()
        self.txt_debug.setText(str(self.debug_value.get_value()))