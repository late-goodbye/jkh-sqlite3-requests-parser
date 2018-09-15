import sqlite3
import requests
import re
import time
from bs4 import BeautifulSoup
from database_handler import DatabaseHandler


def request_house_info(addr: tuple, simple: bool=True):

    if simple:
        url = 'https://www.reformagkh.ru/search/houses?query='
        '{}+{}+{}+{}+{}&mh=on'.format(*addr)
        r = requests.get(url)
        print(r)


def run():
    dh = DatabaseHandler('database')
    dh.fill_database()
    while True:
        try:
            dr = dh.databaseReader()
            for addr in dr:
                request_house_info(addr)
                time.sleep(2)
        except KeyboardInterrupt:
            print('\nBye.')
            dh.close_connection()
            break

if __name__ == '__main__':
    run()
