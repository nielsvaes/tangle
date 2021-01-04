from ..base_node import BaseNode
from ...core import socket_types as socket_types

from ...core.Constants import Colors

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *


class ConvertTo(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super().__init__(scene, title_background_color=Colors.lists, x=x, y=y)
        self.change_title("to: ")

        self.input = self.add_input(socket_types.ListSocketType(self), "in")
        self.output_list = self.add_output(socket_types.ListSocketType(self), "out")

        self.cb_convert_to = self.add_label_combobox("convert to", ["float", "int", "string", "list", "date"], changed_function=self.params_changed)
        self.txt_date_format = self.add_text_line("%Y-%m-%d", text_changed_function=self.date_params_changed)
        self.txt_date_format.setText("%Y-%m-%d")
        self.txt_date_format.setPlaceholderText("date format: %Y-%m-%d")
        self.txt_date_format.setVisible(False)

        self.txt_list_split_char = self.add_text_line("")
        self.txt_list_split_char.setVisible(False)

    def list_params_changed(self):
        pass

    def date_params_changed(self):
        pass