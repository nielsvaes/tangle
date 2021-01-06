from ..base_node import BaseNode
from ...core import socket_types as socket_types

from ...core.Constants import Colors

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import ez_qt as qt_utils
import nv_utils.utils as utils


class CombineLists(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super().__init__(scene, title_background_color=Colors.lists, x=x, y=y)
        self.change_title("combine lists")

        self.output_list = self.add_output(socket_types.ListSocketType(self), "list")

        self.input_01 = self.add_input(socket_types.ListSocketType(self), "list A")
        self.input_02 = self.add_input(socket_types.ListSocketType(self), "list B")

        self.chk_allow_duplicates = self.add_checkbox("Duplicates allowed", change_checked_function=self.duplicates_allowed_changed)
        self.btn_add_input = self.add_button("Add input", clicked_function=self.add_new_input)
        self.add_spacer()
        self.add_label("Combined items")
        self.lw_list = self.add_list_widget()

        self.inputs = [self.input_01, self.input_02]

        self.duplicates_allowed = True

    def add_new_input(self):
        next_letter = chr(ord(self.inputs[-1].name[-1]) + 1)
        input = self.add_input(socket_types.ListSocketType(self), f"list {next_letter}")
        self.inputs.append(input)

    def duplicates_allowed_changed(self):
        self.set_dirty(True)
        self.duplicates_allowed = self.chk_allow_duplicates.isChecked()
        self.compute()

    def update_title(self, count):
        self.change_title(f"list combined : {count}")

    def compute(self, force=False):
        try:
            if self.is_dirty():
                extended_list = []

                for input_socket in self.inputs:
                    input_socket.fetch_connected_value()
                    input_list = input_socket.get_value()
                    if type(input_list) is not list:
                        input_list = [input_list]

                    if self.duplicates_allowed:
                        extended_list.extend(input_list)
                    else:
                        extended_list.extend([item for item in input_list if item not in extended_list])

                self.output_list.set_value(extended_list)
                qt_utils.lw.add_items(self.lw_list, [str(item) for item in extended_list], duplicates_allowed=self.duplicates_allowed, clear=True)

                self.update_title(len(extended_list))
                self.set_dirty(False)
                super().compute(force=force)
        except Exception as err:
            utils.trace(err)

    def save(self):
        node_dict = super().save()
        node_dict["node_specific_params"]["duplicates_allowed"] = self.chk_allow_duplicates.isChecked()

        return node_dict

    def load(self, node_dict, is_duplicate=False, x=None, y=None):
        super().load(node_dict, is_duplicate=is_duplicate, x=x, y=y)

        duplicates_allowed = node_dict.get("node_specific_params").get("duplicates_allowed", True)
        self.duplicates_allowed = duplicates_allowed
        self.chk_allow_duplicates.setChecked(duplicates_allowed)




