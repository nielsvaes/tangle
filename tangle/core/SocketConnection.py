from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import logging

from .Constants import nc, Colors, IO
from ..logger import Logger

class SocketConnection(QGraphicsPathItem):
    def __init__(self, output_socket, input_socket, scene, auto_compute_on_connect=True, auto_compute_on_disconnect=True):
        super().__init__()

        self.output_socket = output_socket
        self.input_socket = input_socket
        self.scene = scene
        self.auto_compute_on_connect = auto_compute_on_connect
        self.auto_compute_on_disconnect = auto_compute_on_disconnect

        self.mouse_over = False

        self.force_connection = True

        self.order_sockets()
        self.is_valid = self.check_validity()
        if self.is_valid:
            self.update_sockets()
            self.update_socket_labels()
            self.__draw()

    def update_sockets(self):
        for socket in [self.input_socket, self.output_socket]:
            socket.add_connection(self)

        self.input_socket.set_value(self.output_socket.get_value())

        input_node = self.input_socket.get_node()
        input_node.set_dirty(True)

        if self.get_input_socket().get_node().get_auto_compute_on_connect():
            input_node.compute()

        if self.input_socket.adjust_color_to_input:
            self.input_socket.override_color(self.output_socket.color)

    def update_socket_labels(self):
        if self.is_valid:
            self.input_socket.set_label_style_connected(True)
            self.output_socket.set_label_style_connected(True)
            self.output_socket.get_node().compute_connected_nodes(output_socket=self.output_socket)

    def order_sockets(self):
        try:
            if self.output_socket.io != IO.output:
                self.output_socket, self.input_socket = self.input_socket, self.output_socket
        except:
            pass

    def check_validity(self):
        error_message = None

        if self.output_socket.socket_type.name != self.input_socket.socket_type.name:
            if self.input_socket.socket_type.name != "debug" and not self.input_socket.socket_type.name != "list":
                error_message = "Output socket type (%s) doesn't match input socket type (%s)" % \
                                (self.output_socket.socket_type.name, self.input_socket.socket_type.name)

        if self.output_socket.name == self.input_socket.name and self.output_socket.parentItem() == self.input_socket.parentItem():
            error_message = "Can't connect to the same socket %s -> %s" % (self.output_socket.name, self.input_socket.name)

        if self.input_socket == self.output_socket:
            error_message = "Output socket (%s) is the same as the input socket (%s)" % \
                                 (self.output_socket.name, self.input_socket.name)

        if self.output_socket.is_connected_to(self.input_socket):
            error_message = "%s -> %s is already connected" % (self.output_socket.name, self.input_socket.name)

        if self.output_socket.io == self.input_socket.io:
            error_message = "Trying to connect %s to %s" % (self.output_socket.io, self.input_socket.io)

        if self.input_socket.is_connected() and self.input_socket.socket_type.accept_multiple == False:
            if self.force_connection:
                for connection in self.input_socket.get_connections():
                    connection.destroy_self()
                return True
            error_message = "%s doesn't allow multiple connections" % self.input_socket.name

        if self.input_socket.get_node().is_child_of(self.output_socket.get_node()):
            error_message = "%s is an input of %s" % (self.input_socket.get_node().get_uuid(), self.output_socket.get_node().get_uuid())

        if self.input_socket.get_node() == self.output_socket.get_node():
            error_message = "Trying to connect to the same node!"

        if error_message is not None:
            Logger().error(error_message)
            return False
            # raise AttributeError(error_message)

        return True

    def redraw(self):
        cv_offset = nc.connection_cv_offset

        start_pos = self.output_socket.get_center_point()
        end_pos = self.input_socket.get_center_point()

        cv1 = QPointF(start_pos.x() + cv_offset, start_pos.y())
        cv2 = QPointF(end_pos.x() - cv_offset, end_pos.y())

        path = QPainterPath(start_pos)

        path.cubicTo(cv1, cv2, end_pos)

        self.setPath(path)

    def destroy_self(self):
        self.scene.removeItem(self)

        for socket in [self.output_socket, self.input_socket]:
            socket.remove_connection(self)
            socket.set_label_style_connected(False)
            # socket.got_disconnected.emit()

        self.input_socket.get_node().set_dirty(True)
        self.input_socket.reset_to_initial_value()

        if self.get_input_socket().get_node().get_auto_compute_on_connect():
            self.input_socket.get_node().compute()

    def get_input_socket(self):
        return self.input_socket

    def get_output_socket(self):
        return self.output_socket

    def hoverEnterEvent(self, event):
        self.mouse_over = True
        super(SocketConnection, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.mouse_over = False
        super(SocketConnection, self).hoverLeaveEvent(event)

    def paint(self, painter, option, widget):
        option.state = QStyle.State_NoChange

        if self.isSelected():
            self.set_selected_colors()
        elif self.mouse_over:
            self.set_hover_colors()
        else:
            self.set_normal_colors()

        super(SocketConnection, self).paint(painter, option, widget)

    def __draw(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True)

        self.set_normal_colors()
        self.redraw()

        self.scene.addItem(self)

    def set_normal_colors(self):
        pen = QPen()
        pen.setStyle(Qt.SolidLine)
        pen.setWidth(nc.connection_width_normal)
        pen.setColor(Colors.connection_normal)
        self.setZValue(nc.connection_z_depth_normal)
        self.setPen(pen)

    def set_hover_colors(self):
        pen = QPen()
        pen.setStyle(Qt.SolidLine)
        pen.setWidth(nc.connection_width_hover)
        # pen.setColor(Colors.connection_hover)
        pen.setColor(self.output_socket.color)
        self.setZValue(nc.connection_z_depth_hover)
        self.setPen(pen)

    def set_selected_colors(self):
        pen = QPen()
        pen.setStyle(Qt.SolidLine)
        pen.setWidth(nc.connection_width_selected)
        pen.setColor(Colors.connection_selected)
        self.setZValue(nc.connection_z_depth_hover)
        self.setPen(pen)

    def __str__(self):
        return "SocketConnection: %s.%s -> %s.%s" % \
               (self.output_socket.get_uuid(True), self.output_socket.name,
                self.input_socket.get_uuid(True), self.input_socket.name)
