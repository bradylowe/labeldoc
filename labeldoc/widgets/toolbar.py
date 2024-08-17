# app/widgets/toolbar.py

import os
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QToolBar

class ToolbarWidget(QToolBar):
    def __init__(self, parent=None):
        super().__init__("Toolbar", parent)
        self.controller = None
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.icon_path = os.path.join(os.path.dirname(__file__), '../../resources/icons')
        self.create_toolbar_actions()

    def set_controller(self, controller):
        """Connect the toolbar to the app controller."""
        self.controller = controller

    def create_toolbar_actions(self):
        open_action = self.addAction(QIcon(os.path.join(self.icon_path, 'open.png')), "Open")
        open_action.triggered.connect(self.open_file_dialog)

        save_action = self.addAction(QIcon(os.path.join(self.icon_path, 'save.png')), "Save")
        save_action.triggered.connect(self.save_annotations)

        self.addSeparator()

        next_page_action = self.addAction(QIcon(os.path.join(self.icon_path, 'next.png')), "Next Page")
        next_page_action.triggered.connect(self.next_page)

        previous_page_action = self.addAction(QIcon(os.path.join(self.icon_path, 'prev.png')), "Previous Page")
        previous_page_action.triggered.connect(self.previous_page)

        undo_action = self.addAction(QIcon(os.path.join(self.icon_path, 'undo.png')), "Undo")
        undo_action.triggered.connect(self.parent().canvas.action_manager.undo)

        redo_action = self.addAction(QIcon(os.path.join(self.icon_path, 'redo.png')), "Redo")
        redo_action.triggered.connect(self.parent().canvas.action_manager.redo)

        self.addSeparator()

        print_log_action = self.addAction(QIcon(os.path.join(self.icon_path, 'log.png')), "Actions Log")
        print_log_action.triggered.connect(self.parent().canvas.action_manager.print_action_log)

    def open_file_dialog(self):
        if self.controller:
            self.controller.open_file_dialog()

    def save_annotations(self):
        if self.controller:
            self.controller.save_annotations()

    def next_page(self):
        if self.controller:
            self.controller.next_page()

    def previous_page(self):
        if self.controller:
            self.controller.previous_page()
