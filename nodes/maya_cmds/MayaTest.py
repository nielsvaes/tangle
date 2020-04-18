from nodes.base_node import BaseNode
from core import socket_types as socket_types

from core.Constants import Colors


class MayaTest(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super().__init__(scene, title_background_color=Colors.float, x=x, y=y)
        self.change_title("cmds test")

    def compute(self, force=False):
        if self.is_dirty():
            super().compute(force=force)
            self.change_title(str(self.output_float.get_value()))
            self.set_dirty(False)

    def load(self, node_dict, is_duplicate=False, x=None, y=None):
        super().load(node_dict, is_duplicate=is_duplicate, x=x, y=y)
        for socket_uuid, socket_dict in node_dict.get("sockets").items():
            self.txt_number.setText(str(socket_dict.get("value")))


