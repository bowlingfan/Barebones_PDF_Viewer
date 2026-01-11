from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, 
    QWidget, 
    QVBoxLayout, 
    QStackedWidget,
    QStackedLayout,
    QPushButton
)
from scenes import (
    details_scene,
    welcome_scene,
    home_scene,
    warnings_scene,
)
from config import ConfigurationClass
#import inspect
#import os

class UIButton(QPushButton):
    def __init__(self, text, font):
        """
        font -> QFont Type
        """
        super().__init__(text=text)
        self.setFont(font)
        
class MainApplication(QWidget):
    def __init__(self):
        super().__init__()

        self.config = ConfigurationClass()
        self.resize(self.config.window_width,self.config.window_width//2)
        self.setWindowTitle("Weather Application")

        self.create_widgets()
        self.design_widgets()
        self.design_layouts()
        self.connect_events()
    """
    Creating/Setup QT Window
    """
    def create_widgets(self):
        self.menu_widget = QWidget()
        self.menu_button_holder_widget = QWidget()
        self.menu_button = UIButton("MENU", self.config.default_font)

        self.home_button = UIButton("Home", self.config.default_font_small)
        self.warnings_button = UIButton("Warnings", self.config.default_font_small)
        self.details_button = UIButton("Details", self.config.default_font_small)

        self.scenes = QStackedWidget()
        self.welcome_scene = welcome_scene.Scene()
        self.home_scene = home_scene.Scene()
        self.warnings_scene = warnings_scene.Scene()
        self.details_scene = details_scene.Scene()

    def design_widgets(self):
        self.menu_button.setMaximumSize(35,35)
        self.menu_button.setMinimumSize(0,35)
        self.menu_button_holder_widget.setMaximumSize(50,50)
        self.menu_widget.setVisible(False)
        #later
        #self.menu_button.setVisible(True)

    def design_layouts(self):
        self.main_layout = QStackedLayout()
        self.main_layout.setStackingMode(QStackedLayout.StackingMode.StackAll) 

        """
        scenes setup
        """
        self.scenes.addWidget(self.welcome_scene)
        self.scenes.addWidget(self.home_scene)
        self.scenes.addWidget(self.warnings_scene)
        self.scenes.addWidget(self.details_scene)
        self.scenes.setCurrentIndex(self.config.scenes_available["welcome_scene"])
        """
        menu widget/button setup.

        local variables: menu_button_holder_layout & menu_widget_layout
        since they SHOULDN'T BE used other than to organize QT widgets.
        """
        menu_button_holder_layout = QVBoxLayout()
        menu_button_holder_layout.setAlignment(Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignLeft)
        menu_button_holder_layout.setContentsMargins(15,15,0,0)
        menu_button_holder_layout.setSpacing(0)
        menu_button_holder_layout.addWidget(self.menu_button)
        self.menu_button_holder_widget.setLayout(menu_button_holder_layout)

        menu_widget_layout = QVBoxLayout()
        menu_widget_layout.setAlignment(Qt.AlignmentFlag.AlignCenter|Qt.AlignmentFlag.AlignLeft)
        menu_widget_layout.setContentsMargins(15,0,0,0)
        menu_widget_layout.setSpacing(5)
        menu_widget_layout.addWidget(self.home_button)
        menu_widget_layout.addWidget(self.warnings_button)
        menu_widget_layout.addWidget(self.details_button)
        self.menu_widget.setLayout(menu_widget_layout)

        """
        main page setup
        """
        self.main_layout.addWidget(self.scenes)
        self.main_layout.addWidget(self.menu_widget)
        self.main_layout.addWidget(self.menu_button_holder_widget)

        self.setLayout(self.main_layout)

    def connect_events(self):
        self.welcome_scene.confirm_button.clicked.connect(self.welcome_confirm_button_clicked)
        self.menu_button.clicked.connect(self.menu_button_clicked)
        self.home_button.clicked.connect(self.home_button_clicked)
        self.warnings_button.clicked.connect(self.warnings_button_clicked)
        self.details_button.clicked.connect(self.details_button_clicked)

    def menu_button_clicked(self):
        self.menu_widget.setVisible(not self.menu_widget.isVisible())
    def home_button_clicked(self):
        self.request_change_scene("home_scene")
    def warnings_button_clicked(self):
        self.request_change_scene("warnings_scene")
    def details_button_clicked(self):
        self.request_change_scene("details_scene")
    """
    Cross-scene events:
        Events that occur within another scene that require changes to MainApplication QWidget.
    """
    def welcome_confirm_button_clicked(self):
        location_text = self.welcome_scene.location_text_box.text()
        if location_text == "":
            self.welcome_scene.guide.setText("Provide a location before pressing confirm.")
            return
        """
        self.config.get_API_data > (error_code [0], msg [1])
        """
        result = self.config.get_API_data(location_text)
        if result[0] != 0:
            self.welcome_scene.guide.setText(result[1])
        else:
            self.request_change_scene("home_scene")
    """
    Utility functions 
    """
    def request_change_scene(self, new_scene):
        if new_scene not in self.config.scenes_available:
            raise BaseException("SCENE NOT VALID")
        self.scenes.setCurrentIndex(self.config.scenes_available[new_scene])

app = QApplication([])

main_window = MainApplication()
#solves dilemma with text files randomly being open in other places
#filename = inspect.getframeinfo(inspect.currentframe()).filename
##path     = os.path.dirname(os.path.abspath(filename))
#print(path)
main_window.show()
app.exec()