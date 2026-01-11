from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, 
    QLabel, 
    QVBoxLayout, 
    QScrollArea
)
from config import ConfigurationClass
import random

class TextLabel(QLabel):
    def __init__(self, text, font):
        """
        font -> QFont Type
        """
        super().__init__(text=text)
        self.setFont(font)

class WarningWidget(QWidget):
    def __init__(self, config : ConfigurationClass):
        super().__init__()
        self.config = config
        self.main_layout = QVBoxLayout()

        self.status_label = TextLabel("WARNING", config.default_font)
        self.message_label = TextLabel("...",config.default_font_small)
        self.message_label.setWordWrap(True)
        
        self.main_layout.addWidget(self.status_label)
        self.main_layout.addWidget(self.message_label)

        self.setLayout(self.main_layout)

class Scene(QWidget):
    def __init__(self):
        super().__init__()

        self.config = ConfigurationClass()
        self.create_widgets()
        self.design_widgets()
        self.design_layouts()
        self.connect_events()

    def create_widgets(self):
        self.header_alert_amount = TextLabel("3 weather alerts.", self.config.default_font)
        self.no_weather_warnings = TextLabel(random.choice(self.config.warnings_config.no_weather_warning_messages), self.config.default_font_small)
        self.scrolling_widget = QWidget()
        self.scrolling_area_warnings = QScrollArea()

    def design_widgets(self):
        self.header_alert_amount.setMaximumHeight(35)
        self.header_alert_amount.setMinimumHeight(35)
        self.header_alert_amount.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.no_weather_warnings.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_weather_warnings.setVisible(False)

    def design_layouts(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(15,15,15,15)

        self.scrolling_area_layout = QVBoxLayout()
        self.scrolling_area_layout.setContentsMargins(0,0,0,0)
        self.scrolling_area_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scrolling_widget.setLayout(self.scrolling_area_layout)

        self.scrolling_area_warnings.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrolling_area_warnings.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrolling_area_warnings.setWidgetResizable(True)
        self.scrolling_area_warnings.setWidget(self.scrolling_widget)

        self.main_layout.addWidget(self.header_alert_amount)
        self.main_layout.addWidget(self.no_weather_warnings)
        self.main_layout.addWidget(self.scrolling_area_warnings)

        self.setLayout(self.main_layout)

    def connect_events(self):
        pass