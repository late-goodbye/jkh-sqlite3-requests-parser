import sys
import sqlite3
import xlrd
from xlrd import XLRDError


class DatabaseHandler:
    def __init__(self, database_name: str):
        self.database_name = database_name
        self.conn = sqlite3.connect('{}.db'.format(self.database_name))
        self.cursor = self.conn.cursor()
        self.cursor.execute('DROP TABLE IF EXISTS input_data')
        self.cursor.execute("""
            CREATE TABLE input_data (
                region text,
                city text,
                street text,
                house text,
                corpus text,
                was_not_found integer)
            """)
        self.cursor.execute('DROP TABLE IF EXISTS result_data')
        self.cursor.execute("""
            CREATE TABLE result_data (
                region text,
                city text,
                street text,
                house text,
                corpus text,
                year text,
                stages integer,
                last_change date,
                series text,
                building_type text,
                house_type text,
                is_wreck integer,
                cadaster_number text,
                overlapping_type text,
                wall_material text)
            """)

    def insert_result(self, result):
        self.cursor.execute("""
            INSERT INTO result_data VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
        """, result)
        self.conn.commit()
        self.cursor.execute("""
            SELECT * FROM result_data
        """)
        print(self.cursor.fetchall())

    def close_connection(self):
        self.conn.close()

    def update(self, addr: tuple, was_found: bool):
        format = -1 if was_found else addr[-1] + 1
        self.cursor.execute("""
            UPDATE input_data
            SET was_not_found={}
            WHERE region=? AND city=? AND street=? AND house=? AND corpus=?
        """.format(format), addr[:-1])
        self.conn.commit()

    def remove(self, addr: tuple):
        self.cursor.execute("""
            DELETE FROM input_data
            WHERE region=? AND city=? AND street=? AND house=? AND corpus=?
        """, addr[:-1])

    def databaseReader(self):
        try:
            self.cursor.execute("""
                SELECT * FROM input_data
                WHERE was_not_found < 3 AND was_not_found > -1
            """)
            if not self.cursor:
                print('Query list is empty...')
            for row in self.cursor:
                yield row
        except (KeyboardInterrupt, GeneratorExit):
            print('Work finished.')
        except:
            print("Something wrong: {}".format(sys.exc_info()[0]))

    def fill_database(
            self,
            source_name: str='test_sample'):
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
                    INSERT INTO input_data VALUES (?, ?, ?, ?, ?, 0)
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
        except:
            print("Something wrong during filling the database: {}".format(
                sys.exc_info()[0]))
            return False
