from PySide2.QtGui import *

from ..plot_node import PlotNode, PlotObject
from ...core import socket_types as socket_types

from ...core.Constants import Colors
import nv_utils.utils as utils

import numpy as np


class AverageGraph(PlotNode):
    def __init__(self, scene, x=0, y=0):
        super().__init__(scene, title_background_color=Colors.average_graph, x=x, y=y)
        self.change_title("avg graph")

        self.input_01 = self.add_input(socket_types.PlotSocketType(self), "in A")
        self.input_02 = self.add_input(socket_types.PlotSocketType(self), "in B")
        self.output_socket = self.add_output(socket_types.PlotSocketType(self), "avg out")

        self.add_label("Average graph")
        self.btn_add_input = self.add_button("Add input", clicked_function=self.add_new_input)

        self.inputs = [self.input_01, self.input_02]


    def add_new_input(self):
        next_letter = chr(ord(self.inputs[-1].name[-1]) + 1)
        input = self.add_input(socket_types.PlotSocketType(self), f"in {next_letter}")
        self.inputs.append(input)

    def compute(self, force=False):
        try:
            if self.is_dirty():
                y_value_lists = []
                copied_plot_objects = []

                if any(input_socket.is_connected() is False for input_socket in self.inputs):
                    self.warning(self.inputs[0], "All sockets must be connected!")
                    return

                for input_socket in self.inputs:
                    input_socket.fetch_connected_value()
                    input_plot_object = input_socket.get_value()
                    y_value_lists.append(input_plot_object.get_y_axis_values())

                    copied = utils.object_copy(input_plot_object)

                    copied_plot_objects.append(utils.object_copy(copied))

                arrays = [np.array(y_value_list) for y_value_list in y_value_lists]
                average_values = [np.mean(zipped_y_values) for zipped_y_values in zip(*arrays)]

                average_plot_object = PlotObject(self.inputs[0].get_value().get_x_axis_values(), average_values)
                average_plot_object.set_color(QColor(0, 255, 0))
                average_plot_object.set_show_markers(True)
                average_plot_object.set_clear_first(True)
                average_plot_object.set_marker_shape("+")

                self.add_plot_object(average_plot_object)

                for copied_plot_object in copied_plot_objects:
                    copied_plot_object.set_color(QColor(255, 0, 255, 120))
                    copied_plot_object.set_clear_first(False)
                    copied_plot_object.set_show_markers(False)
                    copied_plot_object.set_title("")
                    copied_plot_object.set_x_axis_title("")
                    copied_plot_object.set_y_axis_title("")

                    self.add_plot_object(copied_plot_object)

                self.output_socket.set_value(average_plot_object)

                self.set_dirty(False)
                self.refresh()
                super().compute(force=force)

        except Exception as err:
            utils.trace(err)



