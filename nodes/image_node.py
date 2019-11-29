from PyQt5.QtGui import *

from core.Constants import Colors
from nodes.base_node import BaseNode
from viewers.image_viewer import ImageViewer

class ImageNode(BaseNode):
    def __init__(self, scene, title="unnamed_node", title_background_color=Colors.node_selected_border, x=0, y=0):
        super(ImageNode, self).__init__(scene, title, title_background_color, x, y)

        self.__pixmap = QPixmap()

    def get_pixmap(self):
        return self.__pixmap

    def set_pixmap(self, pixmap):
        self.__pixmap = pixmap

    def refresh(self):
        main_window = self.scene.get_main_window()
        try:
            ImageViewer(main_window).set_pixmap(self.get_pixmap())
        except TypeError as err:
            ImageViewer(main_window).set_pixmap(QPixmap())

    def save(self):
        node_dict = {}

        node_dict["uuid"] = self.get_uuid(as_string=True)
        node_dict["x"] = self.get_x()
        node_dict["y"] = self.get_y()
        node_dict["module_path"] = self.get_module_path()
        node_dict["class_name"] = self.get_module_path().split(".")[-1]
        node_dict["module_name"] = self.get_module_path().split(".")[-2]

        return node_dict

    def load(self, node_dict, x=None, y=None):
        super().load(node_dict, x=x, y=y)


