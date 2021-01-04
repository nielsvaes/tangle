from ..image_node import ImageNode
from ...core import socket_types as socket_types

import logging
logging.basicConfig(level=logging.INFO)

from ...core.Constants import Colors
from PIL import Image, ImageQt


class Shrink(ImageNode):
    def __init__(self, scene, x=0, y=0):
        super(Shrink, self).__init__(scene, title_background_color=Colors.shrink, x=x, y=y)
        self.change_title("shrink")

        self.input_image, self.output_image = self.add_input_output(socket_types.PictureSocketType(self), "image")
        # self.output_image = self.add_output(socket_types.PictureSocketType(self), "out")
        self.size = self.add_output(socket_types.TupleSocketType(self), "size")

        percentage_list = ["0", "25", "50", "75"]

        self.cb_percentage = self.add_label_combobox("Reduce by %", percentage_list, changed_function=self.value_changed)

    def value_changed(self):
        self.set_dirty(True)
        self.compute()

    def compute(self, force=False):
        if self.input_image.is_connected():
            self.input_image.fetch_connected_value()

            width, height = self.input_image.get_value().size

            new_width = int((width * (100 - int(self.cb_percentage.currentText()))) / 100)
            new_height = int((height * (100 - int(self.cb_percentage.currentText()))) / 100)

            resized = self.input_image.get_value().resize((new_width, new_height), Image.ANTIALIAS)
            self.output_image.set_value(resized)

            resized_pixmap = ImageQt.toqpixmap(resized)
            self.set_pixmap(resized_pixmap)

            self.size.set_value(resized.size)
            super().compute(force=force)
            self.set_dirty(False)