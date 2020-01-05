import datetime
import logic
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen


from kivymd.app import MDApp
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.label import MDLabel

from kivy.core.window import Window
Window.size = (720 // 2, 1280 // 2)


with open('moneymanager.kv') as f:
    KV = f.read()

App = logic.MoneyManagerAppManager()


class ScreensOptions:
    date = str(datetime.date.today())

    def back_to_main_menu(self, direction):
        self.manager.transition.direction = direction
        self.manager.transition.duration = .3
        self.manager.current = 'main_screen'

    def enter_income_expense(self):
        main_scr = self.manager.get_screen('main_screen')
        current_money = App.get_current_money()
        main_scr.ids.balance.text = 'Balance: ' + str(current_money)
        self.text_input_sum.text = ''
        self.text_input_description.text = ''
        self.back_to_main_menu()


class MainScreen(Screen):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        Clock.schedule_once(self.init_ui, 0)

    def init_ui(self, dt=0):
        day_add = App.get_day_add_money(ScreensOptions.date)
        day_waste = App.get_all_day_waste(ScreensOptions.date)
        current_money = App.get_current_money()
        self.income.text = 'Income: ' + str(day_add)
        self.expense.text = 'Expense: ' + str(day_waste)
        self.balance.text = 'Balance: ' + str(current_money)

    def open_settings(self):
        self.manager.transition.direction = 'left'
        self.manager.transition.duration = .3
        self.manager.current = 'settings_screen'


class IncomeScreen(Screen, ScreensOptions):

    def back_to_main_menu(self):
        return ScreensOptions.back_to_main_menu(self, 'down')

    def enter_income_expense(self):
        return ScreensOptions.enter_income_expense(self)

    def add_m(self):
        sum_ = self.text_input_sum.text
        description = self.text_input_description.text
        if sum_ != '' and description != '':
            App.add_new_money(abs(int(sum_)), description)
            day_add = App.get_day_add_money(ScreensOptions.date)

            main_scr = self.manager.get_screen('main_screen')
            main_scr.ids.income.text = 'Income: ' + str(day_add)

            self.enter_income_expense()


class ExpenseScreen(Screen, ScreensOptions):

    def back_to_main_menu(self):
        return ScreensOptions.back_to_main_menu(self, 'down')

    def add_w(self):
        sum_ = self.text_input_sum.text
        description = self.text_input_description.text
        if sum_ != '' and description != '':
            App.add_waste(abs(int(sum_)), description)
            day_waste = App.get_all_day_waste(ScreensOptions.date)

            main_scr = self.manager.get_screen('main_screen')
            main_scr.ids.expense.text = 'Expense: ' + str(day_waste)

            inf_scr = self.manager.get_screen('info_screen')
            inf_scr.cls_widgets()
            inf_scr.init_ui()

            self.enter_income_expense()


class InfoItems(MDLabel):
    pass


class InfoScreen(Screen, ScreensOptions):

    def __init__(self, **kwargs):
        super(InfoScreen, self).__init__(**kwargs)
        Clock.schedule_once(self.init_ui, 0)

    def init_ui(self, dt=0):
        day_wastes_and_descriptions = App.get_day_wastes_and_descriptions(
            date=ScreensOptions.date, operation='add_waste')
        day_wastes = day_wastes_and_descriptions[0]
        day_description = day_wastes_and_descriptions[1]
        day_wastes_times = App.get_day_wastes_times(
            date=ScreensOptions.date, operation='add_waste')
        n = 0
        for i, j, time in zip(day_wastes, day_description, day_wastes_times):
            n += 1
            text_info = ''
            text_info += '\n{}) [{}]\nWaste: {}\nDescription: {}\n'.format(
                n, time, i, j)
            self.scroll.add_widget(
                InfoItems(text=text_info))

    def cls_widgets(self):
        self.scroll.clear_widgets()

    def back_to_main_menu(self):
        return ScreensOptions.back_to_main_menu(self, 'down')


class SettingsScreen(Screen, ScreensOptions):

    def back_to_main_menu(self):
        return ScreensOptions.back_to_main_menu(self, 'right')


class MoneyMApp(MDApp):

    def __init__(self, **kwargs):
        self.title = "Money manager"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "LightGreen"
        super().__init__(**kwargs)

    def build(self):
        return Builder.load_string(KV)


MoneyMApp().run()
