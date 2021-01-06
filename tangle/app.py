import logging
import os
import nv_utils.io_utils

from PySide2.QtWidgets import *
from PySide2.QtGui import *

from tangle import tangle_window


def main():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(45, 45, 45))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.Highlight, QColor(0, 126, 194))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    palette.setColor(QPalette.Text, QColor(200, 200, 200))
    palette.setColor(QPalette.Button, QColor(60, 60, 60))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(255, 160, 0))

    qApp.setPalette(palette)
    splash_pixmap = QPixmap(os.path.join(os.path.dirname(os.path.realpath(__file__)), "ui", "icons", "splashscreen.png"))
    splash_screen = QSplashScreen(splash_pixmap)
    splash_screen.show()

    qApp.processEvents()

    window = tangle_window.TangleWindow()

    # tangle_window.showMaximized()
    window.show()
    splash_screen.finish(window)

    qApp.exec_()

if __name__ == "__main__":
    main()