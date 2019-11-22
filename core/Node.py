from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import logging
logging.basicConfig(level=logging.DEBUG)
import uuid

from .Constants import nc, Colors, IO
from .NodeTitle import NodeTitle
from .NodeSocket import NodeSocket
from .NodeTitleBackground import NodeTitleBackground


class Node(QGraphicsRectItem):
    def __init__(self, scene, title, title_background_color=Colors.node_selected_border, x=0, y=0):
        super(Node, self).__init__()
        self.scene = scene
        self.name = None

        self.mouse_over = False

        self.height = nc.node_item_height
        self.title_label_size = nc.title_label_size
        self.socket_label_size = nc.socket_size - 6
        self.socket_size = nc.socket_size
        self.socket_offset_from_top = nc.socket_size * 2.5

        self.start_x_pos = x
        self.start_y_pos = y

        self.__draw()

        self.title_background_color = title_background_color
        self.title = self.__add_title(title)

        self.__uuid = uuid.uuid4()

        self.scene.addItem(self)
        self.scene.addItem(self.title)

        self.__input_sockets = []
        self.__output_sockets = []
        self.__num_input_output_sockets = 0

    def add_output(self, socket_type, output_name):
        if self.get_socket(output_name, IO.output) is not None:
            logging.error("Output '%s' is already exists on '%s'" % (output_name, self.name))
            return

        label = NodeTitle(output_name, font_size=self.socket_label_size)

        socket_y_position = self.boundingRect().top() + ((nc.socket_size + 5) * len(self.get_all_sockets()) + self.socket_offset_from_top) - (self.__num_input_output_sockets * nc.socket_size + 5)

        socket_position = QPointF(self.boundingRect().right() - nc.socket_size / 2, socket_y_position)
        socket = NodeSocket(IO.output, socket_type, label, self.scene, position=socket_position)
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

    def add_input(self, socket_type, input_name):
        if self.get_socket(input_name, IO.input) is not None:
            logging.error("Input '%s' is already exists on '%s'" % (input_name, self.name))
            return

        label = NodeTitle(input_name, font_size=self.socket_label_size)

        socket_y_position = self.boundingRect().top() + ((nc.socket_size + nc.socket_spacing) * len(self.get_all_sockets()) + self.socket_offset_from_top) - (self.__num_input_output_sockets * nc.socket_size + nc.socket_spacing)

        socket_position = QPointF(self.boundingRect().left() - nc.socket_size / 2, socket_y_position)
        socket = NodeSocket(IO.input, socket_type, label, self.scene, position=socket_position)
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

    def add_input_output(self, socket_type, input_output_name):
        if self.get_socket(input_output_name, IO.both) is not None:
            logging.error("Input or output '%s' is already exists on '%s'" % (input_output_name, self.name))
            return

        label = NodeTitle(input_output_name, font_size=self.socket_label_size)

        socket_y_position = self.boundingRect().top() + ((nc.socket_size + nc.socket_spacing) * len(self.get_all_sockets()) + self.socket_offset_from_top) - (self.__num_input_output_sockets * (nc.socket_size + nc.socket_spacing))

        input_socket_position = QPointF(self.boundingRect().left() - nc.socket_size / 2, socket_y_position)
        input_socket = NodeSocket(IO.input, socket_type, label, self.scene, position=input_socket_position)
        input_socket.socket_type = socket_type

        output_socket_position = QPointF(self.boundingRect().right() - nc.socket_size / 2, socket_y_position)
        output_socket = NodeSocket(IO.output, socket_type, label, self.scene, position=output_socket_position)
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

    def get_uuid(self, as_string=False):
        if as_string:
            return str(self.__uuid)
        return self.__uuid

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
                node = connection.output_socket.get_node()
                if node not in connected_input_nodes:
                    connected_input_nodes.append(node)

        return connected_input_nodes

    def get_connected_output_nodes(self):
        connected_output_nodes = []
        for socket in self.get_connected_output_sockets():
            for connection in socket.get_connections():
                node = connection.input_socket.get_node()
                if node not in connected_output_nodes:
                    connected_output_nodes.append(node)

        return connected_output_nodes

    def get_connected_output_nodes_recursive(self, node=None):
        connected_output_nodes = []

        if node is None:
            node = self

        for output_node in node.get_connected_output_nodes():
            connected_output_nodes.append(output_node)

            connected_output_nodes += self.get_connected_output_nodes_recursive(node=output_node)

        return connected_output_nodes

    def get_connected_input_nodes_recursive(self, node=None):
        connected_input_nodes = []

        if node is None:
            node = self

        for input_node in node.get_connected_input_nodes():
            connected_input_nodes.append(input_node)

            connected_input_nodes += self.get_connected_input_nodes_recursive(node=input_node)

        return connected_input_nodes

    def is_child_of(self, parent_node, recursive=True):
        if recursive:
            if self in parent_node.get_connected_input_nodes_recursive():
                return True
            return False
        else:
            if self in parent_node.get_connected_input_nodes():
                return True
            return False

    def is_parent_of(self, child_node, recursive=True):
        if recursive:
            if self in child_node.get_connected_output_nodes_recursive():
                return True
            return False
        else:
            if self in child_node.get_connected_output_nodes():
                return True
            return False

    def get_input_nodes_of_type(self, node_type):
        for node in self.get_connected_input_nodes():
            if type(node) == node_type:
                return node
        return None

    def get_output_nodes_of_type(self, node_type):
        for node in self.get_connected_output_nodes():
            if type(node) == node_type:
                return node
        return None

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

    def save(self):
        save_dict = {}
        save_dict["sockets"] = {}
        for socket in self.get_all_sockets():
            save_dict["sockets"][socket.get_uuid(as_string=True)] = socket.save()

        save_dict["uuid"] = self.get_uuid(as_string=True)
        save_dict["x"] = self.get_x()
        save_dict["y"] = self.get_y()
        save_dict["title"] = self.title.toPlainText()
        save_dict["node_type"] = str(type(self))

        return save_dict

    def hoverEnterEvent(self, event):
        self.mouse_over = True
        self.update()

        super(Node, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.mouse_over = False
        self.update()

        super(Node, self).hoverLeaveEvent(event)

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

        super(Node, self).paint(painter, option, widget)

    def __draw(self, ):
        self.node_rect = QRectF(0, 0, nc.node_item_width, self.height)
        self.setRect(self.node_rect)

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
        new_height = (nc.socket_size * 1.5 * total_sockets) + self.height + (nc.socket_size * 1.1)  - (self.__num_input_output_sockets * (nc.socket_size + nc.socket_spacing))
        position = self.pos()
        self.node_rect = QRectF(0, 0, nc.node_item_width, new_height)
        self.setRect(self.node_rect)
        self.setPos(position)
        self.reposition_title(self.title)

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
        pen.setWidth(nc.node_item_border_width_selected)
        pen.setColor(Colors.node_selected_border)
        self.setPen(pen)
        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(Colors.node_selected_background)
        self.setBrush(brush)

    def __add_title(self, title):
        node_title = NodeTitle(title, font_size=self.title_label_size)

        node_title.setParentItem(self)
        self.name = node_title.toPlainText()

        self.reposition_title(title=node_title)

        background = NodeTitleBackground(self.scene, self, self.title_background_color)

        return node_title