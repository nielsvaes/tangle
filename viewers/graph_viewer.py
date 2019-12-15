from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from pyqtgraph import PlotWidget

import nv_utils.utils as utils
from nv_utils.singleton import Singleton

class GraphViewer(QDockWidget, metaclass=Singleton):
    def __init__(self, parent):
        super(GraphViewer, self).__init__(parent)

        self.plot_widget = PlotWidget()
        self.plot_widget.setRenderHint(QPainter.HighQualityAntialiasing)
        self.plot_widget.showGrid(x=True, y=True)
        self.plot_widget.setMenuEnabled(False)

        self.setWidget(self.plot_widget)

        self.setParent(parent)
        self.setWindowTitle("Graph Viewer")
        self.setFloating(True)

        self.set_background_color(QColor(42, 42, 42))

    def set_background_color(self, qcolor):
        self.plot_widget.setBackground(qcolor)

    def plot(self, x_axis, y_axis, pen, clear=False, show_markers=False,
             marker_shape="o", marker_size=20, marker_color=QBrush(QColor(255, 0, 0), Qt.SolidPattern), marker_pen=QPen(QColor(255, 0, 0))):
        if clear:
            self.plot_widget.clear()

        if show_markers:
            self.plot_widget.plot(x_axis, y_axis, pen=pen, symbol=marker_shape, symbolSize=marker_size, symbolBrush=marker_color, symbolPen=marker_pen)
        else:
            self.plot_widget.plot(x_axis, y_axis, pen=pen)

    def clear(self):
        self.plot_widget.getPlotItem().clear()

    def resizeEvent(self, event):
        super().resizeEvent(event)





