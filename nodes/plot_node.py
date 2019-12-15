from ez_settings.ez_settings import EasySettingsBase

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

import pyqtgraph

from core.Constants import Colors
from nodes.base_node import BaseNode

from viewers.graph_viewer import GraphViewer

class PlotNode(BaseNode):
    def __init__(self, scene, title="unnamed_node", title_background_color=Colors.node_selected_border, x=0, y=0):
        super().__init__(scene, title, title_background_color, x, y)

        self.x_axis = []
        self.y_axis = []

        self.pen = QPen()
        self.pen.setColor(QColor(255, 255, 0))
        self.pen.setWidth(0)

    def set_x_axis(self, values_list):
        self.x_axis = values_list

    def get_x_axis(self):
        return self.x_axis

    def set_y_axis(self, values_list):
        self.y_axis = values_list

    def get_y_axis(self):
        return self.y_axis

    def set_color(self, qcolor):
        self.pen.setColor(qcolor)

    def get_color(self):
        return self.pen.color()

    def plot_graphs(self, pen=None, clear=False):
        if pen is None:
            pen = self.pen
        main_window = self.scene.get_main_window()
        GraphViewer(main_window).plot(self.x_axis, self.y_axis, pen=pen, clear=clear)