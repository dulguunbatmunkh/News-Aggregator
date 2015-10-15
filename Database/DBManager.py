# -*- coding: utf-8 -*-
import mysql.connector
from datetime import datetime
from collections import OrderedDict

class DBManager(object):
    """
        Python Class for connecting with MySQL server and accelerate development project using MySQL
        Extremely easy to learn and use, friendly construction.
    """

    __instance = None
    __host = None
    __user = None
    __password = None
    __database = None
    __session = None
    __connection = None

    def __init__(self, host='localhost', user='root', password='', database=''):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database
    # end __init__

    def __open(self):
        try:
            cnx = mysql.connector.connect(host=self.__host,
                                          user=self.__user,
                                          password=self.__password,
                                          database=self.__database,
                                          charset='utf8',
                                          use_unicode=True)
            self.__connection = cnx
            self.__session = cnx.cursor()
        except mysql.connector.Error as e:
            print("Error %d: %s", e.args[0], e.args[1])
    # end  __open

    def __close(self):
        self.__session.close()
        self.__connection.close()
    # end __close

    def select(self, table, where=None, *args, **kwargs):
        result = None
        query = 'SELECT '
        keys = args
        values = tuple(kwargs.values())
        l = len(keys) - 1

        for i, key in enumerate(keys):
            query += "`" + key + "`"
            if i < l:
                query += ","
        ## End for keys

        query += 'FROM %s' % table

        if where:
            query += " WHERE %s" % where
        ## End if where

        self.__open()
        self.__session.execute(query, values)
        number_rows = self.__session.rowcount
        number_columns = len(self.__session.description)

        if number_rows >= 1 and number_columns > 1:
            result = [item for item in self.__session.fetchall()]
        else:
            result = [item[0] for item in self.__session.fetchall()]
        self.__close()

        return result
    # end select

    def select_json(self, sql, *args):
        od = OrderedDict(args)
        query = sql
        values = tuple(od.values())

        self.__open()
        self.__session.execute(query, values)

        number_rows = self.__session.rowcount
        number_columns = len(self.__session.description)

        if number_rows >= 1 and number_columns > 1:
            result = [item for item in self.__session.fetchall()]
        else:
            result = [item[0] for item in self.__session.fetchall()]
        print(result)
        return result

        result = [dict(line) for line in [zip([column[0] for column in
                     self.__session.description], row) for row in self.__session.fetchall()]]

        self.__close()
        return result
    # end select_json

    def update(self, table, where=None, *args, **kwargs):
        query = "UPDATE %s SET " % table
        keys = kwargs.keys()
        values = tuple(kwargs.values()) + tuple(args)
        l = len(keys) - 1
        for i, key in enumerate(keys):
            query += "`" + key + "` = %s"
            if i < l:
                query += ","
                ## End if i less than 1
        ## End for keys
        query += " WHERE %s" % where

        self.__open()
        self.__session.execute(query, values)
        self.__connection.commit()

        # Obtain rows affected
        update_rows = self.__session.rowcount
        self.__close()

        return update_rows
    # end update

    def insert(self, table, *args, **kwargs):
        values = None
        query = "INSERT INTO %s " % table
        if kwargs:
            keys = kwargs.keys()
            values = tuple(kwargs.values())
            query += "(" + ",".join(["`%s`"] * len(keys)) % tuple(keys) + ") VALUES (" + ",".join(
                ["%s"] * len(values)) + ")"
        elif args:
            values = args
            query += " VALUES(" + ",".join(["%s"] * len(values)) + ")"

        self.__open()
        self.__session.execute(query, values)
        self.__connection.commit()
        self.__close()
        return self.__session.lastrowid
    # end insert

    def delete(self, table, where=None, *args):
        query = "DELETE FROM %s" % table
        if where:
            query += ' WHERE %s' % where

        values = tuple(args)

        self.__open()
        self.__session.execute(query, values)
        self.__connection.commit()

        # Obtain rows affected
        delete_rows = self.__session.rowcount
        self.__close()

        return delete_rows
    # end delete

    def select_advanced(self, sql, *args):
        od = OrderedDict(args)
        query = sql
        values = tuple(od.values())

        self.__open()
        self.__session.execute(query, values)
        number_rows = self.__session.rowcount
        number_columns = len(self.__session.description)

        if number_rows >= 1 and number_columns > 1:
            result = [item for item in self.__session.fetchall()]
        else:
            result = [item[0] for item in self.__session.fetchall()]

        self.__close()
        return result
    # end select_advanced

    def insert_many(self, table, keys, values):
        result = None

        query = "INSERT INTO %s " % table
        query += "(" + ",".join(["`%s`"] * len(keys)) % tuple(keys) + ") VALUES (" + ",".join(
            ["%s"] * len(values[0])) + ")"

        try:
            self.__open()

            try:
                self.__session.executemany(query, values)
                self.__connection.commit()
            except MySQLdb.Error as e:
                print(e)
                self.__connection.rollback()

            self.__close()
            result = self.__session.lastrowid
        except:
            print('Database connection error')
            result = -1

        return result
    # end insert_many

# end class
