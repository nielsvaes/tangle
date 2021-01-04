from ..base_node import BaseNode
from ...core import socket_types as socket_types

from ...core.Constants import Colors

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from datetime import datetime

import nv_utils.qt_utils as qt_utils
import nv_utils.utils as utils


class ConvertList(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super().__init__(scene, title_background_color=Colors.lists, x=x, y=y)
        self.change_title("convert list")

        self.input = self.add_input(socket_types.ListSocketType(self), "list in")
        self.output_list = self.add_output(socket_types.ListSocketType(self), "list")

        self.cb_convert_to = self.add_label_combobox("convert to", ["float", "int", "string", "date"], changed_function=self.params_changed)
        self.txt_date_format = self.add_text_line("%Y-%m-%d", text_changed_function=self.params_changed)
        self.txt_date_format.setText("%Y-%m-%d")
        self.txt_date_format.setPlaceholderText("date format: %Y-%m-%d")
        self.txt_date_format.setVisible(False)

    def params_changed(self):
        self.set_dirty(True)
        self.compute()

    def compute(self, force=False):
        try:
            if self.is_dirty():
                converted_list = []

                self.input.fetch_connected_value()
                input_list = self.input.get_value()

                if self.cb_convert_to.currentText() == "date":
                    try:
                        self.txt_date_format.setVisible(not self.txt_date_format.isVisible())
                        converted_list = [datetime.strptime(item, self.txt_date_format.text()) for item in input_list]
                    except Exception as err:
                        utils.trace(err)

                if self.cb_convert_to.currentText() == "float":
                    self.txt_date_format.setVisible(False)
                    converted_list = [float(item) for item in input_list]

                if self.cb_convert_to.currentText() == "string":
                    self.txt_date_format.setVisible(False)
                    converted_list = [str(item) for item in input_list]

                self.output_list.set_value(converted_list)
                self.set_dirty(False)
                super().compute(force=force)
        except Exception as err:
            utils.trace(err)

    def save(self):
        node_dict = super().save()
        node_dict["node_specific_params"]["cb_convert_to"] = self.cb_convert_to.currentText()
        return node_dict

    def load(self, node_dict, is_duplicate=False, x=None, y=None):
        super().load(node_dict, is_duplicate=is_duplicate, x=x, y=y)
        qt_utils.cb.set_to_item(self.cb_convert_to, node_dict.get("node_specific_params").get("cb_convert_to"))



