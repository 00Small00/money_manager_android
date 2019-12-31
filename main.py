from kivy.uix.boxlayout import BoxLayout

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.uix.list import OneLineListItem


from kivy.core.window import Window
Window.size = (720//2, 1280//2)

from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel

with open('moneymanager.kv') as f:
    KV = f.read() 


class ContentNavigationDrawer(BoxLayout):
    def testrealise(self):
        print('Hello')




class TestNavigationDrawer(MDApp):
    def build(self):
        return Builder.load_string(KV)


TestNavigationDrawer().run()