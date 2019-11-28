from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import logging
logging.basicConfig(level=logging.DEBUG)
import uuid

from .SocketConnection import SocketConnection
from .DragConnection import DragConnection
from .Constants import nc, Colors, IO
from .SignalEmitter import SignalEmitter

import nv_utils.utils as utils


class NodeSocket(QGraphicsEllipseItem):
    def __init__(self, io, socket_type, label, scene, position=None):
        super(NodeSocket, self).__init__()
        self.rect = QRectF(0, 0, nc.socket_size, nc.socket_size)
        self.position = position
        self.scene = scene

        self.socket_type = socket_type

        self.io = io
        self.label = label
        self.name = self.label.toPlainText()

        self.connection_start_point = None
        self.connection_end_point = None

        self.drag_connection = None
        self.adjust_color_to_input = True
        self.color = self.socket_type.color
        self.__uuid = uuid.uuid4()
        self.connections = []

        self.got_connected = SignalEmitter()
        self.got_disconnected = SignalEmitter()

        self.__draw()

    def get_value(self):
        return self.socket_type.get_value()

    def set_value(self, value):
        self.socket_type.set_value(value)

    def set_initial_value(self, value):
        self.socket_type.set_initial_value(value)

    def get_initial_value(self):
        return self.socket_type.get_initial_value()

    def reset_to_initial_value(self):
        self.socket_type.reset_to_initial_value()

    def fetch_connected_value(self):
        if self.is_connected():
            if self.socket_type.accept_multiple:
                values_list = []
                for socket in self.get_connected_sockets():
                    values_list.append(socket.get_value())
            else:
                socket = self.get_connected_sockets()[0]
                value = socket.get_value()
                self.set_value(value)
        else:
            # self.set_value(None)
            self.reset_to_initial_value()

    def save(self):
        save_dict = {}
        save_dict["label"] = self.label.toPlainText()
        save_dict["socket_type"] = str(self.socket_type)
        save_dict["io"] = self.io
        save_dict["value"] = self.get_value()
        save_dict["initial_value"] = self.get_initial_value()

        return save_dict

    def get_uuid(self, as_string=False):
        if as_string:
            return str(self.__uuid)
        return self.__uuid

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
            self.label.font.setItalic(True)
            self.label.setDefaultTextColor(self.socket_type.color)
        else:
            if len(self.get_connected_sockets()) == 0:
                self.label.font.setBold(False)
                self.label.font.setItalic(False)
                self.label.setDefaultTextColor(Colors.text_default)
        self.label.draw()

    def get_node(self):
        return self.parentItem()

    def add_connection(self, connection):
        if type(connection) == SocketConnection:
            self.connections.append(connection)

    def remove_connection(self, connection):
        if type(connection) == SocketConnection:
            self.connections.remove(connection)

    def get_connections(self):
        return self.connections

    def override_color(self, color):
        self.color = color
        self.set_label_style_connected(self.is_connected())
        self.__draw()

    def destroy_self(self):
        all_sockets = self.get_node().get_all_sockets()

        all_sockets.remove(self)

        self.scene.removeItem(self)
        self.scene.removeItem(self.label)

    def change_socket_type(self, new_socket_type, new_color=QColor(255, 255, 255), auto_color=True):
        self.socket_type = new_socket_type
        if auto_color:
            self.override_color(self.socket_type.get_color())
        else:
            self.override_color(new_color)

    def set_uuid(self, new_uuid):
        if type(new_uuid) == str:
            new_uuid = uuid.UUID(new_uuid)
        self.__uuid = new_uuid

    def mousePressEvent(self, event):
        self.connection_start_point = event.scenePos()
        output_socket = self.scene.itemAt(self.connection_start_point, QTransform())

        if type(output_socket) == NodeSocket:
            self.drag_connection = DragConnection(output_socket, event.scenePos(), self.scene)

    def mouseMoveEvent(self, event):
        self.connection_end_point = event.scenePos()

        if self.drag_connection is not None:
            self.drag_connection.mouse_position = event.scenePos()
            self.drag_connection.redraw()

    def mouseReleaseEvent(self, event):
        if self.drag_connection is not None:
            self.connection_end_point = self.drag_connection.end_pos
            self.drag_connection.destroy_self()
            self.drag_connection = None

        output_socket = self.scene.itemAt(self.connection_start_point, QTransform())
        input_socket = self.scene.itemAt(self.connection_end_point, QTransform())

        if isinstance(input_socket, NodeSocket):
            try:
                connection = SocketConnection(output_socket, input_socket, self.scene)
            except Exception as err:
                utils.trace(err)
                return

            if connection.is_valid:
                output_socket.set_label_style_connected(True)
                input_socket.set_label_style_connected(True)
                self.get_node().compute_connected_nodes(output_socket=self)
                # self.scene.refresh_network()
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
        self.brush.setColor(self.color)

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