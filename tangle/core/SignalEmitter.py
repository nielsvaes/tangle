from PySide2.QtCore import *

class SignalEmitter(QObject):
    signal = Signal()
    def __init__(self):
        super(SignalEmitter, self).__init__()

    def emit(self):
        self.signal.emit()

