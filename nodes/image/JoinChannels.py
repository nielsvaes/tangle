import itertools
import operator

import logging
logging.basicConfig(level=logging.DEBUG)

from nodes.image_node import ImageNode
from nodes.image.LoadImage import LoadImage
from core import socket_types as socket_types
from core.Constants import Colors

import nv_utils.utils as utils

from PIL import Image, ImageQt


class JoinChannels(ImageNode):
    def __init__(self, scene, x=0, y=0):
        super(JoinChannels, self).__init__(scene, title_background_color=Colors.combine_channel, x=x, y=y)
        self.change_title("join")

        self.input_r = self.add_input(socket_types.PictureSocketType(self), "in R")
        self.input_g = self.add_input(socket_types.PictureSocketType(self), "in G")
        self.input_b = self.add_input(socket_types.PictureSocketType(self), "in B")
        self.input_a = self.add_input(socket_types.PictureSocketType(self), "in A")

        self.output_image = self.add_output(socket_types.PictureSocketType(self), "out")

        self.input_r.override_color(Colors.red)
        self.input_r.adjust_color_to_input = False
        self.input_g.override_color(Colors.green)
        self.input_g.adjust_color_to_input = False
        self.input_b.override_color(Colors.blue)
        self.input_b.adjust_color_to_input = False
        self.input_a.override_color(Colors.gray)
        self.input_a.adjust_color_to_input = False

        self.chk_rgba = self.add_checkbox("Output is RGBA image", checked=False)
        self.black_image = Image.new("L", (100, 100))

        self.set_auto_compute_on_connect(True)

    def get_input_image_size(self):
        self.get_input_nodes_of_type(LoadImage)


    def get_most_common_size(self, image_list):
        sizes = []
        for image in image_list:
            if image is not None:
                sizes.append(image.size)

        # http://stackoverflow.com/questions/1518522/python-most-common-element-in-a-list
        # get an iterable of (item, iterable) pairs
        SL = sorted((x, i) for i, x in enumerate(sizes))
        # print 'SL:', SL
        groups = itertools.groupby(SL, key=operator.itemgetter(0))
        # auxiliary function to get "quality" for an item
        def _auxfun(g):
            item, iterable = g
            count = 0
            min_index = len(sizes)
            for _, where in iterable:
                count += 1
                min_index = min(min_index, where)
            # print 'item %r, count %r, minind %r' % (item, count, min_index)
            return count, -min_index

        # pick the highest-count/earliest item
        return max(groups, key=_auxfun)[0]


    def compute(self):
        if self.input_r.is_connected() or self.input_r.is_connected() or self.input_r.is_connected() or self.input_r.is_connected():

            print("there's a connected input")

            self.input_r.fetch_connected_value()
            self.input_g.fetch_connected_value()
            self.input_b.fetch_connected_value()
            self.input_a.fetch_connected_value()

            channels = [self.input_r.get_value(), self.input_g.get_value(), self.input_b.get_value(),
                        self.input_a.get_value()]

            checked_channels = []

            for channel in channels:
                if channel is None:
                    channel = self.black_image.resize(self.get_most_common_size(channels))

                checked_channels.append(channel)

            try:
                if self.chk_rgba.isChecked():
                    combined_image = Image.merge("RGBA", checked_channels)
                else:
                    combined_image = Image.merge("RGB", checked_channels[:-1])
            except ValueError as err:
                utils.trace(err)
                logging.error("R: ", self.input_r.get_value().size)
                logging.error("G: ", self.input_g.get_value().size)
                logging.error("B: ", self.input_b.get_value().size)
                logging.error("A: ", self.input_a.get_value().size)

                if self.chk_rgba.isChecked():
                    combined_image = Image.merge("RGBA", [self.black_image, self.black_image, self.black_image, self.black_image])
                else:
                    combined_image = Image.merge("RGB", [self.black_image, self.black_image, self.black_image])

            self.output_image.set_value(combined_image)
            self.set_pixmap(ImageQt.toqpixmap(combined_image))
            self.set_dirty(False)


