# app/views/main_view.py

import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
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
        self.toolbar = QToolBar("Toolbar")
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.toolbar)
        self._create_toolbar_actions(self.toolbar)

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

    def _create_toolbar_actions(self, toolbar):
        icon_path = os.path.join(os.path.dirname(__file__), '../../resources/icons')

        open_action = toolbar.addAction(QIcon(os.path.join(icon_path, 'open.png')), "Open")
        open_action.triggered.connect(self.open_file_dialog)

        save_action = toolbar.addAction(QIcon(os.path.join(icon_path, 'save.png')), "Save")
        save_action.triggered.connect(self.save_annotations)

        toolbar.addSeparator()

        next_page_action = toolbar.addAction(QIcon(os.path.join(icon_path, 'next.png')), "Next Page")
        next_page_action.triggered.connect(self.next_page)

        previous_page_action = toolbar.addAction(QIcon(os.path.join(icon_path, 'prev.png')), "Previous Page")
        previous_page_action.triggered.connect(self.previous_page)

        undo_action = toolbar.addAction(QIcon(os.path.join(icon_path, 'undo.png')), "Undo")
        undo_action.triggered.connect(self.canvas.action_manager.undo)

        redo_action = toolbar.addAction(QIcon(os.path.join(icon_path, 'redo.png')), "Redo")
        redo_action.triggered.connect(self.canvas.action_manager.redo)

        toolbar.addSeparator()

        print_log_action = toolbar.addAction(QIcon(os.path.join(icon_path, 'log.png')), "Print Actions Log")
        print_log_action.triggered.connect(self.canvas.action_manager.print_action_log)

        '''
        first_page_action = toolbar.addAction("First Page")
        first_page_action.triggered.connect(self.first_page)

        last_page_action = toolbar.addAction("Last Page")
        last_page_action.triggered.connect(self.last_page)
        '''

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
