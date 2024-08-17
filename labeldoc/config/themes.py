DARK_THEME = """
QMainWindow {
    background-color: #2E2E2E;  /* Dark background for the main window */
    color: #FFFFFF;  /* White text color */
}

QToolBar {
    background-color: #333333;  /* Slightly lighter dark background for the toolbar */
    border: 1px solid #444444;  /* Subtle border for the toolbar */
}

QToolButton {
    background-color: #444444;  /* Dark background for tool buttons */
    color: #FFFFFF;  /* White text on buttons */
    border: 1px solid #555555;  /* Border for tool buttons */
    padding: 6px;  /* Padding inside the buttons */
    margin: 2px;  /* Margin around the buttons */
    border-radius: 4px;  /* Rounded corners for buttons */
}

QToolButton:hover {
    background-color: #555555;  /* Slightly lighter on hover */
}

QMenuBar {
    background-color: #333333;  /* Dark background for menu bar */
    color: #FFFFFF;  /* White text in the menu bar */
}

QMenuBar::item {
    background-color: #333333;  /* Background for menu items */
    color: #FFFFFF;  /* White text for menu items */
}

QMenuBar::item:selected {
    background-color: #555555;  /* Highlight menu items on hover */
}

QStatusBar {
    background-color: #333333;  /* Dark background for status bar */
    color: #FFFFFF;  /* White text in the status bar */
}

QDockWidget {
    background-color: #3E3E3E;  /* Dark background for dock widgets */
    color: #FFFFFF;  /* White text in dock widgets */
    border: 1px solid #444444;  /* Border for dock widgets */
}

QWidget {
    background-color: #2E2E2E;  /* Default dark background for widgets */
    color: #FFFFFF;  /* Default white text for widgets */
    border: 1px solid #444444;  /* Border for widgets */
}

QLabel {
    color: #FFFFFF;  /* White text for labels */
}

QPushButton {
    background-color: #444444;  /* Dark background for push buttons */
    color: #FFFFFF;  /* White text on push buttons */
    border: 1px solid #555555;  /* Border for push buttons */
    padding: 6px;  /* Padding inside buttons */
    border-radius: 4px;  /* Rounded corners for buttons */
}

QPushButton:hover {
    background-color: #555555;  /* Slightly lighter on hover */
}

QLineEdit {
    background-color: #3E3E3E;  /* Dark background for line edits */
    color: #FFFFFF;  /* White text for line edits */
    border: 1px solid #555555;  /* Border for line edits */
    padding: 4px;  /* Padding inside line edits */
}

QScrollBar:vertical {
    background-color: #2E2E2E;  /* Dark background for vertical scroll bars */
    width: 12px;
    margin: 22px 0 22px 0;
}

QScrollBar:horizontal {
    background-color: #2E2E2E;  /* Dark background for horizontal scroll bars */
    height: 12px;
    margin: 0 22px 0 22px;
}

QScrollBar::handle {
    background-color: #555555;  /* Scroll bar handle color */
    border-radius: 4px;
}

QScrollBar::handle:hover {
    background-color: #666666;  /* Lighter handle on hover */
}

QScrollBar::add-line, QScrollBar::sub-line {
    background-color: #333333;
    border: 1px solid #444444;
    subcontrol-origin: margin;
    height: 20px;
    width: 20px;
    border-radius: 4px;
}

QScrollBar::add-line:hover, QScrollBar::sub-line:hover {
    background-color: #555555;
}
"""
