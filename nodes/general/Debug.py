from nodes.base_node import BaseNode
import socket_types as socket_types

class Debug(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super(Debug, self).__init__(scene, x=x, y=y)
        self.change_title("*DEBUG*")

        self.debug_value = self.add_input(socket_types.DebugSocketType(self), "debug value")

        self.lbl_debug = self.add_label_text("Debug value: ")[1]

        self.set_auto_compute_on_connect(True)

    def compute(self):
        self.lbl_debug.setText(str(self.debug_value.get_value()))