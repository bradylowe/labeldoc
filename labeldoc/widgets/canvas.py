# app/widgets/canvas.py

from PyQt6.QtWidgets import QWidget, QSizePolicy
from PyQt6.QtGui import QPainter, QImage, QColor, QTransform
from PyQt6.QtCore import Qt, QPoint, QRect, QSize
from ..utils.image_conversion import pil_to_qimage
from ..actions import ActionManager, ZoomAction, DrawShapeAction, InitialZoomAction, PanAction

class CanvasWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.image: QImage = None
        self.shapes: list = []
        self.zoom_level = 1.0  # Initial zoom level
        self.min_zoom_level = 0.009  # Reduced minimum zoom size by 10%
        self.max_zoom_level = 10.0
        self.offset = QPoint(0, 0)  # Offset for panning
        self.last_pos = QPoint(0, 0)  # Last mouse position
        self.action_manager = ActionManager()

        # Set the canvas to expand and shrink dynamically
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    
    # Basic Canvas functionality

    def add_shape(self, shape):
        self.shapes.append(shape)
        self.update()

    def remove_shape(self, shape):
        if shape in self.shapes:
            self.shapes.remove(shape)
            self.update()
    
    def pan(self, pan_amount):
        new_offset = self.offset + pan_amount
        bounded_offset = self.bound_offset(new_offset)
        self.offset = bounded_offset
        self.update()

    def bound_offset(self, offset):
        """Ensure the offset keeps the image within the canvas bounds."""
        if not self.image or not self.parent():
            return offset

        parent_size = self.get_parent_size()
        image_width = self.image.width() * self.zoom_level
        image_height = self.image.height() * self.zoom_level

        # Calculate the maximum offset (keeping the image within the viewable area)
        max_x_offset = max(0, parent_size.width() - image_width)
        max_y_offset = max(0, parent_size.height() - image_height)

        # Calculate the minimum offset (image can't move out of the viewable area)
        min_x_offset = min(0, (parent_size.width() - image_width))
        min_y_offset = min(0, (parent_size.height() - image_height))

        # Bound the offset within these constraints
        bounded_x = min(max_x_offset, max(min_x_offset, offset.x()))
        bounded_y = min(max_y_offset, max(min_y_offset, offset.y()))

        return QPoint(int(bounded_x), int(bounded_y))


    def set_zoom_level(self, zoom_level):
        self.zoom_level = max(self.min_zoom_level, min(self.max_zoom_level, zoom_level))
        self.update()

    def load_image(self, pil_image):
        """Convert PIL Image to QImage and store it."""
        if pil_image:
            self.image = pil_to_qimage(pil_image)
            self.perform_initial_zoom()
            self.update_aspect_ratio()

    def load_shapes(self, shapes):
        self.shapes = shapes
        self.update()

    def update_aspect_ratio(self):
        """Update the canvas size while maintaining the aspect ratio of the image."""
        if self.image:
            aspect_ratio = self.image.width() / self.image.height()
            parent_size = self.get_parent_size()

            # Calculate new width and height based on the aspect ratio
            if parent_size.width() / parent_size.height() > aspect_ratio:
                # Constrain by height
                new_height = parent_size.height()
                new_width = new_height * aspect_ratio
            else:
                # Constrain by width
                new_width = parent_size.width()
                new_height = new_width / aspect_ratio

            # Set the fixed size of the widget based on the calculated size
            self.setFixedSize(int(new_width), int(new_height))

    def get_parent_size(self):
        """Calculate the available space for the canvas within the parent widget."""
        if self.parent():
            return self.parent().size()
        return self.size()

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
    
    # Zoom helper functions

    def calculate_zoom_to_fit_page(self):
        """Calculate the zoom level needed to fit the entire page in the canvas."""
        if self.image:
            parent_size = self.get_parent_size()
            scale_x = parent_size.width() / self.image.width()
            scale_y = parent_size.height() / self.image.height()
            return min(scale_x, scale_y)
        return 1.0

    def calculate_initial_zoom(self):
        """Calculate and return the initial zoom level to fit the image in the canvas."""
        return self.calculate_zoom_to_fit_page()

    def calculate_zoom_to_fit_width(self):
        """Calculate the zoom level needed to fit the page width in the canvas."""
        if self.image:
            parent_size = self.get_parent_size()
            return parent_size.width() / self.image.width()
        return self.zoom_level

    def update_min_zoom_level(self):
        """Update the minimum zoom level based on the image size and canvas size."""
        if self.image:
            self.min_zoom_level = self.calculate_zoom_to_fit_page()
    
    # Other helper functions

    def update_canvas(self):
        """Update the canvas size based on the current zoom level."""
        self.update()
    
    # Handle events

    def paintEvent(self, event):
        painter = QPainter(self)

        # Fill the background with a light gray color
        painter.fillRect(self.rect(), QColor(200, 200, 200))

        if self.image:

            # Calculate the position to draw the image based on the offset (without centering)
            x = int(self.offset.x())
            y = int(self.offset.y())

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

    def wheelEvent(self, event):
        """Handle zooming when Ctrl is held, and panning otherwise."""
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.handle_zoom_event_from_scroll(event)
        else:
            # Use panning based on the scroll wheel movement for horizontal/vertical scrolls
            delta_x = -event.angleDelta().x()
            delta_y = -event.angleDelta().y()
            self.perform_pan(self.offset, self.offset + QPoint(delta_x, delta_y))

    def resizeEvent(self, event):
        """Handle resizing of the widget to update the zoom and layout accordingly."""
        self.update_min_zoom_level()
        self.update_aspect_ratio()  # Update aspect ratio on resize
        self.offset = self.bound_offset(self.offset)  # Adjust the offset based on new bounds
        self.update()
    
    def mousePressEvent(self, event):
        """Handle mouse press for panning."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_pos = event.pos()

    def mouseMoveEvent(self, event):
        """Handle mouse movement for panning."""
        if event.buttons() & Qt.MouseButton.LeftButton:
            current_pos = event.pos()
            self.perform_pan(self.last_pos, current_pos)
            self.last_pos = current_pos
