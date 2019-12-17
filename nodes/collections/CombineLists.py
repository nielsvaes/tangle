from nodes.base_node import BaseNode
from core import socket_types as socket_types

from core.Constants import Colors

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from ez_settings.ez_settings import EasySettingsBase

import nv_utils.qt_utils as qutils
import nv_utils.utils as utils


class CombineLists(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super().__init__(scene, title_background_color=Colors.lists, x=x, y=y)
        self.change_title("combine lists")

        self.output_list = self.add_output(socket_types.ListSocketType(self), "list")

        self.input_01 = self.add_input(socket_types.ListSocketType(self), "list A")
        self.input_02 = self.add_input(socket_types.ListSocketType(self), "list B")

        self.add_label("Combine lists")
        self.btn_add_input = self.add_button("Add input", clicked_function=self.add_new_input)
        self.add_spacer()
        self.add_label("Combined items")
        self.lw_list = self.add_list_widget()

        self.inputs = [self.input_01, self.input_02]

    def add_new_input(self):
        next_letter = chr(ord(self.inputs[-1].name[-1]) + 1)
        input = self.add_input(socket_types.ListSocketType(self), f"list {next_letter}")
        self.inputs.append(input)

    def compute(self):
        try:
            if self.is_dirty():
                extended_list = []

                for input_socket in self.inputs:
                    input_socket.fetch_connected_value()
                    input_list = input_socket.get_value()
                    if type(input_list) is not list:
                        input_list = list(input_list)
                    extended_list.extend(input_list)

                self.output_list.set_value(extended_list)
                qutils.add_items_to_list_widget(self.lw_list, [str(item) for item in extended_list], duplicates_allowed=True, clear=True)

                self.set_dirty(False)
                super().compute()
        except Exception as err:
            utils.trace(err)


