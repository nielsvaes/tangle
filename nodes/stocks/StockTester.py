from PyQt5.QtGui import *

from nodes.stock_node import StockNode
from nodes.plot_node import PlotNode
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

        x_axis_values = list(range(0, 10))
        y_axis_values = []
        for _ in range(len(x_axis_values)):
            number = random.uniform(-100, 100)
            y_axis_values.append(number)

        self.set_x_axis(x_axis_values)
        self.set_y_axis(y_axis_values)

        self.set_color(QColor(255, 0, 255))
        self.set_clear_first(False)
        self.set_show_markers(True)
        self.set_marker_shape("d")
        self.set_marker_size(15)

        self.refresh()

    def compute(self):
        if self.is_dirty():
            super().compute()



