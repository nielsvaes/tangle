from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class NodeTitle(QGraphicsTextItem):
    def __init__(self, text, font_size=20):
        super(NodeTitle, self).__init__()
        self.font_size = font_size
        self.font = QFont()

        self.text = text
        self.setPlainText(text)

        self.background = None

        self.draw()

    def get_node(self):
        return self.parentItem()

    def draw(self):
        self.font.setPixelSize(self.font_size)
        self.setFont(self.font)

        self.setZValue(100)

    def __str__(self):
        return self.toPlainText()
