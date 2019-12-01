from nodes.base_node import BaseNode
from core import socket_types as socket_types

from core.Constants import Colors


class Boolean(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super().__init__(scene, title_background_color=Colors.blur, x=x, y=y)
        self.change_title("boolean")

        self.output_bool = self.add_output(socket_types.BooleanSocketType(self), "bool")
        self.cb_value = self.add_combobox(["True", "False"], changed_function=self.bool_changed)

    def bool_changed(self):
        if self.cb_value.currentText() == "True":
            self.output_bool.set_value(True)
        else:
            self.output_bool.set_value(False)

        self.change_title(f"{self.output_bool.get_value()}")

        self.set_dirty(True)
        self.compute()

    def compute(self):
        if self.is_dirty():
            super().compute()
            self.set_dirty(False)

    def load(self, node_dict, x=None, y=None):
        super().load(node_dict, x=x, y=y)
        for socket_uuid, socket_dict in node_dict.get("sockets").items():
            #TODO: load value
            # self.txt_number.setText(str(socket_dict.get("value")))
            pass

