from PySide6.QtCore import QPointF
from PySide6.QtGui import Qt, QAction
from PySide6.QtWidgets import QGraphicsProxyWidget, QMenu


class MovableProxyWidget(QGraphicsProxyWidget):
    def __init__(self, widget, parent=None):
        super().__init__(parent)
        self.setWidget(widget)

        self.setFlag(QGraphicsProxyWidget.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsProxyWidget.GraphicsItemFlag.ItemIsSelectable)

        self.dragging = False
        self.dragStartPosition = QPointF()
        self.transition = False

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragStartPosition = event.pos()
            self.dragging = True
            self.setCursor(Qt.CursorShape.ClosedHandCursor)

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.dragging:
            distance = event.pos() - self.dragStartPosition
            newPosition = self.pos() + distance
            self.setPos(newPosition)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            self.setCursor(Qt.CursorShape.OpenHandCursor)  # Reset cursor to an open hand after drag
        super().mouseReleaseEvent(event)

    def contextMenuEvent(self, event):
        """Override to create a context menu on right-click."""
        menu = QMenu()

        # Add actions to the context menu
        if self.transition is False:
            transitionAction = QAction("Add Transition", None)
        else:
            transitionAction = QAction("Remove Transition", None)
        deleteAction = QAction("Delete Element", self)

        transitionAction.triggered.connect(self.addRemoveTransition)
        deleteAction.triggered.connect(self.deleteElement)

        menu.addAction(transitionAction)
        menu.addAction(deleteAction)

        menu.exec(event.screenPos())

    def addRemoveTransition(self):
        """Handle adding/removing transitions (functionality to be defined)."""
        self.transition = not self.transition
        print("Add/Remove Transition clicked.")

    def deleteElement(self):
        """Handle deleting the element from the scene."""
        scene = self.scene()
        if scene:
            scene.removeItem(self)
            self.deleteLater()