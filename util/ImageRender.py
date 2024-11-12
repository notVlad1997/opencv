import cv2
import numpy as np

from ui.movable.MovableLabel import MovableLabel
from ui.movable.MovableProxyWidget import MovableProxyWidget
from ui.movable.ResizablePixmapItem import ResizablePixmapItem
from util.ImageConverter import convertQPixmapToCvImage
from util.canvas.CanvasConverter import drawImageOnCanvas, drawTextOnCanvas


def renderScene(scene, canvas, useTransition=True, alpha=1):
    """Render items in the scene with mixed transition and non-transition behavior."""
    for item in reversed(scene.items()):
        if isinstance(item, ResizablePixmapItem):
            img = convertQPixmapToCvImage(item.pixmap())
            x, y = int(item.pos().x()), int(item.pos().y())

            # Only apply transition if self.transition is True
            if getattr(item, 'transition', False) and useTransition:
                img = cv2.addWeighted(np.zeros_like(img), 1 - alpha, img, alpha, 0)
            drawImageOnCanvas(canvas, img, x, y)

        for item in scene.items():
            if isinstance(item, MovableProxyWidget):
                containedWidget = item.widget()
                if isinstance(containedWidget, MovableLabel):
                    text = containedWidget.text()
                    color = containedWidget.getColor()
                    font = containedWidget.getFontSize()
                    thickness = containedWidget.getThickness()
                    x, y = int(item.pos().x()), int(item.pos().y()) + 20

                    # Only apply transition if self.transition is True
                    if getattr(item, 'transition', False) and useTransition:

                        fadedColor = fadeTextColor(alpha, color)
                        drawTextOnCanvas(canvas, text, x, y, color=fadedColor, fontScale=font, thickness=thickness)
                    else:
                        # Render text without transition
                        drawTextOnCanvas(canvas, text, x, y, color=color, fontScale=font, thickness=thickness)


def addTransition(videoWriter, currentScene, nextScene, framesPerSecond, itemsToTransition, width=800, height=600):
    """Add a fade-out for current scene and fade-in for next scene transition."""
    transitionDuration = 2  # seconds
    frameCount = framesPerSecond * transitionDuration  # Total frames for the transition

    for alpha in np.linspace(1, 0, frameCount):  # Fade current scene out, fade next scene in
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        currentFrame = np.zeros_like(frame)
        nextFrame = np.zeros_like(frame)

        # Render all non-transitioning elements fully in both scenes
        for item in currentScene.items():
            if not getattr(item, 'transition', False):  # Non-transitioning elements
                renderScene(currentScene, currentFrame, useTransition=False)

        for item in nextScene.items():
            if not getattr(item, 'transition', False):  # Non-transitioning elements
                renderScene(nextScene, nextFrame, useTransition=False)

        for item in itemsToTransition:
            # Fade-out for the current scene's items
            if item in currentScene.items():
                renderScene(currentScene, currentFrame, useTransition=True, alpha=alpha)

            # Fade-in for the next scene's items
            if item in nextScene.items():
                renderScene(nextScene, nextFrame, useTransition=True, alpha=1 - alpha)

        for item in currentScene.items():
            if getattr(item, 'transition', False):  # Only for transitioning elements
                itemFrame = np.zeros_like(frame)
                renderScene(currentScene, itemFrame, useTransition=True, alpha=alpha)  # Use alpha blending
                # Composite the itemFrame onto the final frame
                frame = itemFrame

        for item in nextScene.items():
            if getattr(item, 'transition', False):  # Only for transitioning elements
                itemFrame = np.zeros_like(frame)
                renderScene(nextScene, itemFrame, useTransition=True, alpha=1 - alpha)  # Use alpha blending
                # Composite the itemFrame onto the final frame
                frame = itemFrame

        videoWriter.write(frame)


def fadeTextColor(alpha, color=(255, 255, 255)):
    """Return a faded color based on the alpha value."""
    fadedColor = (int(color[0] * alpha), int(color[1] * alpha), int(color[2] * alpha))
    return fadedColor