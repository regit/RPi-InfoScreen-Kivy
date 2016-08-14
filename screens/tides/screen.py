from kivy.uix.label import Label
from kivy.properties import DictProperty, StringProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView

import requests
import time
from datetime import datetime
import dateutil.parser
from dateutil import tz
import pytz

import json
import locale

MIN_TIDES = 7

TYPES_MAP = {"english": {"High": "HW", "Low": "LW"}, "french": { "High": "HM", "Low": "BM" }}

class Tide(BoxLayout):
    desc = StringProperty("")

    def __init__(self, **kwargs):
        super(Tide, self).__init__(**kwargs)
        self.language = kwargs["language"]
        self.buildText(kwargs["summary"])

    def buildText(self, summary):
        summary["ldate"] = dateutil.parser.parse(summary["date"]).astimezone(tz.tzlocal()).strftime("%A, %H:%M")
        summary["type_i18n"] = TYPES_MAP[self.language][summary["type"]]
        self.desc = ("{type_i18n:s}\n{ldate:s}").format(**summary)

class TidesScreen(Screen):
    tidesurl = "https://www.worldtides.info/api?extremes&lat={lat}&lon={lon}&length=172800&key={key}"
    timedata = DictProperty(None)
    next_t = DictProperty(None)
    prev_t = DictProperty(None)
    location = DictProperty(None)

    def __init__(self, **kwargs):
        # Init data by checking cache then calling API
        self.location = kwargs["params"]["location"]
        self.key = kwargs["params"]["key"]
        self.language = kwargs["params"]["language"]
        if self.language == "french":
            locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
        self.get_data()
        self.get_time()
        self.get_next()
        super(TidesScreen, self).__init__(**kwargs)
        self.timer = None
        self.tides_list = self.ids.tides_list
        self.build_tides_list()

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
        n = datetime.utcnow()
        if hasattr(self, "next_extreme") and n >= self.next_extreme:
            self.get_next()

    def get_next(self):
        if self.tides == None or self.tides['status'] != 200:
            self.prev_t = {}
            self.next_t = {}
            return
        found = False
        prev = None
        oldentries = []
        for extreme in self.tides['extremes']:
            date = dateutil.parser.parse(extreme['date'])
            if date > datetime.now(tz = tz.tzutc()):
                next = extreme
                date = date.astimezone(tz.tzlocal())
                next["h"] = date.hour
                next["m"] = date.minute
                next["s"] = date.second
                next["type_i18n"] = TYPES_MAP[self.language][next["type"]]
                self.next_extreme = dateutil.parser.parse(extreme['date']).replace(tzinfo=None)
                date = dateutil.parser.parse(prev['date'])
                date = date.astimezone(tz.tzlocal())
                prev["h"] = date.hour
                prev["m"] = date.minute
                prev["s"] = date.second
                prev["type_i18n"] = TYPES_MAP[self.language][prev["type"]]
                self.next_t = next
                self.prev_t = prev
                break
            else:
                if prev:
                    oldentries.append(prev)
                prev = extreme
        # clean up old entries
        self.tides['extremes'] = [x for x in self.tides['extremes'] if x not in oldentries]
        # fetch new one if our set is small
        if len(self.tides['extremes']) <= MIN_TIDES:
            self.get_data()
        if hasattr(self, "tides_list"):
            self.build_tides_list()

    def build_tides_list(self):
        self.tides_list.clear_widgets()

        w = (len(self.tides['extremes']) - 1) * 150
        tl = BoxLayout(orientation="horizontal", size=(w, 60),
                    size_hint=(None, 1), spacing=5)
        sv = ScrollView(size_hint=(1, 1.1), bar_margin = -5, do_scroll_y = False)
        sv.add_widget(tl)
        for tide in self.tides['extremes']:
            if self.next_t["dt"] < tide["dt"]:
                uptide = Tide(summary = tide, language = self.language)
                tl.add_widget(uptide)
        self.tides_list.add_widget(sv)

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
