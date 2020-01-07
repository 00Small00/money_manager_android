import datetime
import logic

from kivy.base import stopTouchApp
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen


from kivymd.app import MDApp
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.label import MDLabel

from kivy.core.window import Window
Window.size = (720 // 2, 1280 // 2)

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

    def init_ui(self, dt=0, state='Day'):
        if state == 'Day':
            day_add = App.get_day_add_money(ScreensOptions.date)
            day_waste = App.get_all_day_waste(ScreensOptions.date)
        elif state == 'Month':
            day_add = App.get_month_add_money(str(datetime.date.today())[
                                              5:7], str(datetime.date.today())[0:4])
            day_waste = App.get_all_month_waste(str(datetime.date.today())[
                                                5:7], str(datetime.date.today())[0:4])
        elif state == 'Year':
            day_add = App.get_year_add_money(str(datetime.date.today())[0:4])
            day_waste = App.get_all_year_waste(str(datetime.date.today())[0:4])

        current_money = App.get_current_money()
        self.income.text = 'Income: ' + str(day_add)
        self.expense.text = 'Expense: ' + str(day_waste)
        self.balance.text = 'Balance: ' + str(current_money)

    def open_settings(self):
        self.manager.transition.direction = 'left'
        self.manager.transition.duration = .3
        self.manager.current = 'settings_screen'

    def state_day(self):
        self.init_ui()
        self.state_text.text = 'Day info:'

    def state_month(self):
        self.init_ui(state='Month')
        self.state_text.text = 'Month info:'

    def state_year(self):
        self.init_ui(state='Year')
        self.state_text.text = 'Year info:'


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
            day_waste = App.get_all_day_waste(ScreensOptions.date)

            main_scr = self.manager.get_screen('main_screen')
            main_scr.ids.income.text = 'Income: ' + str(day_add)
            main_scr.state_text.text = 'Day info:'
            main_scr.ids.expense.text = 'Expense: ' + str(day_waste)

            inf_scr = self.manager.get_screen('info_screen')
            inf_scr.cls_widgets()
            inf_scr.init_ui(operation='add_new_money')
            inf_scr.ids.info_text.text = 'Income day info:'

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
            day_add = App.get_day_add_money(ScreensOptions.date)

            main_scr = self.manager.get_screen('main_screen')
            main_scr.ids.expense.text = 'Expense: ' + str(day_waste)
            main_scr.state_text.text = 'Day info:'
            main_scr.ids.income.text = 'Income: ' + str(day_add)

            inf_scr = self.manager.get_screen('info_screen')
            inf_scr.cls_widgets()
            inf_scr.init_ui(operation='add_waste')
            inf_scr.ids.info_text.text = 'Expense day info:'

            self.enter_income_expense()


class InfoItems(MDLabel):
    pass


class InfoScreen(Screen, ScreensOptions):

    def __init__(self, **kwargs):
        super(InfoScreen, self).__init__(**kwargs)
        Clock.schedule_once(self.init_ui, 0)

    def init_ui(self, dt=0, operation='add_waste'):
        day_wastes_and_descriptions = App.get_day_wastes_and_descriptions(
            date=ScreensOptions.date, operation=operation)
        day_wastes = day_wastes_and_descriptions[0]
        day_description = day_wastes_and_descriptions[1]
        day_wastes_times = App.get_day_wastes_times(
            date=ScreensOptions.date, operation=operation)

        n = 0
        for i, j, time in zip(day_wastes, day_description, day_wastes_times):
            n += 1
            text_info = ''
            text_info += '\n{}) [{}]\nSum: {}\nDescription: {}\n'.format(
                n, time, i, j)
            self.scroll.add_widget(
                InfoItems(text=text_info))

    def cls_widgets(self):
        self.scroll.clear_widgets()

    def info_tabs(self, tab_operation, tab_text):
        self.ids.info_text.text = tab_text
        self.cls_widgets()
        self.init_ui(operation=tab_operation)

    def back_to_main_menu(self):
        return ScreensOptions.back_to_main_menu(self, 'down')


class SettingsScreen(Screen, ScreensOptions):

    def clear_database(self):
        App.clear_database()
        self.ids.clear_bt.text = 'Reload app!'

    def back_to_main_menu(self):
        return ScreensOptions.back_to_main_menu(self, 'right')


class MainScreenManager(BoxLayout):

    def __init__(self, **kwargs):
        super(MainScreenManager, self).__init__(**kwargs)
        Window.bind(on_keyboard=self._key_handler)

    def _key_handler(self, instance, key, *args):
        if key is 27:
            self.set_previous_screen()
            return True

    def set_previous_screen(self):
        current_screen = self.screen_manager.current
        if current_screen != 'main_screen':
            if current_screen == 'info_screen' \
                    or current_screen == 'income_screen' \
                    or current_screen == 'expense_screen':
                self.back_to_main_menu('down')
            elif current_screen == 'settings_screen':
                self.back_to_main_menu('right')
        else:
            stopTouchApp()

    def back_to_main_menu(self, direction):
        self.screen_manager.transition.direction = direction
        self.screen_manager.transition.duration = .3
        self.screen_manager.current = 'main_screen'


class MoneyMApp(MDApp):

    def __init__(self, **kwargs):
        self.title = "Money manager"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "DeepPurple"
        super().__init__(**kwargs)

    def build(self):
        return Builder.load_file('moneymanager.kv')


MoneyMApp().run()
