from nodes.image_node import ImageNode
from core import socket_types as socket_types

from core.Constants import Colors

from PIL import ImageQt, ImageEnhance


class Desaturation(ImageNode):
    def __init__(self, scene, x=0, y=0):
        super().__init__(scene, title_background_color=Colors.saturation, x=x, y=y)
        self.change_title("desaturation")

        self.input_image, self.output_image = self.add_input_output(socket_types.PictureSocketType(self), "image")

        self.add_label("Desaturation amount")
        self.sld_contrast_amount = self.add_slider(0, 100, 100, changed_function=self.slider_changed, released_function=self.slider_released)


    def slider_changed(self):
        self.compute(compute_next=False)
        self.set_dirty(True)

    def slider_released(self):
        super().compute()

    def compute(self, compute_next=True, force=False):
        if self.input_image.is_connected():
            self.input_image.fetch_connected_value()

            factor = self.sld_contrast_amount.value()

            saturated = ImageEnhance.Color(self.input_image.get_value()).enhance(factor / 100)

            self.output_image.set_value(saturated)

            contrasted_pixmap = ImageQt.toqpixmap(saturated)
            self.set_pixmap(contrasted_pixmap)
            self.refresh()
            if compute_next:
                super().compute(force=force)
            self.set_dirty(False)
