from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

import nv_utils.utils as utils
from nv_utils.singleton import Singleton

class ImageViewer(QDockWidget, metaclass=Singleton):
    def __init__(self, parent):
        super(ImageViewer, self).__init__()

        self.main_widget = QWidget()
        self.main_widget.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.main_widget.setMinimumSize(0, 0)

        self.lbl_pixmap = QLabel()
        self.lbl_pixmap.setScaledContents(False)
        self.lbl_pixmap.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.lbl_pixmap.setMinimumSize(0, 0)

        layout = QGridLayout()
        layout.addWidget(self.lbl_pixmap)
        self.main_widget.setLayout(layout)

        self.setWidget(self.main_widget)

        self.setParent(parent)
        self.setWindowTitle("Tangle - Image Viewer")
        self.setFloating(True)

        print(self)

        # self.setWindowFlags(Qt.Window)

    def resize_pixmap(self):
        try:
            self.lbl_pixmap.setPixmap(self.pixmap.scaled(self.lbl_pixmap.width(), self.lbl_pixmap.height(),
                                                          Qt.KeepAspectRatio, Qt.SmoothTransformation))
        except AttributeError as err:
            utils.trace(err)

    def set_pixmap(self, pixmap):
        self.pixmap = pixmap
        self.lbl_pixmap.setPixmap(self.pixmap)
        self.resize_pixmap()

    def resizeEvent(self, event):
        print("resizing")
        self.resize_pixmap()
        self.main_widget.resizeEvent(event)
        # super(ImageViewer, self).resizeEvent(event)


