from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, 
    QLabel, 
    QPushButton, 
    QVBoxLayout, 
    QHBoxLayout,
    QLineEdit 
)
from config import ConfigurationClass

class Scene(QWidget):
    def __init__(self):
        super().__init__()

        self.config = ConfigurationClass()
        self.create_widgets()
        self.design_widgets()
        self.design_layouts()
        #self.connect_events()

    def create_widgets(self):
        self.header = QLabel("Hi!")
        self.guide = QLabel("Type a location in the United States and press confirm to get started.")
        self.location_text_box = QLineEdit()
        self.confirm_button = QPushButton("CONFIRM")

    def design_widgets(self):
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header.setFont(self.config.default_font)

        self.guide.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.guide.setFont(self.config.default_font_small)

        self.location_text_box.setFixedSize(self.config.welcome_config.user_action_textbox_size)
        self.confirm_button.setFixedSize(self.config.welcome_config.user_action_button_size)
        self.confirm_button.setFont(self.config.default_font)

    def design_layouts(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.user_interaction_layout = QHBoxLayout()
        self.user_interaction_layout.addWidget(self.location_text_box)
        self.user_interaction_layout.addWidget(self.confirm_button)
        
        self.main_layout.addWidget(self.header)
        self.main_layout.addWidget(self.guide)
        self.main_layout.addLayout(self.user_interaction_layout)
        
        self.setLayout(self.main_layout)