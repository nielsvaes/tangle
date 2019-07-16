from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class NodeView(QGraphicsView):
    def __init__(self, scene, parent):
        super(NodeView, self).__init__(parent)
        self.setRenderHint(QPainter.HighQualityAntialiasing)
        self.setObjectName("View")
        # self.setAcceptDrops(True)
        self.setScene(scene)

        self.middle_mouse_down = False
        self.start_x = None
        self.start_y = None
        self.drag_speed = 0.03

        self.zoom = 5

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # self.horizontalScrollBar().setValue(1)
        # self.verticalScrollBar().setValue(1)

        self.setDragMode(QGraphicsView.RubberBandDrag)

        self.scale(0.9, 0.9)

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            release_event = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                       Qt.LeftButton, Qt.NoButton, event.modifiers())
            super().mouseReleaseEvent(release_event)
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            fake_event = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                    Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
            super().mousePressEvent(fake_event)
        else:
            event.accept()
            super(NodeView, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                    Qt.LeftButton, event.buttons() & ~Qt.LeftButton, event.modifiers())
            super().mouseReleaseEvent(fakeEvent)
            self.setDragMode(QGraphicsView.RubberBandDrag)
        else:
            event.accept()
            super(NodeView, self).mouseReleaseEvent(event)

        # if event.button() == Qt.MiddleButton:
        #     self.setDragMode(QGraphicsView.ScrollHandDrag)
        #     event.accept()

    # def mouseMoveEvent(self, event):
    #     if self.middle_mouse_down:
    #         self.horizontalScrollBar().setValue(
    #             (self.horizontalScrollBar().value() - (event.pos().x() - self.start_x) * self.drag_speed))
    #         self.verticalScrollBar().setValue(
    #             (self.verticalScrollBar().value() - (event.pos().y() - self.start_y) * self.drag_speed))
    #         event.accept()
    #     else:
    #         event.ignore()
    #
    #     super(NodeView, self).mouseMoveEvent(event)

    # def mouseReleaseEvent(self, event):
    #     if event.button() == Qt.MiddleButton:
    #         self.setDragMode(QGraphicsView.RubberBandDrag)
    #         self.middle_mouse_down = False
    #         self.setCursor(Qt.ArrowCursor)
    #         event.accept()
    #     else:
    #         event.ignore()
    #
    #     super(NodeView, self).mouseReleaseEvent(event)

    # def dragLeaveEvent(self, event):
    #     print event.source()

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            if self.zoom < 15:
                self.zoom += 1
                self.scale(1.1, 1.1)
        else:
            if self.zoom > 1:
                self.zoom -= 1
                self.scale(0.9, 0.9)



