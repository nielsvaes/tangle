from PyQt5.QtWidgets import *
import datetime
from functools import partial

from nodes.base_node import BaseNode
from core import socket_types as socket_types

from core.Constants import Colors
from nodes.plot_node import PlotNode, PlotObject

import nv_utils.utils as utils


class MakePlotObject(PlotNode):
    def __init__(self, scene, x=0, y=0):
        super().__init__(scene, title_background_color=Colors.vector2, x=x, y=y)
        self.change_title("plotobject")

        # self.input_graph_title = self.add_input(socket_types.StringSocketType(self), "title")

        self.input_x_values = self.add_input(socket_types.ListSocketType(self), "x vals")
        self.input_y_values = self.add_input(socket_types.ListSocketType(self), "y vals")

        # self.input_x_title = self.add_input(socket_types.StringSocketType(self), "x title")
        # self.input_y_title = self.add_input(socket_types.StringSocketType(self), "y title")

        self.output_plot_object = self.add_output(socket_types.PlotSocketType(self), "graph")

        self.po = PlotObject()
        self.output_plot_object.set_value(self.po)
        self.add_plot_object(self.po)

        self.btn_graph_color = self.add_button("Graph color", clicked_function=self.set_graph_color)
        self.btn_marker_color = self.add_button("Marker color", clicked_function=self.set_marker_color)
        self.chk_show_markers = self.add_checkbox("Show markers", change_checked_function=self.compute)
        self.cb_marker_shape = self.add_label_combobox("Marker shape", ["o", "+", "d"], changed_function=self.compute)
        self.txt_marker_size = self.add_label_float("Marker size", number=10.0, number_changed_function=self.compute)[1]
        self.cb_x_axis = self.add_label_combobox("X axis data", ["float", "date"], changed_function=self.compute)

    def set_graph_color(self):
        color_dialog = QColorDialog(self.po.get_color())
        color = color_dialog.getColor()

        self.po.set_color(color)
        self.refresh()

    def set_marker_color(self):
        color_dialog = QColorDialog(self.po.get_marker_color())
        color = color_dialog.getColor()

        self.po.set_marker_color(color)
        self.refresh()

    def compute(self, force=False):
        try:
            if self.input_x_values.is_connected() and self.input_y_values.is_connected():
                # self.input_graph_title.fetch_connected_value()
                # self.po.set_title(self.input_graph_title.get_value())
                # self.input_x_title.fetch_connected_value()
                # self.input_y_title.fetch_connected_value()
                # self.po.set_x_axis_title(self.input_x_title.get_value())
                # self.po.set_y_axis_title(self.input_y_title.get_value())

                self.input_x_values.fetch_connected_value()
                self.input_y_values.fetch_connected_value()

                if self.cb_x_axis.currentText() == "date":
                    dates = [datetime.datetime.strptime(value, '%Y-%m-%d').timestamp() for value in
                             self.input_x_values.get_value()]
                    self.set_type("date")
                    self.po.set_x_axis_values(dates)
                if self.cb_x_axis.currentText() == "float":
                    self.set_type("float")
                    self.po.set_x_axis_values(self.input_x_values.get_value())


                self.po.set_y_axis_values(self.input_y_values.get_value())

                self.po.set_show_markers(self.chk_show_markers.isChecked())
                self.po.set_marker_shape(self.cb_marker_shape.currentText())
                self.po.set_marker_size(float(self.txt_marker_size.text()))

                self.output_plot_object.set_value(self.po)

                super().compute(force=force)
                self.refresh()

                self.set_dirty(False)
        except Exception as err:
            utils.trace(err)


