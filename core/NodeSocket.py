from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import logging

from .SocketConnection import SocketConnection
from .DragConnection import DragConnection
from .Constants import nc, Colors, IO


class NodeSocket(QGraphicsEllipseItem):
    def __init__(self, io, socket_type, label, scene, position=None, color=Qt.green):
        super(NodeSocket, self).__init__()
        self.rect = QRectF(0, 0, nc.socket_size, nc.socket_size)
        self.position = position
        self.scene = scene

        self.socket_type = socket_type

        self.__draw()

        self.io = io
        self.label = label
        self.name = self.label.toPlainText()

        self.connection_start_point = None
        self.connection_end_point = None

        self.drag_connection = None

        #todo change list to function
        self.connections = []

    def get_value(self):
        return self.socket_type.get_value()

    def set_value(self, value):
        self.socket_type.set_value(value)

        # for socket in self.get_connected_sockets():
        #     socket.fetch_connected_value()

    def set_initial_value(self, value):
        self.socket_type.set_initial_value(value)

    def get_initial_value(self):
        self.socket_type.get_initial_value()

    def reset_to_initial_value(self):
        self.socket_type.reset_to_initial_value()

    def fetch_connected_value(self):
        if self.is_connected():
            if self.socket_type.accept_multiple:
                values_list = []
                for socket in self.get_connected_sockets():
                    # socket.fetch_connected_value()
                    values_list.append(socket.get_value())
            else:
                socket = self.get_connected_sockets()[0]
                value = socket.get_value()
                self.set_value(value)

    def get_center_point(self):
        if self.io == IO.input:
            return QPointF(self.scenePos().x() + self.rect.left(), self.scenePos().y() + self.rect.bottom() / 2)
        else:
            return QPointF(self.scenePos().x() + self.rect.right(), self.scenePos().y() + self.rect.bottom() / 2)

    def get_connected_sockets(self):
        connected_sockets = []

        for connection in self.connections:
            if connection.output_socket == self:
                connected_sockets.append(connection.input_socket)
            else:
                connected_sockets.append(connection.output_socket)

        return connected_sockets

    def is_connected(self):
        if len(self.get_connected_sockets()) > 0:
            return True
        return False

    def is_connected_to(self, node_socket):
        for connection in self.connections:
            for socket in [connection.output_socket, connection.input_socket]:
                if socket == node_socket:
                    return True

        return False

    def set_label_style_connected(self, value):
        if value == True:
            self.label.font.setBold(True)
            self.label.setDefaultTextColor(self.socket_type.color)
        else:
            if len(self.get_connected_sockets()) == 0:
                self.label.font.setBold(False)
                self.label.setDefaultTextColor(Colors.text_default)
        self.label.draw()

    def get_parent_node(self):
        return self.parentItem()

    def add_connection(self, connection):
        if type(connection) == SocketConnection:
            self.connections.append(connection)

    def remove_connection(self, connection):
        if type(connection) == SocketConnection:
            self.connections.remove(connection)

    def get_connections(self):
        return self.connections

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

        if isinstance(input_socket, NodeSocket):
            connection = SocketConnection(output_socket, input_socket, self.scene)
            if connection.is_valid:
                output_socket.set_label_style_connected(True)
                input_socket.set_label_style_connected(True)
                logging.info(str(connection))
            else:
                del connection

        else:
            logging.warning("Released at %s, there is no socket here" % self.connection_end_point)


    def __is_output_connected_to_input(self, node_socket):
        if not node_socket.io == self.io:
            return True
        else:
            return False

    def __is_valid_connection(self, input_socket):
        valid = True

        if input_socket == self:
            valid = False
            logging.error("Output and input socket can't be the same!")

        if self.is_connected_to(input_socket):
            valid = False
            logging.error("%s -> %s is already connected" % (self.name, input_socket.name))

        if not self.__is_output_connected_to_input(input_socket):
            valid = False
            logging.error("%s is of type %s, %s is also of type %s" % (
                self.name, self.io, input_socket.name, input_socket.type))

        return valid

    def __draw(self):
        self.brush = QBrush()
        self.brush.setStyle(Qt.SolidPattern)
        self.brush.setColor(self.socket_type.color)

        self.pen = QPen()
        self.pen.setStyle(Qt.SolidLine)
        self.pen.setWidth(1)
        self.pen.setColor(Colors.gray)

        self.setRect(self.rect)
        self.setBrush(self.brush)
        self.setPen(self.pen)

        self.setPos(self.position)

        self.setZValue(nc.node_z_depth)

        self.scene.addItem(self)