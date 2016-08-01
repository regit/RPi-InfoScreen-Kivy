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
    next = DictProperty(None)
    prev = DictProperty(None)
    types_map = {"english": {"High": "HW", "Low": "LW"}, "french": { "High": "HM", "Low": "BM" }}

    def __init__(self, **kwargs):
        # Init data by checking cache then calling API
        self.location = kwargs["params"]["location"]
        self.key = kwargs["params"]["key"]
        self.language = kwargs["params"]["language"]
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
        if n >= self.next_extreme:
            self.get_next()

    def get_next(self):
        found = False
        prev = None
        for extreme in sorted(self.tides['extremes'], key=lambda extr: extr['dt']):
            date = dateutil.parser.parse(extreme['date']).replace(tzinfo=None)
            if date > datetime.now():
                next = extreme
                #date.replace(tzinfo = tz.tzlocal())
                next["h"] = date.hour
                next["m"] = date.minute
                next["s"] = date.second
                next["type_i18n"] = self.types_map[self.language][next["type"]]
                self.next_extreme = dateutil.parser.parse(extreme['date']).replace(tzinfo=None)
                date = dateutil.parser.parse(prev['date'])
                #date.replace(tzinfo = tz.tzlocal())
                prev["h"] = date.hour
                prev["m"] = date.minute
                prev["s"] = date.second
                prev["type_i18n"] = self.types_map[self.language][prev["type"]]
                self.next = next
                self.prev = prev
                break
            else:
                prev = extreme

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
