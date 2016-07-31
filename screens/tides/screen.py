from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
import requests
import time

class TidesScreen(Screen):
    "https://www.worldtides.info/api?extremes&lat={lat}&lon={lon}&length=1209600&maxcalls=5&key={key}"
    forecast = "http://api.wunderground.com/api/{key}/forecast/q/{location}"

    def __init__(self, **kwargs):
        super(TidesScreen, self).__init__(**kwargs)
        # Init data by checking cache then calling API

    def get_data(self):
            self.forecast = requests.get(self.url_forecast).json()
