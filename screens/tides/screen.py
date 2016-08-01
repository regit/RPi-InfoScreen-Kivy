from kivy.uix.label import Label
from kivy.properties import DictProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen

import requests
import time
from datetime import datetime
import dateutil.parser
from dateutil import tz
import pytz

import json

class TidesScreen(Screen):
    tidesurl = "https://www.worldtides.info/api?extremes&lat={lat}&lon={lon}&length=172800&key={key}"
    timedata = DictProperty(None)

    def __init__(self, **kwargs):
        # Init data by checking cache then calling API
        self.location = kwargs["params"]["location"]
        self.key = kwargs["params"]["key"]
        self.get_data()
        self.get_next()
        self.get_time()
        super(TidesScreen, self).__init__(**kwargs)
        self.timer = None

    def buildURL(self, location):
        lon = location['coords']['lon']
        lat = location['coords']['lat']
        return self.tidesurl.format(key=self.key, lon=lon, lat=lat)

    def get_data(self):
        self.url_tides = self.buildURL(self.location)
        #with open('screens/tides/result.json') as data_file:    
        #    self.tides = json.load(data_file)
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
            date = dateutil.parser.parse(extreme['date'])
            if date > datetime.now(pytz.utc): 
                self.next = extreme
                #date.replace(tzinfo = tz.tzlocal())
                self.next["h"] = date.hour
                self.next["m"] = date.minute
                self.next["s"] = date.second
                date = dateutil.parser.parse(self.prev['date'])
                #date.replace(tzinfo = tz.tzlocal())
                self.prev["h"] = date.hour
                self.prev["m"] = date.minute
                self.prev["s"] = date.second
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
