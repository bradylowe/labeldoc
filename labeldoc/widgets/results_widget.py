from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit

class ResultsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Shape Metadata")
        layout.addWidget(self.label)

        self.setLayout(layout)
