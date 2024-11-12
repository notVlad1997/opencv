from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPixmap, QPen, QMouseEvent
from PySide6.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QCheckBox, QSlider, QColorDialog, QFileDialog, QGraphicsView,
    QGraphicsScene, QGraphicsPixmapItem, QGraphicsRectItem
)

from util import ImageTransformer
from util.ImageConverter import convertQimageToCv, convertCvToQimage
from util.ImageTransformer import applyBackgroundColor, applyTextureBackground


class BackgroundEditorDialog(QDialog):
    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Change Background")

        self.graphicsView = QGraphicsView()
        self.graphicsView.setFixedSize(800, 600)
        self.scene = QGraphicsScene(self.graphicsView)
        self.graphicsView.setScene(self.scene)

        self.originalPixmap = pixmap
        self.pixmapItem = QGraphicsPixmapItem(self.originalPixmap)
        self.scene.addItem(self.pixmapItem)

        self.selectionRectangle = None
        self.isSelecting = False

        self.graphicsView.viewport().installEventFilter(self)

        self.bwCheckbox = QCheckBox("Black and White")
        self.bwCheckbox.stateChanged.connect(self.updateImage)

        self.thresholdSlider = QSlider(Qt.Orientation.Horizontal)
        self.thresholdSlider.setRange(0, 255)
        self.thresholdSlider.setValue(127)
        self.thresholdSlider.valueChanged.connect(self.updateImage)

        self.colorPickerButton = QPushButton("Pick Background Color")
        self.colorPickerButton.clicked.connect(self.openColorDialog)
        self.selectedColor = None

        self.selectTextureButton = QPushButton("Select Texture Image")
        self.selectTextureButton.clicked.connect(self.openTextureFileDialog)
        self.texture_path = None

        self.saveButton = QPushButton("Save")
        self.cancelButton = QPushButton("Cancel")

        self.saveButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

        # Layouts
        optionsLayout = QVBoxLayout()
        optionsLayout.addWidget(self.bwCheckbox)
        optionsLayout.addWidget(QLabel("Threshold"))
        optionsLayout.addWidget(self.thresholdSlider)
        optionsLayout.addWidget(self.colorPickerButton)
        optionsLayout.addWidget(self.selectTextureButton)
        optionsLayout.addStretch()
        optionsLayout.addWidget(self.saveButton)
        optionsLayout.addWidget(self.cancelButton)

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.graphicsView)
        mainLayout.addLayout(optionsLayout)
        self.setLayout(mainLayout)

    def openColorDialog(self):
        self.selectTextureButton.setEnabled(False)
        color = QColorDialog.getColor()
        if color.isValid():
            self.selectedColor = color
            self.colorPickerButton.setStyleSheet(f"background-color: {color.name()}")
            self.updateImage()

    def openTextureFileDialog(self):
        self.colorPickerButton.setEnabled(False)
        texture_path, _ = QFileDialog.getOpenFileName(self, "Select Texture Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if texture_path:
            self.texture_path = texture_path
            self.updateImage()

    def eventFilter(self, source, event):
        if source == self.graphicsView.viewport():
            if event.type() == QMouseEvent.Type.MouseButtonPress:
                self.startSelection(event)
            elif event.type() == QMouseEvent.Type.MouseMove and self.isSelecting:
                self.updateSelection(event)
            elif event.type() == QMouseEvent.Type.MouseButtonRelease:
                self.endSelection(event)
        return super().eventFilter(source, event)

    def startSelection(self, event):
        scene_position = self.graphicsView.mapToScene(event.pos())

        if self.selectionRectangle:
            self.scene.removeItem(self.selectionRectangle)
            self.selectionRectangle = None

        self.isSelecting = True
        self.selectionStart = scene_position
        self.selectionRectangle = QGraphicsRectItem(QRectF(self.selectionStart, self.selectionStart))
        self.selectionRectangle.setPen(QPen(Qt.GlobalColor.red, 2, Qt.PenStyle.SolidLine))
        self.scene.addItem(self.selectionRectangle)

    def updateSelection(self, event):
        if self.selectionRectangle:
            current_scene_position = self.graphicsView.mapToScene(event.pos())
            self.selectionRectangle.setRect(QRectF(self.selectionStart, current_scene_position).normalized())

    def endSelection(self, event):
        self.isSelecting = False
        self.selectionEnd = self.graphicsView.mapToScene(event.pos())
        self.updateImage()

    def updateImage(self):
        modified_image = convertQimageToCv(self.originalPixmap.toImage())
        threshold = self.thresholdSlider.value()
        overlay = not self.bwCheckbox.isChecked()

        modified_image = ImageTransformer.grayscaleImage(modified_image, threshold, overlay=overlay)

        if self.selectionRectangle:
            selection_rect = self.selectionRectangle.rect().toRect()
            cv_selection_rect = (
                selection_rect.left(), selection_rect.top(),
                selection_rect.width(), selection_rect.height()
            )

            if self.selectedColor:
                modified_image = ImageTransformer.ROIColorWithinRectangle(
                    modified_image, self.selectedColor, cv_selection_rect)
            elif self.texture_path:
                modified_image = ImageTransformer.ROITextureWithinRectangle(
                    modified_image, self.texture_path, cv_selection_rect, threshold)
        else:
            if self.selectedColor:
                modified_image = applyBackgroundColor(modified_image, self.selectedColor)
            elif self.texture_path:
                modified_image = applyTextureBackground(modified_image, threshold, self.texture_path, overlay)

        updated_pixmap = QPixmap.fromImage(convertCvToQimage(modified_image))
        self.pixmapItem.setPixmap(updated_pixmap)