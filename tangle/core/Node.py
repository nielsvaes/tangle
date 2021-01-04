from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import logging
logging.basicConfig(level=logging.DEBUG)
import uuid

import nv_utils.utils as utils

from .Constants import nc, Colors, IO
from .NodeTitle import NodeTitle
from .NodeSocket import NodeSocket
from .SocketConnection import SocketConnection
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
        self.socket_offset_from_top = nc.socket_size * 2.5

        self.x = x
        self.y = y

        self.title_background_color = title_background_color
        self.title = self.__add_title(title)

        self.icon_circle = self.add_icon_circle()
        self.icon_circle_pixmap = QGraphicsPixmapItem()

        self.draw()

        self.__uuid = uuid.uuid4()

        self.__input_sockets = []
        self.__output_sockets = []
        self.__num_input_output_sockets = 0

        self.scene.addItem(self)
        self.scene.addItem(self.title)

    def add_output(self, socket_type, output_name):
        if self.get_socket(output_name, IO.output) is not None:
            logging.error("Output '%s' is already exists on '%s'" % (output_name, self.name))
            return

        label = NodeTitle(output_name, font_size=self.socket_label_size)

        # socket_y_position = self.boundingRect().top() + (nc.socket_size + 5) - (self.__num_input_output_sockets * nc.socket_size + 5)
        socket_y_position = self.boundingRect().top() + self.socket_offset_from_top + (nc.socket_size + nc.socket_spacing) * len(self.get_all_output_sockets())

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

        # socket_y_position = self.boundingRect().top() + (nc.socket_size + nc.socket_spacing) - (self.__num_input_output_sockets * nc.socket_size + nc.socket_spacing)
        socket_y_position = self.boundingRect().top() + self.socket_offset_from_top + (nc.socket_size + nc.socket_spacing) * len(self.get_all_input_sockets())

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

        y_pos_multiplier = len(utils.get_longest_list([self.get_all_input_sockets(), self.get_all_output_sockets()]))

        output_socket_y_position = self.boundingRect().top() + self.socket_offset_from_top + (nc.socket_size + nc.socket_spacing) * y_pos_multiplier
        input_socket_y_position = self.boundingRect().top() + self.socket_offset_from_top + (nc.socket_size + nc.socket_spacing) * y_pos_multiplier

        input_socket_position = QPointF(self.boundingRect().left() - nc.socket_size / 2, input_socket_y_position)
        input_socket = NodeSocket(IO.input, socket_type, label, self.scene, position=input_socket_position)
        input_socket.socket_type = socket_type

        output_socket_position = QPointF(self.boundingRect().right() - nc.socket_size / 2, output_socket_y_position)
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

    def set_uuid(self, new_uuid):
        if type(new_uuid) == str:
            new_uuid = uuid.UUID(new_uuid)
        self.lbl_uuid.setText(str(new_uuid))
        self.__uuid = new_uuid

    def get_socket_by_uuid(self, search_uuid):
        if type(search_uuid) == str:
            search_uuid = uuid.UUID(search_uuid)
        for socket in self.get_all_sockets():
            if socket.get_uuid() == search_uuid:
                return socket
        return None

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

    def get_connected_output_nodes_recursive(self, start_node=None):
        connected_output_nodes = []

        if start_node is None:
            start_node = self

        for output_node in start_node.get_connected_output_nodes():
            connected_output_nodes.append(output_node)

            connected_output_nodes += self.get_connected_output_nodes_recursive(start_node=output_node)

        return connected_output_nodes

    def get_connected_input_nodes_recursive(self, start_node=None):
        connected_input_nodes = []

        if start_node is None:
            start_node = self

        for input_node in start_node.get_connected_input_nodes():
            connected_input_nodes.append(input_node)

            connected_input_nodes += self.get_connected_input_nodes_recursive(start_node=input_node)

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

    def connect_complete_node(self, other_node):
        output_sockets = self.get_all_output_sockets()
        # if we only have one output, just connect it to everything it can on the other node
        if len(output_sockets) < 2:
            for output_socket in output_sockets:
                for input_socket in other_node.get_all_input_sockets():
                    if not input_socket.is_connected():
                        connection = SocketConnection(output_socket, input_socket, self.scene)
        # if we have more than 1 output socket, only connect it once and then see if the other output
        # sockets can connect to the next input socket on the other node
        else:
            for output_socket in output_sockets:
                has_been_connected = False
                for input_socket in other_node.get_all_input_sockets():
                    if not input_socket.is_connected() and not has_been_connected:
                        connection = SocketConnection(output_socket, input_socket, self.scene)
                        has_been_connected = True


    def add_icon_circle(self):
        icon_circle = QGraphicsEllipseItem()
        icon_circle.setRect(0, 0, nc.icon_circle_size, nc.icon_circle_size)

        x_pos = (self.boundingRect().width() / 2 - nc.icon_circle_size) + self.boundingRect().left()
        y_pos = (self.boundingRect().bottom() - nc.icon_circle_size)

        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(Colors.gray)
        icon_circle.setBrush(brush)

        # icon_circle.setPos(x_pos, y_pos)
        icon_circle.setZValue(nc.socket_z_depth)

        self.scene.addItem(icon_circle)
        icon_circle.setParentItem(self)

        return icon_circle

    def add_icon_circle_pixmap(self, pixmap):
        self.icon_circle_pixmap.setPixmap(pixmap.scaled(nc.icon_circle_pixmap_size, nc.icon_circle_pixmap_size))
        self.icon_circle_pixmap.setTransformationMode(Qt.SmoothTransformation)
        self.scene.addItem(self.icon_circle_pixmap)
        self.icon_circle_pixmap.setZValue(self.icon_circle.zValue())
        self.icon_circle_pixmap.setParentItem(self)

    def reposition_icon_circle(self):
        x_pos = (self.boundingRect().right() / 2 - (nc.icon_circle_size / 2)) + self.boundingRect().left()
        y_pos = (self.boundingRect().bottom() - (nc.icon_circle_size / 2))

        self.icon_circle.setPos(x_pos, y_pos)

    def reposition_icon_circle_pixmap(self):
        x_pos = (self.boundingRect().right() / 2 - (nc.icon_circle_size / 2)) + self.boundingRect().left() + (nc.icon_circle_pixmap_size / 10)
        y_pos = (self.boundingRect().bottom() - (nc.icon_circle_size / 2)) + (nc.icon_circle_pixmap_size / 10)

        self.icon_circle_pixmap.setPos(x_pos, y_pos)

    def reposition_title(self, title=None):
        if title is None:
            title = self.title

        title.setPos(
            (self.boundingRect().width() / 2 - title.boundingRect().width() / 2) + self.boundingRect().left(),
            self.boundingRect().top() - title.boundingRect().height() - nc.title_offset)
        self.name = title.toPlainText()

    def set_auto_label(self):
        """
        This is called to denote that a node will not evaluate automatically when connected, but
        needs the user to hit the Enter key to trigger it's compute function

        :param value:
        :return:
        """
        font = QFont()
        font.setFamily("Monospace")
        font.setPixelSize(nc.auto_text_size)

        text = QGraphicsTextItem("◘")
        text.setFont(font)
        text.setDefaultTextColor(QColor(255, 0, 0, 255))
        text.setPos(self.boundingRect().right() - text.boundingRect().width(),
                    self.boundingRect().bottom() - text.boundingRect().height())

        text.setParentItem(self)

    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        if event.modifiers() == Qt.ControlModifier and event.button() == Qt.RightButton:
            other_node = self.scene.itemAt(event.scenePos(), QTransform())
            if isinstance(other_node, Node):
                self.connect_complete_node(other_node)

        super().mouseReleaseEvent(event)


    def hoverEnterEvent(self, event):
        self.mouse_over = True
        self.update()

        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.mouse_over = False
        self.update()

        super().hoverLeaveEvent(event)

    def itemChange(self, change, value):
        try:
            for socket in self.get_all_sockets():
                for connection in socket.get_connections():
                    connection.redraw()

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

        super().paint(painter, option, widget)

    def draw(self):
        self.node_rect = QRectF(0, 0, nc.node_item_width, self.height)
        self.setRect(self.node_rect)

        self.__set_normal_colors()

        self.setFlag(QGraphicsRectItem.ItemIsSelectable)
        self.setFlag(QGraphicsRectItem.ItemIsMovable)
        self.setFlag(QGraphicsRectItem.ItemSendsGeometryChanges)

        self.setZValue(nc.node_item_z_depth)
        self.setPos(self.x, self.y)

        self.setAcceptHoverEvents(True)

        self.update()

    def __resize(self):
        total_sockets = max(len(self.get_all_input_sockets()), len(self.get_all_output_sockets()))

        new_height = self.height + self.socket_offset_from_top + (total_sockets * (nc.socket_size + nc.socket_spacing))
        position = self.pos()
        self.node_rect = QRectF(0, 0, nc.node_item_width, new_height)
        self.setRect(self.node_rect)
        self.setPos(position)
        self.reposition_title(self.title)
        self.reposition_icon_circle()
        self.reposition_icon_circle_pixmap()

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

        self.node_title_background.setPen(pen)
        self.icon_circle.setPen(pen)

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

        self.node_title_background.setPen(pen)
        self.icon_circle.setPen(pen)

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

        self.node_title_background.setPen(pen)
        self.icon_circle.setPen(pen)

    def __add_title(self, title):
        node_title = NodeTitle(title, font_size=self.title_label_size)

        node_title.setParentItem(self)
        self.name = node_title.toPlainText()

        self.reposition_title(title=node_title)

        self.node_title_background = NodeTitleBackground(self.scene, self, self.title_background_color)

        return node_title