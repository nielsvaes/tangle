from PySide2.QtGui import *

from ..core.Constants import Colors
from .base_node import BaseNode

class ImageNode(BaseNode):
    def __init__(self, scene, title="unnamed_node", title_background_color=Colors.node_selected_border, x=0, y=0):
        super(ImageNode, self).__init__(scene, title, title_background_color, x, y)

        self.__pixmap = QPixmap()

    def get_pixmap(self):
        return self.__pixmap

    def set_pixmap(self, pixmap):
        self.__pixmap = pixmap

    def refresh(self):
        image_viewer = self.scene.get_main_window().get_image_viewer()
        try:
            image_viewer.set_pixmap(self.get_pixmap())
        except TypeError as err:
            image_viewer.set_pixmap(QPixmap())

    def save(self):
        return super().save(save_value=False)

    def load(self, node_dict, x=None, y=None):
        super().load(node_dict, x=x, y=y)


