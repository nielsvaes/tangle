from nodes.base_node import BaseNode
import socket_types as socket_types

import logging
logging.basicConfig(level=logging.INFO)


import PIL
from PIL import Image, ImageQt, ImageOps, ImageEnhance, ImageFilter

class SizeIncrease(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super(SizeIncrease, self).__init__(scene, x=x, y=y)
        self.change_title("resize")

        self.input_image = self.add_input(socket_types.PictureSocketType(self), "in")
        self.output_image = self.add_output(socket_types.PictureSocketType(self), "out")

        percentage_list = ["25", "50", "75", "100"]

        # for i in range(1, 99):
        #     percentage_list.append(str(i))

        self.cb_percentage = self.add_label_combobox("Increase by %", percentage_list, changed_function=self.value_changed)


    # def get_ui(self):
    #     if self.input_image.is_connected() and not self.has_been_changed:
    #         try:
    #             super(Resize, self).get_ui()
    #             width, height = self.input_image.get_value().size
    #             self.txt_width.setText(width)
    #             self.txt_height.setText(height)
    #         except AttributeError as err:
    #             logging.warning("Input connection doesn't have a pixmap assigned!")
    #     else:
    #         super(Resize, self).get_ui()


    def value_changed(self):
        self.set_dirty(True)

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