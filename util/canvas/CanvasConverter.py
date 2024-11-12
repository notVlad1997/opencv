import cv2

from util.ImageConverter import convertQColorRGBtoScalarBGR, convertQtFontSizeToCv2FontScale


def drawImageOnCanvas(canvas, img, x, y):
    """Draw an image on the canvas at the specified (x, y) position, ensuring it fits within bounds."""
    canvasHeight, canvasWidth = canvas.shape[:2]
    imgHeight, imgWidth = img.shape[:2]

    # Adjust for negative x and y coordinates
    if x < 0:
        img = img[:, -x:]
        imgWidth += x
        x = 0
    if y < 0:
        img = img[-y:, :]
        imgHeight += y
        y = 0

    # Calculate available width and height to fit the image within canvas bounds
    availableWidth = min(imgWidth, canvasWidth - x)
    availableHeight = min(imgHeight, canvasHeight - y)

    if availableWidth <= 0 or availableHeight <= 0:
        return

    img = img[:availableHeight, :availableWidth]

    # Draw a black box and overlay the image
    canvas[y:y + availableHeight, x:x + availableWidth] = img

def drawTextOnCanvas(canvas, text, x, y, fontScale=1, color=(255, 255, 255), thickness=2):
    """Draw text on the canvas at the specified (x, y) position."""
    colorBGR = convertQColorRGBtoScalarBGR(color)
    fontSize = convertQtFontSizeToCv2FontScale(fontScale)
    canvasHeight, canvasWidth = canvas.shape[:2]
    x = min(x, canvasWidth - 1)
    y = min(y, canvasHeight - 1)
    cv2.putText(canvas, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, fontSize, colorBGR, int(thickness))