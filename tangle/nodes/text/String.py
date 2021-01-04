from ..base_node import BaseNode
from ...core import socket_types as socket_types

from ...core.Constants import Colors


class String(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super().__init__(scene, title_background_color=Colors.string, x=x, y=y)

        self.change_title("string")

        self.output_string = self.add_output(socket_types.StringSocketType(self), "string")
        self.txt_string = self.add_text_line("", text_changed_function=self.text_changed)

    def text_changed(self):
        self.output_string.set_value(self.txt_string.text())

        self.set_dirty(True)
        self.compute()

    def compute(self, force=False):
        if self.is_dirty():
            super().compute(force=force)
            self.set_dirty(False)

