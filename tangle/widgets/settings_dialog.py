import os
import logging
logging.basicConfig(level=logging.INFO)

from PySide2.QtWidgets import *
from PySide2.QtGui import *

from ez_settings import EZSettings
from ..ui import tangle_settings_ui

SCRIPT_FOLDER = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
UI_PATH = os.path.join(SCRIPT_FOLDER, "ui")
ICONS_PATH = os.path.join(SCRIPT_FOLDER, "ui", "icons")

class SettingsDialog(QDialog, tangle_settings_ui.Ui_tangle_settings):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("Tangle")
        self.setWindowIcon(QIcon(os.path.join(ICONS_PATH, "logo.png")))

        self.connect_ui_elements()
        self.load_settings()
        self.show()


    def connect_ui_elements(self):
        self.btn_save.clicked.connect(self.save_settings)

    def load_checkboxes(self):
        for checkbox in self.findChildren(QCheckBox):
            if EZSettings().exists(checkbox.objectName()):
                checkbox.setChecked(EZSettings().get(checkbox.objectName()))

    def save_checkboxes(self):
        for checkbox in self.findChildren(QCheckBox):
            EZSettings().set(checkbox.objectName(), checkbox.isChecked())

    def load_settings(self):
        self.load_checkboxes()

    def save_settings(self):
        self.save_checkboxes()

        self.accept()