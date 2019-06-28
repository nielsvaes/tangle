from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import itertools
import operator

import sys
import traceback

import logging
logging.basicConfig(level=logging.DEBUG)

from nodes.base_node import BaseNode
import socket_types as socket_types
from core.Constants import Colors

import PIL
from PIL import Image, ImageQt, ImageOps, ImageEnhance, ImageFilter, ImageDraw

class CombineChannels(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super(CombineChannels, self).__init__(scene, x=x, y=y)
        self.change_title("rgb_2_l")

        self.input_r = self.add_input(socket_types.PictureSocketType(self), "in R")
        self.input_g = self.add_input(socket_types.PictureSocketType(self), "in G")
        self.input_b = self.add_input(socket_types.PictureSocketType(self), "in B")
        self.input_a = self.add_input(socket_types.PictureSocketType(self), "in A")

        self.output_image = self.add_output(socket_types.PictureSocketType(self), "RGB")

        self.input_r.override_color(Colors.red)
        self.input_g.override_color(Colors.green)
        self.input_b.override_color(Colors.blue)
        self.input_a.override_color(Colors.gray)

        self.chk_rgba = self.add_checkbox("Output is RGBA image", checked=False)
        self.black_image = Image.new("L", (100, 100))

        self.set_auto_compute_on_connect(True)

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
            print("computing combine")
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
                logging.error(err)
                _, _, tb = sys.exc_info()
                logging.error(traceback.format_list(traceback.extract_tb(tb)[-1:])[-1])

                if self.chk_rgba.isChecked():
                    combined_image = Image.merge("RGBA", [self.black_image, self.black_image, self.black_image, self.black_image])
                else:
                    combined_image = Image.merge("RGB", [self.black_image, self.black_image, self.black_image])


            self.output_image.set_value(combined_image)
            self.set_pixmap(ImageQt.toqpixmap(combined_image))
            self.set_dirty(False)


