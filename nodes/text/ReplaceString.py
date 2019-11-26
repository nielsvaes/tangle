from nodes.base_node import BaseNode
from core import socket_types as socket_types

from core.Constants import Colors

import re

class ReplaceString(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super().__init__(scene, title_background_color=Colors.string, x=x, y=y)

        self.change_title("replace")

        self.input_string, self.output_string = self.add_input_output(socket_types.StringSocketType(self), "string")
        _, self.txt_find = self.add_label_text("find", "", text_changed_function=self.text_changed)
        _, self.txt_replace = self.add_label_text("replace", "", text_changed_function=self.text_changed)
        self.chk_ignore_case = self.add_checkbox("ignore case", checked=True, change_checked_function=self.text_changed)
        self.lbl_replaced_text = self.add_label("")

    def text_changed(self):
        self.set_dirty(True)
        self.compute()

    def compute(self):
        if self.is_dirty():
            self.input_string.fetch_connected_value()

            find = self.txt_find.text()
            replace = self.txt_replace.text()

            new_string = self.input_string.get_value().replace(find, replace)
            if self.chk_ignore_case.isChecked():
                new_string = re.sub(find, replace, self.input_string.get_value(), flags=re.I)

            self.lbl_replaced_text.setText(new_string)

            self.output_string.set_value(new_string)
            super().compute()
            self.set_dirty(False)

