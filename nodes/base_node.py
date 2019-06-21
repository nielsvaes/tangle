from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import logging

from core.NodeItem import NodeItem

class BaseNode(NodeItem):
    def __init__(self, scene, title="unnamed_node", x=0, y=0):
        super(BaseNode, self).__init__(scene, title, x, y)
        self.scene = scene
        self.__auto_compute = False
        self.x = x
        self.y = y

        self.__widget = QWidget()
        self.__layout = QVBoxLayout()

        self.__pixmap = QPixmap()
        self.__is_dirty = False

        self.__widget.setLayout(self.__layout)

        self.add_label(str(self.uuid))



    def refresh(self):
        pass
        # for socket in self.get_all_input_sockets():
        #     socket.fetch_connected_value()
        #     self.compute()

    # def auto_compute(self):
    #     return self.__auto_compute
    #
    # def set_auto_compute(self, value):
    #     self.__auto_compute = value

    def compute(self):
        raise NotImplementedError()

    def set_dirty(self, value):
        self.__is_dirty = value

    def is_dirty(self):
        return self.__is_dirty

    def get_ui(self):
        return self.__widget

    def get_pixmap(self):
        return self.__pixmap

    def set_pixmap(self, pixmap):
        self.__pixmap = pixmap

    def add_button(self, button_text, clicked_function):
        button = QPushButton(button_text)
        button.clicked.connect(clicked_function)
        self.__layout.addWidget(button)

    def add_label(self, label_text):
        label = QLabel(label_text)
        self.__layout.addWidget(label)

    def add_spacer(self):
        spacer = QSpacerItem(10, 20)
        self.__layout.addSpacerItem(spacer)

    def add_slider(self, changed_function):
        pass

    def error(self, socket, text):
        logging.error("Node: %s\nSocket: %s\n%s" % (self.name, socket.name, text))

    def warning(self, socket, text):
        logging.warning("Node: %s\nSocket: %s\n%s" % (self.name, socket.name, text))

    def info(self, socket, text):
        logging.info("Node: %s\nSocket: %s\n%s" % (self.name, socket.name, text))






