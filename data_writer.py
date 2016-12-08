import sqlite3


class CompanyDataWriter(object):
    def __enter__(self):
        self.create_connection()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.connection.close()

    def create_connection(self):
        self.connection = sqlite3.connect('test.db')
        self.create_table()

    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='COMPANY'"
        )
        if not cursor.fetchall():
            with open('table_script.sql') as sql_file:
                self.connection.execute(sql_file.read())

    def add_company_data(self, company_data):
        cursor = self.connection.cursor()
        cursor.execute(
            '''INSERT OR REPLACE INTO COMPANY (
            id, name, est_revenue, url, street, city, zip_code, country, employees_count, industry
            ) VALUES (
            "{key}","{name}","{est_revenue}","{url}","{street}","{city}",
            "{zip_code}","{country}",{employees_count},"{industry}");'''.format(**company_data)
        )
        self.connection.commit()

    def get_all_companies(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM COMPANY")
        return cursor.fetchall()
