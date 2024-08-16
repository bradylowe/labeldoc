# app/main.py

import sys
import argparse
from PyQt5.QtWidgets import QApplication
from .views.main_view import MainWindow
from .config import APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT, DARK_THEME

from .models.document_model import DocumentModel
from .controllers.app_controller import AppController

def main():

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description=f'{APP_NAME} - A document annotation tool.')
    parser.add_argument('file', nargs='?', help='The path to the file to open on startup.')
    args = parser.parse_args()

    app = QApplication(sys.argv)

    # Apply the dark theme
    app.setStyleSheet(DARK_THEME)

    # Initialize the model
    model = DocumentModel()

    # Initialize the main window (view)
    main_window = MainWindow()
    main_window.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
    if args.file:
        main_window.setWindowTitle(f"{APP_NAME} - {args.file}")
        main_window.controller.load_document(args.file)
    else:
        main_window.setWindowTitle(APP_NAME)

    # Initialize the controller, passing the model and the view
    controller = AppController(model, main_window)

    # Set the controller in the view
    main_window.set_controller(controller)

    # Show the main window
    main_window.show()

    # Start the application's event loop
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
