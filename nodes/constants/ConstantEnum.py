from nv_NodeEditor.nodes.base_node import BaseNode
import nv_NodeEditor.socket_types as socket_types

class ConstantEnum(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super(ConstantEnum, self).__init__(scene, x=x, y=y)
        self.change_title("enum")

        socket_type = socket_types.EnumSocketType(self)
        socket_type.add_option("movie")
        socket_type.add_option("radio")
        socket_type.add_option("play")

        self.output = self.add_output(socket_type, "choice")

    def compute(self):
        pass