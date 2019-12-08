from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import logging
logging.basicConfig(level=logging.DEBUG)
import uuid

import nv_utils.utils as utils

from .Constants import nc, Colors, IO
from .NodeTitle import NodeTitle
from .NodeSocket import NodeSocket
from .NodeTitleBackground import NodeTitleBackground

class GroupNode(QGraphicsRectItem):
    def __init__(self, scene, nodes, x=0, y=0):
        super().__init__()
        self.scene = scene
        self.nodes = nodes

        self.offset = 30

        self.horizontal_offset = self.offset / 2
        self.vertical_offset = nc.title_background_height + (self.offset / 2)

        self.__draw()

        self.scene.addItem(self)

        self.parent_nodes()

    def parent_nodes(self):
        for node in self.nodes:
            node.setParentItem(self)
            for socket in node.get_all_connected_sockets():
                for connection in socket.get_connections():
                    connection.setParentItem(self)


    def get_group_rect(self):
        rect = QRectF()
        for node in self.nodes:
            rect = rect.united(node.mapRectToScene(node.rect()))

        rect.setHeight(rect.height() + nc.title_background_height + self.offset)
        rect.setWidth(rect.width() + self.offset)
        rect.setLeft(rect.left() - self.horizontal_offset)
        rect.setTop(rect.top() - self.vertical_offset)

        return rect

    def __draw(self, ):
        self.setRect(self.get_group_rect())

        self.setFlag(QGraphicsRectItem.ItemIsSelectable)
        self.setFlag(QGraphicsRectItem.ItemIsMovable)
        self.setFlag(QGraphicsRectItem.ItemSendsGeometryChanges)

        self.setZValue(nc.group_z_depth)

        self.setAcceptHoverEvents(True)

        self.update()

    def paint(self, painter, option, widget):
        option.state = QStyle.State_NoChange

        pen = QPen()
        pen.setStyle(Qt.DotLine)
        pen.setWidth(1)
        pen.setColor(Colors.node_selected_border)
        self.setPen(pen)
        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(Colors.group_background)
        self.setBrush(brush)


        super().paint(painter, option, widget)

    # def itemChange(self, change, value):
    #     # for node in self.nodes:
    #     #     node.itemChange(change, value)
    #         # for socket in node.get_all_sockets():
    #         #     for connection in socket.get_connections():
    #         #         connection.redraw()
    #
    #     return QGraphicsRectItem.itemChange(self, change, value)