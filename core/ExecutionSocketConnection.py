# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
#
# import logging
#
# from .Constants import nc, Colors, IO
# from .SocketConnection import SocketConnection
#
# # TODO: Break execution
#
# class ExecutionSocketConnection(SocketConnection):
#     def __init__(self, output_socket, input_socket, scene):
#         super(ExecutionSocketConnection, self).__init__(output_socket, input_socket, scene)
#
#     def update_sockets(self):
#         self.input_socket.connection = self
#         self.output_socket.connection = self
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
#         if self.input_socket == self.output_socket:
#             error_message = "Output socket (%s) is the same as the input socket (%s)" % \
#                                  (self.output_socket.name, self.input_socket.name)
#
#         if self.output_socket.is_connected_to(self.input_socket):
#             error_message = "Already connected to this input"
#
#         if self.output_socket.is_connected() or self.input_socket.is_connected():
#             error_message = "Execution sockets can only have 1 connection. " \
#                             "%s is already connected to %s" \
#                             % (self.output_socket.get_node().name, self.output_socket.connection.input_socket.get_node())
#
#         if self.output_socket.io == self.input_socket.io:
#             error_message = "Trying to connection %s to %s" % (self.output_socket.io, self.input_socket.io)
#
#         if self.output_socket.get_node() == self.input_socket.get_node():
#             error_message = "Can't connect ExecutionSocket output to the ExecutionSocket input on the same node"
#
#         if error_message is not None:
#             logging.error(error_message)
#             raise AttributeError(error_message)
#
#
#     def destroy_self(self):
#         self.scene.removeItem(self)
#
#         for socket in [self.output_socket, self.input_socket]:
#             socket.connection = None
#
#     def redraw(self):
#         cv_offset = nc.connection_cv_offset / 3
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
#         # call the base class's super so we don't override the settings here
#         super(SocketConnection, self).paint(painter, option, widget)
#
#     def __set_normal_colors(self):
#         pen = QPen()
#         pen.setStyle(Qt.DashDotDotLine)
#         pen.setWidth(nc.execution_connection_width)
#         pen.setColor(Colors.white)
#         self.setZValue(nc.connection_z_depth_normal)
#         self.setPen(pen)
#
#     def __set_hover_colors(self):
#         pass
#
#     def __set_selected_colors(self):
#         pen = QPen()
#         pen.setStyle(Qt.SolidLine)
#         pen.setWidth(nc.connection_width_selected)
#         pen.setColor(Colors.white)
#         self.setZValue(nc.connection_z_depth_hover)
#         self.setPen(pen)
#
#
#
#     def __str__(self):
#         return "SocketConnection: %s.%s -> %s.%s" % \
#                (self.output_socket.parentItem(), self.output_socket,
#                 self.input_socket.parentItem(), self.input_socket)
