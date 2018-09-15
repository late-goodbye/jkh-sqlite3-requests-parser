import sys
import sqlite3
import xlrd
from xlrd import XLRDError


class DatabaseHandler:
    def __init__(self, database_name: str):
        self.database_name = database_name
        self.conn = sqlite3.connect('{}.db'.format(self.database_name))
        self.cursor = self.conn.cursor()

    def close_connection(self):
        self.conn.close()

    def databaseReader(self):
        try:
            self.cursor.execute('SELECT * FROM input_data')
            for row in self.cursor:
                yield row
        except:
            print("Something wrong: {}".format(sys.exc_info()[0]))

    def fill_database(
            self,
            source_name: str='test_sample',
            sheet_name: str='Лист1'):
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
            worksheet = workbook.sheet_by_name(sheet_name)

            self.cursor.execute('DROP TABLE IF EXISTS input_data')
            self.cursor.execute("""
                CREATE TABLE input_data
                    (region text, city text, street text, house text, corpus text)
                """)

            for row in range(1, worksheet.nrows):
                # 2, 4, 6, 7, 8 is a region, a city, a street, a house, and a corpus
                # columns respectively
                row_data = tuple(
                    worksheet.cell_value(row, col) for col in [2, 4, 6, 7, 8])
                self.cursor.execute("""
                    INSERT INTO input_data VALUES (?, ?, ?, ?, ?)
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
