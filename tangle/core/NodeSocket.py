from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import logging
logging.basicConfig(level=logging.DEBUG)
import uuid

from functools import partial

from .SocketConnection import SocketConnection
from .DragConnection import DragConnection
from .Constants import nc, Colors, IO

from .. import node_db

import ez_utils.general as utils
import ez_qt as qt_utils

class NodeSocket(QGraphicsEllipseItem):
    got_connected = Signal(str)
    got_disconnected = Signal(str)
    def __init__(self, io, socket_type, label, scene, position=None):
        super().__init__()
        self.rect = QRectF(0, 0, nc.socket_size, nc.socket_size)
        self.position = position
        self.scene = scene

        self.mouse_over = False

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

        # self.got_connected = SignalEmitter()
        # self.got_disconnected = SignalEmitter()

        self.__draw()

        self.setAcceptHoverEvents(True)

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
            self.reset_to_initial_value()

    def save(self, save_value=True):
        """
        Saves the socket so it can be serialized

        :param save_value: [bool]  if set to yes, the value of the socket will also be saved if the socket type allows it
        :return: a dictionary with the serialized data
        """
        save_dict = {}
        save_dict["label"] = self.label.toPlainText()
        save_dict["socket_type"] = str(self.socket_type)
        save_dict["io"] = self.io
        if save_value and self.socket_type.get_value_saveable():
            save_dict["value"] = self.get_value()
            save_dict["initial_value"] = self.get_initial_value()

        return save_dict

    def get_uuid(self, as_string=False):
        if as_string:
            return str(self.__uuid)
        return self.__uuid

    def get_center_point(self):
        if self.io == IO.input:
            return QPointF(self.scenePos().x(), self.scenePos().y() + nc.socket_size / 2)
        else:
            return QPointF(self.scenePos().x() + nc.socket_size, self.scenePos().y() + nc.socket_size / 2)

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

    def set_label_style_connected(self, connected):
        if connected:
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

    def get_name(self):
        return self.name

    def get_label_text(self):
        return self.name

    def is_input(self):
        if self.io == IO.input:
            return True
        return False

    def is_output(self):
        if self.io == IO.output:
            return True
        return False

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

        socket_01 = self.scene.itemAt(self.connection_start_point, QTransform())
        socket_02 = self.scene.itemAt(self.connection_end_point, QTransform())

        # we've released the mouse button over another socket
        if isinstance(socket_02, NodeSocket):
            try:
                connection = SocketConnection(socket_01, socket_02, self.scene)
            except Exception as err:
                utils.trace(err)
                return

        # we've released the mouse button where there is no socket
        else:
            if event.button() == Qt.LeftButton:
                self.scene.get_view().info_label.warning("Released at %s, there is no socket here" % self.connection_end_point)

            elif event.button() == Qt.RightButton:
                x = event.screenPos().x()
                y = event.screenPos().y()

                widget = QComboBox()
                widget.blockSignals(True)
                widget.activated.connect(partial(self.add_new_node,
                                                           widget,
                                                           self,
                                                           event.scenePos().x() - nc.node_item_width / 2,
                                                           event.scenePos().y() - nc.node_item_height / 2))
                widget.resize(180, 20)
                self.scene.spawn_widget_at(widget, x, y)

                connectable_nodes = []
                connectable_nodes.append("debug.Debug")
                if socket_01.is_input():
                    for node_dict in node_db.get_node_dicts_with_output_of_type(socket_01.socket_type.name):
                        connectable_nodes.append("%s.%s" % (node_dict.get("module"), node_dict.get("name")))
                if socket_01.is_output():
                    for node_dict in node_db.get_node_dicts_with_input_of_type(socket_01.socket_type.name):
                        connectable_nodes.append("%s.%s" % (node_dict.get("module"), node_dict.get("name")))

                qt_utils.combo_box.add_items(widget, connectable_nodes)
                widget.blockSignals(False)

    def add_new_node(self, combobox, socket, pos_x, pos_y, _):
        module, class_name = combobox.currentText().split(".")
        self.scene.destroy_spawned_widgets()

        new_node = self.scene.add_node_to_view(class_name, module, pos_x - nc.node_item_width / 2, pos_y)
        socket_01 = socket
        if socket_01.is_input():
            socket_02 = new_node.get_all_output_sockets()[0]
            connection = SocketConnection(socket_02, socket, self.scene)
        else:
            socket_02 = new_node.get_all_input_sockets()[0]
            connection = SocketConnection(socket, socket_02, self.scene)

    def hoverEnterEvent(self, event):
        self.mouse_over = True
        for connection in self.get_connections():
            connection.mouse_over = self.mouse_over
            connection.set_hover_colors()
        self.update()

        self.scene.get_main_window().set_help_text(self.socket_type.name)

        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.mouse_over = False
        for connection in self.get_connections():
            connection.mouse_over = self.mouse_over
            connection.set_normal_colors()
        self.update()

        self.scene.get_main_window().set_help_text("")

        super().hoverLeaveEvent(event)

    def paint(self, painter, option, widget):
        option.state = QStyle.State_NoChange

        if self.mouse_over:
            self.set_hover_colors()
        else:
            self.set_normal_colors()

        super().paint(painter, option, widget)

    def __is_output_connected_to_input(self, node_socket):
        if not node_socket.io == self.io:
            return True
        else:
            return False

    def __is_valid_connection(self, input_socket):
        valid = True

        if input_socket == self:
            valid = False
            self.scene.get_view().info_label.error("Output and input socket can't be the same!")

        if self.is_connected_to(input_socket):
            valid = False
            self.scene.get_view().info_label.error("%s -> %s is already connected" % (self.name, input_socket.name))

        if not self.__is_output_connected_to_input(input_socket):
            valid = False
            self.scene.get_view().info_label.error("%s is of type %s, %s is also of type %s" % (
                self.name, self.io, input_socket.name, input_socket.type))

        return valid

    def set_normal_colors(self):
        pen = QPen()
        pen.setStyle(Qt.SolidLine)
        pen.setWidth(nc.node_item_border_width_selected)
        pen.setColor(self.color)
        self.setPen(pen)

    def set_hover_colors(self):
        pen = QPen()
        pen.setStyle(Qt.SolidLine)
        pen.setWidth(nc.node_item_border_width_selected)
        pen.setColor(Colors.node_hover_border)
        self.setPen(pen)

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

        self.setZValue(nc.socket_z_depth)

        self.scene.addItem(self)