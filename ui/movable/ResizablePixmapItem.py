from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor, QAction
from PySide6.QtWidgets import QGraphicsPixmapItem, QMenu, QDialog

from ui.window.BackgroundEditorDialog import BackgroundEditorDialog
from util import ImageConverter, ImageTransformer


class ResizablePixmapItem(QGraphicsPixmapItem):
    def __init__(self, pixmap):
        super().__init__(pixmap)
        self.setFlag(QGraphicsPixmapItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsPixmapItem.GraphicsItemFlag.ItemIsSelectable)
        self.resizing = False
        self.resizeSide = None
        self.transition = False

        self.edgeDistance = 10

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            boundingRectangle = self.boundingRect()
            pos = event.pos()

            is_near_left = pos.x() < self.edgeDistance
            is_near_right = pos.x() > (boundingRectangle.width() - self.edgeDistance)
            is_near_top = pos.y() < self.edgeDistance
            is_near_bottom = pos.y() > (boundingRectangle.height() - self.edgeDistance)

            if is_near_left or is_near_right or is_near_top or is_near_bottom:
                self.resizing = True
                self.setCursor(QCursor(Qt.CursorShape.SizeAllCursor))

                distances = {
                    'right': boundingRectangle.width() - pos.x(),
                    'bottom': boundingRectangle.height() - pos.y()
                }
                self.resizeSide = min(distances, key=distances.get)
            else:
                self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
                super().mousePressEvent(event)  # Allow moving
        elif event.button() == Qt.MouseButton.RightButton:
            self.contextMenuEvent(event)

    def mouseMoveEvent(self, event):
        if self.resizing:
            pixmapImage = self.pixmap().toImage()
            if self.resizeSide == 'right':
                newWidth = max(1, int(event.pos().x() - self.x()))
                newPixmap = ImageTransformer.imageResize(ImageConverter.convertQimageToCv(pixmapImage), width=newWidth)
                self.setPixmap(ImageConverter.convertArrayToPixmap(newPixmap))
            elif self.resizeSide == 'bottom':
                newHeight = max(1, int(event.pos().y() - self.y()))
                newPixmap = ImageTransformer.imageResize(ImageConverter.convertQimageToCv(pixmapImage),
                                                        height=newHeight)
                self.setPixmap(ImageConverter.convertArrayToPixmap(newPixmap))
            self.update()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.resizing = False
        self.resizeSide = None
        super().mouseReleaseEvent(event)

    def contextMenuEvent(self, event):
        """Override to create a context menu on right-click."""
        menu = QMenu()

        if self.transition is False:
            transitionAction = QAction("Add Transition", None)
        else:
            transitionAction = QAction("Remove Transition", None)
        deleteAction = QAction("Delete Element", None)

        transitionAction.triggered.connect(self.addRemoveTransition)
        deleteAction.triggered.connect(self.deleteElement)

        menu.addAction(transitionAction)
        menu.addAction(deleteAction)

        flipMenu = menu.addMenu("Flip")
        flipHorizontallyAction = QAction("Flip Horizontally", None)
        flipVerticallyAction = QAction("Flip Vertically", None)
        flipBothAction = QAction("Flip Both Sides", None)

        flipHorizontallyAction.triggered.connect(lambda: self.setPixmap(ImageTransformer.flipHorizontally(self.pixmap())))
        flipVerticallyAction.triggered.connect(lambda: self.setPixmap(ImageTransformer.flipVertically(self.pixmap())))
        flipBothAction.triggered.connect(lambda: self.setPixmap(ImageTransformer.flipBoth(self.pixmap())))

        flipMenu.addAction(flipHorizontallyAction)
        flipMenu.addAction(flipVerticallyAction)
        flipMenu.addAction(flipBothAction)

        menu.addSeparator()

        changeBackgroundAction = QAction("Change Background", None)
        menu.addAction(changeBackgroundAction)
        changeBackgroundAction.triggered.connect(self.openBackgroundEditor)

        menu.exec(event.screenPos())

    def addRemoveTransition(self):
        """Check if image/text should have transition"""
        self.transition = not self.transition

    def deleteElement(self):
        """Handle deleting the element from the scene."""
        scene = self.scene()
        if scene:
            scene.removeItem(self)

    def openBackgroundEditor(self):
        """Open the background editor dialog."""
        dialog = BackgroundEditorDialog(self.pixmap())
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.applyBackgroundChanges(dialog)

    def applyBackgroundChanges(self, dialog):
        """Apply background changes directly from the dialog."""
        updated_pixmap = dialog.pixmapItem.pixmap()
        self.setPixmap(updated_pixmap)