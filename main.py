import datetime
import logic
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

from kivymd.app import MDApp
from kivymd.uix.navigationdrawer import MDNavigationDrawer

from kivy.core.window import Window
Window.size = (720 // 2, 1280 // 2)


with open('moneymanager.kv') as f:
    KV = f.read()

App = logic.MoneyManagerAppManager()
class MainScreen(Screen):
    def open_settings(self):
        self.manager.transition.direction = 'left'
        self.manager.transition.duration = .3
        self.manager.current = 'settings_screen'
    def add_m(self):
        date = str(datetime.date.today())
        App.add_new_money(100, 'androidtest1')
        s = App.get_day_add_money(date)
        self.incomes.text = str(s)
class InfoScreen(Screen):
    pass
class SettingsScreen(Screen):
    pass


class MoneyMApp(MDApp):

    def __init__(self, **kwargs):
        self.title = "Money manager"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        super().__init__(**kwargs)

    def build(self):
        return Builder.load_string(KV)


MoneyMApp().run()
