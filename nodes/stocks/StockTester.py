from PyQt5.QtGui import *

from nodes.stock_node import StockNode
from nodes.plot_node import PlotNode, PlotObject
from core import socket_types as socket_types

from core.Constants import Colors

from ez_settings.ez_settings import EasySettingsBase

from alpha_vantage.timeseries import TimeSeries

import random

class StockTester(PlotNode):
    def __init__(self, scene, x=0, y=0):
        super().__init__(scene, title_background_color=Colors.equalize, x=x, y=y)
        self.change_title("stocktester")

        # ts = TimeSeries(key=self.key, output_format='pandas')
        # data, meta_data = ts.get_intraday(symbol='MSFT', interval='1min', outputsize='full')
        #
        # print(data)
        # print(type(data))
        # print(meta_data)
        # print(type(meta_data))
        #
        #
        # data['4. close'].plot()
        # plt.title('Intraday Times Series for the MSFT stock (1 min)')
        # plt.show()
        #
        # print(data)
        # print(meta_data)

        x_axis_values = list(range(0, 5))
        y_axis_values = []
        for _ in range(len(x_axis_values)):
            number = random.uniform(0, 100)
            y_axis_values.append(number)

        po = PlotObject()

        po.set_x_axis_values(x_axis_values)
        po.set_y_axis_values(y_axis_values)

        po.set_color(QColor(255, 0, 255))
        po.set_show_markers(True)
        po.set_marker_shape("o")
        po.set_marker_color(QColor(255, 0, 255, 127))
        po.set_marker_size(15)

        po.set_title(f"test data, {len(x_axis_values)} sample points")
        po.set_x_axis_title("Days")
        po.set_y_axis_title("Percentage gain")

        self.add_plot_object(po)

        test_output = self.add_output(socket_types.PlotSocketType(self), "graph")

        test_output.set_value(po)

    def compute(self, force=False):
        if self.is_dirty():
            super().compute(force=force)



