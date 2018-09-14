import sqlite3
import requests
import re
import time
from bs4 import BeautifulSoup
from database_handler import fill_database
from database_handler import databaseReader


def run():
    database_name = 'test'
    fill_database(database_name)
    while True:
        database_reader = databaseReader(database_name)
        for house in database_reader:
            print(house)
            time.sleep(5)


if __name__ == '__main__':
    run()
