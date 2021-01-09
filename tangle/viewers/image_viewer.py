from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import ez_utils

class ImageViewer(QDockWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)

        self.main_widget = QWidget()
        self.main_widget.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.main_widget.setMinimumSize(0, 0)

        self.chk_auto_update = QCheckBox("Automatically update on selection change")
        self.chk_auto_update.setChecked(True)

        self.lbl_pixmap = QLabel()
        self.lbl_pixmap.setScaledContents(False)
        self.lbl_pixmap.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.lbl_pixmap.setMinimumSize(0, 0)

        layout = QVBoxLayout()
        layout.addWidget(self.chk_auto_update)
        layout.addWidget(self.lbl_pixmap)
        self.main_widget.setLayout(layout)

        self.setWidget(self.main_widget)

        self.setParent(parent)
        self.setWindowTitle("Tangle - Image Viewer")
        self.setFloating(True)

    def resize_pixmap(self):
        try:
            self.lbl_pixmap.setPixmap(self.pixmap.scaled(self.lbl_pixmap.width(), self.lbl_pixmap.height(),
                                                          Qt.KeepAspectRatio, Qt.SmoothTransformation))
        except AttributeError as err:
            pass
            ez_utils.general.trace(err)

    def set_pixmap(self, pixmap):
        if self.chk_auto_update.isChecked():
            self.pixmap = pixmap
            self.lbl_pixmap.setPixmap(self.pixmap)
            self.resize_pixmap()

    def clear(self):
        self.lbl_pixmap.setPixmap(QPixmap())

    def resizeEvent(self, event):
        self.resize_pixmap()
        self.main_widget.resizeEvent(event)
        super().resizeEvent(event)


