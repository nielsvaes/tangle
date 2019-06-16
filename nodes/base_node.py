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

    def refresh(self):
        for socket in self.get_all_input_sockets():
            socket.fetch_connected_value()
            self.compute()


    def auto_compute(self):
        return self.__auto_compute

    def set_auto_compute(self, value):
        self.__auto_compute = value

    def compute(self):
        raise NotImplementedError()

    def error(self, socket, text):
        logging.error("Node: %s\nSocket: %s\n%s" % (self.name, socket.name, text))

    def warning(self, socket, text):
        logging.warning("Node: %s\nSocket: %s\n%s" % (self.name, socket.name, text))

    def info(self, socket, text):
        logging.info("Node: %s\nSocket: %s\n%s" % (self.name, socket.name, text))






