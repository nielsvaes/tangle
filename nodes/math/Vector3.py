from nodes.base_node import BaseNode
from core import socket_types as socket_types

from core.Constants import Colors


class Vector3(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super(Vector3, self).__init__(scene, title_background_color=Colors.vector3, x=x, y=y)
        self.change_title("[0.0, 0.0, 0.0]")

        self.output_vector = self.add_output(socket_types.ListSocketType(self), "vec3")
        self.output_x = self.add_output(socket_types.FloatSocketType(self), "x")
        self.output_y = self.add_output(socket_types.FloatSocketType(self), "y")
        self.output_z = self.add_output(socket_types.FloatSocketType(self), "z")
        _, self.txt_x = self.add_label_float("x: ", number_changed_function=self.number_changed)
        _, self.txt_y = self.add_label_float("y: ", number_changed_function=self.number_changed)
        _, self.txt_z = self.add_label_float("z: ", number_changed_function=self.number_changed)

    def number_changed(self):
        for txt in [self.txt_x, self.txt_y, self.txt_z]:
            if txt.text() == "":
                txt.setText("0.0")

        try:
            self.output_vector.set_value([float(self.txt_x.text()), float(self.txt_y.text()), float(self.txt_z.text())])
            self.output_x.set_value(float(self.txt_x.text()))
            self.output_y.set_value(float(self.txt_y.text()))
            self.output_z.set_value(float(self.txt_z.text()))
        except ValueError as err:
            self.output_vector.set_value([0.0, 0.0, 0.0])

        self.compute_connected_nodes()

        self.set_dirty(True)
        self.compute()

    def compute(self):
        if self.is_dirty():
            self.change_title("[%s, %s, %s]" % (self.txt_x.text(), self.txt_y.text(), self.txt_z.text()))
            self.set_dirty(False)

