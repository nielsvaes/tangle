from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import numpy as np

import nv_utils.qt_utils as qutils

class BaseSocketType(QObject):
    is_dirty = pyqtSignal()
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
        self.is_dirty.emit()

    def get_initial_value(self):
        return self.__initial_value

    def set_initial_value(self, value):
        self.__initial_value = value

    def reset_to_initial_value(self):
        self.__value = self.__initial_value

class PictureSocketType(BaseSocketType):
    def __init__(self, parent_node):
        super(PictureSocketType, self).__init__(parent_node)

        self.name = "pic"
        self.color = QColor(90, 100, 170, 255)
        self.set_initial_value(QPixmap())

class ExecutionSocketType(BaseSocketType):
    def __init__(self):
        super(ExecutionSocketType, self).__init__()

        self.name = "exec"
        self.color = QColor(255, 255, 255, 255)


class IntSocketType(BaseSocketType):
    def __init__(self):
        super(IntSocketType, self).__init__()

        self.name = "int"
        self.color = QColor(255, 140, 33, 255)


class FloatSocketType(BaseSocketType):
    def __init__(self, parent_node, label_name):
        super(FloatSocketType, self).__init__(parent_node)

        self.name = "float"
        self.color = QColor(79, 255, 102, 255)

        self.spin_number = QDoubleSpinBox()
        self.spin_number.setKeyboardTracking(False)
        self.spin_number.setDecimals(3)
        self.spin_number.setMaximum(float("inf"))
        self.spin_number.setMinimum(float("-inf"))

        self.layout = QHBoxLayout()
        self.label = QLabel(label_name)

        # self.label_name = label_name
        self.set_value(0.0)

    def get_ui(self):
        self.ui_widget.setLayout(self.layout)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.spin_number)

        self.spin_number.setValue(self.get_value())

        self.spin_number.valueChanged.connect(self.enter_value)

        return self.ui_widget

    def enter_value(self):
        self.set_value(self.spin_number.value())


class StringSocketType(BaseSocketType):
    def __init__(self):
        super(StringSocketType, self).__init__()

        self.name = "string"
        self.color = QColor(206, 234, 145, 255)

class Vector3SocketType(BaseSocketType):
    def __init__(self, parent_node):
        super(Vector3SocketType, self).__init__(parent_node)

        self.name = "vec3"
        self.color = QColor(19, 46, 104, 255)

        self.x_label = QLabel("X")
        self.y_label = QLabel("Y")
        self.z_label = QLabel("Z")

        self.x_spin = QDoubleSpinBox()
        self.y_spin = QDoubleSpinBox()
        self.z_spin = QDoubleSpinBox()

        for spinbox in [self.x_spin, self.y_spin, self.z_spin]:
            spinbox.setKeyboardTracking(False)
            spinbox.setDecimals(3)
            spinbox.setMaximum(float("inf"))
            spinbox.setMinimum(float("-inf"))

        self.layout = QHBoxLayout()

        self.set_value([0.0, 0.0, 0.0])

    def get_ui(self):
        self.ui_widget.setLayout(self.layout)

        self.layout.addWidget(self.x_label)
        self.layout.addWidget(self.x_spin)
        self.layout.addWidget(self.y_label)
        self.layout.addWidget(self.y_spin)
        self.layout.addWidget(self.z_label)
        self.layout.addWidget(self.z_spin)

        self.x_spin.setValue(self.get_value()[0])
        self.y_spin.setValue(self.get_value()[1])
        self.z_spin.setValue(self.get_value()[2])

        return self.ui_widget

    def enter_value(self):
        x = self.x_spin.value()
        y = self.y_spin.value()
        z = self.z_spin.value()

        print("Setting value to ", [x, y, z])

        self.set_value([x, y, z])

class Vector2SocketType(BaseSocketType):
    def __init__(self, parent_node):
        super(Vector2SocketType, self).__init__(parent_node)

        self.name = "vec2"
        self.color = QColor(173, 127, 198, 255)

        self.x_label = QLabel("X")
        self.y_label = QLabel("Y")

        self.x_spin = QDoubleSpinBox()
        self.y_spin = QDoubleSpinBox()

        for spinbox in [self.x_spin, self.y_spin]:
            spinbox.setKeyboardTracking(False)
            spinbox.setDecimals(3)
            spinbox.setMaximum(float("inf"))
            spinbox.setMinimum(float("-inf"))

        self.layout = QHBoxLayout()

        self.set_value([0.0, 0.0])

    def get_ui(self):
        self.ui_widget.setLayout(self.layout)

        self.layout.addWidget(self.x_label)
        self.layout.addWidget(self.x_spin)
        self.layout.addWidget(self.y_label)
        self.layout.addWidget(self.y_spin)

        self.x_spin.setValue(self.get_value()[0])
        self.y_spin.setValue(self.get_value()[1])

        return self.ui_widget

    def enter_value(self):
        x = self.x_spin.value()
        y = self.y_spin.value()

        self.set_value([x, y])

class ListSocketType(BaseSocketType):
    def __init__(self, parent_node):
        super(ListSocketType, self).__init__(parent_node)

        self.name = "list"
        self.color = QColor(255, 30, 172, 255)
        self.accept_multiple = True

        self.layout = QHBoxLayout()

        self.list_widget = QListWidget()
        self.list_widget.model().rowsInserted.connect(self.enter_value)


    def get_ui(self):
        self.ui_widget.setLayout(self.layout)
        self.layout.addWidget(self.list_widget)

        qutils.add_items_to_list_widget(self.list_widget, self.get_value(), clear=True)

        return self.ui_widget

    def enter_value(self):
        self.set_value(qutils.get_all_items_in_list_widget(self.list_widget))

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

    def get_ui(self):
        layout = QHBoxLayout()
        text_edit = QTextEdit()

        self.ui_widget.setLayout(layout)

        try:
            text_edit.setPlainText(self.get_value())
        except Exception as err:
            pass

        layout.addWidget(text_edit)

        return self.ui_widget
