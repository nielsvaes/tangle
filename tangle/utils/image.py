import skimage
from skimage import io
from skimage import filters
from skimage import img_as_ubyte
import numpy as np

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *



def skimage_as_float(image):
    return skimage.img_as_float(image)

def skimage_as_ubyte(image):
    return skimage.img_as_ubyte(image)

def skimage_to_qpixmap(im):
    # image = img_as_ubyte(im, force_copy=True)
    image = im
    height = image.shape[0]
    width = image.shape[1]

    if len(image.shape) == 3:
        qimage_format = QImage.Format_RGB888
    else:
        qimage_format = QImage.Format_Indexed8

    img = QImage(image.data, width, height, image.strides[0], qimage_format)
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
    skimg = np.fromstring(string, dtype=np.uint8).reshape(shape)

    return skimg

def blur(image, amount=10):
    return filters.gaussian(image, sigma=amount, multichannel=True)

