from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import logging

from .DragConnection import DragConnection
from .Constants import nc, Colors, IO
from .ExecutionSocketConnection import ExecutionSocketConnection

import nv_NodeEditor.socket_types as socket_types

class ExecutionSocket(QGraphicsEllipseItem):
    def __init__(self, io, scene, position):
        super(ExecutionSocket, self).__init__()
        self.rect = QRectF(0, 0, nc.execution_socket_size, nc.execution_socket_size)
        self.scene = scene
        self.position = position

        self.__draw()

        self.connection_start_point = None
        self.connection_end_point = None

        self.socket_type = socket_types.ExecutionSocketType()

        self.drag_connection = None

        self.io = io
        self.connection = None

    def is_connected_to(self, execution_socket):
        if self.connection is not None:
            if self.connection.input_socket == execution_socket:
                return True
        return False

    def is_connected(self):
        if self.connection is None:
            return False
        return True

    def get_node(self):
        return self.parentItem()

    def mousePressEvent(self, event):
        self.connection_start_point = event.scenePos()
        output_socket = self.scene.itemAt(self.connection_start_point, QTransform())

        self.drag_connection = DragConnection(output_socket, event.scenePos(), self.scene)

    def mouseMoveEvent(self, event):
        self.connection_end_point = event.scenePos()

        if self.drag_connection is not None:
            self.drag_connection.mouse_position = event.scenePos()
            self.drag_connection.redraw()

    def mouseReleaseEvent(self, event):
        self.connection_end_point = event.scenePos()

        if self.drag_connection is not None:
            self.drag_connection.destroy_self()
            self.drag_connection = None

        output_socket = self.scene.itemAt(self.connection_start_point, QTransform())
        input_socket = self.scene.itemAt(self.connection_end_point, QTransform())

        print(output_socket)
        print(input_socket)

        if isinstance(input_socket, ExecutionSocket):
            connection = ExecutionSocketConnection(output_socket, input_socket, self.scene)
            # output_socket.set_label_connected(True)
            # input_socket.set_label_connected(True)
            logging.info(str(connection))

        else:
            logging.warning("Released at %s, there is no socket here" % self.connection_end_point)
            logging.warning("it's a %s" % type(input_socket))

    def get_center_point(self):
        if self.io == IO.input:
            return QPointF(self.scenePos().x() + self.rect.left(), self.scenePos().y() + self.rect.bottom() / 2)
        else:
            return QPointF(self.scenePos().x() + self.rect.right(), self.scenePos().y() + self.rect.bottom() / 2)


    def __draw(self):
        self.brush = QBrush()
        self.brush.setStyle(Qt.SolidPattern)
        self.brush.setColor(Colors.white)

        self.pen = QPen()
        self.pen.setStyle(Qt.SolidLine)
        self.pen.setWidth(1)
        self.pen.setColor(Colors.black)

        self.setRect(self.rect)
        self.setBrush(self.brush)
        self.setPen(self.pen)

        self.setPos(self.position)

        self.setZValue(nc.node_z_depth)

        self.scene.addItem(self)

#