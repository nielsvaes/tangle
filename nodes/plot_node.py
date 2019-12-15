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

        self.__x_axis = []
        self.__y_axis = []

        self.__pen = QPen()
        self.__pen.setColor(QColor(255, 255, 0))
        self.__pen.setWidth(0)

        self.__clear = True

        self.__show_markers = False
        self.__marker_shape = "o"
        self.__marker_size = 10
        self.__marker_brush = QBrush(QColor(255, 0, 0), Qt.SolidPattern)
        self.__marker_pen = QPen(QColor(255, 0, 0))
        self.__marker_pen.setWidth(0)

    def set_x_axis(self, values_list):
        self.__x_axis = values_list

    def get_x_axis(self):
        return self.__x_axis

    def set_y_axis(self, values_list):
        self.__y_axis = values_list

    def get_y_axis(self):
        return self.__y_axis

    def set_color(self, qcolor):
        self.__pen.setColor(qcolor)

    def get_color(self):
        return self.__pen.color()

    def set_clear_first(self, value):
        self.__clear = value

    def get_clear_first(self):
        return self.__clear

    def set_show_markers(self, value):
        self.__show_markers = value

    def get_show_markers(self):
        return self.__show_markers

    def set_marker_shape(self, shape):
        self.__marker_shape = shape

    def get_marker_shape(self):
        return self.__marker_shape

    def set_marker_color(self, qcolor):
        self.__marker_brush.setColor(qcolor)
        self.__marker_pen.setColor(qcolor)

    def get_marker_color(self):
        return [self.__marker_pen, self.__marker_pen.color()]

    def set_marker_size(self, size):
        self.__marker_size = size

    def get_marker_size(self):
        return self.__marker_size

    def refresh(self):
        main_window = self.scene.get_main_window()
        GraphViewer(main_window).plot(self.__x_axis, self.__y_axis, pen=self.__pen, clear=self.__clear, show_markers=self.__show_markers,
                                      marker_shape=self.__marker_shape, marker_size=self.__marker_size, marker_color=self.__marker_brush,
                                      marker_pen=self.__marker_pen)