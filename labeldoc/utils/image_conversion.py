# app/utils/image_conversion.py

from PyQt5.QtGui import QImage
from PIL import Image

def pil_to_qimage(pil_image):
    """Convert PIL Image to QImage."""
    if pil_image.mode == "RGB":
        r, g, b = pil_image.split()
        pil_image = Image.merge("RGB", (b, g, r))
        image = pil_image.convert("RGBA")
    elif pil_image.mode == "L":
        image = pil_image.convert("RGBA")
    elif pil_image.mode == "P":
        image = pil_image.convert("RGBA")
    else:
        image = pil_image

    data = image.tobytes("raw", "BGRA")
    qimage = QImage(data, image.width, image.height, QImage.Format.Format_ARGB32)
    return qimage
