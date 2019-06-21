import skimage
from skimage import io
from skimage import filters
from skimage import img_as_ubyte
import numpy as np

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import numpy as np


def skimage_to_qpixmap(skimage_array):
    skimage_array = skimage.img_as_ubyte(io.imread(r"D:\Google Drive\Tools\CocoEdit\its-a-me_4.jpg"))

    height = skimage_array.shape[0]
    width = skimage_array.shape[1]

    if len(skimage_array.shape) == 3:
        qimage_format = QImage.Format_RGB888
    else:
        qimage_format = QImage.Format_Indexed8

    img = QImage(skimage_array.data, width, height, skimage_array.strides[0], qimage_format)
    pixmap = QPixmap.fromImage(img)

    return pixmap


def qpixmap_to_skimage(qpixmap):
    qimage = QImage(qpixmap)

    if qimage.hasAlphaChannel():
        channel_count = 4
    else:
        channel_count = 3

    width = qimage.width()
    height = qimage.height()

    string = qimage.bits().asstring(width * height * channel_count)

    shape = (height, width, channel_count)
    skim = np.fromstring(string, dtype=np.uint8).reshape(shape)

    return skim