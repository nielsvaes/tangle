import os
import sys
from functools import partial
import logging
logging.basicConfig(level=logging.INFO)

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

try:
    import qtmodern.styles
    import qtmodern.windows
    modern = True
except:
    logging.warning("Can't find qtmodern!")
    modern = False

from ez_settings.ez_settings import EasySettingsSingleton as ez_settings

SCRIPT_FOLDER = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
UI_PATH = os.path.join(SCRIPT_FOLDER, "ui")
ICONS_PATH = os.path.join(SCRIPT_FOLDER, "ui", "icons")

class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()

        uic.loadUi(os.path.join(UI_PATH, "tangle_settings.ui"), self)
        self.setWindowTitle("Tangle")
        self.setWindowIcon(QIcon(os.path.join(ICONS_PATH, "logo.png")))

        self.connect_ui_elements()
        self.load_settings()
        self.show()


    def connect_ui_elements(self):
        self.btn_save.clicked.connect(self.save_settings)

    def load_checkboxes(self):
        for checkbox in self.findChildren(QCheckBox):
            if ez_settings().setting_exists(checkbox.objectName()):
                checkbox.setChecked(ez_settings().get_value(checkbox.objectName()))

    def save_checkboxes(self):
        for checkbox in self.findChildren(QCheckBox):
            ez_settings().set_value(checkbox.objectName(), checkbox.isChecked())

    def load_settings(self):
        self.load_checkboxes()

    def save_settings(self):
        self.save_checkboxes()

        self.accept()