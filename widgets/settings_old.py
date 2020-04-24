import sys
import inspect

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from ez_settings.ez_settings import EasySettingsSingleton as settings
import core.SettingsConstants as SettingsConstants

WIDGET_DICT = {
    "chk": QCheckBox,
    "txt": QLineEdit,
    "cb": QComboBox
}

class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.build_ui()
        self.show()
        pass

    def get_settings_from_class(self):
        settings_dict = {}

        for _, obj in inspect.getmembers(SettingsConstants):
            if inspect.isclass(obj):
                settings_dict[obj.__name__] = [attr for attr in inspect.getmembers(obj) if not attr[0].startswith("__") and not attr[0].endswith("__")]

        return settings_dict
    def camel_casing_to_space(self, string, capitalize=True):
        if capitalize:
            return string.replace("_", " ").capitalize()
        else:
            return string.replace("_", " ")

    def make_settings_widget(self, settings_tuple):
        prefix = settings_tuple[1].split("_")[0]
        name = settings_tuple[0]
        widget = WIDGET_DICT.get(prefix, None)()

        if type(widget) == QCheckBox:
            widget.setText(self.camel_casing_to_space(name))

        return widget

    def build_ui(self):
        main_layout = QVBoxLayout()

        for category, settings_tuple_list in self.get_settings_from_class().items():
            groupbox = QGroupBox(self.camel_casing_to_space(category.replace("Strings", "")))
            groupbox_layout = QVBoxLayout()
            groupbox.setLayout(groupbox_layout)
            if len(settings_tuple_list) > 0:
                widget = self.make_settings_widget(settings_tuple_list[0])
                groupbox_layout.addWidget(widget)

            main_layout.addWidget(groupbox)

        self.setLayout(main_layout)


