import logging
import os

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtUiTools import *

try:
    import qtmodern.styles
    import qtmodern.windows
    modern = True
except:
    logging.warning("Can't find qtmodern!")
    modern = False

from tangle import tangle_window

def main():
    if modern:
        qtmodern.styles.dark(qApp)

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