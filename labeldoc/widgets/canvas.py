# app/widgets/canvas.py

from PyQt6.QtWidgets import QWidget, QScrollArea
from PyQt6.QtGui import QPainter, QImage, QColor, QTransform
from PyQt6.QtCore import Qt, QPoint
from ..utils.image_conversion import pil_to_qimage
from ..actions import ActionManager, ZoomAction, DrawShapeAction, InitialZoomAction, PanAction

class CanvasWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.image: QImage = None
        self.shapes: list = []
        self.zoom_level = 1.0  # Initial zoom level
        self.min_zoom_level = 0.01
        self.max_zoom_level = 10.0
        self.offset = QPoint(0, 0)  # Offset for panning
        self.last_pos = QPoint(0, 0)  # Last mouse position
        self.action_manager = ActionManager()
        self.setMinimumSize(1, 1)  # Minimum size to allow proper resizing
    
    # Basic Canvas functionality

    def add_shape(self, shape):
        self.shapes.append(shape)
        self.update()

    def remove_shape(self, shape):
        if shape in self.shapes:
            self.shapes.remove(shape)
            self.update()
    
    def pan(self, pan_amount):
        self.offset += pan_amount
        self.update()

    def set_zoom_level(self, zoom_level):
        self.zoom_level = max(self.min_zoom_level, min(self.max_zoom_level, zoom_level))
        self.update_canvas_size()
        self.update()

    def load_image(self, pil_image):
        """Convert PIL Image to QImage and store it."""
        if pil_image:
            self.image = pil_to_qimage(pil_image)
            self.perform_initial_zoom()

    def load_shapes(self, shapes):
        self.shapes = shapes
        self.update()
    
    # Perform Actions (Actions are logged via ActionManager)

    def perform_pan(self, start_pos, end_pos):
        """Perform a pan action from start_pos to end_pos"""
        self.action_manager.do_action(PanAction(self, start_pos, end_pos))
    
    def perform_zoom(self, new_zoom_level):
        old_zoom_level = self.zoom_level
        self.action_manager.do_action(ZoomAction(self, old_zoom_level, new_zoom_level))
    
    def perform_initial_zoom(self):
        action = InitialZoomAction(self)
        self.action_manager.do_action(action)

    def perform_draw_shape(self, shape):
        action = DrawShapeAction(self, shape)
        self.action_manager.do_action(action)
    
    # Zoom helper functions

    def calculate_zoom_to_fit_page(self):
        """Calculate the zoom level needed to fit the entire page in the canvas."""
        if self.image:
            if self.image.width() > 0 and self.image.height() > 0:
                scale_x = self.width() / self.image.width()
                scale_y = self.height() / self.image.height()
                return min(scale_x, scale_y)
        return 1.0

    def calculate_initial_zoom(self):
        """Calculate and return the initial zoom level to fit the image in the canvas."""
        return self.calculate_zoom_to_fit_page()

    def calculate_zoom_to_fit_width(self):
        """Calculate the zoom level needed to fit the page width in the canvas."""
        if self.image:
            if self.image.width() > 0:
                return self.width() / self.image.width()
        return self.zoom_level
    
    def update_min_zoom_level(self):
        """Update the minimum zoom level based on the image size and canvas size"""
        if self.image:
            self.min_zoom_level = self.calculate_zoom_to_fit_page()
    
    # Other helper functions

    def update_canvas_size(self):
        """Update the canvas size based on the current zoom level."""
        if self.image:
            image_width = int(self.image.width() * self.zoom_level)
            image_height = int(self.image.height() * self.zoom_level)
            self.setFixedSize(image_width, image_height)
            self.updateGeometry()

    def get_scroll_area(self):
        """Ensure we find the correct QScrollArea parent."""
        parent = self.parent()
        while parent and not isinstance(parent, QScrollArea):
            parent = parent.parent()
        return parent
    
    # Handle events

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

    def handle_zoom_event_from_scroll(self, event):
        """Adjust the zoom level based on the mouse wheel."""
        zoom_factor = 1.1
        if event.angleDelta().y() > 0:
            new_zoom_level = self.zoom_level * zoom_factor
        else:
            new_zoom_level = self.zoom_level / zoom_factor
        
        self.perform_zoom(new_zoom_level)

    def handle_scroll_event(self, event):
        """Scroll the canvas based on the mouse wheel."""
        # Todo: add action logging
        scroll_area = self.get_scroll_area()
        if scroll_area:
            if event.angleDelta().y() != 0:  # Vertical scrolling
                scroll_area.verticalScrollBar().setValue(
                    scroll_area.verticalScrollBar().value() - event.angleDelta().y()
                )
            if event.angleDelta().x() != 0:  # Horizontal scrolling (if applicable)
                scroll_area.horizontalScrollBar().setValue(
                    scroll_area.horizontalScrollBar().value() - event.angleDelta().x()
                )

    def wheelEvent(self, event):
        """Handle zooming when Ctrl is held, and scrolling otherwise."""
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.handle_zoom_event_from_scroll(event)
        else:
            # Use panning based on the scroll wheel movement for horizontal/vertical scrolls
            delta_x = -event.angleDelta().x()
            delta_y = -event.angleDelta().y()
            self.perform_pan(self.offset, self.offset + QPoint(delta_x, delta_y))

    def mousePressEvent(self, event):
        """Handle mouse press for panning."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_pos = event.pos()

    def mouseMoveEvent(self, event):
        """Handle mouse movement for panning."""
        if event.buttons() & Qt.LeftButton:
            current_pos = event.pos()
            self.perform_pan(self.last_pos, current_pos)
            self.last_pos = current_pos
