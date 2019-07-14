from PyQt5.QtGui import *

from core.Constants import Colors
from nodes.base_node import BaseNode

class ImageNode(BaseNode):
    def __init__(self, scene, title="unnamed_node", title_background_color=Colors.node_selected_border, x=0, y=0):
        super(ImageNode, self).__init__(scene, title, title_background_color, x, y)

        self.__pixmap = QPixmap()

    def get_pixmap(self):
        return self.__pixmap

    def set_pixmap(self, pixmap):
        self.__pixmap = pixmap





