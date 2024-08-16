# app/widgets/canvas.py

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QImage

from ..utils.image_conversion import pil_to_qimage

class CanvasWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image: QImage = None
        self.shapes = []

    def load_image(self, pil_image):
        """Convert PIL Image to QImage and store it."""
        if pil_image:
            self.image = pil_to_qimage(pil_image)
            self.update()

    def load_annotations(self, annotations):
        self.shapes = annotations
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.image:
            painter.drawImage(self.rect(), self.image)
        for shape in self.shapes:
            shape.draw(painter)
