# coding: utf-8
import psycopg2


class PostgresProvider(object):
    cnx = None

    def __init__(self, username, password, server, database):
        self.username = username
        self.password = password
        self.server = server
        self.database = database

    def connect(self):
        if self.cnx:
            return

        try:
            self.cnx = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (self.database,
                                                                                           self.username,
                                                                                           self.server,
                                                                                           self.password))
        except Exception as err:
            raise err

    def insert(self, query):
        cursor = self.cnx.cursor()
        cursor.execute(query)
        id_of_new_row = cursor.fetchone()[0]
        self.cnx.commit()
        return id_of_new_row

    # list o select
    def query(self, query):
        cursor = self.cnx.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows

    # update o delete
    def update(self, query):
        cursor = self.cnx.cursor()
        cursor.execute(query)
        self.cnx.commit()
        return 0
