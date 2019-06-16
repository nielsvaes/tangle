# import logging
# logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
# import re
# from pydoc import locate
#
#
# import nv_NodeEditor.socket_types as socket_types; reload(socket_types)
#
# from PySide2.QtCore import *
# from PySide2.QtWidgets import *
# from PySide2.QtGui import *
# from PySide2.QtUiTools import *
#
# class IO():
#     input = "input"
#     output = "output"
#     both = "output"
#
#     execution_input = "execution_input"
#     execution_output = "execution_output"
#
#
# class Colors():
#     node_normal_border       = QColor(36, 66, 114, 255)
#     node_hover_border        = QColor(36, 114, 62, 255)
#     node_selected_border     = QColor(87, 255, 45, 255)
#
#     node_normal_background   = QColor(20, 20, 20, 255)
#     node_hover_background    = QColor(75, 75, 75, 255)
#     node_selected_background = QColor(75, 75, 75, 255)
#
#     connection_normal        = QColor(150, 150, 150, 255)
#     connection_hover         = QColor(214, 93, 19, 255)
#     connection_selected      = QColor(87, 255, 45, 255)
#
#     socket_output            = QColor(255, 220, 105, 255)
#     socket_input             = QColor(105, 255, 110, 255)
#
#     text_default             = QColor(200, 200, 200, 255)
#     gray                     = QColor(80, 80, 80, 255)
#     white                    = QColor(255, 255, 255, 255)
#     black                    = QColor(0, 0, 0, 255)
#
#
# class NumberConstants():
#     node_border_width_selected = 4
#
#     connection_width_normal    = 2
#     connection_width_hover     = 3
#     connection_width_selected  = 4
#
#     title_offset = 1
#
#     socket_size = 15
#     socket_label_spacing = socket_size * 1.1
#
#     execution_socket_size = 25
#
#     node_z_depth = 10
#
#     connection_z_depth_normal = 1
#     connection_z_depth_hover  = 50
#
# nc = NumberConstants
#
#
#
#
# ###############################################################
# #  ____             _        _    ____                            _   _
# # / ___|  ___   ___| | _____| |_ / ___|___  _ __  _ __   ___  ___| |_(_) ___  _ __
# # \___ \ / _ \ / __| |/ / _ \ __| |   / _ \| '_ \| '_ \ / _ \/ __| __| |/ _ \| '_ \
# #  ___) | (_) | (__|   <  __/ |_| |__| (_) | | | | | | |  __/ (__| |_| | (_) | | | |
# # |____/ \___/ \___|_|\_\___|\__|\____\___/|_| |_|_| |_|\___|\___|\__|_|\___/|_| |_|
# #
# ###############################################################
#
#
# class SocketConnection(QGraphicsPathItem):
#     def __init__(self, output_socket, input_socket, scene):
#         super(SocketConnection, self).__init__()
#
#         self.scene = scene
#
#         self.mouse_over = False
#
#         self.output_socket = output_socket
#         self.input_socket = input_socket
#         self.order_sockets()
#
#         self.check_validity()
#
#         self.update_sockets()
#
#         self.__draw()
#
#     def update_sockets(self):
#         self.input_socket.connections.append(self)
#         self.output_socket.connections.append(self)
#
#         self.input_socket.is_connected = True
#         self.output_socket.is_connected = True
#
#     def order_sockets(self):
#         if self.output_socket.io != IO.output:
#             self.output_socket, self.input_socket = self.input_socket, self.output_socket
#
#     def check_validity(self):
#         error_message = None
#
#         if self.output_socket.socket_type.name != self.input_socket.socket_type.name:
#             if self.input_socket.socket_type.name != "debug" and self.input_socket.socket_type.name != "list":
#                 error_message = "Output socket type (%s) doesn't match input socket type (%s)" % \
#                                 (self.output_socket.socket_type.name, self.input_socket.socket_type.name)
#
#         if self.output_socket.name == self.input_socket.name and self.output_socket.parentItem() == self.input_socket.parentItem():
#             error_message = "Can't connect to the same socket %s -> %s" % (self.output_socket.name, self.input_socket.name)
#
#         if self.input_socket == self.output_socket:
#             error_message = "Output socket (%s) is the same as the input socket (%s)" % \
#                                  (self.output_socket.name, self.input_socket.name)
#
#         if self.output_socket.is_connected_to(self.input_socket):
#             error_message = "%s -> %s is already connected" % (self.output_socket.name, self.input_socket.name)
#
#         if self.output_socket.io == self.input_socket.io:
#             error_message = "Trying to connection %s to %s" % (self.output_socket.io, self.input_socket.io)
#
#         if self.input_socket.is_connected and self.input_socket.socket_type.accept_multiple == False:
#             error_message = "%s doesn't allow multiple connections" % self.input_socket.name
#
#         if error_message is not None:
#             logging.error(error_message)
#             print "\n\n"
#             raise AttributeError(error_message)
#
#     def redraw(self):
#         cv_offset = 60
#
#         start_pos = self.output_socket.get_center_point()
#         end_pos = self.input_socket.get_center_point()
#
#         cv1 = QPointF(start_pos.x() + cv_offset, start_pos.y())
#         cv2 = QPointF(end_pos.x() - cv_offset, end_pos.y())
#
#         path = QPainterPath(start_pos)
#
#         path.cubicTo(cv1, cv2, end_pos)
#
#         self.setPath(path)
#
#     def destroy_self(self):
#         self.scene.removeItem(self)
#
#         for socket in [self.output_socket, self.input_socket]:
#             socket.set_label_connected(False)
#             socket.connections.remove(self)
#             socket.is_connected = False
#
#
#
#     def hoverEnterEvent(self, event):
#         self.mouse_over = True
#         self.update()
#         super(SocketConnection, self).hoverEnterEvent(event)
#
#     def hoverLeaveEvent(self, event):
#         self.mouse_over = False
#         self.update()
#         super(SocketConnection, self).hoverLeaveEvent(event)
#
#     def paint(self, painter, option, widget):
#         option.state = QStyle.State_NoChange
#
#         if self.isSelected():
#             self.__set_selected_colors()
#         elif self.mouse_over:
#             self.__set_hover_colors()
#         else:
#             self.__set_normal_colors()
#
#         super(SocketConnection, self).paint(painter, option, widget)
#
#     def __draw(self):
#         self.setFlag(QGraphicsItem.ItemIsSelectable)
#         self.setAcceptHoverEvents(True)
#
#         self.brush = QBrush()
#         self.brush.setStyle(Qt.SolidPattern)
#         self.brush.setColor(QColor(0, 0, 0, 255))
#
#         self.pen = QPen()
#         self.pen.setStyle(Qt.SolidLine)
#         self.pen.setWidth(nc.connection_width_normal)
#         self.pen.setColor(Colors.connection_normal)
#         self.setPen(self.pen)
#
#         self.setZValue(nc.connection_z_depth_normal)
#         self.redraw()
#
#         self.scene.addItem(self)
#
#     def __set_normal_colors(self):
#         pen = QPen()
#         pen.setStyle(Qt.SolidLine)
#         pen.setWidth(nc.connection_width_normal)
#         pen.setColor(Colors.connection_normal)
#         self.setZValue(nc.connection_z_depth_normal)
#         self.setPen(pen)
#
#     def __set_hover_colors(self):
#         pen = QPen()
#         pen.setStyle(Qt.SolidLine)
#         pen.setWidth(nc.connection_width_hover)
#         # pen.setColor(Colors.connection_hover)
#         pen.setColor(self.output_socket.socket_type.color)
#         self.setZValue(nc.connection_z_depth_hover)
#         self.setPen(pen)
#
#     def __set_selected_colors(self):
#         pen = QPen()
#         pen.setStyle(Qt.SolidLine)
#         pen.setWidth(nc.connection_width_selected)
#         pen.setColor(Colors.connection_selected)
#         self.setZValue(nc.connection_z_depth_hover)
#         self.setPen(pen)
#
#     def __str__(self):
#         return "SocketConnection: %s.%s -> %s.%s" % \
#                (self.output_socket.parentItem().name, self.output_socket.name,
#                 self.input_socket.parentItem().name, self.input_socket.name)
#
#
#
#
#
#
#
#
#
#
#
#
# ################################################################
# #  ____                   ____                            _   _
# # |  _ \ _ __ __ _  __ _ / ___|___  _ __  _ __   ___  ___| |_(_) ___  _ __
# # | | | | '__/ _` |/ _` | |   / _ \| '_ \| '_ \ / _ \/ __| __| |/ _ \| '_ \
# # | |_| | | | (_| | (_| | |__| (_) | | | | | | |  __/ (__| |_| | (_) | | | |
# # |____/|_|  \__,_|\__, |\____\___/|_| |_|_| |_|\___|\___|\__|_|\___/|_| |_|
# #                  |___/
# ###############################################################
#
#
#
#
#
# class DragConnection(QGraphicsPathItem):
#     def __init__(self, output_socket, mouse_position, scene):
#         super(DragConnection, self).__init__()
#         self.scene = scene
#         self.output_socket = output_socket
#         self.mouse_position = mouse_position
#
#         self.__draw()
#
#     def redraw(self):
#         cv_offset = 60
#
#         start_pos = self.output_socket.get_center_point()
#         end_pos = self.mouse_position
#
#         if self.mouse_position.x() > self.output_socket.get_center_point().x():
#             cv1 = QPointF(start_pos.x() + cv_offset, start_pos.y())
#             cv2 = QPointF(end_pos.x() - cv_offset, end_pos.y())
#         else:
#             cv1 = QPointF(start_pos.x() - cv_offset, start_pos.y())
#             cv2 = QPointF(end_pos.x() + cv_offset, end_pos.y())
#
#         path = QPainterPath(start_pos)
#
#         path.cubicTo(cv1, cv2, end_pos)
#
#         self.setPath(path)
#
#     def __draw(self):
#         #self.setFlag(QGraphicsItem.ItemIsSelectable)
#
#         self.brush = QBrush()
#         self.brush.setStyle(Qt.SolidPattern)
#         self.brush.setColor(QColor(0, 0, 0, 255))
#
#         self.pen = QPen()
#         self.pen.setStyle(Qt.SolidLine)
#         self.pen.setWidth(nc.connection_width_hover)
#         try:
#             self.pen.setColor(self.output_socket.socket_type.color)
#         except:
#             self.pen.setColor(Colors.white)
#         self.setPen(self.pen)
#
#         self.setZValue(nc.connection_z_depth_normal)
#         self.redraw()
#
#         self.scene.addItem(self)
#
#     def destroy_self(self):
#         self.scene.removeItem(self)
#
#
#
#
#
#
#
#
#
# ###############################################################
# #  _   _           _      ____             _        _
# # | \ | | ___   __| | ___/ ___|  ___   ___| | _____| |_
# # |  \| |/ _ \ / _` |/ _ \___ \ / _ \ / __| |/ / _ \ __|
# # | |\  | (_) | (_| |  __/___) | (_) | (__|   <  __/ |_
# # |_| \_|\___/ \__,_|\___|____/ \___/ \___|_|\_\___|\__|
# #
# ################################################################
#
#
#
# class NodeSocket(QGraphicsEllipseItem):
#     def __init__(self, io, socket_type, label, scene, position=None, color=Qt.green):
#         super(NodeSocket, self).__init__()
#         self.rect = QRectF(0, 0, nc.socket_size, nc.socket_size)
#         self.position = position
#         self.scene = scene
#
#         self.socket_type = socket_type
#
#         self.__draw()
#
#
#         self.io = io
#         self.label = label
#         self.name = self.label.toPlainText()
#         self.is_connected = False
#
#         self.connection_start_point = None
#         self.connection_end_point = None
#
#         self.drag_connection = None
#
#         self.connections = []
#
#     def get_value(self):
#         return self.socket_type.get_value()
#
#     def get_center_point(self):
#         if self.io == IO.input:
#             return QPointF(self.scenePos().x() + self.rect.left(), self.scenePos().y() + self.rect.bottom() / 2)
#         else:
#             return QPointF(self.scenePos().x() + self.rect.right(), self.scenePos().y() + self.rect.bottom() / 2)
#
#     def get_connected_sockets(self):
#         connected_sockets = []
#
#         for connection in self.connections:
#             if connection.output_socket == self:
#                 connected_sockets.append(connection.input_socket)
#             else:
#                 connected_sockets.append(connection.output_socket)
#
#         return connected_sockets
#
#     def is_connected_to(self, node_socket):
#         for connection in self.connections:
#             for socket in [connection.output_socket, connection.input_socket]:
#                 if socket == node_socket:
#                     return True
#
#         return False
#
#     def set_label_connected(self, value):
#         if value == True:
#             self.label.font.setBold(True)
#             self.label.setDefaultTextColor(self.socket_type.color)
#         else:
#             self.label.font.setBold(False)
#             self.label.setDefaultTextColor(Colors.text_default)
#         self.label.draw()
#
#     # def is_connected(self):
#     #     if len(self.connections) > 0:
#     #         return True
#     #     else:
#     #         return False
#
#     def mousePressEvent(self, event):
#         self.connection_start_point = event.scenePos()
#         output_socket = self.scene.itemAt(self.connection_start_point, QTransform())
#
#         self.drag_connection = DragConnection(output_socket, event.scenePos(), self.scene)
#
#     def mouseMoveEvent(self, event):
#         self.connection_end_point = event.scenePos()
#
#         if self.drag_connection is not None:
#             self.drag_connection.mouse_position = event.scenePos()
#             self.drag_connection.redraw()
#
#     def mouseReleaseEvent(self, event):
#         self.connection_end_point = event.scenePos()
#
#         if self.drag_connection is not None:
#             self.drag_connection.destroy_self()
#             self.drag_connection = None
#
#         output_socket = self.scene.itemAt(self.connection_start_point, QTransform())
#         input_socket = self.scene.itemAt(self.connection_end_point, QTransform())
#
#         print output_socket
#         print input_socket
#
#         if isinstance(input_socket, NodeSocket):
#             connection = SocketConnection(output_socket, input_socket, self.scene)
#             output_socket.set_label_connected(True)
#             input_socket.set_label_connected(True)
#             logging.info(str(connection))
#
#         else:
#             logging.warning("Released at %s, there is no socket here" % self.connection_end_point)
#
#
#     def __is_output_connected_to_input(self, node_socket):
#         if not node_socket.io == self.io:
#             return True
#         else:
#             return False
#
#     def __is_valid_connection(self, input_socket):
#         valid = True
#
#         if input_socket == self:
#             valid = False
#             logging.error("Output and input socket can't be the same!")
#
#         if self.is_connected_to(input_socket):
#             valid = False
#             logging.error("%s -> %s is already connected" % (self.name, input_socket.name))
#
#         if not self.__is_output_connected_to_input(input_socket):
#             valid = False
#             logging.error("%s is of type %s, %s is also of type %s" % (
#                 self.name, self.io, input_socket.name, input_socket.type))
#
#         return valid
#
#     def __draw(self):
#         self.brush = QBrush()
#         self.brush.setStyle(Qt.SolidPattern)
#         self.brush.setColor(self.socket_type.color)
#
#         self.pen = QPen()
#         self.pen.setStyle(Qt.SolidLine)
#         self.pen.setWidth(1)
#         self.pen.setColor(Colors.gray)
#
#         self.setRect(self.rect)
#         self.setBrush(self.brush)
#         self.setPen(self.pen)
#
#         self.setPos(self.position)
#
#         self.setZValue(nc.node_z_depth)
#
#         self.scene.addItem(self)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# ################################################################
# #  _   _           _      ___ _
# # | \ | | ___   __| | ___|_ _| |_ ___ _ __ ___
# # |  \| |/ _ \ / _` |/ _ \| || __/ _ \ '_ ` _ \
# # | |\  | (_) | (_| |  __/| || ||  __/ | | | | |
# # |_| \_|\___/ \__,_|\___|___|\__\___|_| |_| |_|
# #
# ################################################################
#
#
#
#
#
#
#
#
# class NodeItem(QGraphicsRectItem):
#     def __init__(self, scene, title, x=0, y=0):
#         super(NodeItem, self).__init__()
#         self.scene = scene
#         self.name = None
#
#         self.mouse_over = False
#
#         self.height = 30
#         self.title_label_size = 20
#         self.socket_label_size = nc.socket_size - 2
#         self.socket_size = nc.socket_size
#         self.socket_offset_from_top = nc.socket_size * 2.5
#
#         self.start_x_pos = x
#         self.start_y_pos = y
#
#         self.__draw()
#
#         self.title = self.__add_title(title)
#
#         self.scene.addItem(self)
#         self.scene.addItem(self.title)
#
#         self.input_sockets = []
#         self.output_sockets = []
#         self.__num_input_output_sockets = 0
#
#         self.execution_input_socket = None
#         self.execution_output_socket = None
#
#
#     def add_execution_output(self):
#         if self.execution_output_socket is not None:
#             raise IndexError("Node (%s) can only have 1 output execution socket" % self.name)
#
#         position = QPointF(self.boundingRect().right() - nc.execution_socket_size / 2,
#                            self.boundingRect().top()   - nc.execution_socket_size / 2)
#
#         self.execution_output_socket = ExecutionSocket(IO.output, self.scene, position)
#
#         self.execution_output_socket.setParentItem(self)
#
#     def add_execution_input(self):
#         if self.execution_input_socket is not None:
#             raise IndexError("Node (%s) can only have 1 input execution socket" % self.name)
#
#         position = QPointF(self.boundingRect().left() - nc.execution_socket_size / 2,
#                            self.boundingRect().top()  - nc.execution_socket_size / 2)
#
#         self.execution_input_socket = ExecutionSocket(IO.input, self.scene, position)
#
#         self.execution_input_socket.setParentItem(self)
#
#     def add_output(self, socket_type, output_name, color=Colors.socket_output):
#         if self.get_socket(output_name, IO.output) is not None:
#             logging.error("Output '%s' is already exists on '%s'" % (output_name, self.name))
#             return
#
#         label = NodeText(output_name, font_size=self.socket_label_size)
#
#         socket_y_position = self.boundingRect().top() + ((nc.socket_size + 5) * len(self.get_all_sockets()) + self.socket_offset_from_top) - (self.__num_input_output_sockets * nc.socket_size + 5)
#
#         socket_position = QPointF(self.boundingRect().right() - nc.socket_size / 2, socket_y_position)
#         socket = NodeSocket(IO.output, socket_type, label, self.scene, position=socket_position, color=color)
#         socket.socket_type = socket_type
#
#         label_x = self.boundingRect().right() - label.boundingRect().width() - nc.socket_label_spacing
#         label_y = socket.get_center_point().y() - (label.boundingRect().height() / 2) - (nc.socket_size / 8)
#         label_position = QPointF(label_x, label_y)
#
#         label.setPos(label_position.x(), label_position.y())
#
#         socket.label = label
#
#         self.scene.addItem(label)
#
#         label.setParentItem(self)
#         socket.setParentItem(self)
#
#         self.output_sockets.append(socket)
#
#         self.__resize()
#
#     def add_input(self, socket_type, input_name, color=Colors.socket_input):
#         if self.get_socket(input_name, IO.input) is not None:
#             logging.error("Input '%s' is already exists on '%s'" % (input_name, self.name))
#             return
#
#         label = NodeText(input_name, font_size=self.socket_label_size)
#
#         socket_y_position = self.boundingRect().top() + ((nc.socket_size + 5) * len(self.get_all_sockets()) + self.socket_offset_from_top) - (self.__num_input_output_sockets * nc.socket_size + 5)
#
#         socket_position = QPointF(self.boundingRect().left() - nc.socket_size / 2, socket_y_position)
#         socket = NodeSocket(IO.input, socket_type, label, self.scene, position=socket_position, color=color)
#         socket.socket_type = socket_type
#
#         label_x = self.boundingRect().left() + nc.socket_label_spacing
#         label_y = socket.get_center_point().y() - (label.boundingRect().height() / 2) - (nc.socket_size / 8)
#         label_position = QPointF(label_x, label_y)
#
#         label.setPos(label_position.x(), label_position.y())
#
#         socket.label = label
#
#         self.scene.addItem(label)
#
#         label.setParentItem(self)
#         socket.setParentItem(self)
#
#         self.input_sockets.append(socket)
#
#         self.__resize()
#
#     def add_input_output(self, socket_type, input_output_name, color=Colors.socket_input):
#         if self.get_socket(input_output_name, IO.both) is not None:
#             logging.error("Input or output '%s' is already exists on '%s'" % (input_output_name, self.name))
#             return
#
#         label = NodeText(input_output_name, font_size=self.socket_label_size)
#
#         socket_y_position = self.boundingRect().top() + ((nc.socket_size + 5) * len(self.get_all_sockets()) + self.socket_offset_from_top) - (self.__num_input_output_sockets * (nc.socket_size + 5))
#
#         input_socket_position = QPointF(self.boundingRect().left() - nc.socket_size / 2,socket_y_position)
#         input_socket = NodeSocket(IO.input, socket_type, label, self.scene, position=input_socket_position, color=color)
#         input_socket.socket_type = socket_type
#
#         output_socket_position = QPointF(self.boundingRect().right() - nc.socket_size / 2, socket_y_position)
#         output_socket = NodeSocket(IO.output, socket_type, label, self.scene, position=output_socket_position,
#                                    color=color)
#         output_socket.socket_type = socket_type
#
#         label_x = self.boundingRect().width() / 2 - label.boundingRect().width() / 2
#         label_y = output_socket.get_center_point().y() - (label.boundingRect().height() / 2) - (nc.socket_size / 8)
#         label_position = QPointF(label_x, label_y)
#
#         label.setPos(label_position.x(), label_position.y())
#
#         input_socket.label = label
#         output_socket.label = label
#
#         self.scene.addItem(input_socket)
#         self.scene.addItem(output_socket)
#
#         label.setParentItem(self)
#         input_socket.setParentItem(self)
#         output_socket.setParentItem(self)
#
#         self.input_sockets.append(input_socket)
#         self.output_sockets.append(output_socket)
#         self.__num_input_output_sockets += 1
#
#         self.__resize()
#
#     def get_all_sockets(self):
#         return self.output_sockets + self.input_sockets
#
#     def destroy_self(self):
#         all_sockets = self.output_sockets + self.input_sockets
#         all_connections = []
#
#         for socket in all_sockets:
#             for connection in socket.connections:
#                 all_connections.append(connection)
#
#         for connection in all_connections:
#             logging.info("Destroying %s" % connection)
#             connection.destroy_self()
#
#         self.scene.removeItem(self)
#
#     def get_connections(self):
#         all_sockets = self.output_sockets + self.input_sockets
#         all_connections = []
#
#         for socket in all_sockets:
#             for connection in socket.connections:
#                 all_connections.append(connection)
#
#         return all_connections
#
#     def get_socket(self, socket_name, input_output):
#         if input_output == IO.output:
#             for socket in self.output_sockets:
#                 if socket.name == socket_name:
#                     return socket
#         elif input_output == IO.input:
#             for socket in self.input_sockets:
#                 if socket.name == socket_name:
#                     return socket
#         elif input_output == IO.both:
#             for socket in self.get_all_sockets():
#                 if socket.name == socket_name:
#                     return socket
#
#         return None
#
#     def get_connected_sockets(self):
#         pass
#
#     # TODO: add stuff
#
#     def reposition_title(self):
#         # self.title.setPlainText(new_text)
#         self.title.setPos(
#             (self.boundingRect().width() / 2 - self.title.boundingRect().width() / 2) + self.boundingRect().left(),
#             self.boundingRect().top() - self.title.boundingRect().height() - nc.title_offset)
#         self.name = self.title
#         print self.name
#
#     def hoverEnterEvent(self, event):
#         self.mouse_over = True
#         self.update()
#
#         super(NodeItem, self).hoverEnterEvent(event)
#
#     def hoverLeaveEvent(self, event):
#         self.mouse_over = False
#         self.update()
#
#         super(NodeItem, self).hoverLeaveEvent(event)
#
#     def itemChange(self, change, value):
#         try:
#             for socket in self.output_sockets:
#                 for connection in socket.connections:
#                     connection.redraw()
#
#             for socket in self.input_sockets:
#                 for connection in socket.connections:
#                     connection.redraw()
#         except:
#             pass
#         finally:
#             return QGraphicsRectItem.itemChange(self, change, value)
#
#     def paint(self, painter, option, widget):
#         option.state = QStyle.State_NoChange
#
#         if self.isSelected():
#             self.__set_selected_colors()
#         elif self.mouse_over:
#             self.__set_hover_colors()
#         else:
#             self.__set_normal_colors()
#
#         super(NodeItem, self).paint(painter, option, widget)
#
#     def __draw(self, ):
#         self.rect = QRectF(0, 0, 150, self.height)
#         self.setRect(self.rect)
#
#         self.__set_normal_colors()
#
#         self.setFlag(QGraphicsRectItem.ItemIsSelectable)
#         self.setFlag(QGraphicsRectItem.ItemIsMovable)
#         self.setFlag(QGraphicsRectItem.ItemSendsGeometryChanges)
#
#         self.setZValue(100)
#         self.setPos(self.start_x_pos, self.start_y_pos)
#
#         self.setAcceptHoverEvents(True)
#
#         self.update()
#
#     def __resize(self):
#         total_sockets = len(self.get_all_sockets())
#         new_height = (nc.socket_size * 1.5 * total_sockets) - (
#                 nc.socket_size * 1.5 * self.__num_input_output_sockets) + self.height
#         position = self.pos()
#         self.rect = QRectF(0, 0, 150, new_height)
#         self.setRect(self.rect)
#         self.setPos(position)
#
#     def __set_normal_colors(self):
#         pen = QPen()
#         pen.setStyle(Qt.SolidLine)
#         pen.setWidth(1)
#         pen.setColor(Colors.node_normal_border)
#         self.setPen(pen)
#         brush = QBrush()
#         brush.setStyle(Qt.SolidPattern)
#         brush.setColor(Colors.node_normal_background)
#         self.setBrush(brush)
#
#     def __set_hover_colors(self):
#         pen = QPen()
#         pen.setStyle(Qt.SolidLine)
#         pen.setWidth(1)
#         pen.setColor(Colors.node_hover_border)
#         self.setPen(pen)
#         brush = QBrush()
#         brush.setStyle(Qt.SolidPattern)
#         brush.setColor(Colors.node_hover_background)
#         self.setBrush(brush)
#
#     def __set_selected_colors(self):
#         pen = QPen()
#         pen.setStyle(Qt.SolidLine)
#         pen.setWidth(nc.node_border_width_selected)
#         pen.setColor(Colors.node_selected_border)
#         self.setPen(pen)
#         brush = QBrush()
#         brush.setStyle(Qt.SolidPattern)
#         brush.setColor(Colors.node_selected_background)
#         self.setBrush(brush)
#
#     def __add_title(self, title):
#         self.name = title
#         node_title = NodeText(title, font_size=self.title_label_size)
#         node_title.setTextInteractionFlags(Qt.TextEditorInteraction)
#
#         # self.reposition_title()
#
#         node_title.setPos(
#             (self.boundingRect().width() / 2 - node_title.boundingRect().width() / 2) + self.boundingRect().left(),
#             self.boundingRect().top() - node_title.boundingRect().height() - nc.title_offset)
#
#         node_title.setParentItem(self)
#
#         return node_title
#
#
#
#
#
# #######################################################
# #
# #  _____                     _   _             ____             _        _
# # | ____|_  _____  ___ _   _| |_(_) ___  _ __ / ___|  ___   ___| | _____| |_
# # |  _| \ \/ / _ \/ __| | | | __| |/ _ \| '_ \\___ \ / _ \ / __| |/ / _ \ __|
# # | |___ >  <  __/ (__| |_| | |_| | (_) | | | |___) | (_) | (__|   <  __/ |_
# # |_____/_/\_\___|\___|\__,_|\__|_|\___/|_| |_|____/ \___/ \___|_|\_\___|\__|
# #
# #######################################################
#
#
#
#
#
# class ExecutionSocket(QGraphicsEllipseItem):
#     def __init__(self, io, scene, position):
#         super(ExecutionSocket, self).__init__()
#         self.rect = QRectF(0, 0, nc.execution_socket_size, nc.execution_socket_size)
#         self.scene = scene
#         self.position = position
#
#         self.__draw()
#
#         self.connection_start_point = None
#         self.connection_end_point = None
#
#         self.socket_type = socket_types.ExecutionSocketType()
#
#         self.drag_connection = None
#
#         self.io = io
#         self.connection = None
#
#     def mousePressEvent(self, event):
#         self.connection_start_point = event.scenePos()
#         output_socket = self.scene.itemAt(self.connection_start_point, QTransform())
#
#         self.drag_connection = DragConnection(output_socket, event.scenePos(), self.scene)
#
#     def mouseMoveEvent(self, event):
#         self.connection_end_point = event.scenePos()
#
#         if self.drag_connection is not None:
#             self.drag_connection.mouse_position = event.scenePos()
#             self.drag_connection.redraw()
#
#     def mouseReleaseEvent(self, event):
#         self.connection_end_point = event.scenePos()
#
#         if self.drag_connection is not None:
#             self.drag_connection.destroy_self()
#             self.drag_connection = None
#
#         output_socket = self.scene.itemAt(self.connection_start_point, QTransform())
#         input_socket = self.scene.itemAt(self.connection_end_point, QTransform())
#
#         print output_socket
#         print input_socket
#
#         if isinstance(input_socket, ExecutionSocket):
#             connection = ExecutionSocketConnection(output_socket, input_socket, self.scene)
#             # output_socket.set_label_connected(True)
#             # input_socket.set_label_connected(True)
#             logging.info(str(connection))
#
#         else:
#             logging.warning("Released at %s, there is no socket here" % self.connection_end_point)
#
#     def get_center_point(self):
#         if self.io == IO.input:
#             return QPointF(self.scenePos().x() + self.rect.left(), self.scenePos().y() + self.rect.bottom() / 2)
#         else:
#             return QPointF(self.scenePos().x() + self.rect.right(), self.scenePos().y() + self.rect.bottom() / 2)
#
#
#     def __draw(self):
#         print "drawing exe"
#         self.brush = QBrush()
#         self.brush.setStyle(Qt.SolidPattern)
#         self.brush.setColor(Colors.white)
#
#         self.pen = QPen()
#         self.pen.setStyle(Qt.DashLine)
#         self.pen.setWidth(1)
#         self.pen.setColor(Colors.black)
#
#         self.setRect(self.rect)
#         self.setBrush(self.brush)
#         self.setPen(self.pen)
#
#         self.setPos(self.position)
#
#         self.setZValue(nc.node_z_depth)
#
#         self.scene.addItem(self)
#
#
#
#
# class ExecutionSocketConnection(QGraphicsPathItem):
#     def __init__(self, output_socket, input_socket, scene):
#         super(ExecutionSocketConnection, self).__init__()
#
#         self.scene = scene
#
#         self.mouse_over = False
#
#         self.output_socket = output_socket
#         self.input_socket = input_socket
#         self.order_sockets()
#
#         self.check_validity()
#
#         self.update_sockets()
#
#         self.__draw()
#
#     def update_sockets(self):
#         self.input_socket.connections.append(self)
#         self.output_socket.connections.append(self)
#
#         self.input_socket.is_connected = True
#         self.output_socket.is_connected = True
#
#     def order_sockets(self):
#         if self.output_socket.io != IO.output:
#             self.output_socket, self.input_socket = self.input_socket, self.output_socket
#
#     def check_validity(self):
#         error_message = None
#
#         if self.output_socket.socket_type.name != self.input_socket.socket_type.name:
#             if self.input_socket.socket_type.name != "debug" and self.input_socket.socket_type.name != "list":
#                 error_message = "Output socket type (%s) doesn't match input socket type (%s)" % \
#                                 (self.output_socket.socket_type.name, self.input_socket.socket_type.name)
#
#         if self.output_socket.name == self.input_socket.name and self.output_socket.parentItem() == self.input_socket.parentItem():
#             error_message = "Can't connect to the same socket %s -> %s" % (self.output_socket.name, self.input_socket.name)
#
#         if self.input_socket == self.output_socket:
#             error_message = "Output socket (%s) is the same as the input socket (%s)" % \
#                                  (self.output_socket.name, self.input_socket.name)
#
#         if self.output_socket.is_connected_to(self.input_socket):
#             error_message = "%s -> %s is already connected" % (self.output_socket.name, self.input_socket.name)
#
#         if self.output_socket.io == self.input_socket.io:
#             error_message = "Trying to connection %s to %s" % (self.output_socket.io, self.input_socket.io)
#
#         if self.input_socket.is_connected and self.input_socket.socket_type.accept_multiple == False:
#             error_message = "%s doesn't allow multiple connections" % self.input_socket.name
#
#         if error_message is not None:
#             logging.error(error_message)
#             print "\n\n"
#             raise AttributeError(error_message)
#
#     def redraw(self):
#         cv_offset = 60
#
#         start_pos = self.output_socket.get_center_point()
#         end_pos = self.input_socket.get_center_point()
#
#         cv1 = QPointF(start_pos.x() + cv_offset, start_pos.y())
#         cv2 = QPointF(end_pos.x() - cv_offset, end_pos.y())
#
#         path = QPainterPath(start_pos)
#
#         path.cubicTo(cv1, cv2, end_pos)
#
#         self.setPath(path)
#
#     def destroy_self(self):
#         self.scene.removeItem(self)
#
#         for socket in [self.output_socket, self.input_socket]:
#             pass
#             # socket.set_label_connected(False)
#             # socket.connections.remove(self)
#             # socket.is_connected = False
#
#
#
#
#
#
#
# ################################################################
# #  _   _           _     _____         _
# # | \ | | ___   __| | __|_   _|____  _| |_
# # |  \| |/ _ \ / _` |/ _ \| |/ _ \ \/ / __|
# # | |\  | (_) | (_| |  __/| |  __/>  <| |_
# # |_| \_|\___/ \__,_|\___||_|\___/_/\_\\__|
# #
# ################################################################
#
#
#
# class NodeText(QGraphicsTextItem):
#     def __init__(self, text, font_size=20):
#         super(NodeText, self).__init__()
#         self.font_size = font_size
#         self.font = QFont()
#
#         self.text = text
#         self.setPlainText(text)
#
#         self.draw()
#
#     def draw(self):
#         self.font.setPixelSize(self.font_size)
#         self.setFont(self.font)
#
#         # self.setHtml('<b>%s</b>' % self.name)
#
#         self.setZValue(100)
#
#
# # bool ValueAxisLabel::sceneEvent(QEvent *event)
# # {
# #     if (event->type() == QEvent::GraphicsSceneMouseDoubleClick) {
# #         setTextInteractionFlags(Qt::TextEditorInteraction);
# #
# #         bool ret = QGraphicsTextItem::sceneEvent(event);
# #         // QGraphicsTextItem::sceneevent needs to be processed before
# #         // the focus
# #         setFocus(Qt::MouseFocusReason);
# #         return ret;
# #     }
# #     return QGraphicsTextItem::sceneEvent(event);
# # }
#
#
#
#
#
# ################################################################
# #  _   _           _    __     ___
# # | \ | | ___   __| | __\ \   / (_) _____      __
# # |  \| |/ _ \ / _` |/ _ \ \ / /| |/ _ \ \ /\ / /
# # | |\  | (_) | (_| |  __/\ V / | |  __/\ V  V /
# # |_| \_|\___/ \__,_|\___| \_/  |_|\___| \_/\_/
# #
# ################################################################
#
#
#
# class NodeView(QGraphicsView):
#     def __init__(self, scene, parent):
#         super(NodeView, self).__init__(parent)
#         self.setObjectName("View")
#         # self.setAcceptDrops(True)
#         self.setScene(scene)
#
#         self.middle_mouse_down = False
#         self.start_x = None
#         self.start_y = None
#         self.drag_speed = 0.03
#
#         self.horizontalScrollBar().setValue(1)
#         self.verticalScrollBar().setValue(1)
#         # self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
#         # self.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
#         self.setDragMode(QGraphicsView.RubberBandDrag)
#
#         print "RELOADED View"
#
#     def mousePressEvent(self, event):
#         if event.button() == Qt.MiddleButton:
#             self.middle_mouse_down = True
#             self.start_x = event.pos().x()
#             self.start_y = event.pos().y()
#
#             self.setCursor(Qt.ClosedHandCursor)
#             event.accept()
#         else:
#             super(NodeView, self).mousePressEvent(event)
#
#         # if event.button() == Qt.MiddleButton:
#         #     self.setDragMode(QGraphicsView.ScrollHandDrag)
#         #     event.accept()
#
#     def mouseMoveEvent(self, event):
#         if self.middle_mouse_down:
#             self.horizontalScrollBar().setValue(
#                 (self.horizontalScrollBar().value() - (event.pos().x() - self.start_x) * self.drag_speed))
#             self.verticalScrollBar().setValue(
#                 (self.verticalScrollBar().value() - (event.pos().y() - self.start_y) * self.drag_speed))
#             event.accept()
#         else:
#             event.ignore()
#
#         super(NodeView, self).mouseMoveEvent(event)
#
#     def mouseReleaseEvent(self, event):
#         if event.button() == Qt.MiddleButton:
#             self.setDragMode(QGraphicsView.RubberBandDrag)
#             self.middle_mouse_down = False
#             self.setCursor(Qt.ArrowCursor)
#             event.accept()
#         else:
#             event.ignore()
#
#         super(NodeView, self).mouseReleaseEvent(event)
#
#     # def dragLeaveEvent(self, event):
#     #     print event.source()
#
#     def wheelEvent(self, event):
#         if event.delta() > 0:
#             self.scale(1.1, 1.1)
#         else:
#             self.scale(0.9, 0.9)
#
#
#
#
#
#
#
#
#
#
#
#
# ###############################################################
# #  _   _           _      ____
# # | \ | | ___   __| | ___/ ___|  ___ ___ _ __   ___
# # |  \| |/ _ \ / _` |/ _ \___ \ / __/ _ \ '_ \ / _ \
# # | |\  | (_) | (_| |  __/___) | (_|  __/ | | |  __/
# # |_| \_|\___/ \__,_|\___|____/ \___\___|_| |_|\___|
# #
# ###############################################################
#
#
#
#
#
# class NodeScene(QGraphicsScene):
#     def __init__(self):
#         super(NodeScene, self).__init__()
#
#     def dragLeaveEvent(self, event):
#         # print event
#         # print event.source()
#         # class_name = event.source().selectedItems()[0].text(0)
#         # module = event.source().selectedItems()[0].parent().text(0)
#         #
#         # x = event.scenePos().x()
#         # y = event.scenePos().y()
#         #
#         # self.add_node_to_view(class_name, module, x, y)
#         event.accept()
#         pass
#
#     def dragMoveEvent(self, event):
#         event.accept()
#
#     def dropEvent(self, event):
#         class_name = event.source().selectedItems()[0].text(0)
#         module = event.source().selectedItems()[0].parent().text(0)
#
#         x = event.scenePos().x()
#         y = event.scenePos().y()
#
#         self.add_node_to_view(class_name, module, x, y)
#
#     def add_node_to_view(self, class_name, module, x=0, y=0):
#         class_path = ".".join(["nv_NodeEditor", "nodes", module, class_name, class_name])
#         node_class = locate(class_path)
#         node_instance = node_class(self, x, y)
#
#     def get_all_nodes(self):
#         # from nv_NodeEditor.nodes.base_node import BaseNode
#         nodes = []
#         for item in self.items():
#             if issubclass(type(item), BaseNode):
#                 nodes.append(item)
#
#         return nodes
#
#     def get_nonexisting_name(self, name):
#         for node in self.get_all_nodes():
#             if name == node.name:
#                 pass
#             #TODO: generate unique name, now battlefield
#
#     def keyPressEvent(self, event):
#         # from nv_NodeEditor.nodes.base_node import BaseNode
#         if event.key() == Qt.Key_Delete:
#             for item in self.selectedItems():
#                 try:
#                     item.destroy_self()
#                 except:
#                     pass
#         if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
#             for item in self.items():
#                 if issubclass(type(item), BaseNode):
#                     try:
#                         item.reposition_title()
#                     except StandardError, err:
#                         print err
#                         pass
#         else:
#             super(NodeScene, self).keyPressEvent(event)
#
# from nv_NodeEditor.nodes.base_node import BaseNode