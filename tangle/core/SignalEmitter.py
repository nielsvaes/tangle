from PySide2.QtCore import *

class SignalEmitter(QObject):
    signal = Signal()
    def __init__(self):
        super(SignalEmitter, self).__init__()

    def fire(self, *args):
        print(args)
        self.signal.emit()

