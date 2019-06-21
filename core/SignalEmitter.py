from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class SignalEmitter(QObject):
    signal = pyqtSignal()
    def __init__(self):

        super(SignalEmitter, self).__init__()

