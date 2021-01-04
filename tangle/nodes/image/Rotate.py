from ..image_node import ImageNode
from ...core import socket_types as socket_types

from ...core.Constants import Colors
from PIL import ImageQt


class Rotate(ImageNode):
    def __init__(self, scene, x=0, y=0):
        super(Rotate, self).__init__(scene, title_background_color=Colors.rotate, x=x, y=y)
        self.change_title("rotate")

        self.input_image, self.output_image = self.add_input_output(socket_types.PictureSocketType(self), "image")

        self.chk_counter_clockwise = self.add_checkbox("Counter clockwise", change_checked_function=self.value_changed)
        self.cd_degrees = self.add_label_combobox("Rotate by degrees", ["90", "180", "270"],
                                                  changed_function=self.value_changed)
    def value_changed(self):
        self.set_dirty(True)
        self.compute()

    def compute(self, force=False):
        if self.input_image.is_connected():
            self.input_image.fetch_connected_value()

            rotated = self.input_image.get_value()

            degrees_to_rotate = int(self.cd_degrees.currentText())
            if not self.chk_counter_clockwise.isChecked():
                degrees_to_rotate = degrees_to_rotate * -1

            rotated = rotated.rotate(degrees_to_rotate, expand=True)

            self.output_image.set_value(rotated)

            rotated_pixmap = ImageQt.toqpixmap(rotated)
            self.set_pixmap(rotated_pixmap)
            self.refresh()
            super().compute(force=force)
            self.set_dirty(False)