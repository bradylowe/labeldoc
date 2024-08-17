# app/widgets/canvas.py

from PyQt5.QtWidgets import QWidget, QScrollArea
from PyQt5.QtGui import QPainter, QImage, QColor, QTransform
from PyQt5.QtCore import Qt, QPoint

from ..utils.image_conversion import pil_to_qimage

class CanvasWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image: QImage = None
        self.shapes: list = []
        self.zoom_level = 1.0  # Initial zoom level
        self.offset = QPoint(0, 0)  # Offset for panning
        self.setMinimumSize(1, 1)  # Minimum size to allow proper resizing

    def load_image(self, pil_image):
        """Convert PIL Image to QImage and store it."""
        if pil_image:
            self.image = pil_to_qimage(pil_image)
            self.calculate_initial_zoom()
            self.update()

    def load_shapes(self, shapes):
        self.shapes = shapes
        self.update()
    
    def calculate_initial_zoom(self):
        """Calculate the initial zoom level to fit the image in the canvas."""
        if self.image:
            image_width = self.image.width()
            image_height = self.image.height()

            # Calculate the zoom level needed to fit the image in the canvas
            if image_width > 0 and image_height > 0:
                scale_x = self.width() / image_width
                scale_y = self.height() / image_height
                self.zoom_level = min(scale_x, scale_y)

                # Set the size of the widget to match the zoomed image
                self.setMinimumSize(int(image_width * self.zoom_level), int(image_height * self.zoom_level))

    def paintEvent(self, event):
        painter = QPainter(self)

        # Fill the background with a light gray color
        painter.fillRect(self.rect(), QColor(200, 200, 200))

        if self.image:
            # Calculate the size of the image based on the zoom level
            image_width = self.image.width() * self.zoom_level
            image_height = self.image.height() * self.zoom_level

            # Calculate the position to center the image
            x = int((self.width() - image_width) / 2 + self.offset.x())
            y = int((self.height() - image_height) / 2 + self.offset.y())

            # Create a transformation for zooming
            transform = QTransform()
            transform.scale(self.zoom_level, self.zoom_level)

            # Apply the transformation and draw the image
            painter.setTransform(transform)
            painter.drawImage(QPoint(x, y), self.image)
        
        if self.shapes:
            for shape in self.shapes:
                shape.draw(painter)

    def update_canvas_size(self):
        """Update the canvas size based on the current zoom level."""
        if self.image:
            image_width = int(self.image.width() * self.zoom_level)
            image_height = int(self.image.height() * self.zoom_level)
            self.setMinimumSize(image_width, image_height)
            self.resize(image_width, image_height)
            self.updateGeometry()

    def change_zoom_event(self, event):
        """Adjust the zoom level based on the mouse wheel."""
        zoom_factor = 1.1
        if event.angleDelta().y() > 0:
            self.zoom_level *= zoom_factor
        else:
            self.zoom_level /= zoom_factor

        # Update the canvas size and trigger a repaint
        self.update_canvas_size()
        self.update()

    def canvas_scroll_event(self, event):
        """Scroll the canvas based on the mouse wheel."""
        scroll_area = self.find_parent_scroll_area()
        if scroll_area:
            if event.angleDelta().y() != 0:  # Vertical scrolling
                scroll_area.verticalScrollBar().setValue(
                    scroll_area.verticalScrollBar().value() - event.angleDelta().y()
                )
            if event.angleDelta().x() != 0:  # Horizontal scrolling (if applicable)
                scroll_area.horizontalScrollBar().setValue(
                    scroll_area.horizontalScrollBar().value() - event.angleDelta().x()
                )

    def find_parent_scroll_area(self):
        """Ensure we find the correct QScrollArea parent."""
        parent = self.parent()
        while parent and not isinstance(parent, QScrollArea):
            parent = parent.parent()
        return parent

    def wheelEvent(self, event):
        """Handle zooming when Ctrl is held, and scrolling otherwise."""
        if event.modifiers() == Qt.ControlModifier:
            self.change_zoom_event(event)
        else:
            self.canvas_scroll_event(event)

    def mousePressEvent(self, event):
        """Handle mouse press for panning."""
        if event.button() == Qt.LeftButton:
            self.last_pos = event.pos()

    def mouseMoveEvent(self, event):
        """Handle mouse movement for panning."""
        if event.buttons() & Qt.LeftButton:
            delta = event.pos() - self.last_pos
            self.offset += delta
            self.last_pos = event.pos()
            self.update()
