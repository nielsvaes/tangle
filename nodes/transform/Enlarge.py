from nodes.image_node import ImageNode
import socket_types as socket_types

import logging
logging.basicConfig(level=logging.INFO)


from core.Constants import Colors
from PIL import Image, ImageQt, ImageOps, ImageEnhance, ImageFilter

class Enlarge(ImageNode):
    def __init__(self, scene, x=0, y=0):
        super(Enlarge, self).__init__(scene, title_background_color=Colors.enlarge, x=x, y=y)
        self.change_title("resize")

        self.input_image = self.add_input(socket_types.PictureSocketType(self), "in")
        self.output_image = self.add_output(socket_types.PictureSocketType(self), "out")

        percentage_list = ["25", "50", "75", "100"]

        self.cb_percentage = self.add_label_combobox("Increase by %", percentage_list, changed_function=self.value_changed)

    def value_changed(self):
        self.set_dirty(True)
        self.scene.refresh_network()

    def compute(self):
        if self.input_image.is_connected():
            self.input_image.fetch_connected_value()

            width, height = self.input_image.get_value().size

            new_width = int((width * (int(self.cb_percentage.currentText()) + 100)) / 100)
            new_height = int((height * (int(self.cb_percentage.currentText()) + 100)) / 100)

            resized = self.input_image.get_value().resize((new_width, new_height), Image.ANTIALIAS)
            self.output_image.set_value(resized)

            print(resized.size)

            resized_pixmap = ImageQt.toqpixmap(resized)
            self.set_pixmap(resized_pixmap)

            self.set_dirty(False)