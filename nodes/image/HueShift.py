from nodes.image_node import ImageNode
from core import socket_types as socket_types

from core.Constants import Colors
from PIL import ImageQt, Image

import numpy as np

import nv_utils.utils as utils

class HueShift(ImageNode):
    def __init__(self, scene, x=0, y=0):
        super().__init__(scene, title_background_color=Colors.blur, x=x, y=y)
        self.change_title("hue")

        self.input_image, self.output_image = self.add_input_output(socket_types.PictureSocketType(self), "image")

        self.sld_hue_value = self.add_slider(0, 360, 0, changed_function=self.slider_changed, released_function=self.slider_released)


    def slider_changed(self):
        self.compute(compute_next=False)
        self.set_dirty(True)

    def slider_released(self):
        super().compute()

    def hue_shift(self, image, amount):
        # https://stackoverflow.com/questions/35417927/how-to-change-the-hsv-values-of-an-image-in-python
        original_mode = image.mode
        hsv_img = image.convert('HSV')
        hsv = np.array(hsv_img)
        hsv[..., 0] = (hsv[..., 0] + amount) % 360
        new_img = Image.fromarray(hsv, 'HSV')
        return new_img.convert(original_mode)


    def compute(self, compute_next=True):
        try:
            if self.input_image.is_connected():
                self.input_image.fetch_connected_value()

                colorized_image = self.hue_shift(self.input_image.get_value(), self.sld_hue_value.value())
                self.output_image.set_value(colorized_image)

                colorized_pixmap = ImageQt.toqpixmap(colorized_image)
                self.set_pixmap(colorized_pixmap)
                self.refresh()
                if compute_next:
                    super().compute()
                self.set_dirty(False)
        except Exception as err:
            utils.trace(err)

    def save(self):
        node_dict = super().save()
        node_dict["sld_hue_value"] = self.sld_hue_value.value()

        return node_dict

    def load(self, node_dict, x=None, y=None):
        super().load(node_dict, x=x, y=y)
        self.sld_hue_value.setValue(node_dict.get("sld_hue_value"))







