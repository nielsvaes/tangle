from ez_settings.ez_settings import EasySettingsBase

from PyQt5.QtGui import *
from PyQt5.QtCore import *

from core.Constants import Colors
from nodes.base_node import BaseNode

from viewers.graph_viewer import GraphViewer

class PlotNode(BaseNode):
    def __init__(self, scene, title="unnamed_node", title_background_color=Colors.node_selected_border, x=0, y=0):
        super().__init__(scene, title, title_background_color, x, y)

        self.__plot_objects = []

    def add_plot_object(self, plot_object):
        self.__plot_objects.append(plot_object)

    def remove_plot_object(self, plot_object):
        self.__plot_objects.remove(plot_object)

    def get_plot_objects(self):
        return self.__plot_objects

    def refresh(self):
        main_window = self.scene.get_main_window()
        for plot_object in self.get_plot_objects():
            GraphViewer(main_window).plot(plot_object)


class PlotObject(QObject):
    def __init__(self, x_axis_values=[], y_axis_values=[]):
        super().__init__()

        self.__title = "unnamed graph"

        self.__x_axis_values = x_axis_values
        self.__y_axis_values = y_axis_values

        self.__x_axis_title = ""
        self.__y_axis_title = ""

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

    # def copy_self(self):
    #     po = PlotObject()
    #     po.set_x_axis_values(self.get_x_axis_values())
    #     po.set_y_axis_values(self.get_y_axis_values())
    #     po.set_x_axis_title(self.get_x_axis_title())
    #     po.set_y_axis_title(self.get_y_axis_title())

    def set_x_axis_values(self, values_list):
        self.__x_axis_values = values_list

    def get_x_axis_values(self):
        return self.__x_axis_values

    def set_y_axis_values(self, values_list):
        self.__y_axis_values = values_list

    def get_y_axis_values(self):
        return self.__y_axis_values

    def set_x_axis_title(self, title):
        self.__x_axis_title = title

    def get_x_axis_title(self):
        return self.__x_axis_title

    def set_y_axis_title(self, title):
        self.__y_axis_title = title

    def get_y_axis_title(self):
        return self.__y_axis_title

    def set_color(self, qcolor):
        self.__pen.setColor(qcolor)
        self.__pen.setWidth(0)

    def get_color(self):
        return self.__pen.color()

    def set_title(self, title):
        self.__title = title

    def get_title(self):
        return self.__title

    def set_pen(self, qpen):
        self.__pen = qpen

    def get_pen(self):
        return self.__pen

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
        return self.__marker_pen.color()

    def get_marker_pen(self):
        return self.__marker_pen

    def set_marker_size(self, size):
        self.__marker_size = size

    def get_marker_size(self):
        return self.__marker_size