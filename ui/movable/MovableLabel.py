
from PySide6.QtGui import QFont, Qt, QColor
from PySide6.QtWidgets import QLabel


class MovableLabel(QLabel):
    def __init__(self, text="", parent=None, thickness=1):
        super().__init__(text, parent)
        self.thickness = thickness
        self.setFont(QFont('Arial', 28))
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

    # Overriding the mousePressEvent to allow dragging
    def mousePressEvent(self, event):
        pass

    def getFontSize(self):
        return self.font().pointSize()

    def getThickness(self):
        return self.thickness

    def getColor(self):
        style_sheet = self.styleSheet()
        color_name = style_sheet.split("color: ")[1].split(";")[0].strip()
        return QColor(color_name)
