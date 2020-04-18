from nodes.image_node import ImageNode
from core import socket_types as socket_types

from core.Constants import Colors
from PIL import ImageQt, ImageFilter

from nv_utils.decorators import timeit

class Blur(ImageNode):
    def __init__(self, scene, x=0, y=0):
        super(Blur, self).__init__(scene, title_background_color=Colors.blur, x=x, y=y)
        self.change_title("blur")

        self.input_image, self.output_image = self.add_input_output(socket_types.PictureSocketType(self), "image")

        self.sld_blur_amount = self.add_slider(0, 50, 0, changed_function=self.slider_changed, released_function=self.slider_released)

    def slider_changed(self):
        self.compute(compute_next=False)
        self.set_dirty(True)

    def slider_released(self):
        super().compute(force=force)

    @timeit
    def compute(self, compute_next=True):
        if self.input_image.is_connected():
            self.input_image.fetch_connected_value()

            blurred = self.input_image.get_value().filter(ImageFilter.GaussianBlur(radius=self.sld_blur_amount.value()))
            self.output_image.set_value(blurred)

            blurred_pixmap = ImageQt.toqpixmap(blurred)
            self.set_pixmap(blurred_pixmap)
            self.refresh()
            if compute_next:
                super().compute(force=force)
            self.set_dirty(False)
