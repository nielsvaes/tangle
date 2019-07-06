from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import logging

from .Constants import nc, Colors, IO

class SocketConnection(QGraphicsPathItem):
    def __init__(self, output_socket, input_socket, scene):
        # super(SocketConnection, self).__init__()
        super(SocketConnection, self).__init__()

        self.scene = scene

        self.mouse_over = False

        self.force_connection = True

        self.output_socket = output_socket
        self.input_socket = input_socket

        self.order_sockets()
        self.is_valid = self.check_validity()
        if self.is_valid:
            self.update_sockets()
            self.__draw()

    def update_sockets(self):
        for socket in [self.input_socket, self.output_socket]:
            socket.add_connection(self)

        self.input_socket.set_value(self.output_socket.get_value())

        input_node = self.input_socket.get_node()
        if input_node.auto_compute_on_connect():
            input_node.compute()

    def order_sockets(self):
        try:
            if self.output_socket.io != IO.output:
                self.output_socket, self.input_socket = self.input_socket, self.output_socket
        except:
            pass

    def check_validity(self):
        error_message = None

        if self.output_socket.socket_type.name != self.input_socket.socket_type.name:
            if self.input_socket.socket_type.name != "debug" and self.input_socket.socket_type.name != "list" and not self.output_socket.socket_type.name in self.input_socket.socket_type.accepted_inputs:
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

        if error_message is not None:
            logging.error(error_message)
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
            # socket.is_connected = False
            socket.set_label_style_connected(False)

        self.input_socket.get_node().set_dirty(True)
        self.input_socket.reset_to_initial_value()

        print("done destroying this connection")

    def hoverEnterEvent(self, event):
        self.mouse_over = True
        super(SocketConnection, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.mouse_over = False
        super(SocketConnection, self).hoverLeaveEvent(event)

    def paint(self, painter, option, widget):
        option.state = QStyle.State_NoChange

        if self.isSelected():
            self.__set_selected_colors()
        elif self.mouse_over:
            self.__set_hover_colors()
        else:
            self.__set_normal_colors()

        super(SocketConnection, self).paint(painter, option, widget)

    def __draw(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True)

        self.__set_normal_colors()
        self.redraw()

        self.scene.addItem(self)

    def __set_normal_colors(self):
        pen = QPen()
        pen.setStyle(Qt.SolidLine)
        pen.setWidth(nc.connection_width_normal)
        pen.setColor(Colors.connection_normal)
        self.setZValue(nc.connection_z_depth_normal)
        self.setPen(pen)

    def __set_hover_colors(self):
        pen = QPen()
        pen.setStyle(Qt.SolidLine)
        pen.setWidth(nc.connection_width_hover)
        # pen.setColor(Colors.connection_hover)
        pen.setColor(self.output_socket.color)
        self.setZValue(nc.connection_z_depth_hover)
        self.setPen(pen)

    def __set_selected_colors(self):
        pen = QPen()
        pen.setStyle(Qt.SolidLine)
        pen.setWidth(nc.connection_width_selected)
        pen.setColor(Colors.connection_selected)
        self.setZValue(nc.connection_z_depth_hover)
        self.setPen(pen)

    def __str__(self):
        return "SocketConnection: %s.%s -> %s.%s" % \
               (self.output_socket.parentItem().name, self.output_socket.name,
                self.input_socket.parentItem().name, self.input_socket.name)
