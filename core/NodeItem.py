from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import logging
logging.basicConfig(level=logging.DEBUG)
import uuid

from .Constants import nc, Colors, IO
from .NodeText import NodeText
from .NodeSocket import NodeSocket
from .ExecutionSocket import ExecutionSocket

class NodeItem(QGraphicsRectItem):
    def __init__(self, scene, title, x=0, y=0):
        super(NodeItem, self).__init__()
        self.scene = scene
        self.name = None

        self.mouse_over = False

        self.height = 30
        self.title_label_size = 20
        self.socket_label_size = nc.socket_size - 2
        self.socket_size = nc.socket_size
        self.socket_offset_from_top = nc.socket_size * 2.5

        self.start_x_pos = x
        self.start_y_pos = y

        self.__draw()

        self.title = self.__add_title(title)
        self.uuid = uuid.uuid4()
        logging.debug(self.uuid)

        self.scene.addItem(self)
        self.scene.addItem(self.title)

        self.__input_sockets = []
        self.__output_sockets = []
        self.__num_input_output_sockets = 0

        self.execution_input_socket = None
        self.execution_output_socket = None


    def add_execution_output(self):
        if self.execution_output_socket is not None:
            raise IndexError("Node (%s) can only have 1 output execution socket" % self.name)

        position = QPointF(self.boundingRect().right() - nc.execution_socket_size / 2,
                           self.boundingRect().top()   - nc.execution_socket_size / 2)

        self.execution_output_socket = ExecutionSocket(IO.output, self.scene, position)

        self.execution_output_socket.setParentItem(self)

    def add_execution_input(self):
        if self.execution_input_socket is not None:
            raise IndexError("Node (%s) can only have 1 input execution socket" % self.name)

        position = QPointF(self.boundingRect().left() - nc.execution_socket_size / 2,
                           self.boundingRect().top()  - nc.execution_socket_size / 2)

        self.execution_input_socket = ExecutionSocket(IO.input, self.scene, position)

        self.execution_input_socket.setParentItem(self)

    def add_output(self, socket_type, output_name, color=Colors.socket_output):
        if self.get_socket(output_name, IO.output) is not None:
            logging.error("Output '%s' is already exists on '%s'" % (output_name, self.name))
            return

        label = NodeText(output_name, font_size=self.socket_label_size)

        socket_y_position = self.boundingRect().top() + ((nc.socket_size + 5) * len(self.get_all_sockets()) + self.socket_offset_from_top) - (self.__num_input_output_sockets * nc.socket_size + 5)

        socket_position = QPointF(self.boundingRect().right() - nc.socket_size / 2, socket_y_position)
        socket = NodeSocket(IO.output, socket_type, label, self.scene, position=socket_position, color=color)
        socket.socket_type = socket_type

        label_x = self.boundingRect().right() - label.boundingRect().width() - nc.socket_label_spacing
        label_y = socket.get_center_point().y() - (label.boundingRect().height() / 2) - (nc.socket_size / 8)
        label_position = QPointF(label_x, label_y)

        label.setPos(label_position.x(), label_position.y())

        socket.label = label

        self.scene.addItem(label)

        label.setParentItem(self)
        socket.setParentItem(self)

        self.__output_sockets.append(socket)

        self.__resize()

        return socket

    def add_input(self, socket_type, input_name, color=Colors.socket_input):
        if self.get_socket(input_name, IO.input) is not None:
            logging.error("Input '%s' is already exists on '%s'" % (input_name, self.name))
            return

        label = NodeText(input_name, font_size=self.socket_label_size)

        socket_y_position = self.boundingRect().top() + ((nc.socket_size + 5) * len(self.get_all_sockets()) + self.socket_offset_from_top) - (self.__num_input_output_sockets * nc.socket_size + 5)

        socket_position = QPointF(self.boundingRect().left() - nc.socket_size / 2, socket_y_position)
        socket = NodeSocket(IO.input, socket_type, label, self.scene, position=socket_position, color=color)
        socket.socket_type = socket_type

        label_x = self.boundingRect().left() + nc.socket_label_spacing
        label_y = socket.get_center_point().y() - (label.boundingRect().height() / 2) - (nc.socket_size / 8)
        label_position = QPointF(label_x, label_y)

        label.setPos(label_position.x(), label_position.y())

        socket.label = label

        self.scene.addItem(label)

        label.setParentItem(self)
        socket.setParentItem(self)

        self.__input_sockets.append(socket)

        self.__resize()

        return socket

    def add_input_output(self, socket_type, input_output_name, color=Colors.socket_input):
        if self.get_socket(input_output_name, IO.both) is not None:
            logging.error("Input or output '%s' is already exists on '%s'" % (input_output_name, self.name))
            return

        label = NodeText(input_output_name, font_size=self.socket_label_size)

        socket_y_position = self.boundingRect().top() + ((nc.socket_size + 5) * len(self.get_all_sockets()) + self.socket_offset_from_top) - (self.__num_input_output_sockets * (nc.socket_size + 5))

        input_socket_position = QPointF(self.boundingRect().left() - nc.socket_size / 2,socket_y_position)
        input_socket = NodeSocket(IO.input, socket_type, label, self.scene, position=input_socket_position, color=color)
        input_socket.socket_type = socket_type

        output_socket_position = QPointF(self.boundingRect().right() - nc.socket_size / 2, socket_y_position)
        output_socket = NodeSocket(IO.output, socket_type, label, self.scene, position=output_socket_position,
                                   color=color)
        output_socket.socket_type = socket_type

        label_x = self.boundingRect().width() / 2 - label.boundingRect().width() / 2
        label_y = output_socket.get_center_point().y() - (label.boundingRect().height() / 2) - (nc.socket_size / 8)
        label_position = QPointF(label_x, label_y)

        label.setPos(label_position.x(), label_position.y())

        input_socket.label = label
        output_socket.label = label

        self.scene.addItem(input_socket)
        self.scene.addItem(output_socket)

        label.setParentItem(self)
        input_socket.setParentItem(self)
        output_socket.setParentItem(self)

        self.__input_sockets.append(input_socket)
        self.__output_sockets.append(output_socket)
        self.__num_input_output_sockets += 1

        self.__resize()

        return [input_socket, output_socket]

    def change_title(self, new_title):
        self.title.setPlainText(new_title)
        self.reposition_title()

    def is_execution_connected(self):
        if self.is_executing_node():
            for execution_socket in [self.execution_output_socket, self.execution_input_socket]:
                if execution_socket.connection is not None:
                    return True
            return False
        else:
            raise AttributeError("%s is not an executing node!" % self.name)

    def is_execution_output_connected(self):
        if self.is_executing_node():
            if self.execution_output_socket.connection is not None:
                return True
            return False
        else:
            raise AttributeError("%s is not an executing node!" % self.name)

    def is_execution_input_connected(self):
        if self.execution_input_socket.connection is not None:
            return True
        return False

    def get_connected_execution_output_node(self):
        if not self.is_execution_output_connected():
            raise RuntimeError("%s doesn't have its output ExecutionSocket connected!" % self.name)

        return self.execution_output_socket.connection.input_socket.get_node()

    def get_connected_execution_input_node(self):
        if not self.is_execution_input_connected():
            raise RuntimeError("%s doesn't have its input ExecutionSocket connected!" % self.name)

        return self.execution_input_socket.connection.input_socket.get_node()

    def is_executing_node(self):
        if self.execution_output_socket is not None or self.execution_input_socket is not None:
            return True
        return False

    def get_all_sockets(self):
        return self.__output_sockets + self.__input_sockets

    def get_all_input_sockets(self):
        return self.__input_sockets
    
    def get_all_output_sockets(self):
        return self.__output_sockets

    def get_all_connected_sockets(self):
        connected_sockets = []
        for socket in self.get_all_sockets():
            if socket.is_connected():
                connected_sockets.append(socket)

        return connected_sockets

    def get_connected_input_sockets(self):
        connected_sockets = []
        for socket in self.get_all_input_sockets():
            if socket.is_connected():
                connected_sockets.append(socket)

        return connected_sockets

    def get_connected_output_sockets(self):
        connected_sockets = []
        for socket in self.get_all_output_sockets():
            if socket.is_connected():
                connected_sockets.append(socket)

        return connected_sockets

    def get_connected_input_nodes(self):
        connected_input_nodes = []
        for socket in self.get_connected_input_sockets():
            for connection in socket.get_connections():
                connected_input_nodes.append(connection.output_socket.get_parent_node())

        return connected_input_nodes

    def get_connected_output_nodes(self):
        connected_output_nodes = []
        for socket in self.get_connected_output_sockets():
            for connection in socket.get_connections():
                connected_output_nodes.append(connection.input_socket.get_parent_node())

        return connected_output_nodes

    def get_input_socket_types(self):
        input_socket_types = []
        for socket in self.get_all_input_sockets():
            input_socket_types.append(socket.socket_type)
        return input_socket_types
        
    def get_output_socket_types(self):
        output_socket_types = []
        for socket in self.get_all_output_sockets():
            output_socket_types.append(socket.socket_type)
        return output_socket_types

    def get_all_socket_types(self):
        all_socket_types = []
        for socket in self.get_all_sockets():
            all_socket_types.append(socket.socket_type)
        return all_socket_types

    def destroy_self(self):
        all_connections = []

        for socket in self.get_all_sockets():
            for connection in socket.connections:
                all_connections.append(connection)

            #socket.socket_type.destroy_ui()
            #del socket.socket_type

        for connection in all_connections:
            logging.info("Destroying %s" % connection)
            connection.destroy_self()

        for execution_socket in [self.execution_input_socket, self.execution_output_socket]:
            if execution_socket is not None:
                try:
                    execution_socket.connection.destroy_self()
                except:
                    logging.warning("Can't call destroy_self() on ExecutionSocketConnection: %s" % execution_socket.connection)

        self.scene.removeItem(self)

    def get_socket_connections(self):
        all_sockets = self.__output_sockets + self.__input_sockets
        all_connections = []

        for socket in all_sockets:
            for connection in socket.connections:
                all_connections.append(connection)

        return all_connections

    def get_socket(self, socket_name, input_output):
        if input_output == IO.output:
            for socket in self.__output_sockets:
                if socket.name == socket_name:
                    return socket
        elif input_output == IO.input:
            for socket in self.__input_sockets:
                if socket.name == socket_name:
                    return socket
        elif input_output == IO.both:
            for socket in self.get_all_sockets():
                if socket.name == socket_name:
                    return socket

        return None


    def reposition_title(self, title=None):
        if title is None:
            title = self.title

        title.setPos(
            (self.boundingRect().width() / 2 - title.boundingRect().width() / 2) + self.boundingRect().left(),
            self.boundingRect().top() - title.boundingRect().height() - nc.title_offset)
        self.name = title.toPlainText()

    def hoverEnterEvent(self, event):
        self.mouse_over = True
        self.update()

        super(NodeItem, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.mouse_over = False
        self.update()

        super(NodeItem, self).hoverLeaveEvent(event)

    def itemChange(self, change, value):
        try:
            for socket in self.__output_sockets:
                for connection in socket.connections:
                    connection.redraw()

            for socket in self.__input_sockets:
                for connection in socket.connections:
                    connection.redraw()

            if self.execution_input_socket.connection is not None:
                self.execution_input_socket.connection.redraw()

            if self.execution_output_socket.connection is not None:
                self.execution_output_socket.connection.redraw()


        except Exception  as err:
            pass
        finally:
            return QGraphicsRectItem.itemChange(self, change, value)


    def paint(self, painter, option, widget):
        option.state = QStyle.State_NoChange

        if self.isSelected():
            self.__set_selected_colors()
        elif self.mouse_over:
            self.__set_hover_colors()
        else:
            self.__set_normal_colors()

        super(NodeItem, self).paint(painter, option, widget)

    def __draw(self, ):
        self.rect = QRectF(0, 0, 150, self.height)
        self.setRect(self.rect)

        self.__set_normal_colors()

        self.setFlag(QGraphicsRectItem.ItemIsSelectable)
        self.setFlag(QGraphicsRectItem.ItemIsMovable)
        self.setFlag(QGraphicsRectItem.ItemSendsGeometryChanges)

        self.setZValue(100)
        self.setPos(self.start_x_pos, self.start_y_pos)

        self.setAcceptHoverEvents(True)

        self.update()

    def __resize(self):
        total_sockets = len(self.get_all_sockets())
        new_height = (nc.socket_size * 1.5 * total_sockets) - (
                nc.socket_size * 1.5 * self.__num_input_output_sockets) + self.height
        position = self.pos()
        self.rect = QRectF(0, 0, 150, new_height)
        self.setRect(self.rect)
        self.setPos(position)

    def __set_normal_colors(self):
        pen = QPen()
        pen.setStyle(Qt.SolidLine)
        pen.setWidth(1)
        pen.setColor(Colors.node_normal_border)
        self.setPen(pen)
        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(Colors.node_normal_background)
        self.setBrush(brush)

    def __set_hover_colors(self):
        pen = QPen()
        pen.setStyle(Qt.SolidLine)
        pen.setWidth(1)
        pen.setColor(Colors.node_hover_border)
        self.setPen(pen)
        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(Colors.node_hover_background)
        self.setBrush(brush)

    def __set_selected_colors(self):
        pen = QPen()
        pen.setStyle(Qt.SolidLine)
        pen.setWidth(nc.node_border_width_selected)
        pen.setColor(Colors.node_selected_border)
        self.setPen(pen)
        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(Colors.node_selected_background)
        self.setBrush(brush)

    def __add_title(self, title):
        node_title = NodeText(title, font_size=self.title_label_size)

        node_title.setParentItem(self)
        self.name = node_title.toPlainText()

        self.reposition_title(title=node_title)

        return node_title