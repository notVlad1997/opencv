from PySide6.QtCore import QRectF
from PySide6.QtGui import QColor, Qt, QPen
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsScene


class SceneWithSizeArea(QGraphicsScene):
    def __init__(self, parent=None, width=800, height=600):
        super().__init__(parent)
        self.width = width
        self.height = height

        self.sizeArea = QGraphicsRectItem(QRectF(0, 0, self.width, self.height))

        pen = QPen(QColor(255, 0, 0, 200), 2, Qt.PenStyle.SolidLine)  # Red border
        self.sizeArea.setPen(pen)

        self.addItem(self.sizeArea)
