from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
import requests
import time

class TidesScreen(Screen):
    tidesurl = "https://www.worldtides.info/api?extremes&lat={lat}&lon={lon}&length=86400&key={key}"

    def __init__(self, **kwargs):
        super(TidesScreen, self).__init__(**kwargs)
        # Init data by checking cache then calling API
        self.location = kwargs["params"]["location"]
        self.key = kwargs["params"]["key"]
        self.get_data()
        self.get_next()

    def buildURL(self, location):
        lon = location['coords']['lon']
        lat = location['coords']['lat']
        return self.tidesurl.format(key=self.key, lon=lon, lat=lat)

    def get_data(self):
        self.url_tides = self.buildURL(self.location)
        try:
            self.tides = requests.get(self.url_tides).json()
        except:
            self.tides = None

    def get_next(self):
        for extreme in self.tides['extremes']:
            if extreme['dt'] > time.time(): 
                t = time.gmtime(extreme['dt'])
                self.next = extreme
                self.next["h"] = t.tm_hour
                self.next["m"] = t.tm_min
                self.next["s"] = t.tm_sec
                break
