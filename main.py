import sys

import cv2
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsScene, QPushButton, \
    QHBoxLayout, QWidget, QMessageBox

from ui.SceneWithSizeArea import SceneWithSizeArea
from ui.TextInputDialog import TextInputDialog
from ui.movable.ResizablePixmapItem import ResizablePixmapItem
from ui_form import Ui_MainWindow
from util import ImageConverter, ImageIO


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.actionAdd_Image.triggered.connect(self.addItem)
        self.ui.actionAdd_Frame.triggered.connect(self.addFrame)
        self.ui.actionAdd_Text.triggered.connect(self.addText)
        self.ui.actionSave_Image.triggered.connect(self.saveImage)
        self.ui.actionSave_Video.triggered.connect(self.saveVideo)

        self.ui.actionAdd_Text.setEnabled(False)
        self.ui.actionAdd_Image.setEnabled(False)
        self.ui.actionSave_Video.setEnabled(False)
        self.ui.actionSave_Image.setEnabled(False)

        self.scenes = []
        self.currentSceneIndex = None

        self.timelineScene = QGraphicsScene(self)
        self.ui.graphicsView_2.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.ui.graphicsView_2.setScene(self.timelineScene)

        self.currentFrameTimelinePosition = 0
        self.buttonWidth = 50
        self.buttonHeight = 30
        self.padding = 10
        self.lastButton = None

        self.frameDuration = 5
        self.framesPerSecond = 30

        self.width = 800
        self.height = 600
        self.sizeArea = None

    def createNewScene(self):
        """Creates a new scene"""
        newScene = SceneWithSizeArea(self)
        self.scenes.append(newScene)
        self.currentSceneIndex = len(self.scenes) - 1
        self.ui.graphicsView.setScene(newScene)

    def switchScene(self, index, button):
        """ Switch the scene when a button is pressed
        :arg index: index of the scene
        :arg button: The button which was pressed to toggle on
        """
        if 0 <= index < len(self.scenes):
            self.currentSceneIndex = index
            self.ui.graphicsView.setScene(self.scenes[index])
            self.ui.graphicsView.viewport().update()  # Force update to redraw the view

            if self.lastButton:
                self.lastButton.setChecked(False)

            button.setChecked(True)
            self.lastButton = button


    def addItem(self):
        """Open Image File dialog"""
        fileDialog = QFileDialog(self)
        filePath, _ = fileDialog.getOpenFileName(
            self, "Select an Image", "", "Image Files (*.png *.jpg *.bmp *.jpeg);;All Files (*)"
        )

        if filePath:
            image = cv2.imread(filePath)
            if image is None:
                print("Error: Could not load image.")
                return

            qImage = ImageConverter.convertCvToQimage(image)
            pixmap = QPixmap.fromImage(qImage)

            pixmapItem = ResizablePixmapItem(pixmap)
            pixmapItem.setPos(0, 0)
            self.scenes[self.currentSceneIndex].addItem(pixmapItem)

            self.ui.actionSave_Video.setEnabled(True)
            self.ui.actionSave_Image.setEnabled(True)

    def addFrame(self):
        """Adds a new frame and button to the timeline."""
        self.createNewScene()

        frameIndex = len(self.scenes) - 1

        newButton = QPushButton(f"Frame {len(self.scenes)}")
        newButton.setCheckable(True)

        currentFrameTimelinePosition = self.currentFrameTimelinePosition

        buttonWidget = QWidget()
        buttonLayout = QHBoxLayout(buttonWidget)
        buttonLayout.addWidget(newButton)
        buttonWidget.setLayout(buttonLayout)
        buttonWidget.setFixedSize(self.buttonWidth, self.buttonHeight)

        proxy_widget = self.timelineScene.addWidget(buttonWidget)
        proxy_widget.setPos(currentFrameTimelinePosition, 0)

        self.currentFrameTimelinePosition += self.buttonWidth - self.padding

        newButton.clicked.connect(lambda _, index=frameIndex, btn=newButton: self.switchScene(index, btn))
        self.switchScene(index=frameIndex, button=newButton)

        self.ui.actionAdd_Text.setEnabled(True)
        self.ui.actionAdd_Image.setEnabled(True)


    def addText(self):
        """Adds a new text to the scene."""
        inputWidget = TextInputDialog(self.scenes, self.currentSceneIndex)
        proxyWidget = self.scenes[self.currentSceneIndex].addWidget(inputWidget)
        inputWidget.setProxyWidget(proxyWidget)
        proxyWidget.setPos(50, 50)

        self.ui.actionSave_Video.setEnabled(True)
        self.ui.actionSave_Image.setEnabled(True)


    def flip(self, method):
        """Flips the selected image"""
        global currentQImage
        currentQImage = method(currentQImage)

    def saveImage(self):
        """Save the current scene (frame) as an image."""
        fileDialog = QFileDialog(self)
        filePath, _ = fileDialog.getSaveFileName(
            self,
            "Save Image",  # Title
            "",  # Default file path
            "Image Files (*.png *.jpg);;All Files (*)"  # Supported file types
        )
        if filePath:
            ImageIO.saveSceneAsImage(filename=filePath, scene=self.scenes[self.currentSceneIndex])
            QMessageBox.information(self, "Image Save", "Image saved successfully!")
        else:
            QMessageBox.information(self, "Image Save", "Image not saved!")

    def setFrameDuration(self):
        """Set the frame duration based on textEdit value."""
        textValue = self.ui.textEdit.toPlainText()
        if textValue.isdigit():
            self.frameDuration = int(textValue)
        else:
            self.frameDuration = 5

    def saveVideo(self):
        """Trigger saving video logic."""
        self.setFrameDuration()
        outputFilename = QFileDialog.getSaveFileName(self, "Save Video", "", "Video Files (*.mp4);;All Files (*)")[0]
        if outputFilename:
            ImageIO.saveScenesAsVideo(outputFilename, framesPerSecond=self.framesPerSecond,
                                      frameDuration=self.frameDuration, scenes=self.scenes)
            QMessageBox.information(self, "Video Save", "Video saved successfully!")
        else:
            QMessageBox.information(self, "Video Save", "Video not saved!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
