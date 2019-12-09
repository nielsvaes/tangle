from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import logging
logging.basicConfig(level=logging.DEBUG)

import nv_utils.utils as utils

from .Constants import nc, Colors, IO

class GroupNode(QGraphicsRectItem):
    def __init__(self, scene, nodes, x=0, y=0):
        super().__init__()
        self.mouse_over = False

        self.scene = scene
        self.nodes = nodes

        self.offset = 30

        self.horizontal_offset = self.offset / 2
        self.vertical_offset = nc.title_background_height + (self.offset / 2)

        self.draw()

        self.scene.addItem(self)
        self.setZValue(nc.group_z_depth)

        self.parent_nodes()

    def parent_nodes(self):
        for node in self.nodes:
            node.setParentItem(self)

    def get_group_rect(self):
        rect = QRectF()
        for node in self.nodes:
            rect = rect.united(node.mapRectToScene(node.rect()))

        rect.setHeight(rect.height() + nc.title_background_height + self.offset)
        rect.setWidth(rect.width() + self.offset)
        rect.setLeft(rect.left() - self.horizontal_offset)
        rect.setTop(rect.top() - self.vertical_offset)

        return [rect.x(), rect.y(), rect.width(), rect.height()]

    def draw(self, ):
        x, y, width, height = self.get_group_rect()
        self.setRect(x, y, width, height)

        self.setFlag(QGraphicsRectItem.ItemIsSelectable)
        self.setFlag(QGraphicsRectItem.ItemIsMovable)
        self.setFlag(QGraphicsRectItem.ItemSendsGeometryChanges)

        self.setAcceptHoverEvents(True)

        self.update()

    def __set_normal_colors(self):
        pen = QPen()
        pen.setStyle(Qt.DotLine)
        pen.setWidth(1)
        pen.setColor(Colors.node_normal_border)
        self.setPen(pen)
        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(Colors.group_background)
        self.setBrush(brush)

    def __set_hover_colors(self):
        pen = QPen()
        pen.setStyle(Qt.DotLine)
        pen.setWidth(1)
        pen.setColor(Colors.node_hover_border)
        self.setPen(pen)
        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(Colors.group_background)
        self.setBrush(brush)

    def __set_selected_colors(self):
        pen = QPen()
        pen.setStyle(Qt.DotLine)
        pen.setWidth(nc.node_item_border_width_selected)
        pen.setColor(Colors.node_selected_border)
        self.setPen(pen)
        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(Colors.group_background)
        self.setBrush(brush)


    def itemChange(self, *args, **kwargs):
        try:
            for node in self.nodes:
                node.itemChange(*args, **kwargs)
        except Exception as err:
            utils.trace(err)
        finally:
            return QGraphicsRectItem.itemChange(self, *args, **kwargs)

    def hoverEnterEvent(self, event):
        self.mouse_over = True
        self.update()

        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.mouse_over = False
        self.update()

        super().hoverLeaveEvent(event)

    def paint(self, painter, option, widget):
        option.state = QStyle.State_NoChange

        if self.isSelected():
            self.__set_selected_colors()
        elif self.mouse_over:
            self.__set_hover_colors()
        else:
            self.__set_normal_colors()

        super().paint(painter, option, widget)
