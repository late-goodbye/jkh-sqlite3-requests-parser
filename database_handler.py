import sys
import sqlite3
from sqlite3 import OperationalError
import xlrd
from xlrd import XLRDError


class DatabaseHandler:
    def __init__(self, database_name: str):
        self.database_name = database_name
        self.conn = sqlite3.connect('{}.db'.format(self.database_name))
        self.cursor = self.conn.cursor()
        self.cursor.execute('DROP TABLE IF EXISTS result_data')
        self.cursor.execute("""
            CREATE TABLE result_data (
                id integer PRIMARY KEY,
                year text,
                stages integer,
                last_change date,
                series text,
                building_type text,
                house_type text,
                is_wreck integer,
                cadaster_number text,
                overlapping_type text)
            """)
        self.cursor.execute('DROP TABLE IF EXISTS input_data')
        self.cursor.execute("""
            CREATE TABLE input_data (
                id integer PRIMARY KEY,
                region text,
                city text,
                street text,
                house text,
                corpus text,
                was_not_found integer,
                result_id integer,
                FOREIGN KEY (result_id) REFERENCES result_data(id))
            """)
        self.cursor.execute('DROP TABLE IF EXISTS wall_materials')
        self.cursor.execute("""
            CREATE TABLE wall_materials (
                result_id integer,
                material text,
                FOREIGN KEY (result_id) REFERENCES result_data(id)
            )
        """)

    def insert_result(self, result):
        self.cursor.execute("""
            INSERT INTO result_data (year, stages, last_change, series,
                building_type, house_type, is_wreck, cadaster_number,
                overlapping_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, result[:-2])
        self.cursor.execute('SELECT last_insert_rowid()')
        id = self.cursor.fetchone()[0]
        self.cursor.execute("""
            UPDATE input_data
            SET result_id={}
            WHERE id={}
        """.format(id, result[-1]))
        for material_name in result[-2].split(','):
            self.cursor.execute("""
                INSERT INTO wall_materials (result_id, material)
                VALUES ({}, ?)
            """.format(id), (material_name.strip().lower(), ))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

    def update(self, id: int, code: int):
        self.cursor.execute("""
            UPDATE input_data
            SET was_not_found={}
            WHERE id = ?
        """.format(code), (id, ))
        self.conn.commit()

    def database_reader(self):
        try:
            self.cursor.execute("""
                SELECT region, city, street, house, corpus, was_not_found, id
                FROM input_data
                WHERE was_not_found < 3 AND was_not_found > -1
            """)
            for row in self.cursor:
                yield row
        except (KeyboardInterrupt, GeneratorExit):
            print('Work finished.')
        except:
            print("Something wrong: {}".format(sys.exc_info()[0]))

    def check_found(self):
        self.cursor.execute("""
            SELECT COUNT(1) FROM input_data
            WHERE was_not_found = -1
        """)
        print("Found: {}".format(self.cursor.fetchone()[0]))

        self.cursor.execute("""
            SELECT COUNT(1) FROM input_data
            WHERE was_not_found = 3
        """)
        print("Not found: {}".format(self.cursor.fetchone()[0]))

        self.cursor.execute("""
            SELECT COUNT(1) FROM input_data
            WHERE was_not_found IN (0, 1, 2)
        """)
        print("In query: {}".format(self.cursor.fetchone()[0]))

    def count_brick_houses(self):
        self.cursor.execute("""
            SELECT region, count(1) FROM input_data
            INNER JOIN result_data ON input_data.result_id = result_data.id
            INNER JOIN wall_materials ON wall_materials.result_id = result_data.id
            WHERE material = 'кирпичные'
            GROUP BY region
        """)
        print('\nNumber of brick houses:')
        for row in self.cursor.fetchall():
            print('\t{}: {}'.format(row[0], row[1]))
        print()

    def found_max_stages(self):
        print("Max stages per wall material per city: ")
        self.cursor.execute("""
            SELECT DISTINCT region, city FROM input_data
        """)
        cities = self.cursor.fetchall()
        for city in cities:
            self.cursor.execute("""
                SELECT material, MAX(stages) FROM input_data
                INNER JOIN result_data ON input_data.result_id = result_data.id
                INNER JOIN wall_materials ON result_data.id = wall_materials.result_id
                WHERE region = ? AND city = ?
                GROUP BY material
            """, city)
            city_name = city[0].split()[0] if not city[1] else city[1]
            print('\t{}:'.format(city_name))
            for material in self.cursor.fetchall():
                print('\t\t{}: {}'.format(material[0], material[1]))
            print()

    def fill_database(self, source_name: str='test_sample'):
        """
        This method fills database by using an .xlsx file with sample data

        Args:
            source_name (str): a sample data filename without extension
            sheet_name (str): name of a sheet with the data
            database_name (str): name of the database to be filled in

        Returns:
            True in case of success, False in another case

        Raises:
            FileNotFoundError: if .xlsx file wasn't found
            XLRDError: if .xlsx found but sheet_name is wrong
            IndexError: if col or row index is wrong
        """

        try:
            workbook = xlrd.open_workbook('{}.xlsx'.format(source_name))
            worksheet = workbook.sheet_by_index(0)

            for row in range(1, worksheet.nrows):
                # 2, 4, 6, 7, 8 is a region, a city, a street, a house, and a corpus
                # columns respectively
                row_data = tuple(
                    worksheet.cell_value(row, col) for col in [2, 4, 6, 7, 8])
                self.cursor.execute("""
                    INSERT INTO input_data (
                        region, city, street, house, corpus, was_not_found
                    ) VALUES (?, ?, ?, ?, ?, 0)
                """, row_data)
            self.conn.commit()
            return True

        except FileNotFoundError:
            print("{}.xlsx wasn't found in the current firectory.".format(
                source_name))
            return False
        except XLRDError:
            print("Sheet with name {} wasn't found in file {}.xlsx.".format(
                sheet_name, source_name))
            return False
        except IndexError:
            print("Wrong index in sheet {} in file {}.xlsx.".format(
                sheet_name, source_name))
            return False
        except OperationalError:
            print("Wrong operation")
            return False
        except:
            print("Something wrong during filling the database: {}".format(
                sys.exc_info()[0]))
            return False
