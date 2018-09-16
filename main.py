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
                # self.dh.insert_result(
                    # addr + self.request_house_info(m.group(0)))
                self.request_house_info(m.group(0))
                self.dh.remove(addr)
                print('{}, {}, {}, {}, {}, {} removed from query list ' \
                    'due to it was found'.format(*addr))
            elif addr[-1] == 1:
                print('{}, {}, {}, {}, {}, {} was not found ' \
                    '(the second try)'.format(*addr))
                self.dh.insert_back(addr)
            elif addr[-1] == 2:
                print('{}, {}, {}, {}, {}, {} was not found three times ' \
                    'and removed'.format(*addr))
                self.dh.remove(addr)
            else:
                self.dh.insert_back(addr)
                print('{}, {}, {}, {}, {}, {} was not found ' \
                    '(the first try)'.format(*addr))

    def request_house_info(self, profile_url: str) -> tuple:
        url = 'https://www.reformagkh.ru{}'.format(profile_url)
        r = requests.get(url)
        text = ' '.join(r.text.split('\n'))

        year = re.search(
            r'Год ввода дома в эксплуатацию.*?<span>(?P<year>.*?)</span>', text
        ).group('year').strip()
        print(year)

        stages = re.search(
            r'Количество этажей.*?<span>наибольшее.*?' \
            r'<span>(?P<stages>.*?)</span>', text
        ).group('stages').strip()
        print(stages)

        last_change = ' '.join(re.search(
            r'Последнее изменение анкеты.*?' \
            r'<span class="black_text">(?P<last_change>.*?)</span>', text
        ).group('last_change').strip().split())
        print(last_change)

        series = re.search(
            r'Серия, тип постройки здания.*?<span>(?P<series>.*?)</span>', text
        ).group('series').strip()
        print(series)

        building_type = series

        house_type = re.search(
            r'Тип дома.*?<span>(?P<house_type>.*?)</span>', text
        ).group('house_type').strip()
        print(house_type)

        is_wreck = re.search(
            r'Дом признан аварийным.*?<span>(?P<is_wreck>.*?)</span>', text
        ).group('is_wreck').strip()
        is_wreck = 1 if is_wreck == 'Да' else 0
        print(is_wreck)

        cadaster_number = re.search(
            r'Кадастровый номер.*?10px;">(?P<cadaster_number>.*?)</td>', text
        ).group('cadaster_number').strip()
        print(cadaster_number)

        overlapping_type = re.search(
            r'Тип перекрытий.*?<span>(?P<overlapping_type>.*?)</span>', text
        ).group('overlapping_type').strip()
        print(overlapping_type)

        wall_material = re.search(
            r'Материал несущих стен.*?<span>(?P<wall_material>.*?)</span>', text
        ).group('wall_material').strip()
        print(wall_material)

        return (
            year, stages, last_change, series, building_type, house_type,
            is_wreck, cadaster_number, overlapping_type, wall_material,
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
