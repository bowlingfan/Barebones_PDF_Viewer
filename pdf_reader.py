from PyQt6.QtGui import QPixmap, QImage
import fitz
import re

class PDF_Reader():
    def __init__(self, file_name=""):
        """0 = VALID, 1 = FAILED, 2 = WARNING"""
        self.status = 0
        self.error_msg = None
        self.file_name = file_name
        self.document = None
        self.open_file(self.file_name)

    def __del__(self):
        if self.document is not None:
            self.document.close()
    
    """
    debug: printing the object will print the status and message.
    """
    def __str__(self):
        return f'status: [{self.status}], \n\tmessage: {self.error_msg}'

    def get_file_name(self):
        return self.file_name
    
    def get_max_pages(self):
        if self.document is not None:
            return (self.document.page_count // 2) + 1 if self.document.page_count % 2 == 1 else (self.document.page_count // 2)
        else:
            return 1
        
    def open_file(self, file_name):
        self.status = 0; self.error_msg = None
        if file_name == "": 
            self.status = 1; self.error_msg = f'No file directory was provided.'
            return None
        try:
            self.document = fitz.open(file_name) 
        except:
            self.status = 1; self.error_msg = f'File with "{file_name}" directory did not exist/could not be opened.'
            return None
        
    def get_page_pixmap(self, page_number, dpi=75):
        self.status = 0; self.error_msg = None
        if self.document is None:
            self.status = 2; self.error_msg = "Safe Call: No PDF has been opened yet?"
            return None
        
        page = None

        try:
            page = self.document.load_page(page_number)
        except:
            self.status = 1; self.error_msg = f'The document opened couldn\'t load the page number "{page_number+1}": is it out of bounds or valid?'
            return None
        
        pixmap = page.get_pixmap(dpi=dpi)
        format = QImage.Format.Format_RGBA8888 if pixmap.alpha else QImage.Format.Format_RGB888
        q_image = QImage(pixmap.samples, pixmap.width, pixmap.height, pixmap.stride, format)
        return QPixmap.fromImage(q_image)