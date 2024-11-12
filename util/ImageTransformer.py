import cv2
import numpy as np

from util import ImageConverter
from util.ImageConverter import convertQColorRGBtoScalarBGR


def imageResize(image, width = None, height = None, inter = cv2.INTER_LANCZOS4):
    if width is None:
        aspectRatio = image.shape[0] / image.shape[1]
        width = int(height / aspectRatio)
    if height is None:
        aspectRatio = image.shape[1] / image.shape[0]
        height = int(width / aspectRatio)

    resized = cv2.resize(image, (int(width), int(height)), interpolation = inter)

    return resized


def flipHorizontally(pixmap):
    """Flip the pixmap horizontally."""
    pixmapImage = pixmap.toImage()
    cvImage = ImageConverter.convertQimageToCv(pixmapImage)
    flipped = cv2.flip(cvImage, 1)  #
    return ImageConverter.convertArrayToPixmap(flipped)


def flipVertically(pixmap):
    """Flip the pixmap horizontally."""
    pixmapImage = pixmap.toImage()
    cvImage = ImageConverter.convertQimageToCv(pixmapImage)
    flipped = cv2.flip(cvImage, 0)
    return ImageConverter.convertArrayToPixmap(flipped)


def flipBoth(pixmap):
    """Flip the pixmap both horizontally and vertically."""
    pixmapImage = pixmap.toImage()
    cvImage = ImageConverter.convertQimageToCv(pixmapImage)
    flipped = cv2.flip(cvImage, -1)
    return ImageConverter.convertArrayToPixmap(flipped)


def grayscaleImage(image, threshold, overlay=False):
    """Apply a threshold overlay on a color image or convert to full black and white."""

    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _, bw_mask = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)

    bw_mask_3ch = cv2.cvtColor(bw_mask, cv2.COLOR_GRAY2RGB)

    if image.shape[2] == 4:
        bw_mask_3ch = cv2.cvtColor(bw_mask_3ch, cv2.COLOR_RGB2RGBA)

    if bw_mask_3ch.shape[:2] != image.shape[:2]:
        bw_mask_3ch = cv2.resize(bw_mask_3ch, (image.shape[1], image.shape[0]))

    if overlay:
        return cv2.addWeighted(image, 0.7, bw_mask_3ch, 0.3, 0)
    else:
        return bw_mask_3ch


def ensure_within_bounds(rect, width, height):
    """Ensure the rectangle is within the image boundaries."""
    x, y, w, h = rect
    x = max(0, min(x, width))
    y = max(0, min(y, height))
    return x, y, w, h

def convert_image_channels(image, target_channels):
    """Convert image to match target number of channels."""
    if image.shape[2] == 4 and target_channels == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
    if image.shape[2] == 3 and target_channels == 4:
        return cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    return image

def load_and_resize_texture(texture_path, target_shape):
    """Load and resize a texture image to match a target shape."""
    texture = cv2.imread(texture_path, cv2.IMREAD_UNCHANGED)
    return cv2.resize(texture, target_shape[::-1])  # shape[::-1] for (width, height)

def create_colored_background(image, color):
    """Create a full-sized background image with a given color."""
    bgr_color = convertQColorRGBtoScalarBGR(color)
    if image.shape[2] == 4:  # If the image has an alpha channel
        bgra_color = (*bgr_color, 255)  # Ensure alpha is fully opaque
        return np.full_like(image, bgra_color, dtype=np.uint8)
    else:
        return np.full_like(image, bgr_color, dtype=np.uint8)

def apply_masked_background(foreground, background, mask):
    """Apply a masked background over a foreground image."""
    return cv2.bitwise_and(background, background, mask=mask) + cv2.bitwise_and(foreground, foreground, mask=cv2.bitwise_not(mask))

def applyBackgroundColor(image, color):
    """Change the background color of an image."""
    image = convert_image_channels(image, 3)
    mask = cv2.inRange(image, (200, 200, 200), (255, 255, 255))
    color_background = create_colored_background(image, color)
    return apply_masked_background(image, color_background, mask)

def applyTextureBackground(image, threshold, texture_path, overlay=False):
    """Apply a texture as the background for an image based on a threshold."""
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _, background_mask = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)

    texture_image = load_and_resize_texture(texture_path, image.shape[:2])
    texture_image = convert_image_channels(texture_image, image.shape[2])

    if overlay:
        image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2RGB)
        if image.shape[2] == 4:
            image = convert_image_channels(image, 4)

    return apply_masked_background(image, texture_image, background_mask)


def process_roi(image, rect, background_color):
    """Fill the background with the color and retain the selected rectangle."""
    x, y, w, h = ensure_within_bounds(rect, *image.shape[:2])

    full_background = create_colored_background(image, background_color)

    selected_area = image[y:y + h, x:x + w]

    gray_selected_area = cv2.cvtColor(selected_area, cv2.COLOR_BGR2GRAY)
    _, object_mask = cv2.threshold(gray_selected_area, 127, 255, cv2.THRESH_BINARY_INV)

    inverted_mask = cv2.bitwise_not(object_mask)

    foreground = cv2.bitwise_and(selected_area, selected_area, mask=object_mask)
    background_in_rectangle = cv2.bitwise_and(full_background[y:y + h, x:x + w], full_background[y:y + h, x:x + w],
                                              mask=inverted_mask)

    combined_rectangle = cv2.add(foreground, background_in_rectangle)

    full_background[y:y + h, x:x + w] = combined_rectangle

    return full_background

def ROIColorWithinRectangle(image, color, rect):
    """Keep the selected ROI unchanged and apply a background color to the rest of the image."""
    return process_roi(image, rect, color)

def ROITextureWithinRectangle(image, texture_path, rect, threshold, color=None):
    """Apply a texture or color background outside a selected rectangle."""
    def process(roi):
        if color:
            background = create_colored_background(roi, color)
        else:
            background = roi.copy()

        return applyTextureBackground(background, threshold, texture_path)

    return process_roi(image, rect, process)