# app/views/main_view.py

import os
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QMainWindow, 
    QToolBar, 
    QDockWidget, 
    QHBoxLayout, 
    QWidget, 
    QFileDialog, 
    QMessageBox, 
    QScrollArea,
)

from ..widgets.canvas import CanvasWidget
from ..widgets.results_widget import ResultsWidget
from ..widgets.toolbar import ToolbarWidget
from ..controllers.app_controller import AppController

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.controller: AppController = None
        self.setWindowTitle("Canvas")
        self.setGeometry(100, 100, 1200, 800)

        # Create the scroll area and set the CanvasWidget as its widget
        self.scroll_area = QScrollArea()
        self.canvas = CanvasWidget(self.scroll_area)
        self.scroll_area.setWidget(self.canvas)
        self.scroll_area.setWidgetResizable(True)

        # Set the scroll area as the central widget
        self.setCentralWidget(self.scroll_area)

        # Toolbar on the left
        self.toolbar = ToolbarWidget(self)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.toolbar)

        # Results widget on the right
        self.results_widget = ResultsWidget()
        dock = QDockWidget("Results", self)
        dock.setWidget(self.results_widget)
        dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

        # Add status bar at the bottom
        self.statusBar().showMessage("Ready")

    def set_controller(self, controller):
        """Connect the main window to the app controller."""
        self.controller = controller
        self.toolbar.set_controller(controller)

    def open_file_dialog(self):
        """Open a file dialog to select a document and load it."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Document", "", "Images (*.png *.xpm *.jpg *.bmp);;All Files (*)")
        if file_name:
            self.controller.load_document(file_name)
            self.statusBar().showMessage(f"Loaded: {file_name}")

    def save_annotations(self):
        """Save annotations and update the status bar."""
        self.controller.save_annotations()
        self.statusBar().showMessage("Annotations saved successfully.")

    def next_page(self):
        """Navigate to the next page."""
        self.controller.next_page()
        self.statusBar().showMessage(f"Page {self.controller.model.current_page_index + 1} of {len(self.controller.model.pages)}")

    def previous_page(self):
        """Navigate to the previous page."""
        self.controller.previous_page()
        self.statusBar().showMessage(f"Page {self.controller.model.current_page_index + 1} of {len(self.controller.model.pages)}")

    def first_page(self):
        """Navigate to the first page."""
        self.controller.first_page()
        self.statusBar().showMessage(f"Page 1 of {len(self.controller.model.pages)}")

    def last_page(self):
        """Navigate to the last page."""
        self.controller.last_page()
        self.statusBar().showMessage(f"Page {self.controller.model.current_page_index + 1} of {len(self.controller.model.pages)}")

    def load_page(self, image_path, shapes):
        """Load the image and annotations into the canvas."""
        self.canvas.load_image(image_path)
        self.canvas.load_shapes(shapes)

    def get_current_shapes(self):
        """Return the current shapes from the canvas."""
        return self.canvas.shapes
