from PyQt6.QtCore import QSize
from PyQt6.QtGui import QFont, QFontDatabase
import requests
"""
PRIVATE VARIABLES IF NOT IN class.__init__()
"""
default_font_directory = "resource/Roboto-Light.ttf"
"""
CLASSES/CONFIGS
"""
# °
class DetailsConfig():
    def __init__(self):
        pass
class WarningConfig():
    def __init__(self):
        self.no_weather_warning_messages = [
            "You're safe for this one."
        ]
class HomeConfig():
    def __init__(self):
        self.temperature_display_font_size = 80
class WelcomeConfig():
    def __init__(self):
        self.user_action_textbox_size = QSize(300,35)
        self.user_action_button_size = QSize(100,35)
class ConfigurationClass():
    def __init__(self):
        self.window_width=700

        self.scenes_available = {
            "welcome_scene":0,
            "home_scene":1,
            "warnings_scene":2,
            "details_scene":3
        }

        self.default_font_size = 15
        self.default_font_small_size = 8

        self.default_font = self.make_font(self.default_font_size)
        self.default_font_small = self.make_font(self.default_font_small_size)

        """
        base_url_api_geocoder -> {suggested location}?geoit=JSON
        base_url_api_weather -> {latitude},{longitude}

        check of the following:
        - error
        - throttled? (api limited)
        - must be in US due to NOAA limits
        """
        self.base_url_api_geocoder="https://geocode.xyz/"
        self.base_url_api_weather="https://api.weather.gov/points/"
        self.geocode_data=None
        self.weather_forecast_data=None
        self.weather_forecast_hourly_data=None

        #todo later
        self.alerts_data=None

        # configs for specific scenes
        self.welcome_config = WelcomeConfig()
        self.home_config = HomeConfig()
        self.warnings_config = WarningConfig()
    def make_default_QFont(self):
        """
        Returns QFont object with default settings.
        """
        qid = QFontDatabase.addApplicationFont(default_font_directory)
        # There is only 1 child font of the given Font Family.
        return QFont(QFontDatabase.applicationFontFamilies(qid)[0])
    def make_font(self, fontSize : int):
        font = self.make_default_QFont()
        font.setPointSize(fontSize)
        return font
    def get_API_data(self, suggested_location : str):
        """
        Returns (error_code [int], msg [str]) (type: tuple)
        enum error_code:
        - 3 | GEOCODE.XYZ exclusive | Province/Country must be US.
        - 2 |                       | Throttled API call.
        - 1 |                       | Error not listed in this docstring.
        - 0 | default               | successful

        msg [str] will be used to show as error msg for welcome_scene.guide QLabel.
        """
        # Multiple API calls to be stored for this variable.
        # geocode.xyz call to convert location to latt/longt coordinates.
        main_url = self.base_url_api_geocoder+suggested_location+"?geoit=JSON"
        api_call_holder = requests.get(main_url)

        geocode_data = api_call_holder.json()
        # Check Cases
        if 'error' in geocode_data:
            return (1,  f'An error occurred. Please try again.')
        # for geocode specifically, if throttled occurs all JSON data is encoded to "Throttled! .
        # for this in particular we'll retry the call 5 times, if it fails, then kill/ask to retry.
        elif geocode_data['latt'][:len("Throttled!")] == "Throttled!":
            return (2, f'Weather data could not be retrieved. Please try again after one second.')
        elif geocode_data['standard']['prov'] != 'US':
            return (3, f'Location must be in the United States.')
        
        latitude=round(float(geocode_data['latt']),4)
        longitude=round(float(geocode_data['longt']),4)

        # Get location weather BASE data
        main_url=self.base_url_api_weather+f'{str(latitude)},{str(longitude)}'
        api_call_holder = requests.get(main_url)
        # Throttled Error Case
        if api_call_holder.status_code == 403:
            return (2, f'Weather data could not be retrieved. Please try again after one second.')
        weather_forecast_data = api_call_holder.json()

        main_url=weather_forecast_data['properties']['forecast']
        main_url_2=weather_forecast_data['properties']['forecastHourly']

        # Get location weather FORECAST data
        api_call_holder = requests.get(main_url)
        # Throttled Error Case
        if api_call_holder.status_code == 403:
            return (2, f'Weather data could not be retrieved. Please try again after one second.')
        weather_forecast_data = api_call_holder.json()

        # Get location weather FORECAST HOURLY data
        api_call_holder = requests.get(main_url_2)
        # Throttled Error Case
        if api_call_holder.status_code == 403:
            return (2, f'Weather data could not be retrieved. Please try again after one second.')
        weather_forecast_hourly_data = api_call_holder.json()

        # If no errors show up, assume successful and set class variables.
        self.geocode_data = geocode_data
        self.weather_forecast_data = weather_forecast_data
        self.weather_forecast_hourly_data = weather_forecast_hourly_data
        return (0, "")