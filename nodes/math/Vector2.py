from nodes.base_node import BaseNode
from core import socket_types as socket_types

from core.Constants import Colors


class Vector2(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super().__init__(scene, title_background_color=Colors.vector2, x=x, y=y)

        self.output_vector = self.add_output(socket_types.Vector2SocketType(self), "vec2")
        self.output_x = self.add_output(socket_types.FloatSocketType(self), "x")
        self.output_y = self.add_output(socket_types.FloatSocketType(self), "y")
        _, self.txt_x = self.add_label_float("x: ", number_changed_function=self.number_changed)
        _, self.txt_y = self.add_label_float("y: ", number_changed_function=self.number_changed)

        initial_value = [0.0, 0.0]
        self.output_vector.set_initial_value(initial_value)
        self.change_title(str(self.output_vector.get_value()))


    def number_changed(self):
        for txt in [self.txt_x, self.txt_y]:
            if txt.text() == "":
                txt.setText("0.0")

        x_value = float(self.txt_x.text())
        y_value = float(self.txt_y.text())

        try:
            print("setting vector value")
            self.output_vector.set_value([x_value, y_value])
            self.output_x.set_value(x_value)
            self.output_y.set_value(y_value)
            print("the value is %s" % self.output_vector.get_value())
        except ValueError as err:
            self.output_vector.set_value([0.0, 0.0])

        self.compute()



    def compute(self):
        self.change_title("[%s, %s]" % (self.txt_x.text(), self.txt_y.text()))
        super().compute()
        self.set_dirty(False)

