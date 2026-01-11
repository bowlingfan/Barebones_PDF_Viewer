from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QStackedLayout, 
    QWidget, 
    QLabel, 
    QPushButton, 
    QVBoxLayout, 
    QHBoxLayout, 
)
from config import ConfigurationClass

class UIButton(QPushButton):
    def __init__(self, text, font):
        """
        font -> QFont Type
        """
        super().__init__(text=text)
        self.setFont(font)

class TextLabel(QLabel):
    def __init__(self, text, font):
        """
        font -> QFont Type
        """
        super().__init__(text=text)
        self.setFont(font)
        self.setMaximumHeight(15)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

class Scene(QWidget):
    def __init__(self):
        super().__init__()

        self.config = ConfigurationClass()
        self.create_widgets()
        self.design_widgets()
        self.design_layouts()
        self.connect_events()

    def create_widgets(self):
        self.decrement_day_button = UIButton("<",self.config.default_font)
        self.increment_day_button = UIButton(">",self.config.default_font)
        self.day_display = TextLabel("Sunday - January 11th",self.config.default_font)

        self.temperature_high_display = TextLabel("high temperature 10°",self.config.default_font_small)
        self.temperature_low_display = TextLabel("low temperature 10°",self.config.default_font_small)
        self.precipitation_chance_display = TextLabel("precip 75%",self.config.default_font_small)
        self.wind_display = TextLabel("10 mph SW",self.config.default_font_small)
        self.forecasted_weather_display = TextLabel("Partly Sunny",self.config.default_font)

        self.precipitation_bar = QWidget()

    def design_widgets(self):
        self.precipitation_bar.setFixedHeight(200)
        self.precipitation_bar.setStyleSheet("""
            QWidget {
                background-color: #0083FF
            }
        """)
        self.decrement_day_button.setFixedSize(35,35)
        self.increment_day_button.setFixedSize(35,35)
        self.day_display.setMaximumHeight(35)
        self.forecasted_weather_display.setMaximumHeight(35)

    def design_layouts(self):
        self.main_layout = QStackedLayout()
        self.main_layout.setStackingMode(QStackedLayout.StackingMode.StackAll)

        # Only used to add to QStackedLayout. Should not be used anywhere else.
        container_widget = QWidget()
        self.container_layout = QVBoxLayout()

        # Only used to add to QStackedLayout. Should not be used anywhere else.
        precipitation_bar_holder = QWidget()
        precipitation_bar_holder_layout = QVBoxLayout()

        precipitation_bar_holder_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        precipitation_bar_holder_layout.setContentsMargins(0,0,0,0)
        precipitation_bar_holder_layout.addWidget(self.precipitation_bar)

        self.day_display_row = QHBoxLayout()
        self.detailed_info_layout = QVBoxLayout()

        self.day_display_row.addWidget(self.decrement_day_button, 0, Qt.AlignmentFlag.AlignRight)
        self.day_display_row.addSpacing(10)
        self.day_display_row.addWidget(self.day_display)
        self.day_display_row.addSpacing(10)
        self.day_display_row.addWidget(self.increment_day_button, 0, Qt.AlignmentFlag.AlignLeft)

        self.detailed_info_layout.addWidget(self.temperature_high_display)
        self.detailed_info_layout.addWidget(self.temperature_low_display)
        self.detailed_info_layout.addWidget(self.precipitation_chance_display)
        self.detailed_info_layout.addWidget(self.wind_display)
        self.detailed_info_layout.addWidget(self.forecasted_weather_display)

        self.container_layout.setContentsMargins(65,15,65,15)
        self.container_layout.addLayout(self.day_display_row,2)
        self.container_layout.addLayout(self.detailed_info_layout)
        """
        final changes
        """
        container_widget.setLayout(self.container_layout)
        precipitation_bar_holder.setLayout(precipitation_bar_holder_layout)

        self.main_layout.addWidget(precipitation_bar_holder)
        self.main_layout.addWidget(container_widget)

        self.setLayout(self.main_layout)

    def connect_events(self):
        pass