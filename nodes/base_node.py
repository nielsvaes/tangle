from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import inspect

import logging
logging.basicConfig(level=logging.INFO)

from core.NodeItem import NodeItem
from core.SignalEmitter import SignalEmitter

import nv_utils.qt_utils as qutils

class BaseNode(NodeItem):
    def __init__(self, scene, title="unnamed_node", x=0, y=0):
        super(BaseNode, self).__init__(scene, title, x, y)
        self.scene = scene
        self.__auto_compute = False
        self.__x = x
        self.__y = y

        self.dirty_signal = SignalEmitter()
        self.compute_time = None

        self.__widget = QWidget()
        self.__layout = QVBoxLayout()

        self.__is_dirty = True
        self.__auto_compute_on_connect = False

        self.__widget.setLayout(self.__layout)

        self.add_label(str(self.get_uuid()))

    def refresh(self):
        pass

    def compute(self):
        raise NotImplementedError()

    def set_dirty(self, value):
        #
        # curframe = inspect.currentframe()
        # calframe = inspect.getouterframes(curframe, 2)
        # print('caller name:', calframe[1][3])
        self.__is_dirty = value
        # if value == True:
        #     self.dirty_signal.signal.emit()

    def is_dirty(self):
        return self.__is_dirty

    def get_ui(self):
        return self.__widget

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def set_auto_compute_on_connect(self, value):
        self.__auto_compute_on_connect = value

    def auto_compute_on_connect(self):
        return self.__auto_compute_on_connect

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

    def add_checkbox(self, label, checked=True, change_checked_function=None):
        checkbox = QCheckBox(label)
        checkbox.setChecked(checked)

        if change_checked_function is not None:
            checkbox.stateChanged.connect(change_checked_function)

        self.__layout.addWidget(checkbox)

        return checkbox

    def add_slider(self, minimum, maximum, start, changed_function=None, released_function=None):
        slider = QSlider()
        slider.setMinimum(minimum)
        slider.setMaximum(maximum)
        slider.setValue(start)
        slider.setOrientation(Qt.Horizontal)
        if changed_function is not None:
            slider.sliderMoved.connect(changed_function)

        if released_function is not None:
            slider.sliderReleased.connect(released_function)

        self.__layout.addWidget(slider)

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

    def add_custom_widget(self, widget):
        self.__layout.addWidget(widget)

        return widget

    def error(self, socket, text):
        logging.error("Node: %s\nSocket: %s\n%s" % (self.name, socket.name, text))

    def warning(self, socket, text):
        logging.warning("Node: %s\nSocket: %s\n%s" % (self.name, socket.name, text))

    def info(self, socket, text):
        logging.info("Node: %s\nSocket: %s\n%s" % (self.name, socket.name, text))






