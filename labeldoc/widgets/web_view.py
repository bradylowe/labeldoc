# labeldoc/widgets/web_view.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QToolBar, QTabWidget, QMainWindow
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, QEventLoop, QByteArray
from pdf2image import convert_from_bytes


class WebView(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)

    def load_url(self, url):
        self.setUrl(QUrl(url))

    def generate_pil_images_from_webpage(self):
        """Generate a list of PIL images from the current tab."""
        pdf_data = QByteArray()

        # Create an event loop to wait for the PDF generation to finish
        event_loop = QEventLoop()

        # Callback function that will be called when the PDF is generated
        def on_pdf_generated(data):
            nonlocal pdf_data
            pdf_data = data
            event_loop.quit()

        # Start the PDF generation
        self.page().printToPdf(on_pdf_generated)

        # Block the execution until the PDF is saved
        event_loop.exec()

        # Convert the QByteArray to bytes
        pdf_bytes = pdf_data.data()

        # Convert the PDF bytes to PIL images
        pil_images = convert_from_bytes(pdf_bytes)

        return pil_images

    def print_to_pdf(self, file_name):
        """Print the current web page to a PDF file."""
        try:
            self.page().printToPdf(file_name)
        except Exception as e:
            print(f"Error printing to PDF: {e}")


class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Web Browser")

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Toolbar with back, forward, refresh, and URL bar
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        # Add navigation buttons and URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        self.back_button = QPushButton("<")
        self.back_button.clicked.connect(self.back)
        self.forward_button = QPushButton(">")
        self.forward_button.clicked.connect(self.forward)
        self.refresh_button = QPushButton("R")
        self.refresh_button.clicked.connect(self.refresh_page)
        self.new_tab_button = QPushButton("+")
        self.new_tab_button.clicked.connect(self.open_new_tab)

        self.toolbar.addWidget(self.back_button)
        self.toolbar.addWidget(self.forward_button)
        self.toolbar.addWidget(self.refresh_button)
        self.toolbar.addWidget(self.url_bar)
        self.toolbar.addWidget(self.new_tab_button)

        # Add tabs
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.layout.addWidget(self.tabs)

        # Add first tab
        self.add_new_tab(QUrl('https://www.google.com'), 'New Tab')

    def add_new_tab(self, url=None, label="New Tab"):
        browser_tab = WebView()
        if url:
            browser_tab.load(url)
        else:
            browser_tab.load_url('https://www.google.com')
        index = self.tabs.addTab(browser_tab, label)
        self.tabs.setCurrentIndex(index)
        self.url_bar.setText(browser_tab.url().toString())

        browser_tab.urlChanged.connect(lambda: self.update_url(browser_tab))

    def navigate_to_url(self):
        url = self.url_bar.text()
        current_browser = self.tabs.currentWidget()
        current_browser.load_url(url)

    def update_url(self, browser):
        self.url_bar.setText(browser.url().toString())

    def back(self):
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.back()

    def forward(self):
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.forward()

    def refresh_page(self):
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.reload()

    def open_new_tab(self):
        self.add_new_tab(QUrl('https://www.github.com/bradylowe'), 'New Tab')

    def close_current_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            self.close()

    def load_url(self, url):
        current_browser = self.tabs.currentWidget()
        current_browser.load_url(url)
