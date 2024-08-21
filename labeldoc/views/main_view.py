# app/views/main_view.py

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QDockWidget, QFileDialog, QWidget, QHBoxLayout

from ..widgets.canvas import CanvasWidget
from ..widgets.results_widget import ResultsWidget
from ..widgets.toolbar import ToolbarWidget
from ..controllers.app_controller import AppController

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.controller: AppController = None
        self.setWindowTitle("LabelDoc")
        self.setGeometry(100, 100, 1200, 800)

        # Set central layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create the CanvasWidget and add it to the layout
        self.canvas = CanvasWidget(self)
        layout.addWidget(self.canvas)

        # Toolbar on the left
        self.toolbar = ToolbarWidget(self)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.toolbar)

        # Results widget on the right
        self.results_widget = ResultsWidget()
        results_dock = QDockWidget("Results", self)
        results_dock.setWidget(self.results_widget)
        results_dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, results_dock)

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
    
    def load_current_browser_page(self):
        """Print the current web page in the active browser tab to a PDF, convert it to PIL images, and load them into the canvas."""
        if hasattr(self.controller, 'browser_window'):
            browser = self.controller.browser_window
            current_tab = browser.tabs.currentWidget()
            if current_tab:
                try:
                    pil_images = current_tab.generate_pil_images_from_webpage()
                    self.controller.load_images(pil_images)  # Assuming you have a method to handle a list of PIL images
                except RuntimeError as e:
                    print(f"Failed to load browser page: {e}")
