# app/controllers/app_controller.py
from ..models.document_model import DocumentModel
from ..views.main_view import CanvasWidget

class AppController:
    def __init__(self, model, view):
        self.model: DocumentModel = model
        self.view: CanvasWidget = view
        self.view.set_controller(self)

    def load_document(self, file_path):
        self.model.load_document(file_path)
        self.update_view()

    def save_annotations(self):
        current_page_index = self.model.current_page_index
        shapes = self.view.get_current_shapes()
        self.model.save_annotations(current_page_index, shapes)

    def next_page(self):
        if not self.model.is_last_page():
            self.save_annotations()
            self.model.next_page()
            self.update_view()

    def previous_page(self):
        if not self.model.is_first_page():
            self.save_annotations()
            self.model.prev_page()
            self.update_view()

    def first_page(self):
        self.save_annotations()
        self.model.first_page()
        self.update_view()

    def last_page(self):
        self.save_annotations()
        self.model.last_page()
        self.update_view()

    def update_view(self):
        pil_image = self.model.get_current_page()
        current_annotations = self.model.get_current_annotations()
        self.view.load_page(pil_image, current_annotations)
