import os
import logging
logging.basicConfig(level=logging.INFO)

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from ez_settings.ez_settings import EZSettings as settings
from ..core.Constants import sc
from ..ui import about_ui

SCRIPT_FOLDER = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
UI_PATH = os.path.join(SCRIPT_FOLDER, "ui")
ICONS_PATH = os.path.join(SCRIPT_FOLDER, "ui", "icons")

class AboutDialog(QDialog, about_ui.Ui_tangle_about):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join(ICONS_PATH, "logo.png")))
        self.lbl_logo.setPixmap(QPixmap(os.path.join(ICONS_PATH, "logo.png")).scaled(self.lbl_logo.height(), self.lbl_logo.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.lbl_version.setText(str(settings().get(sc.version, 0.00)))
        self.lbl_website.setText("<a href=http://www.nielsvaes.be>www.nielsvaes.be</a>")
        self.lbl_website.setOpenExternalLinks(True)
        self.show()
        self.btn_close.clicked.connect(self.close)
