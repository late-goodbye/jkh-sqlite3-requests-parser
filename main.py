import sqlite3
import requests
import re
import time
from bs4 import BeautifulSoup
from database_handler import DatabaseHandler


class Main:

    def __init__(self):
        self.dh = DatabaseHandler('database')
        self.dh.fill_database()

    def request_house_profile(self, addr: tuple, simple: bool=True):

        if simple:
            url = ('https://www.reformagkh.ru/search/houses?query='
                '{}+{}+{}+{}+{}&mh=on'.format(*addr)) \
                .replace('.0', '').replace(' ', '+')
            print(url)
            r = requests.get(url)
            print(r)
            m = re.search(r'/myhouse/profile/view/[0-9]+', r.text)
            print('{} {} {} {} {} {}'.format(*addr))
            if m:
                self.request_house_info(m.group(0))
                self.dh.remove(addr)
                print('{} {} {} {} {} {} removed from query list due to it was found'.format(*addr))
            elif addr[-1] == 1:
                print('{} {} {} {} {} {} was not found (the second try)'.format(*addr))
                self.dh.insert_back(addr)
            elif addr[-1] == 2:
                print('{} {} {} {} {} {} was not found three times and removed'.format(*addr))
                self.dh.remove(addr)
            else:
                self.dh.insert_back(addr)
                print('{} {} {} {} {} {} was not found (the first try)'.format(*addr))

    def request_house_info(self, profile_url: str):
        url = 'https://www.reformagkh.ru{}'.format(profile_url)
        r = requests.get(url)
        info = tuple(
            re.search(r'')

        )

    def run(self):

        while True:
            try:
                dr = self.dh.databaseReader()
                for addr in dr:
                    self.request_house_profile(addr)
                    time.sleep(5)
            except KeyboardInterrupt:
                print('\nBye.')
                self.dh.close_connection()
                break

if __name__ == '__main__':
    main = Main()
    main.run()
