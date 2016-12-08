import sqlite3


class CompanyDataWriter(object):
    def __enter__(self):
        self.create_connection()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.connection.close()

    def create_connection(self):
        self.connection = sqlite3.connect('test.db')

    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='COMPANY'"
        )
        if not cursor.fetchall():
            with open('table_script.sql') as sql_file:
                self.connection.execute(sql_file.read())

    def add_company_data(self, company_data):
        pass
