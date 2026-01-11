from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, 
    QLabel, 
    QVBoxLayout, 
    QHBoxLayout, 
)
from config import ConfigurationClass

class TextLabel(QLabel):
    def __init__(self, text, font):
        """
        font -> QFont Type
        """
        super().__init__(text=text)
        self.setFont(font)
        self.setMaximumHeight(15)

class Scene(QWidget):
    def __init__(self):
        super().__init__()

        self.config = ConfigurationClass()
        self.create_widgets()
        self.design_widgets()
        self.design_layouts()
        #self.connect_events()

    def create_widgets(self):
        self.location_header = TextLabel("Location Test", self.config.default_font)
        self.temperature_display = TextLabel("75°",self.config.make_font(self.config.home_config.temperature_display_font_size))
        # detailed
        self.feels_like_display = TextLabel("Feels like: ", self.config.default_font_small)
        self.preciptation_display = TextLabel("Preciptation: ", self.config.default_font_small)
        self.wind_display = TextLabel("Wind: 6 N", self.config.default_font_small)
        self.message = TextLabel("Aren't you excited? It's sunny.", self.config.default_font_small)

    def design_widgets(self):
        self.location_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.location_header.setFont(self.config.default_font)

        self.temperature_display.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)
        self.temperature_display.setMaximumHeight(self.config.window_width//2)

        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def design_layouts(self):
        self.main_layout = QVBoxLayout()

        self.header_row = QHBoxLayout()
        self.header_row.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
        self.main_info_row = QHBoxLayout()
        self.main_info_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.detailed_info = QVBoxLayout()
        self.detailed_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.msg_row = QHBoxLayout()
        self.msg_row.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.header_row.addWidget(self.location_header)
        self.main_info_row.addWidget(self.temperature_display)
        self.main_info_row.addLayout(self.detailed_info)
        self.detailed_info.addWidget(self.feels_like_display)
        self.detailed_info.addWidget(self.preciptation_display)
        self.detailed_info.addWidget(self.wind_display)
        self.msg_row.addWidget(self.message)

        self.main_layout.addLayout(self.header_row)
        self.main_layout.addLayout(self.main_info_row)
        self.main_layout.addLayout(self.msg_row)

        self.setLayout(self.main_layout)
    
    def connect_events(self):
        pass