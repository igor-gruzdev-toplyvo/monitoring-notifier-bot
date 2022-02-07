import sqlite3
from dotenv import load_dotenv
from os import environ
from datetime import datetime


class Executor:

    load_dotenv()

    def __init__(self) -> None:
        self.connector = sqlite3.connect(environ.get("DB_PATH"))
        self.cursor = self.connector.cursor()
        self.current_date = datetime.date(datetime.now())
        self.current_time = datetime.time(datetime.now()).strftime("%H:%M:%S")

    def create_table(self):
        def __init_table():
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS monitoring (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hostname TEXT NOT NULL,
                    usage_percentage INTEGER NOT NULL,
                    date TEXT NOT NULL,
                    time TEXT NOT NULL
                )"""
            )
            self.connector.commit()

        def __create_service_index():
            self.cursor.execute(
                """CREATE INDEX IF NOT EXISTS hostname_ind on monitoring (hostname)"""
            )
            self.connector.commit()

        def __create_date_index():
            self.cursor.execute(
                """CREATE INDEX IF NOT EXISTS date_ind on monitoring (date)"""
            )
            self.connector.commit()

        __init_table()
        __create_service_index()
        __create_date_index()
        self.connector.close()

    def write_entry(self, hostname, usage_percentage):
        self.cursor.execute(
            """INSERT INTO monitoring (
                    hostname, usage_percentage, date, time
                )
                VALUES (
                    '{}', {}, '{}', '{}'
                )
            """.format(hostname, usage_percentage, self.current_date, self.current_time)
        )
        self.connector.commit()
        self.connector.close()

    def select_period(self):
        data_list = []

        query = self.cursor.execute(
            """SELECT usage_percentage FROM monitoring ORDER BY id DESC LIMIT 5"""
        )
        
        rows = self.cursor.fetchall()

        for row in rows:
            data_list.append(row[0])

        return data_list
