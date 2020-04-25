from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from .SettingsConstants import ApplicationSettings as aps

from ez_settings.ez_settings import EasySettingsSingleton as ez_settings

class NodeView(QGraphicsView):
    def __init__(self, scene, parent):
        super(NodeView, self).__init__(parent)
        if ez_settings().get_value(aps.chk_high_quality_view, True):
            self.setRenderHint(QPainter.HighQualityAntialiasing)
        self.setObjectName("View")
        self.setScene(scene)

        self.zoom = 5

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

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            if self.zoom < 15:
                self.zoom += 1
                self.scale(1.1, 1.1)
        else:
            if self.zoom > 0.8:
                self.zoom -= 1
                self.scale(0.9, 0.9)



