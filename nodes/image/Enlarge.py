from nodes.image_node import ImageNode
from core import socket_types as socket_types

import logging
logging.basicConfig(level=logging.INFO)


from core.Constants import Colors
from PIL import Image, ImageQt


class Enlarge(ImageNode):
    def __init__(self, scene, x=0, y=0):
        super(Enlarge, self).__init__(scene, title_background_color=Colors.enlarge, x=x, y=y)
        self.change_title("enlarge")

        self.input_image, self.output_image = self.add_input_output(socket_types.PictureSocketType(self), "in")
        self.size = self.add_output(socket_types.TupleSocketType(self), "size")

        percentage_list = ["25", "50", "75", "100"]

        self.cb_percentage = self.add_label_combobox("Increase by %", percentage_list, changed_function=self.value_changed)

    def value_changed(self):
        self.set_dirty(True)
        super().compute(force=force)

    def compute(self, force=False):
        if self.input_image.is_connected():
            self.input_image.fetch_connected_value()

            width, height = self.input_image.get_value().size

            new_width = int((width * (int(self.cb_percentage.currentText()) + 100)) / 100)
            new_height = int((height * (int(self.cb_percentage.currentText()) + 100)) / 100)

            resized = self.input_image.get_value().resize((new_width, new_height), Image.ANTIALIAS)
            self.output_image.set_value(resized)

            resized_pixmap = ImageQt.toqpixmap(resized)
            self.set_pixmap(resized_pixmap)

            self.size.set_value(resized.size)
            super().compute(force=force)
            self.set_dirty(False)