from PySide2.QtCore import *
from PySide2.QtUiTools import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class StyleSheets:
    normal = "background-color: rgb(76, 76, 76); border-radius: 10px; padding: 10px"
    error = "background-color: rgb(200, 76, 76); border-radius: 10px; padding: 10px"
    success = "background-color: rgb(76, 150, 76); border-radius: 10px; padding: 10px"
    warning = "background-color: rgb(191, 176, 59); border-radius: 10px; padding: 10px; color: rgb(0, 0, 0);"

class InfoLabel(QLabel):
    def __init__(self, text, fade_time=500, stay_time=2000):
        super().__init__(text)
        self.__fade_time = fade_time
        self.__fade_effect = QGraphicsOpacityEffect()
        self.__animation = QPropertyAnimation(self.__fade_effect, QByteArray(b"opacity"))
        self.__animation.setDuration(self.__fade_time)

        self.__stay_time = fade_time + stay_time

        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__fade_out)
        self.__time_has_finished = True

        self.setGraphicsEffect(self.__fade_effect)

    def info(self, text):
        self.setStyleSheet(StyleSheets.normal)
        self.setText(text)
        self.__fade_in()

    def error(self, text):
        self.setStyleSheet(StyleSheets.error)
        self.setText(text)
        self.__fade_in()

    def success(self, text):
        self.setStyleSheet(StyleSheets.success)
        self.setText(text)
        self.__fade_in()

    def warning(self, text):
        self.setStyleSheet(StyleSheets.warning)
        self.setText(text)
        self.__fade_in()

    def __fade_in(self):
        self.__animation.setStartValue(0.0)
        self.__animation.setEndValue(1.0)
        self.__animation.setEasingCurve(QEasingCurve.Linear)
        self.__animation.start()

        self.__timer.start(self.__stay_time)

    def __fade_out(self):
        self.__animation.setStartValue(1.0)
        self.__animation.setEndValue(0.0)
        self.__animation.setEasingCurve(QEasingCurve.Linear)
        self.__animation.start()
        self.__timer.stop()



