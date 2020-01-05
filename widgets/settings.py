import sys
import inspect

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from ez_settings.ez_settings import EasySettings
import core.SettingsConstants as SettingsConstants

class SettingsWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        pass

    def get_categories(self):
        for _, obj in inspect.getmembers(SettingsConstants):
            if inspect.isclass(obj):
                yield obj.__name__

    def camel_casing_to_space(self, string, capitalize=True):
        if capitalize:
            return string.replace("_", " ").capitalize()
        else:
            return string.replace("_", " ")

    def build_ui(self):
        main_layout = QVBoxLayout()

        for category in self.get_categories():
            group_box = QGroupBox(self.camel_casing_to_space(category.replace("Strings", "")))

            main_layout.addWidget(group_box)

        self.setLayout(main_layout)


