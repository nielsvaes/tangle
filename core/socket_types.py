from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import numpy as np
from PIL import Image

from core.Constants import Colors

import nv_utils.qt_utils as qutils

class BaseSocketType(QObject):
    #is_dirty = pyqtSignal()
    def __init__(self, parent_node):
        super(BaseSocketType, self).__init__()

        self.__value = None
        self.__initial_value = None
        self.__parent_node = parent_node

        self.name = "base"
        self.accepted_inputs = []

        self.ui_widget = QWidget()

        self.accept_multiple = False
        self.color = QColor(105, 105, 105, 255)

    # def get_ui(self):
    #     raise NotImplementedError()

    def get_color(self):
        return self.color

    def get_parent_node(self):
        return self.__parent_node

    def destroy_ui(self):
        for child in self.ui_widget.findChildren(QWidget):
            child.deleteLater()

        for layout in self.ui_widget.findChildren(QLayout):
            del layout

    def get_value(self):
        return self.__value

    def set_value(self, value):
        if type(value) == np.ndarray:
            if np.all(value) == np.all(self.__value):
                return
        else:
            if self.__value == value:
                return

        self.__value = value
        # self.is_dirty.emit()
        self.get_parent_node().set_dirty(True)

    def get_initial_value(self):
        return self.__initial_value

    def set_initial_value(self, value, also_set_value=True):
        self.__initial_value = value
        if also_set_value:
            self.__value = value

    def reset_to_initial_value(self):
        self.__value = self.__initial_value

    def set_accept_multiple(self, value):
        self.accept_multiple = value

class PictureSocketType(BaseSocketType):
    def __init__(self, parent_node):
        super(PictureSocketType, self).__init__(parent_node)

        self.name = "pic"
        self.color = QColor(90, 100, 170, 255)
        self.set_initial_value(None)

    def reset_to_initial_value(self):
        super().reset_to_initial_value()
        self.get_parent_node().set_pixmap(self.get_initial_value())

class TupleSocketType(BaseSocketType):
    def __init__(self, parent_node):
        super(TupleSocketType, self).__init__(parent_node)

        self.name = "tuple"
        self.color = QColor(255, 230, 40, 255)
        self.set_initial_value(tuple())

class IntSocketType(BaseSocketType):
    def __init__(self):
        super(IntSocketType, self).__init__()

        self.name = "int"
        self.color = QColor(255, 140, 33, 255)

class BooleanSocketType(BaseSocketType):
    def __init__(self, parent_node):
        super(BooleanSocketType, self).__init__(parent_node)

        self.name = "bool"
        self.color = QColor(80, 140, 33, 255)
        self.set_initial_value(False)

class FloatSocketType(BaseSocketType):
    def __init__(self, parent_node):
        super(FloatSocketType, self).__init__(parent_node)

        self.name = "float"
        self.color = Colors.float
        self.set_initial_value(0.0)
        self.reset_to_initial_value()


class StringSocketType(BaseSocketType):
    def __init__(self, parent_node):
        super(StringSocketType, self).__init__(parent_node)

        self.name = "string"
        self.color = Colors.string
        self.set_initial_value("")
        self.reset_to_initial_value()

class ListSocketType(BaseSocketType):
    def __init__(self, parent_node):
        super(ListSocketType, self).__init__(parent_node)

        self.name = "list"
        self.color = Colors.lists
        self.set_initial_value([])
        self.reset_to_initial_value()

class Vector3SocketType(BaseSocketType):
    def __init__(self, parent_node):
        super().__init__(parent_node)

        self.name = "vector3"
        self.color = Colors.vector3
        self.set_initial_value([0.0, 0.0, 0.0])
        self.reset_to_initial_value()

class Vector2SocketType(BaseSocketType):
    def __init__(self, parent_node):
        super().__init__(parent_node)

        self.name = "vector2"
        self.color = Colors.vector2
        self.set_initial_value([0.0, 0.0])
        self.reset_to_initial_value()



class EnumSocketType(BaseSocketType):
    def __init__(self, parent_node, options=[]):
        super(EnumSocketType, self).__init__(parent_node)

        self.name = "enum"
        self.accepted_inputs = ["list"]
        self.color = QColor(255, 81, 81, 255)
        self.layout = QHBoxLayout()

        self.combobox = QComboBox()
        self.combobox.currentIndexChanged.connect(self.enter_value)

        self.__value_dictionary = {}
        self.__value_dictionary["index"] = 0
        self.__value_dictionary["options"] = options

        self.set_value(self.__value_dictionary)
        self.set_initial_value(self.__value_dictionary)


    def get_ui(self):
        self.combobox.blockSignals(True)
        self.ui_widget.setLayout(self.layout)

        self.layout.addWidget(self.combobox)
        qutils.add_items_to_combobox(self.combobox, self.get_value().get("options"), clear=True)

        self.combobox.setCurrentIndex(self.get_value().get("index"))
        self.combobox.blockSignals(False)

        return self.ui_widget

    def add_option(self, option):
        if option not in self.__value_dictionary.get("options"):
            self.__value_dictionary.get("options").append(option)

    def enter_value(self, index):
        self.__value_dictionary["index"] = index
        self.set_value(self.__value_dictionary)

        # self.is_dirty.emit()

    def get_choice(self):
        return self.get_value().get("options")[self.get_value().get("index")]

class DebugSocketType(BaseSocketType):
    def __init__(self, parent_node):
        super(DebugSocketType, self).__init__(parent_node)

        self.name = "debug"
        self.color = QColor(90, 90, 70, 255)

    # def get_ui(self):
    #     layout = QHBoxLayout()
    #     text_edit = QTextEdit()
    #
    #     self.ui_widget.setLayout(layout)
    #
    #     try:
    #         text_edit.setPlainText(self.get_value())
    #     except Exception as err:
    #         pass
    #
    #     layout.addWidget(text_edit)
    #
    #     return self.ui_widget
