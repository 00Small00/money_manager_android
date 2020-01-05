from kivy.utils import platform
import datetime
import tinydb
import os
android_path = '/storage/emulated/0/Android/data/'
path_exist = os.path.isdir(android_path + 'com.moneymanager')
if platform == 'android':
    if path_exist == False:
        os.mkdir(android_path + 'com.moneymanager')


class DataBaseTinyDB:
    date = str(datetime.date.today())
    time = datetime.datetime.now().time().strftime('%H:%M:%S')
    dbQuery = tinydb.Query()

    def __init__(self, name):

        if platform == 'android':
            self.db = tinydb.TinyDB(
                '/storage/emulated/0/Android/data/com.moneymanager/' + name + '.json')
        else:
            self.db = tinydb.TinyDB(name + '.json')

        if self.db.all() != []:
            self.current_money = [i['current_money']
                                  for i in self.db.all()][-1]
        else:
            self.current_money = 0

    def add_waste(self, waste, description):
        self.current_money
        self.current_money -= waste
        self.db.insert({'date': DataBaseTinyDB.date, 'time': DataBaseTinyDB.time,
                        'current_money': self.current_money,
                        'description': description, 'waste': waste, 'operation': 'add_waste'})

    def add_new_money(self, waste, description):
        self.current_money
        self.current_money += waste
        self.db.insert({'date': DataBaseTinyDB.date, 'time': DataBaseTinyDB.time,
                        'current_money': self.current_money,
                        'description': description, 'waste': waste, 'operation': 'add_new_money'})

    def get_current_money(self):
        return self.current_money

    def get_all_day_waste(self, date):
        get_day_info = [i['waste'] for i in self.db.search(DataBaseTinyDB.dbQuery.date == date) if i[
            'operation'] == 'add_waste']
        return sum(get_day_info)

    def get_day_add_money(self, date):
        get_day_info = [i['waste'] for i in self.db.search(DataBaseTinyDB.dbQuery.date == date) if i[
            'operation'] == 'add_new_money']
        return sum(get_day_info)

    def get_day_wastes_and_descriptions(self, date, operation):
        day_wastes = [i['waste'] for i in self.db.search(DataBaseTinyDB.dbQuery.date == date) if i[
            'operation'] == operation]
        day_description = [i['description'] for i in self.db.search(DataBaseTinyDB.dbQuery.date == date) if i[
            'operation'] == operation]

        return day_wastes, day_description

    def get_day_wastes_times(self, date, operation):
        day_times = [i['time'] for i in self.db.search(DataBaseTinyDB.dbQuery.date == date) if i[
            'operation'] == operation]
        return day_times


class DataManipulateConsole:
    date = str(datetime.date.today())

    def __init__(self):
        pass

    def show_day_data(self, current_money, all_day_waste, date):
        return '[{}] (Current money: {}): \nToday waste: {}'.format(date, current_money, all_day_waste)

    def show_day_info(self, day_wastes_and_descriptions, day_wastes_times):
        day_wastes = day_wastes_and_descriptions[0]
        day_description = day_wastes_and_descriptions[1]
        text = ''
        n = 0
        for i, j, time in zip(day_wastes, day_description, day_wastes_times):
            n += 1
            text += '{}) [{}] waste: {}; description: "{}";\n'.format(
                n, time, i, j)
        return text


class MoneyManagerAppManager:

    def __init__(self, database_name='default', database=DataBaseTinyDB, data_manipulate_method=None):
        self._database = database(database_name)
        self._data_manipulate_method = data_manipulate_method

    @property
    def database(self):
        return self._database

    def add_waste(self, waste, description):
        return self._database.add_waste(waste, description)

    def add_new_money(self, waste, description):
        return self._database.add_new_money(waste, description)

    def get_current_money(self):
        return self._database.get_current_money()

    def get_all_day_waste(self, date):
        return self._database.get_all_day_waste(date)

    def get_day_add_money(self, date):
        return self._database.get_day_add_money(date)

    def get_day_wastes_and_descriptions(self, date, operation):
        return self._database.get_day_wastes_and_descriptions(date, operation)

    def get_day_wastes_times(self, date, operation):
        return self._database.get_day_wastes_times(date, operation)

    def show_day_data(self, date):
        return self._data_manipulate_method.show_day_data(self, self.get_current_money(), self.get_all_day_waste(date), date)

    def show_day_info(self, date, operation):
        return self._data_manipulate_method.show_day_info(self, self.get_day_wastes_and_descriptions(date, operation), self.get_day_wastes_times(date, operation))
# Tests


def add_waste_test(App):
    return App.add_waste(4, 'classtest444443')


def add_money_test(App):
    return App.add_new_money(100, 'classtest1')


def get_current_money_test(App):
    return 'Current money: {}'.format(App.get_current_money())


def get_day_waste_test(App):
    return 'Today waste: {}'.format(App.get_all_day_waste(str(datetime.date.today())))


def get_day_add_money_test(App):
    return 'Today added money: {}'.format(
        App.get_day_add_money(str(datetime.date.today())))


def get_day_wastes_and_descriptions_test(App):
    return App.get_day_wastes_and_descriptions(str(datetime.date.today()), 'add_waste')


def show_day_data_test(App):
    return App.show_day_data(str(datetime.date.today()))


def main():
    App = MoneyManagerAppManager(
        database_name='test', data_manipulate_method=DataManipulateConsole)
    all_d = [i for i in App.database.db.all()]
    # add_waste_test(App)
    # add_money_test(App)
    print('Database len: {}'.format(len(all_d)))
    print(get_current_money_test(App))
    print(get_day_waste_test(App))
    print(get_day_add_money_test(App))
    print(get_day_wastes_and_descriptions_test(App))
    print(show_day_data_test(App))
    print(App.get_day_wastes_times(str(datetime.date.today()), 'add_waste'))
    print(App.show_day_info(str(datetime.date.today()), 'add_waste'))
    print(App.get_day_wastes_times(str(datetime.date.today()), 'add_new_money'))
    print(App.show_day_info(str(datetime.date.today()), 'add_new_money'))


if __name__ == '__main__':
    main()
    # pass
