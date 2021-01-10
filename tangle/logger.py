import os
import datetime

class Status:
    SUCCESS = "success"
    WARNING = "warning"
    INFO    = "info"
    ERROR   = "error"
    DEBUG   = "debug"


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(object, metaclass=Singleton):
    def __init__(self, info_label, file_path=None):
        super(Logger, self).__init__()

        self.__info_label = info_label
        self.file_path = file_path if file_path is not None else os.path.join(os.path.expanduser("~"), "tangle.log")

        self.debug("\n\n====================== NEW LOG ======================", show_in_info_label=False)

    def success(self, message, show_in_info_label=True):
        self.__add_to_log(Status.SUCCESS, message, show_in_info_label)

    def warning(self, message, show_in_info_label=True):
        self.__add_to_log(Status.WARNING, message, show_in_info_label)

    def info(self, message, show_in_info_label=True):
        self.__add_to_log(Status.INFO, message, show_in_info_label)

    def error(self, message, show_in_info_label=True):
        self.__add_to_log(Status.ERROR, message, show_in_info_label)

    def debug(self, message, show_in_info_label=True):
        self.__add_to_log(Status.DEBUG, message, show_in_info_label)

    def __add_to_log(self, status, message, show_in_info_label):
        time = datetime.datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
        line = "[%s] | %s | %s" % (time, status, message)

        with open(self.file_path, "a") as out_file:
            out_file.write(line + "\n")

        if show_in_info_label:
            self.__info_label.show_message(status, message)

