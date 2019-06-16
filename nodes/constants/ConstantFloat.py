from nv_NodeEditor.nodes.base_node import BaseNode
import nv_NodeEditor.socket_types as socket_types

class ConstantFloat(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super(ConstantFloat, self).__init__(scene, x=x, y=y)
        self.change_title("float")
        self.label_name = "value"

        socket_type = socket_types.FloatSocketType(self, self.label_name)

        self.output = self.add_output(socket_type, self.label_name)
        self.output.set_initial_value(0)

    def compute(self):
        self.change_title("%s" % self.output.get_value())