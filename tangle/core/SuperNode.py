from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import logging
logging.basicConfig(level=logging.DEBUG)
import uuid

from .Node import Node

class SuperNode(Node):
    def __init__(self, node_list, scene, title, x, y):
        super().__init__(scene, title, x=x, y=y)

        self.node_list = node_list

    def get_input_sockets(self):
        inputs = []
        for node in self.node_list:
            inputs += node.get_all_input_sockets()
        return inputs

    def get_output_sockets(self):
        outputs = []
        for node in self.node_list:
            outputs += node.get_all_output_sockets()
        return outputs

    def reparent_sockets(self):
        for node in self.get_input_sockets():
            pass