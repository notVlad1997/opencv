from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QSlider, QLabel, QHBoxLayout, QColorDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from ui.movable.MovableLabel import MovableLabel
from ui.movable.MovableProxyWidget import MovableProxyWidget


class TextInputDialog(QWidget):
    def __init__(self, scenes, currentIndex):
        """
        Initializes a TextInputDialog that will be placed in the provided scene.
        """
        super().__init__()
        self.proxyWidget = None
        self.scenes = scenes
        self.currentIndex = currentIndex

        self.textInput = QLineEdit()
        self.textInput.setPlaceholderText("Enter text here")

        self.sizeSlider = QSlider(Qt.Orientation.Horizontal)
        self.sizeSlider.setMinimum(10)
        self.sizeSlider.setMaximum(72)
        self.sizeSlider.setValue(14)
        self.sizeDisplay = QLineEdit()
        self.sizeDisplay.setReadOnly(True)
        self.sizeDisplay.setText(str(self.sizeSlider.value()))

        self.sizeSlider.valueChanged.connect(self.updateSizeDisplay)

        self.thicknessSlider = QSlider(Qt.Orientation.Horizontal)
        self.thicknessSlider.setMinimum(1)
        self.thicknessSlider.setMaximum(10)
        self.thicknessSlider.setValue(1)
        self.thicknessDisplay = QLineEdit()
        self.thicknessDisplay.setReadOnly(True)
        self.thicknessDisplay.setText(str(self.thicknessSlider.value()))

        self.thicknessSlider.valueChanged.connect(self.updateThicknessDisplay)

        self.colorDisplay = QLineEdit()
        self.colorDisplay.setReadOnly(True)
        self.colorDisplay.setPlaceholderText("Select color")
        self.selectedColor = QColor(255, 255, 255)
        self.updateColorDisplay()

        self.colorButton = QPushButton("Choose Color")

        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")

        inputWidget = QWidget()
        layout = QVBoxLayout(inputWidget)
        layout.addWidget(self.textInput)

        sizeLayout = QHBoxLayout()
        sizeLayout.addWidget(QLabel("Font Size:"))
        sizeLayout.addWidget(self.sizeSlider)
        sizeLayout.addWidget(self.sizeDisplay)
        layout.addLayout(sizeLayout)

        thicknessLayout = QHBoxLayout()
        thicknessLayout.addWidget(QLabel("Thickness:"))
        thicknessLayout.addWidget(self.thicknessSlider)
        thicknessLayout.addWidget(self.thicknessDisplay)
        layout.addLayout(thicknessLayout)

        colorLayout = QHBoxLayout()
        colorLayout.addWidget(QLabel("Text Color:"))
        colorLayout.addWidget(self.colorButton)
        colorLayout.addWidget(self.colorDisplay)
        layout.addLayout(colorLayout)

        layout.addWidget(okButton)
        layout.addWidget(cancelButton)
        self.setLayout(layout)

        okButton.clicked.connect(self.onOkClicked)
        cancelButton.clicked.connect(self.onCancelClicked)
        self.colorButton.clicked.connect(self.onColorButtonClicked)

    def updateSizeDisplay(self, value):
        self.sizeDisplay.setText(str(value))

    def updateThicknessDisplay(self, value):
        self.thicknessDisplay.setText(str(value))

    def updateColorDisplay(self):
        color_name = self.selectedColor.name()
        self.colorDisplay.setText(f"{color_name}")

    def onOkClicked(self):
        input_text = self.textInput.text()
        if input_text:
            label = MovableLabel(input_text, thickness=self.thicknessDisplay.text())
            font_size = self.sizeSlider.value()
            font = label.font()
            font.setPointSize(font_size)
            label.setFont(font)
            label.setStyleSheet(f"color: {self.selectedColor.name()}")

            pos = self.proxyWidget.pos()
            self.scenes[self.currentIndex].removeItem(self.proxyWidget)
            label_proxy_widget = MovableProxyWidget(label)
            self.scenes[self.currentIndex].addItem(label_proxy_widget)
            label_proxy_widget.setPos(pos)

    def onCancelClicked(self):
        self.scenes[self.currentIndex].removeItem(self.proxyWidget)

    def onColorButtonClicked(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.selectedColor = color
            self.updateColorDisplay()

    def setProxyWidget(self, proxyWidget):
        self.proxyWidget = proxyWidget
