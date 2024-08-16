# app/models/document_model.py

from pdf2image import convert_from_path
from PIL import Image

class DocumentModel:
    def __init__(self):
        self.pages: list[Image.Image] = []  # List of PIL.Image objects
        self.annotations = {}  # Annotations by page index
        self.current_page_index = 0

    def load_document(self, file_path):
        """Load the document and split it into pages."""
        self.pages = self.split_document_into_pages(file_path)
        self.current_page_index = 0

    def split_document_into_pages(self, file_paths):
        """Load images from a path or list of paths (PDF or PNG)"""
        if isinstance(file_paths, str):
            file_paths = [file_paths]
        
        images = []
        for path in file_paths:
            clean_path = path.lower()
            if clean_path.endswith('.pdf'):
                images.extend(convert_from_path(path))
            elif clean_path.endswith('.png'):
                images.append(Image.open(path))
            else:
                raise ValueError(f'Could not load {path}. File type not supported.')
        
        return images

    def get_current_page(self):
        return self.pages[self.current_page_index] if self.pages else None

    def get_current_annotations(self):
        return self.annotations.get(self.current_page_index, [])

    def save_annotations(self, page_index, shapes):
        """Save the shapes for the current page."""
        self.annotations[page_index] = shapes
    
    def next_page(self):
        """Move to the next page in the document."""
        if self.current_page_index < len(self.pages) - 1:
            self.current_page_index += 1
    
    def prev_page(self):
        """Move to the previous page in the document."""
        if self.current_page_index > 0:
            self.current_page_index -= 1
    
    def first_page(self):
        """Move to the first page in the document."""
        self.current_page_index = 0
    
    def last_page(self):
        """Move to the last page in the document."""
        self.current_page_index = len(self.pages) - 1
    
    def is_first_page(self) -> bool:
        """Check if the current page is the first page in the document."""
        return self.current_page_index == 0
    
    def is_last_page(self) -> bool:
        """Check if the current page is the last page in the document."""
        return self.current_page_index == len(self.pages) - 1
