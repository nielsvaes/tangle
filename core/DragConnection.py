# from PyQt5.QtUiTools import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from .Constants import nc, Colors, IO

class DragConnection(QGraphicsPathItem):
    def __init__(self, output_socket, mouse_position, scene):
        super(DragConnection, self).__init__()
        self.scene = scene
        self.output_socket = output_socket
        self.mouse_position = mouse_position

        self.all_sockets = []
        self.find_all_sockets()

        self.__draw()

    def find_all_sockets(self):
        for node in self.scene.get_all_nodes():
            self.all_sockets += node.get_all_sockets()

    def redraw(self):
        cv_offset = nc.connection_cv_offset

        start_pos = self.output_socket.get_center_point()
        end_pos = self.mouse_position

        for socket in self.all_sockets:
            center_point = socket.get_center_point()
            if self.__get_distance(end_pos, center_point) < nc.socket_size:
                end_pos = center_point


        if self.mouse_position.x() > self.output_socket.get_center_point().x():
            cv1 = QPointF(start_pos.x() + cv_offset, start_pos.y())
            cv2 = QPointF(end_pos.x() - cv_offset, end_pos.y())
        else:
            cv1 = QPointF(start_pos.x() - cv_offset, start_pos.y())
            cv2 = QPointF(end_pos.x() + cv_offset, end_pos.y())

        path = QPainterPath(start_pos)

        path.cubicTo(cv1, cv2, end_pos)

        self.setPath(path)

    def __get_distance(self, point1, point2):
        import math
        x1 = point1.x()
        y1 = point1.y()

        x2 = point2.x()
        y2 = point2.y()

        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        return distance

    def __draw(self):
        #self.setFlag(QGraphicsItem.ItemIsSelectable)

        self.brush = QBrush()
        self.brush.setStyle(Qt.SolidPattern)
        self.brush.setColor(QColor(0, 0, 0, 255))

        self.pen = QPen()
        self.pen.setStyle(Qt.DotLine)
        self.pen.setWidth(nc.connection_width_hover)
        try:
            self.pen.setColor(self.output_socket.socket_type.color)
        except:
            self.pen.setColor(Colors.white)
        self.setPen(self.pen)

        self.setZValue(nc.connection_z_depth_normal)
        self.redraw()

        self.scene.addItem(self)

    def destroy_self(self):
        self.scene.removeItem(self)

