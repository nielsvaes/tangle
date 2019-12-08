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

        self.draw()

        self.scene.addItem(self)
        self.setZValue(nc.group_z_depth)

        self.parent_nodes()
        # self.setFlag(QGraphicsItem.ItemStacksBehindParent)

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

        return [rect.x(), rect.y(), rect.width(), rect.height()]

    def draw(self, ):
        x, y, width, height = self.get_group_rect()
        self.setRect(0, 0, width, height)

        self.setFlag(QGraphicsRectItem.ItemIsSelectable)
        self.setFlag(QGraphicsRectItem.ItemIsMovable)
        self.setFlag(QGraphicsRectItem.ItemSendsGeometryChanges)

        self.setPos(x, y)

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
