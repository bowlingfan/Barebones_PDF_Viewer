from PyQt6.QtWidgets import (
    QApplication, 
    QWidget, 
    QPushButton, 
    QLabel, 
    QLineEdit, 
    QStackedWidget,
    QMessageBox,
    QHBoxLayout,  
    QVBoxLayout,
    QSizePolicy,
    QFileDialog,
    QScrollArea,
)

from PyQt6.QtCore import Qt, QSize, QEvent
from PyQt6.QtGui import QTransform, QPixmap, QIcon, QPalette, QColor

from sys import argv
import os

import ui_config as uic #ui_config.py
import pdf_reader as pdf_r #pdf_reader.py
import bookmark as pdf_b #bookmark.py

# when building, prevents issues with icons not showing up.
base_directory = os.path.dirname(__file__)
# used for more than one class
ui_config = uic.UI_Config

class LogoPushButton(QPushButton):
    def __init__(self, text=""):
        super().__init__()
        self.setText(text)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.setMinimumSize(50, 30)
        self.setMaximumSize(75, 50)

        self.setStyleSheet("""                  
            QPushButton {
                font-size: 17px;
                background-color: transparent;
                border: solid #0044BA;
                border-width: 0px 0px 1px 0px;            
            }
                           
            QPushButton:hover {
                background-color: #DBDBDB;            
            }
        """)

class PDF_Viewer_App(QWidget):
    pdf = pdf_r.PDF_Reader(ui_config.current_directory)
    bookmark = pdf_b.PDF_Bookmark()

    def __init__(self):
        super().__init__()
        self.resize(ui_config.width, ui_config.height)

        self.update_config_from_pdf()
        self.ctrl_press = False

        self.create_widgets()
        self.design_widgets()
        self.design_layouts()
        self.connect_events()

        self.update_page_displays()

    """
    Main UI Functionality: Creating Widgets, designing them, designing layouts and connecting PyQT events (through PyQT slots.)
    """
    def create_widgets(self):
        self.open_new_file_button = LogoPushButton()
        self.bookmark_button = LogoPushButton()

        self.left_arrow_button = LogoPushButton("<")
        self.right_arrow_button = LogoPushButton(">")

        self.page_number_label = QLineEdit(str(ui_config.current_page_number))
        self.page_limit_label = QLabel(str(ui_config.max_page_number))

        self.zoom_in_button = LogoPushButton("+")
        self.zoom_out_button = LogoPushButton("-")

        self.rotate_left_button = LogoPushButton()
        self.rotate_right_button = LogoPushButton()

        self.page_display_1 = QLabel("Left Page")
        self.page_display_2 = QLabel("Right Page")

    def design_widgets(self):
        # Modify Widgets
        self.page_number_label.setMaxLength(len(str(ui_config.max_page_number)))
        self.page_number_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page_number_label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.page_number_label.setMinimumWidth(50)
        self.page_number_label.setMaximumWidth(75)

        self.open_new_file_button.setToolTip("Open New PDF")
        self.bookmark_button.setToolTip("Bookmark Page")
        self.rotate_left_button.setToolTip("Rotate Page Left by 90°")
        self.rotate_right_button.setToolTip("Rotate Page Right by 90°")

        open_file_pixmap = QPixmap(os.path.join(base_directory, "icons/open_file.png"))
        bookmark_pixmap = QPixmap(os.path.join(base_directory, "icons/bookmark.png"))
        rotate_left_pixmap = QPixmap(os.path.join(base_directory, "icons/rotate_left.png"))
        rotate_right_pixmap = QPixmap(os.path.join(base_directory, "icons/rotate_right.png"))

        open_file_icon = QIcon(open_file_pixmap)
        bookmark_icon = QIcon(bookmark_pixmap)
        rotate_left_icon = QIcon(rotate_left_pixmap)
        rotate_right_icon = QIcon(rotate_right_pixmap)

        self.open_new_file_button.setIcon(open_file_icon)
        self.bookmark_button.setIcon(bookmark_icon)
        self.rotate_left_button.setIcon(rotate_left_icon)
        self.rotate_right_button.setIcon(rotate_right_icon)

        self.open_new_file_button.setIconSize(self.open_new_file_button.size())
        self.bookmark_button.setIconSize(self.bookmark_button.size())
        self.rotate_left_button.setIconSize(QSize(self.rotate_left_button.width(), 30))
        self.rotate_right_button.setIconSize(QSize(self.rotate_right_button.width(), 30))

        # Style Sheet setting for Widgets
        self.setStyleSheet(
        """               
            QScrollBar {
                width: 5px;
                height: 5px;
            }

            QLineEdit {
                font-size: 17px;
                background-color: transparent;
                border: solid #0044BA;
                border-width: 0px 0px 1px 0px;
            }

            QLineEdit:hover {
                background-color: #DBDBDB;
            }
        """
        )

        self.open_new_file_button.setStyleSheet(""" QPushButton { border: None; } QPushButton:hover {background-color: #DBDBDB; color: white; } """)
        self.bookmark_button.setStyleSheet(""" QPushButton { border: None; } QPushButton:hover {background-color: #DBDBDB; color: white; } """)

    def design_layouts(self):
        self.main_layout = QVBoxLayout()

        # header controls
        self.header_controls = QHBoxLayout()
        self.header_controls.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.rotate_controls = QVBoxLayout()
        self.rotate_actual_controls = QHBoxLayout()
        self.rotate_controls.addWidget(QLabel("rotate"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.rotate_actual_controls.addWidget(self.rotate_left_button)
        self.rotate_actual_controls.addWidget(self.rotate_right_button)
        self.rotate_controls.addLayout(self.rotate_actual_controls)

        self.zoom_controls = QVBoxLayout()
        self.zoom_actual_controls = QHBoxLayout()
        self.zoom_controls.addWidget(QLabel("zoom"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.zoom_actual_controls.addWidget(self.zoom_in_button)
        self.zoom_actual_controls.addWidget(self.zoom_out_button)
        self.zoom_controls.addLayout(self.zoom_actual_controls)

        self.page_controls = QVBoxLayout()
        self.page_actual_controls = QHBoxLayout()
        self.page_actual_controls.addWidget(self.left_arrow_button)
        self.page_actual_controls.addWidget(self.page_number_label)
        self.page_actual_controls.addWidget(self.right_arrow_button)
        self.page_controls.addWidget(self.page_limit_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.page_controls.addLayout(self.page_actual_controls)

        self.special_controls = QHBoxLayout()
        
        self.special_controls.addWidget(self.open_new_file_button)
        self.special_controls.addWidget(self.bookmark_button)

        # add all layouts to the "parent layout"
        self.header_controls.addLayout(self.special_controls)
        self.header_controls.addSpacing(ui_config.header_spacing)
        self.header_controls.addLayout(self.page_controls, 3)
        self.header_controls.addSpacing(ui_config.header_spacing)
        self.header_controls.addLayout(self.rotate_controls, 3)
        self.header_controls.addSpacing(ui_config.header_spacing)
        self.header_controls.addLayout(self.zoom_controls, 3)

        # page display
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(""" QScrollArea { border: solid #000000; border-width: 1px 0px 0px 0px; } """)

        self.page_display = QWidget()
        page_display_layout = QHBoxLayout()

        page_display_layout.addWidget(self.page_display_1)
        page_display_layout.addWidget(self.page_display_2)

        self.page_display.setLayout(page_display_layout)
        scroll_area.setWidget(self.page_display)

        self.main_layout.addLayout(self.header_controls, 1)
        self.main_layout.addWidget(scroll_area, 15)
        self.setLayout(self.main_layout)

    def connect_events(self):
        self.left_arrow_button.clicked.connect(self.decrement_page_count)
        self.right_arrow_button.clicked.connect(self.increment_page_count)
        self.page_number_label.textChanged.connect(self.text_changed_event)
        self.rotate_left_button.clicked.connect(self.rotate_pages_left)
        self.rotate_right_button.clicked.connect(self.rotate_pages_right)
        self.open_new_file_button.clicked.connect(self.get_new_directory)
        self.zoom_in_button.clicked.connect(self.increment_page_zoom)
        self.zoom_out_button.clicked.connect(self.decrement_page_zoom)
        self.bookmark_button.clicked.connect(self.bookmark_clicked)
    
    """
    PyQT Supported Events Override
    """
    def resizeEvent(self, window):
        ui_config.update_zoom_lim(window.size())
        self.update_page_displays()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_Left or key == Qt.Key.Key_A:
            self.decrement_page_count()
        elif key == Qt.Key.Key_Right or key == Qt.Key.Key_D:
            self.increment_page_count()
        if key == Qt.Key.Key_Control:
            self.ctrl_press = True
    
    def keyReleaseEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_Control:
            self.ctrl_press = False

    def wheelEvent(self, event):
        if not self.ctrl_press:
            return
        self.zoom_page_scroll(event.angleDelta().y())
    
    """
    Custom Events that are used to slot an event for specific PyQT widgets like QPushButton/QLineEdit
    """
    def increment_page_count(self):
        ui_config.current_page_number = min(ui_config.current_page_number+1, ui_config.max_page_number)
        self.page_number_label.setText(str(ui_config.current_page_number))
        self.update_page_displays()
    
    def decrement_page_count(self):
        ui_config.current_page_number = max(ui_config.current_page_number-1, 1)
        self.page_number_label.setText(str(ui_config.current_page_number))
        self.update_page_displays()

    def increment_page_zoom(self):
        ui_config.dpi_zoom = min(ui_config.dpi_zoom+5, ui_config.max_zoom)
        self.update_page_displays()

    def decrement_page_zoom(self):
        ui_config.dpi_zoom = max(ui_config.dpi_zoom-5, ui_config.min_zoom)
        self.update_page_displays()

    def rotate_pages_right(self):
        self.page_display_1.setPixmap(self.page_display_1.pixmap().transformed(QTransform().rotate(90)))
        self.page_display_2.setPixmap(self.page_display_2.pixmap().transformed(QTransform().rotate(90)))

    def rotate_pages_left(self):
        self.page_display_1.setPixmap(self.page_display_1.pixmap().transformed(QTransform().rotate(-90)))
        self.page_display_2.setPixmap(self.page_display_2.pixmap().transformed(QTransform().rotate(-90)))

    def text_changed_event(self, text):
        try:
            ui_config.current_page_number = int(text)
            ui_config.current_page_number = min(max(ui_config.current_page_number, 1), ui_config.max_page_number)
            self.page_number_label.setText(str(ui_config.current_page_number))
            self.update_page_displays()
        except:
            pass
    
    def get_new_directory(self):
        new_directory = QFileDialog()
        new_directory.setFileMode(QFileDialog.FileMode.ExistingFile)
        new_directory.setNameFilter("*.pdf")

        if (new_directory.exec()):
            self.open_pdf(new_directory.selectedFiles()[0])
            if self.pdf.status == 0:
                return 0
        
        #If unsuccessful, return -1 to not go to the "main page" (from home page)
        return -1

    def bookmark_clicked(self):
        directory = ui_config.current_directory
        if self.bookmark.directory_exists(directory):
            self.bookmark.remove_bookmark_data(directory)
            QMessageBox.warning(self, "Bookmark Information", "Bookmark removed.")
        else:
            self.bookmark.add_bookmark_data(directory, ui_config.current_page_number)
            QMessageBox.warning(self, "Bookmark Information", "Bookmark added.")
        self.update_bookmark_icon(directory)

    """
    Extra functions for use.
    """
    def update_config_from_pdf(self):
        ui_config.update_zoom_lim(self.size())
        ui_config.current_page_number = 1
        ui_config.max_page_number = self.pdf.get_max_pages()

    def update_page_displays(self):
        self.page_display_1.clear(); self.page_display_2.clear()
        page_number = ui_config.current_page_number-1
        page_1 = self.pdf.get_page_pixmap(page_number*2, ui_config.dpi_zoom)
        page_2 = self.pdf.get_page_pixmap(page_number*2+1, ui_config.dpi_zoom)
        if page_1:
            self.page_display_1.setPixmap(page_1)
        if page_2:
            self.page_display_1.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.page_display_2.setVisible(True)
            self.page_display_2.setPixmap(page_2)
        else:
            self.page_display_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.page_display_2.setVisible(False)

    def open_pdf(self, directory):
        ui_config.current_directory = directory
        self.pdf.open_file(ui_config.current_directory)

        if self.pdf.status == 0:
            self.update_config_from_pdf()

            self.page_number_label.setMaxLength(len(str(ui_config.max_page_number)))

            new_page_number = self.bookmark.get_bookmark_page_number(ui_config.current_directory)
            if new_page_number != -1:
                ui_config.current_page_number = new_page_number
            self.update_page_displays()

            self.page_number_label.setText(str(ui_config.current_page_number))
            self.page_limit_label.setText(str(ui_config.max_page_number))

            self.update_bookmark_icon(directory)

    def update_bookmark_icon(self, directory):
        if self.bookmark.directory_exists(directory):
            bookmark_pixmap = QPixmap(os.path.join(base_directory, "icons/bookmarked.png"))
            bookmark_icon = QIcon(bookmark_pixmap)
            self.bookmark_button.setIcon(bookmark_icon)
        else:
            bookmark_pixmap = QPixmap(os.path.join(base_directory, "icons/bookmark.png"))
            bookmark_icon = QIcon(bookmark_pixmap)
            self.bookmark_button.setIcon(bookmark_icon)

    def exec_open_pdf_from_windows(self, directory):
        self.open_pdf(directory)

    """
    Helper Functions
    """
    def zoom_page_scroll(self, delta):
        if delta > 0:
            self.increment_page_zoom()
        else:
            self.decrement_page_zoom()

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(ui_config.width, ui_config.height)
        self.setAutoFillBackground(True)

        self.create_widgets()
        self.design_widgets()
        self.design_layouts()
        self.connect_events()

    """
    Main UI Functionality: Creating Widgets, designing them, designing layouts and connecting PyQT events (through PyQT slots.)
    """
    def create_widgets(self):
        self.header_label = QLabel("hello there!")
        self.open_file_button = QPushButton("open pdf")
        self.quit_button = QPushButton("quit")

    def design_widgets(self):
        # Modify Widgets
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.open_file_button.setFixedSize(100, 25)
        self.quit_button.setFixedSize(100, 25)

        # Style Sheet Setting for Widgets
        self.open_file_button.setStyleSheet(
            """
            QPushButton {
                border: 2px solid #0044BA;
            }
            
            QPushButton:hover {
                background-color: #0044BA;
                color: white;
            }
            """
        )

        self.quit_button.setStyleSheet(
            """
            QPushButton {
                border: 2px solid #0044BA;
            }
            
            QPushButton:hover {
                background-color: #0044BA;
                color: white;
            }
            """
        )

    def design_layouts(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.setContentsMargins(0,0,0,0)

        self.main_layout.addWidget(self.header_label)
        self.main_layout.addWidget(self.open_file_button)
        self.main_layout.addWidget(self.quit_button)

        self.setLayout(self.main_layout)

    def connect_events(self):
        self.quit_button.clicked.connect(self.quit_button_clicked)

    """
    Custom Events that are used to slot an event for specific PyQT widgets like QPushButton/QLineEdit
    """
    def quit_button_clicked(self):
        quit()

    # event functions here

"""
Main Window:
- Holds HomePage Widget
- Holds PDF_Viewer_App Widget
Main Runner to run all other functionalities.
"""
class Runner_App(QWidget):
    def __init__(self):
        super().__init__()

        self.resize(ui_config.width, ui_config.height)
        self.setWindowTitle("Custom PDF Viewer")

        self.pages = QStackedWidget()

        self.home_page = HomePage()
        self.home_page.open_file_button.clicked.connect(self.open_file_button_clicked)
        self.pdf_app = PDF_Viewer_App()

        self.pages.addWidget(self.home_page)
        self.pages.addWidget(self.pdf_app)

        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.pages)

        self.pages.setCurrentIndex(0)
        self.setLayout(self.main_layout)

        # If we used the "Open with..." feature on windows, then open the PDF directly and skip to the main page.
        if len(argv) > 1:
            self.directory = argv[1]
            self.exec_open_pdf()
            
    # Direct calls to PDF App.
    def exec_open_pdf(self):
        self.pdf_app.exec_open_pdf_from_windows(self.directory)
        self.pages.setCurrentIndex(1)

    def open_file_button_clicked(self):
        status = self.pdf_app.get_new_directory()
        if status == 0:
            self.pages.setCurrentIndex(1)

"""
str_find_backwards attempts to find the character/string "find" in string starting at the end and working backwards.
"""
def str_find_backwards(string, find):
    for i in range(len(string)-1, -1, -1):
        if string[i] == find:
            return i+1
    return -1

app = QApplication([])
app.setWindowIcon(QIcon(os.path.join(base_directory, 'icons/pdf.ico')))
main_window = Runner_App()
main_window.show()

app.exec()