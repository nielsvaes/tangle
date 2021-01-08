from ..base_node import BaseNode
from ...core import socket_types as socket_types

from ...core.Constants import Colors

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import ez_qt as qt_utils
import ez_utils.general as utils


class List(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super().__init__(scene, title_background_color=Colors.lists, x=x, y=y)
        self.items = []

        self.update_title()

        self.output_list = self.add_output(socket_types.ListSocketType(self), "list")
        self.lw_list = self.add_list_widget(custom_context_menu_function=self.show_context_menu)
        _, self.txt_item = self.add_label_text("add item: ")

        self.txt_item.returnPressed.connect(self.return_pressed)

    def show_context_menu(self):
        list_menu = QMenu(self.lw_list)
        list_menu.addAction("Remove selected from list", self.remove_selected_from_list)
        list_menu.addAction("Clear", self.clear_list)

        list_menu.popup(QCursor.pos())

    def remove_selected_from_list(self):
        for item in self.lw_list.selectedItems():
            self.items.remove(utils.try_parse(item.text()))
        qt_utils.lw.remove_items(self.lw_list, selected=True)
        self.update_title()
        self.output_list.set_value(self.items)
        self.set_dirty(True)
        self.compute()

    def clear_list(self):
        self.items = []
        qt_utils.lw.add_items(self.lw_list, [str(item) for item in self.items], duplicates_allowed=True,
                              clear=True)
        self.update_title()
        self.output_list.set_value(self.items)
        self.set_dirty(True)
        self.compute()

    def return_pressed(self):
        self.items.append(utils.try_parse(self.txt_item.text()))

        qt_utils.lw.add_items(self.lw_list, [str(item) for item in self.items], duplicates_allowed=True, clear=True)
        self.output_list.set_value(self.items)

        self.set_dirty(True)
        self.txt_item.clear()
        self.update_title()
        self.compute()

    def update_title(self):
        self.change_title(f"list: {len(self.items)}")

    def compute(self, force=False):
        if self.is_dirty():
            super().compute(force=force)

    def load(self, node_dict, is_duplicate=False, x=None, y=None):
        super().load(node_dict, is_duplicate=is_duplicate, x=x, y=y)
        for socket_uuid, socket_dict in node_dict.get("sockets").items():
            if socket_dict.get("label") == self.output_list.get_name():
                self.items = socket_dict.get("value")
                qt_utils.lw.add_items(self.lw_list, [str(item) for item in self.items],
                                      duplicates_allowed=True, clear=True)
                self.update_title()
                self.output_list.set_value(self.items)


