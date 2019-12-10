from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from functools import partial
import uuid

import logging
logging.basicConfig(level=logging.INFO)

from core.Node import Node
from core.SignalEmitter import SignalEmitter
from core.Constants import Colors

import nv_utils.qt_utils as qutils

class BaseNode(Node):
    def __init__(self, scene, title="unnamed_node", title_background_color=Colors.node_selected_border ,x=0, y=0):
        super(BaseNode, self).__init__(scene, title, title_background_color, x, y)
        self.scene = scene
        self.__auto_compute = False
        self.__x = x
        self.__y = y

        self.__module_path = None

        self.dirty_signal = SignalEmitter()
        self.compute_time = None

        self.__widget = QWidget()
        self.__layout = QVBoxLayout()

        self.__is_dirty = True
        self.__auto_compute_on_connect = False

        self.__widget.setLayout(self.__layout)

        self.lbl_node_type = self.add_label(str(type(self)))
        self.lbl_uuid = self.add_label(str(self.get_uuid()))

    def refresh(self):
        pass

    def set_module_path(self, module_path):
        self.__module_path = module_path

    def get_module_path(self):
        return self.__module_path

    def compute(self):
        self.compute_connected_nodes()

    def set_dirty(self, is_dirty, emit=False):
        self.__is_dirty = is_dirty

    def compute_connected_nodes(self, output_socket=None):
        if output_socket is None:
            for node in self.get_connected_output_nodes():
                node.set_dirty(True)
                node.compute()
        else:
            for connected_node in [socket.get_node() for socket in output_socket.get_connected_sockets()]:
                connected_node.set_dirty(True)
                connected_node.compute()

    def is_dirty(self):
        return self.__is_dirty

    def get_ui(self):
        return self.__widget

    def get_x(self):
        return self.scenePos().x()

    def get_y(self):
        return self.scenePos().y()

    def get_main_window(self):
        return self.scene.get_main_window()

    def add_button(self, button_text, clicked_function):
        button = QPushButton(button_text)
        button.clicked.connect(clicked_function)
        self.__layout.addWidget(button)

        return button

    def add_label(self, label_text):
        label = QLabel(label_text)
        self.__layout.addWidget(label)

        return label

    def add_spacer(self):
        spacer = QSpacerItem(10, 20)
        self.__layout.addSpacerItem(spacer)

        return spacer

    def add_text_line(self, text="", text_changed_function=None):
        txt_line = QLineEdit()

        if text_changed_function is not None:
            txt_line.textChanged.connect(text_changed_function)

        self.__layout.addWidget(txt_line)

        return txt_line

    def add_label_text_button(self, label_text, button_text, clicked_function):
        layout = QHBoxLayout()
        label = QLabel(label_text)
        txt_line = QLineEdit()
        button = QPushButton(button_text)

        button.clicked.connect(clicked_function)

        layout.addWidget(label)
        layout.addWidget(txt_line)
        layout.addWidget(button)

        self.__layout.addLayout(layout)

        return[label, txt_line, button]

    def add_label_text(self, label_text, txt_text="", text_changed_function=None):
        layout = QHBoxLayout()
        label = QLabel(label_text)
        txt_line = QLineEdit(str(txt_text))

        layout.addWidget(label)
        layout.addWidget(txt_line)

        if text_changed_function is not None:
            txt_line.textChanged.connect(text_changed_function)

        self.__layout.addLayout(layout)

        return[label, txt_line]

    def add_label_float(self, label_text, number=0.000, number_changed_function=None):
        layout = QHBoxLayout()
        label = QLabel(label_text)

        # float_validator = QDoubleValidator()
        # float_validator.setDecimals(3)

        txt_float = QLineEdit(str(number))
        # txt_float.setValidator(float_validator)

        layout.addWidget(label)
        layout.addWidget(txt_float)

        if number_changed_function is not None:
            txt_float.textChanged.connect(number_changed_function)

        self.__layout.addLayout(layout)

        return[label, txt_float]

    def add_checkbox(self, label, checked=True, change_checked_function=None):
        checkbox = QCheckBox(label)
        checkbox.setChecked(checked)

        if change_checked_function is not None:
            checkbox.stateChanged.connect(change_checked_function)

        self.__layout.addWidget(checkbox)

        return checkbox

    def add_slider(self, minimum, maximum, start, changed_function=None, released_function=None):
        def set_label_text(slider, label):
            label.setText(str(slider.value()))

        layout = QHBoxLayout()
        slider = QSlider()
        slider.setMinimum(minimum)
        slider.setMaximum(maximum)
        slider.setValue(start)
        slider.setOrientation(Qt.Horizontal)

        label = QLabel(str(slider.value()))

        if changed_function is not None:
            slider.sliderMoved.connect(changed_function)

        if released_function is not None:
            slider.sliderReleased.connect(released_function)

        slider.valueChanged.connect(partial(set_label_text, slider, label))

        layout.addWidget(slider)
        layout.addWidget(label)

        self.__layout.addLayout(layout)

        return slider

    def add_combobox(self, items=[], changed_function=None):
        combobox = QComboBox()
        qutils.add_items_to_combobox(combobox, items=items)

        if changed_function is not None:
            combobox.currentIndexChanged.connect(changed_function)

        self.__layout.addWidget(combobox)

        return combobox

    def add_label_combobox(self, label_text, items=[], changed_function=None):
        layout = QHBoxLayout()
        label = QLabel(label_text)
        combobox = QComboBox()
        qutils.add_items_to_combobox(combobox, items=items)

        layout.addWidget(label)
        layout.addWidget(combobox)

        if changed_function is not None:
            combobox.currentIndexChanged.connect(changed_function)

        self.__layout.addLayout(layout)

        return combobox

    def add_spinbox(self, value=0, changed_function=None):
        spin_number = QDoubleSpinBox()
        spin_number.setKeyboardTracking(False)
        spin_number.setDecimals(3)
        spin_number.setMaximum(float("inf"))
        spin_number.setMinimum(float("-inf"))
        spin_number.setButtonSymbols(QAbstractSpinBox.NoButtons)

        spin_number.valueChanged.connect(changed_function)

        self.__layout.addWidget(spin_number)

        return spin_number

    def add_label_spinbox(self, label_text, value=0, changed_function=None):
        layout = QHBoxLayout()

        label = QLabel(label_text)

        spin_number = QDoubleSpinBox()
        spin_number.setKeyboardTracking(False)
        spin_number.setDecimals(3)
        spin_number.setMaximum(float("inf"))
        spin_number.setMinimum(float("-inf"))

        layout.addWidget(label)
        layout.addWidget(spin_number)

        spin_number.valueChanged.connect(changed_function)

        self.__layout.addLayout(layout)

        return spin_number

    def add_custom_widget(self, widget):
        self.__layout.addWidget(widget)

        return widget

    def save(self, save_value=True):
        node_dict = {}
        node_dict["sockets"] = {}
        for socket in self.get_all_sockets():
            node_dict["sockets"][socket.get_uuid(as_string=True)] = socket.save(save_value=save_value)

        for socket in self.get_connected_output_sockets():
            node_dict["sockets"][socket.get_uuid(as_string=True)]["connections"] = {}
            for index, socket_connection in enumerate(socket.get_connections()):
                connected_input_socket = socket_connection.get_input_socket()
                node_dict["sockets"][socket.get_uuid(as_string=True)]["connections"][index] = [socket.get_uuid(as_string=True), connected_input_socket.get_uuid(as_string=True)]

        node_dict["uuid"] = self.get_uuid(as_string=True)
        node_dict["x"] = self.get_x()
        node_dict["y"] = self.get_y()
        node_dict["module_path"] = self.get_module_path()
        node_dict["class_name"] = self.get_module_path().split(".")[-1]
        node_dict["module_name"] = self.get_module_path().split(".")[-2]

        return node_dict

    def duplicate(self):
        node_dict = self.save()
        scene_dict = {}
        scene_dict[node_dict.get("uuid")] = node_dict
        self.scene.open_network(scene_dict=scene_dict, with_values=True, with_connections=False, is_duplicate=True)
        return node_dict

    def load(self, node_dict, x=None, y=None):
        if x is not None:
            x_pos = x
        else:
            x_pos = node_dict.get("x")
        if y is not None:
            y_pos = y
        else:
            y_pos = node_dict.get("y")

        self.setPos(x_pos, y_pos)
        self.set_uuid(node_dict.get("uuid"))

    def error(self, socket, text):
        logging.error("Node: %s\nSocket: %s\n%s" % (self.name, socket.name, text))

    def warning(self, socket, text):
        logging.warning("Node: %s\nSocket: %s\n%s" % (self.name, socket.name, text))

    def info(self, socket, text):
        logging.info("Node: %s\nSocket: %s\n%s" % (self.name, socket.name, text))

    def __str__(self):
        return "%s - %s" % (self.__class__.__name__, self.get_uuid(as_string=True))




