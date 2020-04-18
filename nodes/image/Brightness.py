from nodes.image_node import ImageNode
from core import socket_types as socket_types

from core.Constants import Colors
from PIL import ImageQt, ImageEnhance


class Brightness(ImageNode):
    def __init__(self, scene, x=0, y=0):
        super(Brightness, self).__init__(scene, title_background_color=Colors.brightness, x=x, y=y)
        self.change_title("brightness")

        self.input_image, self.output_image = self.add_input_output(socket_types.PictureSocketType(self), "image")

        self.add_label("Brightness amount")
        self.sld_contrast_amount = self.add_slider(0, 400, 100, changed_function=self.slider_changed, released_function=self.slider_released)


    def slider_changed(self):
        self.compute(compute_next=False)
        self.set_dirty(True)

    def slider_released(self):
        super().compute(force=force)


    def compute(self, compute_next=True):
        if self.input_image.is_connected():
            self.input_image.fetch_connected_value()

            factor = self.sld_contrast_amount.value()

            brightened = ImageEnhance.Brightness(self.input_image.get_value()).enhance(factor / 100)

            self.output_image.set_value(brightened)

            contrasted_pixmap = ImageQt.toqpixmap(brightened)
            self.set_pixmap(contrasted_pixmap)
            self.refresh()
            if compute_next:
                super().compute(force=force)
            self.set_dirty(False)
