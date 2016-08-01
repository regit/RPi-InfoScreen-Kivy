from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
import requests
import time

class TidesScreen(Screen):
    tidesurl = "https://www.worldtides.info/api?extremes&lat={lat}&lon={lon}&length=86400&key={key}"

    def __init__(self, **kwargs):
        # Init data by checking cache then calling API
        self.location = kwargs["params"]["location"]
        self.key = kwargs["params"]["key"]
        self.get_data()
        self.get_next()
        super(TidesScreen, self).__init__(**kwargs)

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

    def get_time(self):
        """Sets self.timedata to current time."""
        n = datetime.now()
        self.timedata["h"] = n.hour
        self.timedata["m"] = n.minute
        self.timedata["s"] = n.second

    def get_next(self):
        found = False
        for extreme in sorted(self.tides['extremes'], key=lambda extr: extr['dt']):
            if extreme['dt'] > time.time(): 
                t = time.gmtime(extreme['dt'])
                self.next = extreme
                self.next["h"] = t.tm_hour
                self.next["m"] = t.tm_min
                self.next["s"] = t.tm_sec
                t = time.gmtime(self.prev['dt'])
                self.prev["h"] = t.tm_hour
                self.prev["m"] = t.tm_min
                self.prev["s"] = t.tm_sec
                break
            else:
                self.prev = extreme

    def update(self, dt):
        self.get_time()

    def on_enter(self):
        # We only need to update the clock every second.
        self.timer = Clock.schedule_interval(self.update, 1)

    def on_pre_enter(self):
        self.get_time()

    def on_pre_leave(self):
        # Save resource by unscheduling the updates.
        Clock.unschedule(self.timer)
