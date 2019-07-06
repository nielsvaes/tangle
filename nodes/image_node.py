from PyQt5.QtGui import *

import logging
logging.basicConfig(level=logging.INFO)

from nodes.base_node import BaseNode

class ImageNode(BaseNode):
    def __init__(self, scene, title="unnamed_node", x=0, y=0):
        super(ImageNode, self).__init__(scene, title, x, y)

        self.__pixmap = QPixmap()

    def get_pixmap(self):
        return self.__pixmap

    def set_pixmap(self, pixmap):
        self.__pixmap = pixmap





