import sqlite3
import requests
import re
import time
from bs4 import BeautifulSoup
from database_handler import DatabaseHandler


def run():
    dh = DatabaseHandler('database')
    dh.fill_database()
    while True:
        try:
            dr = dh.databaseReader()
            for house in dr:
                print(house)
                time.sleep(2)
        except KeyboardInterrupt:
            print('\nBye.')
            dh.close_connection()
            break

if __name__ == '__main__':
    run()
