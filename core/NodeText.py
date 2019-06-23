from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import re


class NodeText(QGraphicsTextItem):
    def __init__(self, text, font_size=20):
        super(NodeText, self).__init__()
        self.font_size = font_size
        self.font = QFont()

        self.text = text
        self.setPlainText(text)

        self.draw()

    def draw(self):
        self.font.setPixelSize(self.font_size)
        self.setFont(self.font)

        # self.setHtml('<b>%s</b>' % self.name)

        self.setZValue(100)

    def __str__(self):
        return self.toPlainText()


# bool ValueAxisLabel::sceneEvent(QEvent *event)
# {
#     if (event->type() == QEvent::GraphicsSceneMouseDoubleClick) {
#         setTextInteractionFlags(Qt::TextEditorInteraction);
#
#         bool ret = QGraphicsTextItem::sceneEvent(event);
#         // QGraphicsTextItem::sceneevent needs to be processed before
#         // the focus
#         setFocus(Qt::MouseFocusReason);
#         return ret;
#     }
#     return QGraphicsTextItem::sceneEvent(event);
# }