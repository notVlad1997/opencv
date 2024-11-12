import cv2
import numpy as np
from PySide6.QtGui import QImage, QPixmap, QColor


def convertCvToQimage(cv2Image):
    """  Converts a QImage into an opencv MAT format  """
    imageRGB = cv2.cvtColor(cv2Image, cv2.COLOR_BGR2RGB)
    height, width, channel = imageRGB.shape
    qImage = QImage(imageRGB.data, width, height, channel * width, QImage.Format.Format_RGB888)
    return qImage

def convertQimageToCv(qImage):
    """  Converts a QImage into an opencv MAT format  """
    incomingImage = qImage.convertToFormat(QImage.Format.Format_RGBA8888)

    width = incomingImage.width()
    height = incomingImage.height()

    ptr = incomingImage.bits()

    arr = np.array(ptr).reshape(height, width, 4)  #  Copies the data
    arr = arr[..., [2, 1, 0, 3]]  # Rearranging to BGRA
    return arr

def convertArrayToPixmap(array):
    """Convert a NumPy array (with shape [height, width, channels]) to QPixmap."""
    # Ensure array is in the right format
    if array.shape[2] == 4:
        array = cv2.cvtColor(array, cv2.COLOR_BGRA2RGBA)  # Convert from BGRA to RGBA
    else:
        array = cv2.cvtColor(array, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB

    height, width, channel = array.shape
    bytesPerLine = 4 * width
    qimage = QImage(array.data, width, height, bytesPerLine, QImage.Format.Format_RGBA8888)
    return QPixmap.fromImage(qimage)

def convertQPixmapToCvImage(pixmap):
    """Convert QPixmap to an OpenCV image."""
    qImage = pixmap.toImage()
    qImageBits = qImage.bits()
    img = np.array(qImageBits, dtype=np.uint8).reshape((qImage.height(), qImage.width(), 4))
    return cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

def convertQColorRGBtoScalarBGR(color):
    bgrColor = (255,255,255)
    if isinstance(color, QColor):
        r, g, b, _ = color.getRgb()
        bgrColor = (b, g, r)
        bgrColor = tuple(int(c) for c in bgrColor)

    return bgrColor

def convertQtFontSizeToCv2FontScale(qtFontSize):
    return qtFontSize / 24.0
