import cv2
import numpy as np

from ui.movable.MovableProxyWidget import MovableProxyWidget
from ui.movable.ResizablePixmapItem import ResizablePixmapItem
from util.ImageRender import renderScene, addTransition


def saveSceneAsImage(filename, scene, width=800, height=600):
    """Save the current scene as an image using OpenCV, ensuring text appears on top and images don't exceed bounds."""
    canvas = np.zeros((height, width, 3), dtype=np.uint8)
    renderScene(scene, canvas)
    cv2.imwrite(filename, canvas)

def saveScenesAsVideo(outputFilename, framesPerSecond, frameDuration, scenes, width=800, height=600):
    """Create and save a video using OpenCV."""
    videoWriter = cv2.VideoWriter(outputFilename, cv2.VideoWriter.fourcc(*'mp4v'),
                                  framesPerSecond, (width, height))

    for sceneIndex, scene in enumerate(scenes):
        # Determine if there's a transition to the next scene
        hasTransition = sceneIndex < len(scenes) - 1

        # Time allocation for transition if it exists
        transitionDuration = 2 if hasTransition else 0  # 2 seconds for transition
        staticFrameDuration = frameDuration - transitionDuration

        # Render the static part of the scene (e.g., 3 seconds if 2 seconds are reserved for transition)
        for frame_num in range(framesPerSecond * staticFrameDuration):
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            renderScene(scene, frame)
            videoWriter.write(frame)

        # Handle transition if there's a next scene
        if hasTransition:
            nextScene = scenes[sceneIndex + 1]
            # Collect items that require transition
            itemsToTransition = [
                item for item in scene.items()
                if (isinstance(item, ResizablePixmapItem) and getattr(item, 'transition', True))
                   or (isinstance(item, MovableProxyWidget) and getattr(item.widget(), 'transition', True))
            ]

            # If there are items with transition, handle the fade-out and fade-in
            if itemsToTransition:
                addTransition(videoWriter, scene, nextScene, framesPerSecond, itemsToTransition, width, height)
            else:
                # If no transition items, render the next scene as normal
                for frame_num in range(framesPerSecond * frameDuration):
                    frame = np.zeros((height, width, 3), dtype=np.uint8)
                    renderScene(nextScene, frame)
                    videoWriter.write(frame)

    videoWriter.release()

