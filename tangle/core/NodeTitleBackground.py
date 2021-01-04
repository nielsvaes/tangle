from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from .Constants import nc

class NodeTitleBackground(QGraphicsRectItem):
    def __init__(self, scene, node, color):
        super(NodeTitleBackground, self).__init__()
        self.scene = scene
        self.mouse_over = False
        self.node = node
        self.color = color

        self.height = nc.title_background_height

        self.__draw()

        self.setParentItem(self.node)

    def __draw(self):
        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(self.color)
        self.setBrush(brush)

        background_rect = QRectF(0, 0, nc.node_item_width, nc.title_background_height)
        self.setRect(background_rect)
        self.setPos(self.node.rect().left(), self.node.rect().top() - nc.title_background_height)

    def hoverEnterEvent(self, event):
        self.mouse_over = True
        self.update()

        super(NodeTitleBackground, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.mouse_over = False
        self.update()

        super(NodeTitleBackground, self).hoverLeaveEvent(event)

    # def paint(self, painter, option, widget):
    #     option.state = QStyle.State_NoChange
    #
    #     if self.isSelected():
    #         self.__set_selected_colors()
    #     elif self.mouse_over:
    #         self.__set_hover_colors()
    #     else:
    #         self.__set_normal_colors()
    #
    #     super(NodeTitleBackground, self).paint(painter, option, widget)